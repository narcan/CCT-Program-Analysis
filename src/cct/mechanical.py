"""Mechanical effect of Bolsa Familia (BF) on poverty.

Two pieces:

1. Identification of BF income in annual PNAD, where BF has no item of its
   own and sits in the catch-all "juros de caderneta de poupanca e de outras
   aplicacoes, dividendos e outros rendimentos" (V1273). We follow the
   "typical values" method used by the IPEA group (Soares, Ribas & Osorio
   2007/2010; Souza, Osorio & Soares 2011, IPEA TD 1654; Souza, Osorio,
   Paiva & Soares 2019, IPEA TD 2499): a value in V1273 is classified as a
   programme transfer when it equals a benefit amount that the programme
   rules made possible in the reference month (September). The exact
   implementation rules in TD 2499 could not be read from this environment
   (the IPEA site is blocked), so the rule sets below are reconstructed from
   the benefit schedules in the laws and decrees, and offered in variants
   that are validated against the direct receipt questions in the 2004 and
   2006 supplements and against PNAD Continua for 2012-2015.

2. Poverty with and without BF income: weighted headcount (FGT0) of persons
   whose household per-capita income is at or below a line.

Benefit schedule (monthly R$), from the programme laws and decrees:
  Bolsa Escola (Lei 10.219/2001): R$15 per child 6-15, max 3.
  Bolsa Alimentacao (MP 2.206-1/2001): R$15 per child 0-6/pregnant, max 3.
  Auxilio Gas (Decreto 4.102/2002): R$7.50/month (R$15 every two months).
  Cartao Alimentacao (Lei 10.689/2003): R$50.
  PETI: R$25 per child (rural), R$40 (urban).
  Bolsa Familia (Lei 10.836/2004; Decreto 5.209/2004):
    2003-10 to 2007-07: basic 50, variable 15 (max 3)
    2007-08 (Decreto 6.157/2007): basic 58, variable 18 (max 3)
    2008-03: youth variable BVJ 30 (max 2)
    2008-07 (Decreto 6.491/2008): basic 62, variable 20, BVJ 30
    2009-09 (Decreto 6.917/2009): basic 68, variable 22, BVJ 33
    2011-03/04 (Decreto 7.447/2011): basic 70, variable 32, BVJ 38;
        variable limit raised to 5 from 2011-09 (Lei 12.512/2011)
    2012-06 (Decreto 7.758/2012): Beneficio para Superacao da Extrema
        Pobreza (BSP), a top-up of any amount that lifts the family's
        per-capita income to the extreme poverty line (families with
        children 0-6 first, all extreme poor families from 2013-03)
    2014-06 (Decreto 8.232/2014): basic 77, variable 35, BVJ 42
    2016-07 (Decreto 8.794/2016): basic 85, variable 39, BVJ 46
    2018-07 (Decreto 9.396/2018): basic 89, variable 41, BVJ 48
"""
from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np
import pandas as pd

# National minimum wage in force in September of each year (R$/month).
MIN_WAGE = {
    2001: 180, 2002: 200, 2003: 240, 2004: 260, 2005: 300, 2006: 350,
    2007: 380, 2008: 415, 2009: 465, 2011: 545, 2012: 622, 2013: 678,
    2014: 724, 2015: 788, 2016: 880, 2017: 937, 2018: 954, 2019: 998,
    2020: 1045, 2021: 1100, 2022: 1212, 2023: 1320, 2024: 1412, 2025: 1518,
}

# BF parameters in force in September of each PNAD year:
# (basic, variable, max_variable, bvj, max_bvj). None = programme absent.
BF_PARAMS = {
    2001: None, 2002: None, 2003: None,
    2004: (50, 15, 3, 0, 0),
    2005: (50, 15, 3, 0, 0),
    2006: (50, 15, 3, 0, 0),
    2007: (58, 18, 3, 0, 0),
    2008: (62, 20, 3, 30, 2),
    2009: (68, 22, 3, 33, 2),
    2011: (70, 32, 5, 38, 2),
    2012: (70, 32, 5, 38, 2),
    2013: (70, 32, 5, 38, 2),
    2014: (77, 35, 5, 42, 2),
    2015: (77, 35, 5, 42, 2),
}
# Previous schedule, still possible in September because of payment lags
# right after a readjustment (2007-08 and 2009-09 changes).
BF_PREV = {2007: (50, 15, 3, 0, 0), 2009: (62, 20, 3, 30, 2)}
BSP_YEARS = {2012, 2013, 2014, 2015}


def _bf_values(params) -> set[float]:
    if params is None:
        return set()
    basic, var, kmax, bvj, jmax = params
    out = set()
    for b in (0, basic):
        for k in range(kmax + 1):
            for j in range(jmax + 1):
                v = b + k * var + j * bvj
                if v > 0:
                    out.add(float(v))
    return out


def _legacy_values(year: int) -> set[float]:
    """Values from the pre-BF federal programmes (Bolsa Escola, Bolsa
    Alimentacao, Auxilio Gas, Cartao Alimentacao) and their combinations.
    Legacy benefits were phased out by 2006-2007; we allow them up to 2007.
    PETI (R$25/40 per child) was merged into BF only in 2006 and kept its
    own values; we allow up to 3 children."""
    if year > 2007:
        return set()
    be = [0, 15, 30, 45]                       # Bolsa Escola
    ba = [0, 15, 30, 45] if year >= 2001 else [0]  # Bolsa Alimentacao
    ag = [0, 7.5] if year >= 2002 else [0]     # Auxilio Gas, monthly
    ca = [0, 50] if year >= 2003 else [0]      # Cartao Alimentacao
    peti = [0, 25, 50, 75, 40, 80, 120]
    out = set()
    for a, b, c, d, e in itertools.product(be, ba, ag, ca, peti):
        v = a + b + c + d + e
        if v > 0:
            out.add(v)
    return out


@lru_cache(maxsize=None)
def typical_values(year: int, include_legacy: bool = True) -> frozenset:
    """All integer amounts consistent with federal transfer programme rules
    in September of `year`. Amounts with 50 centavos (auxilio gas) are
    entered in PNAD as integers, so both floor and ceil are accepted."""
    vals = set(_bf_values(BF_PARAMS.get(year)))
    if year in BF_PREV:
        vals |= _bf_values(BF_PREV[year])
    if include_legacy:
        vals |= _legacy_values(year)
        # BF families could also still hold Auxilio Gas / PETI in transition.
        if year <= 2007:
            extra = set()
            for v in list(_bf_values(BF_PARAMS.get(year))):
                for add in (7.5, 15, 25, 40):
                    extra.add(v + add)
            vals |= extra
    out = set()
    for v in vals:
        out.add(float(np.floor(v)))
        out.add(float(np.ceil(v)))
    return frozenset(out)


def flag_bf_pnad(v1273: pd.Series, year: int, rule: str = "tv") -> pd.Series:
    """Boolean flag: is this person's V1273 value classified as BF/programme
    income?

    rules:
      "tv"   typical values only (exact matches to the benefit schedule).
      "tvb"  typical values, plus, in BSP years (2012+), any value from 1 up
             to the BSP-compatible ceiling (below the minimum wage) that is
             not a round multiple of 50 above 100 (which look like rents,
             private transfers or interest). This captures BSP top-ups.
      "lt_mw" any positive value strictly below the minimum wage (an upper
             bound that also catches small interest and other income).
    """
    v = pd.to_numeric(v1273, errors="coerce")
    v = v.where(v < 1e11)
    pos = v > 0
    tv = v.isin(typical_values(year))
    if rule == "tv":
        return (pos & tv).fillna(False)
    mw = MIN_WAGE[year]
    if rule == "lt_mw":
        return (pos & (v < mw)).fillna(False)
    if rule == "tvb":
        if year not in BSP_YEARS:
            return (pos & tv).fillna(False)
        roundish = (v > 100) & (v % 50 == 0)
        bsp = pos & (v < mw) & ~roundish
        return (pos & (tv | bsp)).fillna(False)
    raise ValueError(rule)


# --------------------------------------------------------------------------
# Poverty lines
# --------------------------------------------------------------------------
# Souza et al. (2019, TD 2499) measure poverty with fixed real lines equal to
# the BF eligibility lines of 2018: R$89 (extreme poverty) and R$178
# (poverty) per person per month, in force from July 2018 (Decreto
# 9.396/2018), deflated with the INPC.
LINE_EXTREME_2018 = 89.0
LINE_POVERTY_2018 = 178.0
LINE_BASE = (2018, 7)


def fgt0(pc_income: np.ndarray, weight: np.ndarray, line: float) -> float:
    """Weighted headcount ratio: share of persons with pc income <= line."""
    ok = ~np.isnan(pc_income) & ~np.isnan(weight)
    w = weight[ok]
    return float(np.sum(w * (pc_income[ok] <= line)) / np.sum(w))


def poverty_table(pc_with: np.ndarray, pc_without: np.ndarray,
                  weight: np.ndarray, lines: dict[str, float]) -> pd.DataFrame:
    rows = []
    for name, z in lines.items():
        p1 = fgt0(pc_with, weight, z)
        p0 = fgt0(pc_without, weight, z)
        rows.append({"line": name, "line_value": z,
                     "rate_with_bf": p1, "rate_without_bf": p0,
                     "pct_reduction": 100 * (p0 - p1) / p0 if p0 else np.nan,
                     "pp_reduction": 100 * (p0 - p1)})
    return pd.DataFrame(rows)
