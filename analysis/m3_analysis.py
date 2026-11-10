"""M3 steps 2-4: series, Datt-Ravallion decomposition, growth-elasticity
benchmark. Reads only the raw pull (data/raw/pip/<latest>/).

Usage: python analysis/m3_analysis.py
Outputs in output/M3/.
"""
from __future__ import annotations

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from m3_common import (COUNTRY, LINES, OUT, WDI_INDICATORS, P, spells,  # noqa: E402
                       survey_table)
from cct import decompose as D  # noqa: E402

COLORS = {3.00: "#2a78d6", 4.20: "#eb6834", 8.30: "#1baf7a"}  # categorical slots 1-3
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def load_cf(pull_dir, year, z):
    rec = P.load_raw(pull_dir / f"{P.cf_name(year, z)}.json")["response"]
    assert len(rec) == 1 and rec[0]["reporting_year"] == year
    return rec[0]


def load_wdi(pull_dir):
    out = {}
    for ind, col in WDI_INDICATORS.items():
        rec = P.load_raw(pull_dir / f"wdi_{COUNTRY}_{ind}.json")["response"][1]
        out[col] = {int(r["date"]): r["value"] for r in rec if r["value"] is not None}
    return pd.DataFrame(out).rename_axis("year").sort_index()


# ----------------------------------------------------------------- series
def build_series(df, wdi):
    cols = ["year", "survey_acronym", "comparable_spell", "welfare_type", "line",
            "headcount", "poverty_gap", "poverty_severity", "mean", "median", "gini"]
    s = df[cols].merge(wdi, left_on="year", right_index=True, how="left")
    s.to_csv(OUT / "m3_series.csv", index=False)
    return s


def plot_series(s):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8.5), sharex=True)
    for ax, var, lab in [(axes[0], "headcount", "Headcount (% of population)"),
                         (axes[1], "poverty_gap", "Poverty gap (% of line)")]:
        # break / policy markers (drawn first, recessive)
        ax.axvspan(2014.5, 2016.5, color="#f0efec", zorder=0)
        for x in (2011.5,):
            ax.axvline(x, color=INK2, lw=1.2, ls="--", zorder=1)
        for x in (2003.75, 2020.25, 2021.85, 2023.2):
            ax.axvline(x, color=INK2, lw=0.8, ls=":", zorder=1)
        for z in LINES:
            g = s[s["line"] == z]
            for cs, gg in g.groupby("comparable_spell"):
                mk = "o" if gg["survey_acronym"].iloc[0] == "PNAD" else "s"
                ax.plot(gg["year"], 100 * gg[var], color=COLORS[z], lw=2, marker=mk,
                        ms=4.5, label=f"${z:.2f}/day" if cs == "1981 - 2011" else None)
            last = g.iloc[-1]
            dy = {3.00: -4, 4.20: 4, 8.30: 0}[z] if var == "poverty_gap" else 0
            ax.annotate(f"${z:.2f}", (last["year"], 100 * last[var]), xytext=(6, dy),
                        textcoords="offset points", va="center", fontsize=9, color=INK)
        ax.set_ylabel(lab, color=INK)
        ax.grid(axis="y", color=GRID, lw=0.8)
        ax.set_ylim(bottom=0)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(colors=INK2)
    top = axes[0]
    ymax = top.get_ylim()[1]
    notes = [(2003.75, "2003 Bolsa Familia\nlaunched (Oct)"), (2011.5, "Survey break:\nPNAD | PNAD Continua"),
             (2015.5, "2015-16\nrecession"), (2020.25, "2020 Auxilio\nEmergencial"),
             (2021.85, "Nov 2021-22\nAuxilio Brasil"), (2023.2, "2023 Bolsa\nFamilia relaunch")]
    for i, (x, t) in enumerate(notes):
        top.text(x, ymax * (0.98 - 0.13 * (i % 3)), t, fontsize=7.5, color=INK2,
                 ha="center", va="top", bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
    axes[0].legend(frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.62), fontsize=9,
                   title="2021 PPP line", title_fontsize=9)
    axes[1].set_xlabel("Survey year (circles: PNAD; squares: PNAD Continua)", color=INK)
    fig.suptitle("Brazil, poverty by survey year (World Bank PIP, 2021 PPP)\n"
                 "Two survey series, not spliced. PIP has no PNAD/PNAD Continua overlap years.",
                 fontsize=11, color=INK, x=0.06, ha="left")
    fig.text(0.06, 0.005, "2020 and 2021 use PNAD Continua 5th-visit income (PNADC-E5); other "
             "PNADC years use the 1st visit (PNADC-E1). Source: PIP API, version in MANIFEST_M3.md.",
             fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(OUT / "m3_fig_series.png", dpi=150)
    plt.close(fig)


# ----------------------------------------------------------- decomposition
def decomposition(df, pull_dir):
    obs = df.set_index(["year", "line"])
    rows = []
    for a, b, kind in spells(df):
        mua, mub = obs.loc[(a, LINES[0]), "mean"], obs.loc[(b, LINES[0]), "mean"]
        for z in LINES:
            za, zb = round(z * mua / mub, 2), round(z * mub / mua, 2)
            ca, cb = load_cf(pull_dir, a, za), load_cf(pull_dir, b, zb)
            for meas in ("headcount", "poverty_gap"):
                p11, p22 = obs.loc[(a, z), meas], obs.loc[(b, z), meas]
                p21, p12 = ca[meas], cb[meas]
                # Headcount and normalized gap are homogeneous of degree 0 in
                # (line, incomes), so the scaled-line query needs no conversion.
                d = D.datt_ravallion(p11, p22, p21, p12)
                rows.append({"start": a, "end": b, "kind": kind, "line": z, "measure": meas,
                             "years": b - a, "p_start": p11, "p_end": p22,
                             "mean_start": mua, "mean_end": mub,
                             "gini_start": obs.loc[(a, z), "gini"], "gini_end": obs.loc[(b, z), "gini"],
                             "line_cf_start": za, "line_cf_end": zb, "p_mu2_L1": p21, "p_mu1_L2": p12,
                             **d})
    dec = pd.DataFrame(rows)
    dec.to_csv(OUT / "m3_decomposition.csv", index=False)
    return dec


# ----------------------------------------------------- elasticity benchmark
def elasticity(df, dec, wdi):
    obs = df.set_index(["year", "line"])
    periods = [(1992, 2002), (1995, 2002), (2002, 2011), (2003, 2011), (2012, 2014), (2014, 2019)]
    gdp = wdi["gdp_pc_ppp2021"]
    rows = []
    for a, b in periods:
        n = b - a
        for z in LINES:
            Ha, Hb = obs.loc[(a, z), "headcount"], obs.loc[(b, z), "headcount"]
            mua, mub = obs.loc[(a, z), "mean"], obs.loc[(b, z), "mean"]
            sa = float(D.sigma_from_gini(obs.loc[(a, z), "gini"]))
            sb = float(D.sigma_from_gini(obs.loc[(b, z), "gini"]))
            ln_a = float(D.lognormal_headcount(z, mua, sa))
            # distribution-neutral, log-normal: sigma fixed at start, survey mean path
            ln_b_mean = float(D.lognormal_headcount(z, mub, sa))
            # distribution-neutral, log-normal: sigma fixed, mean grows with GDP pc
            ln_b_gdp = float(D.lognormal_headcount(z, mua * gdp[b] / gdp[a], sa))
            # log-normal with actual sigma path (fit check)
            ln_b_fit = float(D.lognormal_headcount(z, mub, sb))
            r = dec[(dec.start == a) & (dec.end == b) & (dec.line == z) & (dec.measure == "headcount")]
            p21 = float(r["p_mu2_L1"].iloc[0])
            rows.append({
                "start": a, "end": b, "line": z, "H_start": Ha, "H_end": Hb,
                "elasticity_lognormal_start": float(D.lognormal_growth_elasticity(z, mua, sa)),
                "mean_growth_pa": D.annualized_log_change(mua, mub, n),
                "gdp_pc_growth_pa": D.annualized_log_change(gdp[a], gdp[b], n),
                "actual_pa": D.annualized_log_change(Ha, Hb, n),
                "lognormal_neutral_surveymean_pa": D.annualized_log_change(ln_a, ln_b_mean, n),
                "lognormal_neutral_gdp_pa": D.annualized_log_change(ln_a, ln_b_gdp, n),
                "empirical_neutral_surveymean_pa": D.annualized_log_change(Ha, p21, n),
                "lognormal_fit_H_start": ln_a, "lognormal_fit_H_end": ln_b_fit,
            })
    el = pd.DataFrame(rows)
    el.to_csv(OUT / "m3_elasticity.csv", index=False)
    return el


def plot_decomp(dec):
    agg = dec[(dec.kind == "aggregate") & (dec.measure == "headcount")
              & ~((dec.start == 2019) & (dec.end == 2024))].copy()
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), sharey=True)
    for ax, z in zip(axes, LINES):
        g = agg[agg.line == z]
        x = np.arange(len(g))
        gr = 100 * g["growth_shapley"] / g["years"]
        rd = 100 * g["redistribution_shapley"] / g["years"]
        ax.bar(x - 0.2, gr, 0.38, color="#2a78d6", label="Growth (mean)", edgecolor="white", lw=1)
        ax.bar(x + 0.2, rd, 0.38, color="#eb6834", label="Redistribution (Lorenz)", edgecolor="white", lw=1)
        ax.scatter(x, 100 * g["change"] / g["years"], color=INK, s=22, zorder=3, label="Total change")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xticks(x, [f"{a}-\n{b}" for a, b in zip(g.start, g.end)], fontsize=8)
        ax.set_title(f"${z:.2f}/day line", fontsize=10, color=INK)
        ax.grid(axis="y", color=GRID, lw=0.8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("Change in headcount, points per year", color=INK)
    axes[0].legend(frameon=False, fontsize=8, loc="lower left")
    fig.suptitle("Datt-Ravallion decomposition (Shapley), Brazil survey spells. "
                 "Spells do not cross the 2011/2012 survey break.", fontsize=10, color=INK, x=0.06, ha="left")
    fig.tight_layout()
    fig.savefig(OUT / "m3_fig_decomposition.png", dpi=150)
    plt.close(fig)


def md_tables(dec, el, version):
    agg = dec[(dec.kind == "aggregate")].copy()
    lines = [f"# M3 tables (PIP `{version}`)", "", "## Method", "",
             "- Datt-Ravallion: P(mu, L) with mu the PIP survey mean (2021 PPP $/day) and L the "
             "Lorenz curve. P(mu_end, L_start) is the PIP headcount (or gap) of the start survey "
             "at the line z * mu_start / mu_end; P(mu_start, L_end) is the end survey at "
             "z * mu_end / mu_start. This is exact because headcount and the normalized gap "
             "depend on incomes only through y / z. Growth and redistribution are the Shapley "
             "averages over both reference years (sum exactly to the change). PIP rounds "
             "query lines to $0.01 and outputs to 4 decimals (error under 0.05 points here).",
             "- Spells never cross the 2011 (PNAD) / 2012 (PNAD Continua) break.",
             "- Growth-elasticity benchmark (Bourguignon 2003): log-normal welfare, sigma from "
             "the start-year Gini (G = 2 Phi(sigma/sqrt2) - 1) held fixed, mean moved by the "
             "survey mean (or by WDI GDP per capita, PPP 2021). Empirical neutral uses the "
             "actual start-year distribution scaled to the end-year mean. Rates are "
             "100 * ln(end/start) / years.",
             "",
             "## Datt-Ravallion decomposition, multi-year spells",
             "", "Changes in percentage points (headcount) or points of the line (poverty gap), "
             "whole spell. Shapley split (exact). DR residual is from the original "
             "start-year-reference method.", "",
             "| spell | line | measure | start | end | change | growth | redistribution | DR residual |",
             "|---|---|---|---|---|---|---|---|---|"]
    for _, r in agg.iterrows():
        lines.append(f"| {int(r.start)}-{int(r.end)} | ${r.line:.2f} | {r.measure} | {100*r.p_start:.1f} | "
                     f"{100*r.p_end:.1f} | {100*r.change:+.1f} | {100*r.growth_shapley:+.1f} | "
                     f"{100*r.redistribution_shapley:+.1f} | {100*r.residual_dr:+.2f} |")
    lines += ["", "## Growth-elasticity benchmark (headcount, % change per year, log points)", "",
              "| spell | line | H start | H end | elasticity (LN, start) | survey mean growth | GDP pc growth | "
              "actual | LN neutral, survey mean | LN neutral, GDP pc | empirical neutral, survey mean |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in el.iterrows():
        lines.append(f"| {int(r.start)}-{int(r.end)} | ${r.line:.2f} | {100*r.H_start:.1f} | {100*r.H_end:.1f} | "
                     f"{r.elasticity_lognormal_start:.2f} | {r.mean_growth_pa:+.1f} | {r.gdp_pc_growth_pa:+.1f} | "
                     f"{r.actual_pa:+.1f} | {r.lognormal_neutral_surveymean_pa:+.1f} | "
                     f"{r.lognormal_neutral_gdp_pa:+.1f} | {r.empirical_neutral_surveymean_pa:+.1f} |")
    (OUT / "m3_tables.md").write_text("\n".join(lines) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pull_dir = P.latest_pull_dir()
    version = P.latest_version(P.load_raw(pull_dir / "pip_versions.json")["response"])["version"]
    df = survey_table(pull_dir)
    wdi = load_wdi(pull_dir)
    s = build_series(df, wdi)
    plot_series(s)
    dec = decomposition(df, pull_dir)
    el = elasticity(df, dec, wdi)
    plot_decomp(dec)
    md_tables(dec, el, version)
    (OUT / "m3_run_info.json").write_text(json.dumps(
        {"pip_version": version, "pull_dir": str(pull_dir.relative_to(P.REPO))}, indent=1))
    print("done", version)


if __name__ == "__main__":
    main()
