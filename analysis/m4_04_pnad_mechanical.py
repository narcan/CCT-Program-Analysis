"""M4: Bolsa Familia mechanical effect in annual PNAD, 2001-2015.

1. Validates the BF identification rules against the direct receipt
   questions in the 2004 and 2006 supplements.
2. Poverty with and without BF income, every PNAD year, three rules.

Run: python analysis/m4_04_pnad_mechanical.py
Outputs: output/M4/pnad_validation.csv, output/M4/pnad_poverty.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import mechanical as m  # noqa: E402
from cct import pnad  # noqa: E402

OUT = pnad.ROOT / "output" / "M4"
YEARS = sorted(pnad.PNAD_URLS)
RULES = ["tv", "tvb", "lt_mw"]
MAIN_RULE = {y: ("tvb" if y in m.BSP_YEARS else "tv") for y in YEARS}


def self_report(dom: pd.DataFrame, year: int) -> pd.DataFrame:
    d = dom.copy()
    d["hh"] = d["V0102"].astype(str) + d["V0103"].astype(str)
    if year == 2004:
        d["rep_bf"] = d["V2005"].eq("1")
        d["rep_any"] = (d["V2005"].eq("1") | d["V2003"].eq("1") | d["V0620"].eq("2")
                        | d["V2007"].eq("1") | d["V2012"].eq("2") | d["V2014"].eq("2")
                        | d["V1600"].eq("2"))
        d["answered"] = d["V2005"].isin(["1", "3"])
    elif year == 2006:
        d["rep_bf"] = d["V2403"].eq("1")
        d["rep_any"] = d["rep_bf"] | d["V2407"].eq("1") | d["V2409"].eq("1")
        d["answered"] = d["V2403"].isin(["1", "3"])
    return d.set_index("hh")[["rep_bf", "rep_any", "answered"]]


def validation() -> pd.DataFrame:
    rows = []
    for y in (2004, 2006):
        pes, dom = pnad.load_pnad(y)
        sr = self_report(dom, y)
        for rule in RULES:
            f = m.pnad_person_frame(pes, y, rule)
            h = f.drop_duplicates("hh").set_index("hh")
            h = h.join(sr, how="inner")
            h = h[h["answered"]]
            w = h["weight"] * h["n_members"]  # persons
            flag = h["hh_bf"] > 0
            for ref in ("rep_bf", "rep_any"):
                r = h[ref]
                rows.append({
                    "year": y, "rule": rule, "reference": ref,
                    "persons_flagged_M": (w * flag).sum() / 1e6,
                    "persons_reporting_M": (w * r).sum() / 1e6,
                    "sensitivity": (w * (flag & r)).sum() / (w * r).sum(),
                    "precision": (w * (flag & r)).sum() / (w * flag).sum(),
                    "false_pos_rate": (w * (flag & ~r)).sum() / (w * ~r).sum(),
                })
    return pd.DataFrame(rows)


def poverty_all() -> pd.DataFrame:
    rows = []
    for y in YEARS:
        pes, _ = pnad.load_pnad(y)
        lines = m.lines_for(y, 9)
        for rule in RULES:
            f = m.pnad_person_frame(pes, y, rule)
            t = m.poverty_table(f["pc_with"].values, f["pc_without"].values,
                                f["weight"].values, lines)
            rec = f[f["bf_flag"]]
            t["year"] = y
            t["rule"] = rule
            t["main"] = rule == MAIN_RULE[y]
            t["recipients_M"] = rec["weight"].sum() / 1e6
            t["bf_monthly_total_Rbn"] = (rec["v1273"] * rec["weight"]).sum() / 1e9
            hh = f.drop_duplicates("hh")
            t["hh_income_monthly_total_Rbn"] = (hh["hh_income"] * hh["weight"]).sum() / 1e9
            t["bf_share_income_pct"] = 100 * t["bf_monthly_total_Rbn"] / t["hh_income_monthly_total_Rbn"]
            t["persons_lifted_M"] = [
                (f["weight"] * ((f["pc_without"] <= z) & (f["pc_with"] > z))).sum() / 1e6
                for z in t["line_value"]]
            rows.append(t)
            print(y, rule, t[["line", "pct_reduction"]].round(1).values.tolist(), flush=True)
    return pd.concat(rows, ignore_index=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    v = validation()
    v.to_csv(OUT / "pnad_validation.csv", index=False, float_format="%.4f")
    print(v.round(3).to_string())
    p = poverty_all()
    p.to_csv(OUT / "pnad_poverty.csv", index=False, float_format="%.4f")
