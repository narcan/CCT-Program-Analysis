"""Unit tests for the M4 microdata pipeline (no network needed)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import mechanical as m  # noqa: E402
from cct import pnad  # noqa: E402

SAS = """
DATA PES2006;
     INPUT  @00001  V0101  $4.   /* ANO */
            @00005  UF     $2.   /* UF */
            @00005  V0102  $8.   /* CONTROLE */
            @00013  V1273   6.   /* VALOR */
            @00019  V4605   5.2  /* PROB */
            @0024 Ano   $4.   /* PNADC style */
;
"""


def test_parse_sas_input():
    lay = pnad.parse_sas_input(SAS)
    assert lay["V0101"] == pnad.Field("V0101", 1, 4, True, 0)
    assert lay["UF"].start == 5 and lay["V0102"].width == 8
    assert lay["V1273"].char is False and lay["V1273"].width == 6
    assert lay["V4605"].decimals == 2
    assert lay["ANO"].start == 24


def test_read_fwf(tmp_path):
    lay = pnad.parse_sas_input(SAS)
    p = tmp_path / "x.txt"
    p.write_text("20061100001500009512345\n2006110000160000001.500\n")
    df = pnad.read_fwf(p, lay, ["V0101", "UF", "V1273", "V4605", "MISSING"])
    assert list(df.columns) == ["V0101", "UF", "V1273", "V4605"]
    assert df["UF"].tolist() == ["11", "11"]
    assert df["V1273"].tolist() == [95.0, 0.0]
    assert np.isclose(df["V4605"].iloc[0], 123.45)  # implied decimals
    assert np.isclose(df["V4605"].iloc[1], 1.5)     # explicit point kept


def test_typical_values_2006_and_2015():
    tv06 = m.typical_values(2006)
    for v in (15, 30, 45, 50, 65, 80, 95):
        assert v in tv06
    assert 350 not in tv06  # minimum wage = BPC, never BF
    tv15 = m.typical_values(2015)
    for v in (77, 35, 112, 147, 182, 42):
        assert v in tv15
    assert 102 in m.typical_values(2014)  # pre-June-2014 schedule still allowed
    assert 102 not in tv15
    assert all(v < m.MIN_WAGE[2015] for v in tv15)
    assert m.typical_values(2002) and max(m.typical_values(2002)) < m.MIN_WAGE[2002]


def test_flag_rules():
    v = pd.Series([95, 350, 1e12, np.nan, 0, 120, 150, 133])
    tv = m.flag_bf_pnad(v, 2006, "tv").tolist()
    assert tv == [True, False, False, False, False, True, False, False]
    tvb = m.flag_bf_pnad(v, 2015, "tvb").tolist()
    # 2015: 95 and 133 look like BSP top-ups; 150 is a round value; 350 < MW
    assert tvb[0] and tvb[7] and not tvb[6] and not tvb[2]
    assert m.flag_bf_pnad(v, 2006, "lt_mw").tolist()[1] is False  # 350 == MW


def test_fgt0_and_table():
    inc = np.array([10.0, 50.0, 100.0, 200.0])
    w = np.array([1.0, 1.0, 1.0, 1.0])
    assert m.fgt0(inc, w, 50.0) == 0.5
    t = m.poverty_table(inc, inc - np.array([0, 40, 0, 0]), w, {"x": 50.0})
    assert np.isclose(t["rate_with_bf"].iloc[0], 0.5)
    assert np.isclose(t["rate_without_bf"].iloc[0], 0.5)
    t2 = m.poverty_table(inc + np.array([0, 10, 0, 0]), inc, w, {"x": 50.0})
    assert np.isclose(t2["pct_reduction"].iloc[0], 50.0)


def test_person_frame_excludes_non_members_and_subtracts_bf():
    pes = pd.DataFrame({
        "V0102": ["1"] * 4, "V0103": ["1"] * 4, "UF": ["11"] * 4,
        "V0401": ["1", "2", "3", "7"], "V8005": [30, 30, 5, 40],
        "V4721": [400.0, 400.0, 400.0, 400.0],
        "V1273": [95.0, np.nan, np.nan, 50.0],
        "V4729": [100, 100, 100, 100],
    })
    f = m.pnad_person_frame(pes, 2006, "tv")
    assert len(f) == 3  # domestic worker excluded
    assert np.allclose(f["pc_with"], 400 / 3)
    assert np.allclose(f["pc_without"], (400 - 95) / 3)
