"""M2 tasks 3-4: power, Type S and Type M of the interrupted time series (ITS).

Synthetic series = effect path + AR(1) noise (log headcount), observed only at
Brazil's survey years (no 1991, 1994, 2000, 2010; 2020-2021 dropped as the
COVID aid years would be dummied out or dropped in M3). The trend and GDP terms
of the true process do not need to be simulated: OLS on a design that contains
them is exactly invariant to them, so y = effect + noise is equivalent.

ITS specification (the M3 regression):
    log H_t = a + b (t - 2003) + c g_t + d R_t + e (t - 2003) 1[t >= 2004] + u_t
g_t = actual GDP-per-capita growth (WDI), R_t = coverage ramp (0 before 2004,
0.60 / 0.78 / 0.99 in 2004-2006, 1 after). Newey-West (Bartlett) SEs with
floor(4 (n/100)^(2/9)) lags, t(n-k) critical values, alpha = 0.05 two-sided.

Tests:
  mechanical  DGP = mechanical effect only; test d = 0.
  longrun     DGP = mechanical 15% + long-run effect; test e = 0 (the post-slope
              is the only term that can separate a slowly growing long-run
              effect from the mechanical step). Primary test for H2.1.
Noise cases: main (PIP 1995-2019 fit), pessimistic (PIP 1981-2019 fit),
main_rho05 (main SD, rho 0.5), thesis_main / thesis_pess (thesis $2 data),
mixed (noisy before 1995, main after: the realistic case for a 1981 start).
Series start 1995 (main design) or 1981 (long design). A 1981 start with the
main noise assumes the 1980s were as calm as post-1995; they were not, so for
the long design read the mixed or pessimistic rows.
  longrun_joint  DGP = long-run only (no mechanical); joint NW Wald test of
              d = e = 0. "Can any break at all be seen?" Generous to detection.
Newey-West with about 20 points over-rejects (empirical size about 20%), so
'power' is size-adjusted (critical value simulated under the null from
independent draws); 'power_nominal' keeps the textbook critical value.
Type S and Type M (Gelman & Carlin 2014) are computed against the pseudo-true
coefficient, the coefficient obtained by regressing the noise-free effect path
on the design (for longrun, the long-run path alone).
Run: python analysis/m2_power.py -> output/M2/results.csv, power_curves.png
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m2_exposure  # noqa: E402
import m2_noise  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "M2"
NSIM = 4000
SEED = 20261110
ALPHA = 0.05
MISSING = {1991, 1994, 2000, 2010, 2020, 2021}
STARTS = (1995, 1981)
ENDS = (2015, 2019, 2024)
THETAS = (0.0, 0.05, 0.10, 0.20, 0.30)


def survey_years(start, end):
    return [y for y in range(start, end + 1) if y not in MISSING]


def design(years, g):
    t = np.asarray(years, float)
    post = (t >= 2004).astype(float)
    return np.column_stack([np.ones_like(t), t - 2003, g.reindex(years).to_numpy(),
                            m2_exposure.mechanical_ramp(years), (t - 2003) * post])


def simulate_noise(rng, rho, sigma_u, nsim, y0=1981, y1=2024):
    """Unit-variance stationary AR(1), scaled by sigma_u (a number, or a
    {year: sd} mapping for the mixed case)."""
    T = y1 - y0 + 1
    u = np.empty((nsim, T))
    u[:, 0] = rng.normal(0, 1, nsim)
    eps = rng.normal(0, np.sqrt(1 - rho ** 2), (nsim, T))
    for i in range(1, T):
        u[:, i] = rho * u[:, i - 1] + eps[:, i]
    sd = (lambda y: sigma_u[y]) if isinstance(sigma_u, dict) else (lambda y: sigma_u)
    return {y: sd(y) * u[:, y - y0] for y in range(y0, y1 + 1)}


def ols_nw(X, Y):
    """X (n,k), Y (nsim,n). Returns beta (nsim,k), cov (nsim,k,k)."""
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    B = Y @ X @ XtXi                       # (nsim,k)
    E = Y - B @ X.T                        # (nsim,n)
    U = X[None, :, :] * E[:, :, None]      # (nsim,n,k)
    L = int(np.floor(4 * (n / 100) ** (2 / 9)))
    S = np.einsum("snk,snj->skj", U, U)
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = np.einsum("snk,snj->skj", U[:, l:, :], U[:, :-l, :])
        S += w * (G + np.transpose(G, (0, 2, 1)))
    S *= n / (n - k)                       # small-sample scaling
    V = XtXi[None] @ S @ XtXi[None]
    return B, V


def summarize(est, stat, true, crit_nom, crit_adj):
    """Power at the nominal and the size-adjusted critical value; Type S / M use
    the size-adjusted rejections (the honest ones)."""
    rej_nom = stat > crit_nom
    rej = stat > crit_adj
    sig = est[rej]
    if abs(true) < 1e-9 or rej.sum() == 0:
        ts, tm = np.nan, np.nan
    else:
        ts = float((np.sign(sig) != np.sign(true)).mean())
        tm = float(np.abs(sig).mean() / abs(true))
    return dict(power_nominal=float(rej_nom.mean()), power=float(rej.mean()), type_s=ts, type_m=tm,
                mean_est=float(est.mean()), sd_est=float(est.std()), true_coef=float(true),
                crit_nominal=float(crit_nom), crit_size_adj=float(crit_adj))


def t_stat(X, Y, j):
    B, V = ols_nw(X, Y)
    return B[:, j], np.abs(B[:, j] / np.sqrt(V[:, j, j]))


def wald_stat(X, Y):
    B, V = ols_nw(X, Y)
    b2, V2 = B[:, 3:5], V[:, 3:5, 3:5]
    return B[:, 4], np.einsum("si,sij,sj->s", b2, np.linalg.inv(V2), b2) / 2


def run():
    """Newey-West with about 20 observations over-rejects badly (the empirical
    size is near 20%, not 5%). So every test also gets a size-adjusted critical
    value: the 95th percentile of its statistic under the null, simulated from
    an independent set of noise draws. 'power' is size-adjusted;
    'power_nominal' uses the textbook t / F critical value."""
    t0 = time.time()
    g = m2_noise.gdp_growth()
    noise = m2_noise.noise_params()
    shares = m2_exposure.exposure_shares().set_index("year")
    rows = []
    cell = 0
    for ni, (ncase, (rho, sig)) in enumerate(noise.items()):
        for start in STARTS:
            for end in ENDS:
                rng = np.random.default_rng([SEED, ni, start, end])
                u = simulate_noise(rng, rho, sig, NSIM)
                u0 = simulate_noise(np.random.default_rng([SEED + 1, ni, start, end]), rho, sig, NSIM)
                yrs = survey_years(start, end)
                n = len(yrs)
                X = design(yrs, g)
                k = X.shape[1]
                tcrit = stats.t.ppf(1 - ALPHA / 2, n - k)
                fcrit = stats.f.ppf(1 - ALPHA, 2, n - k)
                U = np.column_stack([u[y] for y in yrs])
                U0 = np.column_stack([u0[y] for y in yrs])
                proj = np.linalg.pinv(X)
                paths = m2_exposure.effect_paths(yrs, shares)
                mech15 = paths[("mechanical", 0.15)]
                q = 1 - ALPHA
                crit_mech = np.quantile(t_stat(X, U0, 3)[1], q)
                crit_lr = np.quantile(t_stat(X, U0 + mech15, 4)[1], q)
                crit_joint = np.quantile(wald_stat(X, U0)[1], q)
                sig_lbl = sig if not isinstance(sig, dict) else f"{sig[1981]:.4f}/{sig[2024]:.4f}"
                base = dict(noise_case=ncase, rho=rho, sigma_u=sig_lbl, start=start, end=end, n_obs=n,
                            n_sims=NSIM, seed=f"{SEED}-{ni}-{start}-{end}")
                for size in (0.0, 0.15, 0.25):
                    p = paths[("mechanical", size)] if size else np.zeros(n)
                    est, st = t_stat(X, U + p, 3)
                    rows.append({**base, "test": "mechanical", "scenario": "mechanical",
                                 "effect_size": size, "national_effect_end": size,
                                 **summarize(est, st, (proj @ p)[3], tcrit, crit_mech)})
                    cell += 1
                for sc in m2_exposure.SCENARIOS:
                    S_end = shares.loc[end, f"S_{sc}"]
                    for th in THETAS:
                        p = paths[(f"longrun_{sc}", th)]
                        true = (proj @ p)[4]
                        est, st = t_stat(X, U + mech15 + p, 4)
                        rows.append({**base, "test": "longrun", "scenario": sc, "effect_size": th,
                                     "national_effect_end": th * S_end,
                                     **summarize(est, st, true, tcrit, crit_lr)})
                        est, st = wald_stat(X, U + p)
                        rows.append({**base, "test": "longrun_joint", "scenario": sc,
                                     "effect_size": th, "national_effect_end": th * S_end,
                                     **summarize(est, st, true, fcrit, crit_joint)})
                        cell += 2
    df = pd.DataFrame(rows)
    print(f"{cell} cells x {NSIM} sims in {time.time() - t0:.1f}s")
    return df


def plot(df):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = {"low": "#2a78d6", "central": "#eb6834", "generous": "#1baf7a"}
    ink, muted = "#0b0b0b", "#52514e"
    panels = [("main", 1995, "Main noise"), ("pessimistic", 1995, "Pessimistic noise"),
              ("mixed", 1981, "Long series, mixed noise")]
    fig, axes = plt.subplots(3, 3, figsize=(13, 10.5), sharey=True, facecolor="#fcfcfb")
    for r, (ncase, start, label) in enumerate(panels):
        for c, end in enumerate(ENDS):
            ax = axes[r, c]
            ax.set_facecolor("#fcfcfb")
            d = df[(df.noise_case == ncase) & (df.start == start) & (df.end == end)]
            for sc, col in colors.items():
                s = d[(d.test == "longrun") & (d.scenario == sc)].sort_values("effect_size")
                ax.plot(s.effect_size * 100, s.power, color=col, lw=2, marker="o", ms=5,
                        label=f"Long-run, {sc} exposure")
                j = d[(d.test == "longrun_joint") & (d.scenario == sc)].sort_values("effect_size")
                ax.plot(j.effect_size * 100, j.power, color=col, lw=1.2, ls="--", alpha=0.8)
            m = d[(d.test == "mechanical") & (d.effect_size == 0.15)].power.iloc[0]
            ax.axhline(m, color=ink, lw=1.5, ls=":")
            ax.text(0.5, m - 0.02, f"Mechanical 15%: {m:.0%}", va="top", fontsize=8, color=ink)
            ax.axhline(0.5, color=muted, lw=0.8)
            ax.axhline(0.2, color=muted, lw=0.8, ls="--")
            ax.set_ylim(0, 1.02)
            ax.set_xticks([0, 5, 10, 20, 30])
            ax.grid(axis="y", color="#e5e4df", lw=0.6)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            ax.set_title(f"{label}, {start}-{end}", fontsize=10, color=ink)
            if r == len(panels) - 1:
                ax.set_xlabel("Individual effect: % less adult poverty among exposed", fontsize=9)
            if c == 0:
                ax.set_ylabel("Power (alpha 0.05)", fontsize=9)
    h, l = axes[0, 0].get_legend_handles_labels()
    h += [plt.Line2D([], [], color=muted, ls="--", lw=1.2), plt.Line2D([], [], color=ink, ls=":")]
    l += ["Dashed: joint break test, no mechanical effect present", "Mechanical effect, 15%"]
    fig.legend(h, l, loc="lower center", ncol=3, fontsize=8.5, frameon=False)
    fig.suptitle("Size-adjusted power to detect Bolsa Familia effects in Brazil's national headcount "
                 "(interrupted time series, survey years only)", fontsize=11.5, color=ink)
    fig.text(0.5, 0.06, "Solid: post-slope test with the mechanical effect present (primary). "
             "Grey lines at 50% (kill criterion) and 20% (H2.1). 4,000 simulations per point.",
             ha="center", fontsize=8.5, color=muted)
    fig.tight_layout(rect=(0, 0.08, 1, 0.97))
    fig.savefig(OUT / "power_curves.png", dpi=150, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    df = run()
    df.to_csv(OUT / "results.csv", index=False, float_format="%.4f")
    plot(df)
    pd.set_option("display.width", 220)
    show = df[(df.start == 1995) & (df.noise_case == "main") & (df.end == 2024)]
    print(show[["test", "scenario", "effect_size", "national_effect_end",
                "power_nominal", "power", "type_s", "type_m"]].round(3).to_string())
