"""M4: Bolsa Familia mechanical effect in PNAD Continua (annual visit files)
and the 2017 benchmark against Souza, Osorio, Paiva & Soares (2019).

Primary income concept (since the M4 correction, 2026-11-11): "effective"
(VD5002), which reproduces TD 2499's 2016-2017 levels; "habitual" (VD5008)
is kept as a labelled sensitivity (column `main` is False for it).

Run: python analysis/m4_05_pnadc_mechanical.py
Outputs: output/M4/pnadc_poverty.csv, output/M4/benchmark_2017.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import mechanical as m  # noqa: E402
from cct import pnadc  # noqa: E402
from cct.pnad import ROOT  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from m4_03_build_pnadc import PLAN  # noqa: E402

OUT = ROOT / "output" / "M4"

MAIN_CONCEPT = "effective"
CONCEPTS = ("effective", "habitual")

# Published benchmark (TD 2499, abstract and summary): in 2017 BF reduced
# extreme poverty by 25% and poverty by 15%; it lifted 3.4 million people
# out of extreme poverty and 3.2 million out of poverty.
SOUZA_2017 = {"extreme": {"pct_reduction": 25.0, "persons_lifted_M": 3.4},
              "poverty": {"pct_reduction": 15.0, "persons_lifted_M": 3.2}}


def one(year: int, visit: int, concept: str) -> pd.DataFrame:
    df = pnadc.load_pnadc(year, visit)
    f = pnadc.person_frame(df, year, concept)
    lines = m.lines_for(year, None)
    t = m.poverty_table(f["pc_with"].values, f["pc_without"].values,
                        f["weight"].values, lines)
    w = f["weight"]
    t["persons_lifted_M"] = [((f["pc_without"] <= z) & (f["pc_with"] > z)).mul(w).sum() / 1e6
                             for z in t["line_value"]]
    rec = f[f["bf_value"] > 0]
    t["year"], t["visit"], t["concept"] = year, visit, concept
    t["main"] = concept == MAIN_CONCEPT
    t["bf_item"] = ",".join(sorted(f["bf_item"].unique()))
    t["share_new_item"] = float(np.average(f["bf_item"] == "V5002A2", weights=w))
    t["recipients_M"] = rec["weight"].sum() / 1e6
    t["bf_monthly_total_Rbn_nominal"] = (rec["bf_value"] * rec["weight"]).sum() / 1e9
    t["persons_in_bf_hh_M"] = w[f["hh_bf"] > 0].sum() / 1e6
    return t


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for y, v in PLAN:
        for concept in CONCEPTS:
            t = one(y, v, concept)
            rows.append(t)
            print(y, v, concept, t[["line", "pct_reduction"]].round(1).values.tolist(), flush=True)
    res = pd.concat(rows, ignore_index=True)
    res.to_csv(OUT / "pnadc_poverty.csv", index=False, float_format="%.4f")

    b = res[res["year"] == 2017].copy()
    b["souza_pct_reduction"] = b["line"].map(lambda k: SOUZA_2017[k]["pct_reduction"])
    b["souza_persons_lifted_M"] = b["line"].map(lambda k: SOUZA_2017[k]["persons_lifted_M"])
    b["gap_pct_points"] = b["pct_reduction"] - b["souza_pct_reduction"]
    b["passes_2pt_criterion"] = b["gap_pct_points"].abs() <= 2
    cols = ["year", "concept", "line", "line_value", "rate_without_bf", "rate_with_bf",
            "pct_reduction", "souza_pct_reduction", "gap_pct_points",
            "persons_lifted_M", "souza_persons_lifted_M", "passes_2pt_criterion"]
    b[cols].to_csv(OUT / "benchmark_2017.csv", index=False, float_format="%.4f")
    print(b[cols].round(3).to_string())
