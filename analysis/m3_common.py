"""Shared definitions for the M3 scripts."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import pandas as pd  # noqa: E402

from cct import pip as P  # noqa: E402

COUNTRY = "BRA"
PPP_ROUND = "2021"
LINES = [3.00, 4.20, 8.30]
OUT = REPO / "output" / "M3"

# Multi-year spells reported alongside consecutive survey pairs. Each must
# lie within one comparable spell (PNAD 1981-2011 or PNADC 2012-2024);
# none crosses the 2011/2012 survey break.
AGG_SPELLS = [
    (1992, 2002), (1995, 2002), (2003, 2011), (2012, 2014),
    (2014, 2019), (2019, 2022), (2022, 2024), (2019, 2024),
]

WDI_INDICATORS = {
    "NY.GDP.PCAP.KD": "gdp_pc_const2015usd",
    "NY.GDP.PCAP.PP.KD": "gdp_pc_ppp2021",
}


def main_name(z: float) -> str:
    return f"pip_{COUNTRY}_all_" + f"{z:.2f}".replace(".", "p")


def survey_table(pull_dir: Path) -> pd.DataFrame:
    rows = []
    for z in LINES:
        rec = P.load_raw(pull_dir / f"{main_name(z)}.json")
        rows.extend(rec["response"])
    df = pd.DataFrame(rows)
    df = df[df["estimation_type"] == "survey"].copy()
    df["year"] = df["reporting_year"].astype(int)
    df["line"] = df["poverty_line"].round(2)
    return df.sort_values(["line", "year"]).reset_index(drop=True)


def spells(df: pd.DataFrame) -> list[tuple[int, int, str]]:
    """Consecutive survey pairs within each comparable spell, plus AGG_SPELLS."""
    one = df[df["line"] == LINES[0]]
    out = []
    for cs, g in one.groupby("comparable_spell"):
        yrs = sorted(g["year"])
        out += [(a, b, "consecutive") for a, b in zip(yrs[:-1], yrs[1:])]
    spell_of = dict(zip(one["year"], one["comparable_spell"]))
    for a, b in AGG_SPELLS:
        assert spell_of[a] == spell_of[b], (a, b)
        out.append((a, b, "aggregate"))
    return out
