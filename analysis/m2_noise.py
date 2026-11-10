"""M2 task 1: noise in Brazil's national headcount after removing GDP growth.

Model, in log headcount at survey years only (no interpolation):
    log H_t = X_t b + u_t,   X = [1, t, GDP-per-capita growth_t, kinks]
    u_t stationary AR(1) on the calendar-year clock: Corr(u_s, u_t) = rho^|s-t|,
which handles the missing survey years (1991, 1994, 2000, 2010) exactly.
b, rho and sigma_u are fitted jointly by Gaussian maximum likelihood (GLS
profiled over b). We compare with rho = 0 by AIC.

Kinks: a slope change at 2003 (program era) and, for the modern series, at
2014 (recession) plus a level dummy for the 2012 PNAD -> PNADC spell break.
They soak up the program and the recession so that what is left is noise; this
makes the noise estimate, if anything, too small (generous to detectability).

Cases:
  main         PIP $3.00 (2021 PPP), 1995-2019 (stops before COVID aid and the 2023 reform)
  pessimistic  PIP $3.00, 1981-2019 (adds the hyperinflation years)
  diag_through_2024  PIP 1995-2024 without 2020-2021, diagnostic only
  thesis_main  thesis data fgt0ppp2 ($2 line), 1995-2009
  thesis_pess  thesis data fgt0ppp2, 1981-2009
Also reported: SD of year-to-year changes (pp and log points) between
consecutive survey years, raw and after removing GDP growth.
Run: python analysis/m2_noise.py   -> output/M2/noise.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m2_data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "M2"
COVID = {2020, 2021}


def gdp_growth():
    return pd.Series(m2_data.wdi_series("wdi_gdppc_growth.json")).sort_index() / 100.0


def pip_series():
    rows = [r for r in m2_data.pip_rows() if r["reporting_level"] == "national"
            and not r["is_interpolated"]]
    s = pd.Series({r["reporting_year"]: r["headcount"] * 100 for r in rows}).sort_index()
    return s


def thesis_series():
    d = pd.read_csv(ROOT / "Data" / "ThesisDataCSV.csv", encoding="latin1", low_memory=False)
    b = d[d["country"] == "Brazil"].set_index("year")["fgt0ppp2"].dropna()
    return b.astype(float)


def design(years, g, kinks, spell_break=None):
    t = np.asarray(years, float)
    cols = [np.ones_like(t), t - 2003, g.reindex(years).to_numpy()]
    for k in kinks:
        cols.append(np.clip(t - k, 0, None))
    if spell_break is not None:
        cols.append((t >= spell_break).astype(float))
    return np.column_stack(cols)


def ar1_corr(years, rho):
    t = np.asarray(years, float)
    return rho ** np.abs(t[:, None] - t[None, :])


def profile_loglik(y, X, years, rho):
    """Concentrated Gaussian log-likelihood for AR(1) errors; returns (ll, b, sigma2)."""
    R = ar1_corr(years, rho)
    L = np.linalg.cholesky(R)
    ys = np.linalg.solve(L, y)
    Xs = np.linalg.solve(L, X)
    b, *_ = np.linalg.lstsq(Xs, ys, rcond=None)
    e = ys - Xs @ b
    n = len(y)
    s2 = e @ e / n
    ll = -0.5 * n * (np.log(2 * np.pi * s2) + 1) - np.log(np.diag(L)).sum()
    return ll, b, s2


def fit_ar1(y, X, years):
    f = lambda r: -profile_loglik(y, X, years, r)[0]
    opt = minimize_scalar(f, bounds=(0.0, 0.95), method="bounded")
    rho = float(opt.x)
    ll1, b, s2 = profile_loglik(y, X, years, rho)
    ll0, b0, s20 = profile_loglik(y, X, years, 0.0)
    k = X.shape[1]
    return dict(rho=rho, sigma_u=float(np.sqrt(s2)), sigma_e=float(np.sqrt(s2 * (1 - rho ** 2))),
                aic_ar1=2 * (k + 2) - 2 * ll1, aic_white=2 * (k + 1) - 2 * ll0,
                sigma_white=float(np.sqrt(s20)), b=b)


def change_sd(h, g):
    """SD of changes between consecutive (1-year-apart) survey years."""
    yrs = [y for y in h.index if y - 1 in h.index]
    dpp = np.array([h[y] - h[y - 1] for y in yrs])
    dlog = np.array([np.log(h[y]) - np.log(h[y - 1]) for y in yrs])
    gg = g.reindex(yrs).to_numpy()
    Z = np.column_stack([np.ones_like(gg), gg])
    bl, *_ = np.linalg.lstsq(Z, dlog, rcond=None)
    resid = dlog - Z @ bl
    return dict(n_changes=len(yrs), sd_change_pp=float(dpp.std(ddof=1)),
                sd_change_log=float(dlog.std(ddof=1)),
                sd_change_log_net_gdp=float(resid.std(ddof=2)), gdp_elasticity_changes=float(bl[1]))


CASES = {
    "main": dict(src="pip", start=1995, end=2019, kinks=[2003, 2014], spell=2012),
    "pessimistic": dict(src="pip", start=1981, end=2019, kinks=[2003, 2014], spell=2012),
    # Diagnostic only, not used in the simulation: adding 2022-2024 pulls in the
    # 2023 Bolsa Familia reform (21M families, much larger benefits), a policy
    # shift that the kinks cannot absorb, so the "noise" becomes a policy effect.
    "diag_through_2024": dict(src="pip", start=1995, end=2024, kinks=[2003, 2014], spell=2012),
    "thesis_main": dict(src="thesis", start=1995, end=2009, kinks=[2003], spell=None),
    "thesis_pess": dict(src="thesis", start=1981, end=2009, kinks=[2003], spell=None),
}


def estimate_all():
    g = gdp_growth()
    series = {"pip": pip_series(), "thesis": thesis_series()}
    rows = []
    for name, c in CASES.items():
        h = series[c["src"]]
        h = h[(h.index >= c["start"]) & (h.index <= c["end"]) & ~h.index.isin(COVID)]
        years = list(h.index)
        y = np.log(h.to_numpy())
        X = design(years, g, c["kinks"], c["spell"])
        fit = fit_ar1(y, X, years)
        ch = change_sd(h, g)
        rows.append(dict(case=name, source=c["src"], start=c["start"], end=c["end"], n=len(years),
                         rho=fit["rho"], sigma_u_log=fit["sigma_u"], sigma_e_log=fit["sigma_e"],
                         sigma_white_log=fit["sigma_white"], aic_ar1=fit["aic_ar1"],
                         aic_white=fit["aic_white"], gdp_coef_levels=fit["b"][2], **ch))
    return pd.DataFrame(rows)


def noise_params():
    """(rho, sigma_u) on the log scale for the simulation, by case.

    main_rho05 is a sensitivity case: main-case sigma_u with rho forced to 0.5,
    because rho is poorly pinned down with about 20 points.
    """
    df = estimate_all().set_index("case")
    p = {k: (float(df.loc[k, "rho"]), float(df.loc[k, "sigma_u_log"]))
         for k in ("main", "pessimistic", "thesis_main", "thesis_pess")}
    p["main_rho05"] = (0.5, p["main"][1])
    return p


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    df = estimate_all()
    df.to_csv(OUT / "noise.csv", index=False, float_format="%.4f")
    pd.set_option("display.width", 200)
    print(df.round(4).to_string())
