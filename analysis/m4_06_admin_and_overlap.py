"""M4: survey Bolsa Familia totals vs administrative spending, and the
PNAD / PNAD Continua 2012-2015 overlap.

Run after m4_04 and m4_05.
Outputs: output/M4/survey_vs_admin.csv, output/M4/overlap_2012_2015.csv,
         output/M4/series_main.csv

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
    b = pc[(pc["concept"] == "habitual") & (pc["line"] == "extreme")]
    b = b.assign(survey="PNADC", detail="visit" + b["visit"].astype(str) + " " + b["bf_item"],
                 survey_Rbn_year=12 * b["bf_monthly_total_Rbn_nominal"])
    s = pd.concat([a[["year", "survey", "detail", "recipients_M", "survey_Rbn_year"]],
                   b[["year", "survey", "detail", "recipients_M", "survey_Rbn_year"]]])
    s = s.merge(ADMIN, on="year", how="left")
    s["survey_over_admin"] = s["survey_Rbn_year"] / s["admin_Rbn_year"]
    s.sort_values(["year", "survey"]).to_csv(OUT / "survey_vs_admin.csv", index=False, float_format="%.3f")
    print(s.dropna(subset=["admin_Rbn_year"]).round(3).to_string())

    # main series, both surveys
    m1 = pn[pn["main"]][["year", "line", "rate_with_bf", "rate_without_bf", "pct_reduction",
                         "persons_lifted_M"]].assign(survey="PNAD", concept="V4721 (Sept)")
    m2 = pc[["year", "line", "rate_with_bf", "rate_without_bf", "pct_reduction",
             "persons_lifted_M", "concept"]].assign(survey="PNADC")
    ser = pd.concat([m1, m2], ignore_index=True)
    ser.to_csv(OUT / "series_main.csv", index=False, float_format="%.4f")

    ov = ser[ser["year"].between(2012, 2015)].pivot_table(
        index=["year", "line"], columns=["survey", "concept"], values="pct_reduction")
    ov.to_csv(OUT / "overlap_2012_2015.csv", float_format="%.2f")
    print(ov.round(1).to_string())
    # also the rule sensitivity in the overlap
    sens = pn[pn["year"].between(2012, 2015)].pivot_table(
        index=["year", "line"], columns="rule", values="pct_reduction")
    print(sens.round(1).to_string())


if __name__ == "__main__":
    main()
