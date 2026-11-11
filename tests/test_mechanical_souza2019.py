"""Tests for the TD 2499 (Souza, Osorio, Paiva & Soares 2019) household rule."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import mechanical as m  # noqa: E402


def _hh(ids, ages, v1273, income=300.0):
    n = len(ids)
    return pd.DataFrame({
        "V0102": ids, "V0103": ["1"] * n, "UF": ["29"] * n,
        "V0401": ["1"] + ["3"] * (n - 1), "V8005": ages,
        "V4721": [income] * n, "V1273": v1273, "V4729": [100] * n,
    })


def test_bounds_2009():
    # 2009 schedule 68/22 (max 3)/33 (max 2), previous 62/20/30
    mn, mx = m.souza2019_bounds(2009, [1], [2], [1], [5])
    assert mn[0] == 20
    assert mx[0] == 68 + 3 * 22 + 33
    mn, mx = m.souza2019_bounds(2009, [0], [0], [0], [2])
    assert mx[0] == 68  # extreme-poor family without children: basic only


def test_bounds_bsp_year_scale_with_household_size():
    _, mx = m.souza2019_bounds(2014, [0], [1], [0], [6])
    assert mx[0] >= 77 * 6


def test_household_sum_and_bpc_split():
    # two members split R$ 50 + R$ 22 (=72, within 2009 bounds for a family
    # with one child); a third person's BPC (one minimum wage) is excluded
    pes = _hh(["1", "1", "1"], [35, 8, 70], [50.0, 22.0, 465.0], income=900.0)
    f = m.pnad_person_frame(pes, 2009, "souza2019")
    assert np.allclose(f["hh_bf"], 72.0)
    assert np.allclose(f["pc_without"], (900 - 72) / 3)
    assert f["bf_flag"].tolist() == [True, True, False]


def test_household_sum_above_max_is_not_bf():
    # R$ 300 of other income is above any 2009 BF amount for this family
    pes = _hh(["2", "2"], [40, 10], [300.0, np.nan], income=1000.0)
    f = m.pnad_person_frame(pes, 2009, "souza2019")
    assert np.allclose(f["hh_bf"], 0.0)
    assert np.allclose(f["pc_with"], f["pc_without"])


def test_person_rules_unchanged():
    pes = _hh(["3", "3"], [30, 5], [95.0, np.nan], income=400.0)
    f = m.pnad_person_frame(pes, 2006, "tv")
    assert np.allclose(f["pc_without"], (400 - 95) / 2)


def test_bsp_2012_only_with_young_children():
    _, mx_young = m.souza2019_bounds(2012, [1], [0], [0], [6])
    _, mx_old = m.souza2019_bounds(2012, [0], [1], [0], [6])
    assert mx_young[0] >= 70 * 6
    assert mx_old[0] == 70 + 32
