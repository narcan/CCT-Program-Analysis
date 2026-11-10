"""The Python port of ThesisDataCoding.do must reproduce the interpolated
variables stored in Data/ThesisDataCSV.csv (the file behind the published
tables), and the derived variables the regressions use.

A small number of cells in the archived CSV cannot be rebuilt from the raw
columns of the same file, because the raw columns were edited after the
interpolated columns were made (or the CSV export rounded them). They are
listed in KNOWN_DIFFS with the reason; none of them is a Brazil regression
variable, and the test fails if any other cell differs.
"""

import numpy as np
import pandas as pd
import pytest

from cct.clean_2012 import IPOLATE, build

KENYA_BLOCK = ("Kenya", range(2004, 2011))  # interpolated columns shifted in the CSV export

KNOWN_DIFFS = {
    # variable: list of (country, years, reason)
    "*": [(*KENYA_BLOCK, "row block 2004-2010 corrupted in the CSV's i* columns")],
    "ifgt0": [("Ukraine", range(1989, 1996), "CSV interpolates through a 0 in 1992 that the raw column no longer has")],
    "ifgt1": [("Ukraine", range(1989, 1996), "as ifgt0")],
    "igenpop": [("Brazil", [1983, 1988], "raw population revised by about 1 million after interpolation"),
                ("Mexico", [2005], "raw population revised by 1 million")],
    "igovconsumexp": [("Laos", range(1989, 2000), "CSV rounded to 3 significant digits"),
                      ("Lesotho", [1997, 1998], "rounded"),
                      ("Mozambique", [1986], "rounded")],
}


@pytest.fixture(scope="module")
def d():
    return build()


def _excluded(d, var):
    mask = pd.Series(False, index=d.index)
    for v in ("*", var):
        for country, years, _ in KNOWN_DIFFS.get(v, []):
            mask |= (d["country"] == country) & d["year"].isin(list(years))
    return mask


@pytest.mark.parametrize("var", [i for _, i in IPOLATE])
def test_interpolated_columns_match_csv(d, var):
    a, b = d[var], d[f"{var}_csv"]
    keep = ~_excluded(d, var)
    a, b = a[keep], b[keep]
    assert (a.isna() == b.isna()).all(), d.loc[a.index[a.isna() != b.isna()], ["country", "year"]]
    both = a.notna()
    np.testing.assert_allclose(a[both], b[both], rtol=1e-6, atol=1e-6)  # CSV: Stata floats, 6 decimals


def test_known_diffs_are_few(d):
    # Guard against the exception list silently growing.
    total = sum(int(_excluded(d, v).sum()) for _, v in IPOLATE)
    assert total < 25 * 12 + 40


@pytest.mark.parametrize("var", ["ifgt0", "ifgt1", "igovgdpppp", "igovgini"])
def test_brazil_regression_inputs_exact(d, var):
    b = d[d["country"] == "Brazil"]
    a, c = b[var], b[f"{var}_csv"]
    assert (a.isna() == c.isna()).all()
    # The CSV holds Stata floats (about 7 significant digits).
    np.testing.assert_allclose(a.dropna(), c.dropna(), rtol=1e-6, atol=1e-6)


def test_interp_flags_brazil(d):
    b = d[d["country"] == "Brazil"].set_index("year")
    assert b.index[b["ifgt0_interp"] == 1].tolist() == [1991, 1994, 2000, 2006, 2007]
    assert b.loc[b["fgt0ppp2"].notna()].index.min() == 1981
    # rate of change touching an interpolated level is flagged
    assert b.loc[[1991, 1992, 2006, 2007, 2008], "rcfgt0_interp"].eq(1).all()
    assert b.loc[[2004, 2005, 2009], "rcfgt0_interp"].eq(0).all()


def test_rates_and_lags_match_table1_data_rows(d):
    # ERRATA.md item 5, "Data" rows, computed from the CSV's own i* columns.
    b = d[d["country"] == "Brazil"]
    for v, (n, mean, sd) in {"rcfgt0": (28, -0.036, 0.093), "rcfgt1": (28, -0.039, 0.128)}.items():
        s = b[v].dropna()
        assert len(s) == n
        assert round(s.mean(), 3) == mean
        assert round(s.std(), 3) == sd


def test_lag_respects_year_gaps(d):
    b = d[d["country"] == "Brazil"].set_index("year")
    assert np.isnan(b.loc[1980, "lfgt0"])
    assert b.loc[1982, "lfgt0"] == b.loc[1981, "ifgt0"]


def test_table5_rate_of_change_sample(d):
    # Published Table 5 N: 189 Latin America CCT, 119 non-CCT country-years.
    la = d[d["region"] == "Latin America"]
    assert la.loc[la["eventualcct"] == 1, "rcfgt0"].notna().sum() == 189
    assert la.loc[la["eventualcct"] == 0, "rcfgt0"].notna().sum() == 119


def test_cct_recodes(d):
    y = d["yearfromcct"]
    assert set(d["cctstage"].unique()) <= {0, 1, 2, 3}
    assert (d.loc[y.isna() | (y <= 0), "cctstage"] == 0).all()
    assert (d.loc[y.between(1, 2), "cctstage"] == 1).all()
    assert (d.loc[y.between(3, 4), "cctstage"] == 2).all()
    assert (d.loc[y >= 5, "cctstage"] == 3).all()
    assert (d["cctstate"] == (y > 0).astype(int)).all()
    b = d[d["country"] == "Brazil"].set_index("year")
    assert b.loc[2003, "cctstage"] == 0 and b.loc[2004, "cctstage"] == 1
    assert b.loc[2006, "cctstage"] == 2 and b.loc[2008, "cctstage"] == 3
