"""Python port of Data/ThesisDataCoding.do (Avila 2012).

The original .do file stays in the repository as the historical record. This
module rebuilds, from the raw columns of Data/ThesisDataCSV.csv:

1. Linear interpolation within country (Stata ``by country: ipolate y year``),
   producing the ``i*`` columns, plus a ``<var>_interp`` flag column that is 1
   where the value was filled by interpolation rather than observed.
2. One-year lags (Stata ``L.`` after ``tsset countryid year``): missing unless
   the previous row of the same country is exactly ``year - 1``.
3. Rates of change ``(x_t - x_{t-1}) / x_{t-1}`` (the ``rc*`` columns). The
   thesis calls these "log differences"; they are simple percentage changes.
4. The ``cctstage`` (0-3) and ``cctstate`` (0/1) recodes of ``yearfromcct``.

Quirks of the original code are reproduced on purpose and noted inline:
``rceducompleteprimary`` uses the non-interpolated level in the numerator, and
the DPT immunization lag and rate use the non-interpolated series.

Usage:
    python -m cct.clean_2012      # writes data/clean/thesis_2012_clean.parquet
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_CSV = ROOT / "Data" / "ThesisDataCSV.csv"
CLEAN_PARQUET = ROOT / "data" / "clean" / "thesis_2012_clean.parquet"

# (raw column, interpolated column) pairs, in the order of the ipolate block
# at the top of ThesisDataCoding.do.
IPOLATE = [
    ("fgt0ppp2", "ifgt0"),
    ("fgt1ppp2", "ifgt1"),  # the .do names it ifgt1ppp2; every later line uses ifgt1
    ("educhildout", "ieduchildout"),
    ("educompleteprimary", "ieducompleteprimary"),
    ("genpop", "igenpop"),
    ("genpopgrowth", "igenpopgrowth"),
    ("genpopdensity", "igenpopdensity"),
    ("govedugdp", "igovedugdp"),
    ("govgini", "igovgini"),
    ("govconsumexp", "igovconsumexp"),
    ("govgdpppp", "igovgdpppp"),
    ("govgdppppcapita", "igovgdppppcapita"),
    ("labforce", "ilabforce"),
    ("labprimaryedu", "ilabprimaryedu"),
    ("medmortinfant", "imedmortinfant"),
    ("meddptimmuinfant", "imeddptimmuinfant"),
    ("medmeaimmuinfant", "imedmeaimmuinfant"),
    ("medcalpday", "imedcalpday"),
    ("medundernourishment", "imedundernourishment"),
    ("medlowweightnewborn", "imedlowweightnewborn"),
    ("medprenatalcare", "imedprenatalcare"),
    ("medlifeexpbirth", "imedlifeexpbirth"),
    ("meddrpk", "imeddrpk"),
    ("medskilledbirth", "imedskilledbirth"),
    ("medh2o", "imedh2o"),
]

# The archived CSV stores these two interpolated series in millions (the Stata
# label for igovgdpppp says "in millions of current international $"); the raw
# columns are in units. Rates of change are unaffected by the scale.
SCALE = {"igenpop": 1e-6, "igovgdpppp": 1e-6}

# Short stem used in the lag (l*) and rate-of-change (rc*) names.
STEM = {i: i[1:] for _, i in IPOLATE}
STEM["ifgt0"] = "fgt0"
STEM["ifgt1"] = "fgt1"

# Where the .do file builds a lag or a numerator from a non-interpolated column.
LAG_SOURCE_OVERRIDE = {"meddptimmuinfant": "meddptimmuinfant", "medmeaimmuinfant": "medmeaimmuinfant"}
NUMERATOR_OVERRIDE = {
    "educompleteprimary": "educompleteprimary",
    "meddptimmuinfant": "meddptimmuinfant",
    "medmeaimmuinfant": "medmeaimmuinfant",
}


def load_raw(path: Path = RAW_CSV) -> pd.DataFrame:
    return pd.read_csv(path, encoding="latin1", low_memory=False)


def ipolate(df: pd.DataFrame, y: str, x: str = "year", by: str = "country") -> pd.Series:
    """Stata ``by <by>: ipolate y x``: linear interpolation of y on x within
    group, never extrapolating beyond the first or last observed x. Duplicate x
    values within a group are averaged first, as Stata does."""
    out = pd.Series(np.nan, index=df.index, dtype=float)
    for _, g in df.groupby(by, sort=False):
        obs = g.loc[g[y].notna(), [x, y]]
        if obs.empty:
            continue
        pts = obs.groupby(x)[y].mean()
        xs, ys = pts.index.to_numpy(dtype=float), pts.to_numpy(dtype=float)
        gx = g[x].to_numpy(dtype=float)
        vals = np.interp(gx, xs, ys)
        vals[(gx < xs.min()) | (gx > xs.max())] = np.nan
        out.loc[g.index] = vals
    return out


def lag(df: pd.DataFrame, var: str) -> pd.Series:
    """Stata ``L.var`` under ``tsset countryid year``. Assumes df is sorted by
    country and year."""
    prev = df.groupby("country")[var].shift(1)
    prev_year = df.groupby("country")["year"].shift(1)
    return prev.where(prev_year == df["year"] - 1)


def rate_of_change(num: pd.Series, lagged: pd.Series) -> pd.Series:
    """(x_t - x_{t-1}) / x_{t-1}. Division by zero gives missing, as in Stata."""
    with np.errstate(divide="ignore", invalid="ignore"):
        r = (num - lagged) / lagged
    return r.replace([np.inf, -np.inf], np.nan)


def cct_recodes(yearfromcct: pd.Series) -> pd.DataFrame:
    """recode yearfromcct (min/0 .=0) (1/2=1) (3/4=2) (5/max=3), gen(cctstage)
    recode yearfromcct (min/0 .=0) (1/max=1), gen(cctstate)

    Stata recode applies the first matching rule; non-integer values between
    rules would stay unchanged, but yearfromcct is integer-valued here."""
    y = yearfromcct
    stage = np.select([y.isna() | (y <= 0), y <= 2, y <= 4], [0, 1, 2], default=3)
    state = np.where(y.isna() | (y <= 0), 0, 1)
    return pd.DataFrame({"cctstage": stage.astype(int), "cctstate": state.astype(int)}, index=y.index)


# Raw poverty values of exactly 0 (Chile 2009, Kyrgyz Republic 1988): the
# interpolated columns behind the published tables interpolate through the 0
# but set the 0 cell itself to missing (so no -100% rate of change enters
# Table 5). Reproduced here; the step is not in the surviving .do file.
ZERO_IS_MISSING = ["fgt0ppp2", "fgt1ppp2"]


def build(raw: pd.DataFrame | None = None) -> pd.DataFrame:
    """Rebuild every variable ThesisDataCoding.do creates. The ``i*`` columns
    already present in the CSV are kept as ``<name>_csv`` for comparison and
    replaced by freshly interpolated values."""
    if raw is None:
        raw = load_raw()
    d = raw.sort_values(["country", "year"]).reset_index(drop=True).copy()
    new = {}
    for src, icol in IPOLATE:
        if icol in d.columns:
            new[f"{icol}_csv"] = d[icol]
        new[icol] = ipolate(d, src) * SCALE.get(icol, 1.0)
        if src in ZERO_IS_MISSING:
            new[icol] = new[icol].mask(d[src] == 0)
        new[f"{icol}_interp"] = (d[src].isna() & new[icol].notna()).astype(int)
    d = d.drop(columns=[i for _, i in IPOLATE if i in d.columns])
    d = pd.concat([d, pd.DataFrame(new, index=d.index)], axis=1)

    lags, rcs = {}, {}
    for src, icol in IPOLATE:
        stem = STEM[icol]
        lag_src = LAG_SOURCE_OVERRIDE.get(src, icol)
        lags[f"l{stem}"] = lag(d, lag_src)
        num = d[NUMERATOR_OVERRIDE.get(src, icol)]
        rcs[f"rc{stem}"] = rate_of_change(num, lags[f"l{stem}"])
        # A rate of change touches an interpolated value if either end was filled.
        flag = d[f"{icol}_interp"]
        rcs[f"rc{stem}_interp"] = ((flag == 1) | (lag(d, f"{icol}_interp") == 1)).astype(int)
    d = pd.concat([d, pd.DataFrame(lags), pd.DataFrame(rcs)], axis=1)
    d = pd.concat([d, cct_recodes(d["yearfromcct"])], axis=1)
    return d


def main() -> None:
    d = build()
    CLEAN_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    d.to_parquet(CLEAN_PARQUET, index=False)
    print(f"wrote {CLEAN_PARQUET.relative_to(ROOT)}: {d.shape[0]} rows, {d.shape[1]} columns")


if __name__ == "__main__":
    main()
