"""M4: survey Bolsa Familia totals vs administrative spending, and the
PNAD / PNAD Continua 2012-2015 overlap.

Run after m4_04 and m4_05.
Outputs: output/M4/survey_vs_admin.csv, output/M4/overlap_2012_2015.csv,
         output/M4/series_main.csv, output/M4/benchmark_souza2019.csv

Primary specification (M4 correction, 2026-11-11): PNAD rule "souza2019",
PNADC effective income, lines R$89/R$178 at June 2018 prices. In
series_main.csv the column `main` marks it; PNADC habitual income and the
PNAD person-level rule tv/tvb are the labelled sensitivities.

ADMINISTRATIVE FIGURES. The official series (MDS VIS DATA, Portal da
Transparencia, SIAFI) could not be reached from this environment (gov.br
hosts are blocked). The figures below were collected by web search and are
labelled with their source and type. Only the 2024 figure comes from an
official government outlet; the others are secondary citations. Treat the
ratios as indicative until replaced by the official annual series.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct.pnad import ROOT  # noqa: E402

OUT = ROOT / "output" / "M4"

# Souza et al. (2019, TD 2499), Grafico 6: headcount % without BF / with BF
# (extreme without, extreme with, poverty without, poverty with).
# "label" = printed labels; "chart" = read from the chart's vector paths
# (see notes/souza_2019.md and output/M4/M4_income_check.md).
SOUZA_LABEL = {2001: (7.9, 7.7, 20.7, 20.6), 2003: (7.5, 6.9, 20.2, 19.8),
               2005: (6.4, 5.3, 17.2, 16.0), 2007: (5.5, 4.5, 14.0, 12.6),
               2009: (5.1, 3.8, 11.6, 10.1), 2011: (4.8, 3.7, 10.0, 8.4),
               2013: (4.8, 3.4, 8.8, 7.1), 2015: (4.1, 2.8, 8.2, 6.7),
               2017: (6.6, 4.9, 10.6, 9.1)}
SOUZA_CHART = {2002: (7.14, 6.62, 19.93, 19.56), 2004: (7.32, 5.95, 19.16, 18.00),
               2006: (5.71, 4.42, 15.17, 13.59), 2008: (5.15, 3.82, 11.89, 10.54),
               2012: (4.35, 3.07, 9.15, 7.21), 2014: (3.59, 2.28, 7.21, 5.62),
               2016: (6.01, 4.28, None, None)}


def benchmark(ser: pd.DataFrame) -> pd.DataFrame:
    """Our cut vs Souza et al. for every year they publish, primary spec and
    the originally reported spec (PNAD tv/tvb, PNADC habitual)."""
    rows = []
    for y, src in [(y, "label") for y in SOUZA_LABEL] + [(y, "chart") for y in SOUZA_CHART]:
        pub = SOUZA_LABEL.get(y) or SOUZA_CHART.get(y)
        survey = "PNAD" if y <= 2015 else "PNADC"
        for line, i in (("extreme", 0), ("poverty", 2)):
            if pub[i] is None:
                continue
            p = 100 * (pub[i] - pub[i + 1]) / pub[i]
            r = {"year": y, "survey": survey, "line": line, "source": src,
                 "published_cut": p}
            for name, spec in (("primary", "main"), ("old", "old")):
                q = ser[(ser["year"] == y) & (ser["line"] == line) & (ser["survey"] == survey)]
                q = q[q["main"]] if spec == "main" else q[q["spec"].isin(["tv", "tvb", "habitual"])]
                v = float(q["pct_reduction"].iloc[0]) if len(q) else np.nan
                r[f"{name}_cut"] = v
                r[f"{name}_gap"] = v - p
            rows.append(r)
    b = pd.DataFrame(rows).sort_values(["line", "year"])
    b["primary_within_2pt"] = b["primary_gap"].abs() <= 2
    b["old_within_2pt"] = b["old_gap"].abs() <= 2
    return b

ADMIN = pd.DataFrame([
    # year, R$ billion per year (nominal), type, source
    (2004, 5.3, "secondary", "Redalyc article '18 anos de progresso' (cites ~R$5.3 bn in 2004)"),
    (2013, 24.5, "secondary", "academic paper cited in web search (R$24.5 bn spent in 2013)"),
    (2014, 25.3, "secondary", "MDS budget figure cited in Neder (AgEcon Search): R$25.3 bn presented for 2014"),
    (2015, 26.4, "secondary", "World Bank blog 'Protegendo os novos pobres' (R$26.4 bn in 2015)"),
    (2024, 168.3, "official", "Agencia Gov, Dec 2024: R$168.3 bn transferred in 2024"),
], columns=["year", "admin_Rbn_year", "admin_type", "admin_source"])


def main() -> None:
    pn = pd.read_csv(OUT / "pnad_poverty.csv")
    pc = pd.read_csv(OUT / "pnadc_poverty.csv")

    # survey totals: one row per year/source
    a = pn[pn["main"] & (pn["line"] == "extreme")][["year", "rule", "recipients_M", "bf_monthly_total_Rbn"]]
    a = a.assign(survey="PNAD", detail=a["rule"], survey_Rbn_year=12 * a["bf_monthly_total_Rbn"])
    b = pc[pc["main"] & (pc["line"] == "extreme")]
    b = b.assign(survey="PNADC", detail="visit" + b["visit"].astype(str) + " " + b["bf_item"],
                 survey_Rbn_year=12 * b["bf_monthly_total_Rbn_nominal"])
    s = pd.concat([a[["year", "survey", "detail", "recipients_M", "survey_Rbn_year"]],
                   b[["year", "survey", "detail", "recipients_M", "survey_Rbn_year"]]])
    s = s.merge(ADMIN, on="year", how="left")
    s["survey_over_admin"] = s["survey_Rbn_year"] / s["admin_Rbn_year"]
    s.sort_values(["year", "survey"]).to_csv(OUT / "survey_vs_admin.csv", index=False, float_format="%.3f")
    print(s.dropna(subset=["admin_Rbn_year"]).round(3).to_string())

    # main series, both surveys
    cols = ["year", "line", "line_value", "rate_without_bf", "rate_with_bf", "pct_reduction",
            "pp_reduction", "persons_lifted_M", "recipients_M"]
    # PNAD: primary rule plus the originally reported tv/tvb rule
    old = pn["rule"] == np.where(pn["year"].isin([2012, 2013, 2014, 2015]), "tvb", "tv")
    m1 = pn[pn["main"] | old][cols + ["rule", "main"]].rename(columns={"rule": "spec"})
    m1 = m1.assign(survey="PNAD", concept="V4721 (Sept)")
    m2 = pc[cols + ["concept", "main"]].assign(survey="PNADC", spec=pc["concept"])
    ser = pd.concat([m1, m2], ignore_index=True)
    ser["label"] = np.where(ser["main"], "primary", "sensitivity")
    ser = ser[["year", "survey", "spec", "label", "main", "concept"] + cols[1:]]
    ser = ser.sort_values(["year", "survey", "line", "main"], ascending=[True, True, True, False])
    ser.to_csv(OUT / "series_main.csv", index=False, float_format="%.4f")

    bm = benchmark(ser)
    bm.to_csv(OUT / "benchmark_souza2019.csv", index=False, float_format="%.2f")
    print(bm.round(1).to_string())

    ov = ser[ser["year"].between(2012, 2015)].pivot_table(
        index=["year", "line"], columns=["survey", "spec"], values="pct_reduction")
    ov.to_csv(OUT / "overlap_2012_2015.csv", float_format="%.2f")
    print(ov.round(1).to_string())
    # also the rule sensitivity in the overlap
    sens = pn[pn["year"].between(2012, 2015)].pivot_table(
        index=["year", "line"], columns="rule", values="pct_reduction")
    print(sens.round(1).to_string())


if __name__ == "__main__":
    main()
