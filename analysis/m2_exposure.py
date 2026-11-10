"""M2 task 2: effect paths.

Mechanical effect: Souza, Osorio, Paiva & Soares (2019, IPEA TD 2499) report
that Bolsa Familia income lowers measured poverty by about 15% (25% for
extreme poverty). It is phased in with coverage: ramp_t = min(1, F_t / E),
with F_t families covered in December and E = 11.1M, the government's 2006
target (its estimate of the number of poor families). Zero before 2004.

Long-run effect: national relative reduction = theta x S_t, where theta is the
individual relative reduction in adult poverty among exposed adults and S_t is
the share of poor working-age adults (18-64) who were exposed as children.

Exposure: a person born in year b is exposed if their family was enrolled while
they still had at least 3 years of eligible age (0-17) left, i.e. by year b+15.
With enrollment treated as persistent once reached:
    P(b) = reach x max_{y <= b+15, y >= b} min(1, F_y / E)
reach = share of today's poor adults whose childhood family was in the target
group AND actually reached (exclusion errors). Scenarios:
    low        reach 0.5
    central    reach 0.7
    generous   reach 1.0 and Bolsa Escola (2001-2002) counted as exposure
S_t = sum over ages 18-64 of pop(age, t) P(t - age) / pop(18-64, t), using all
adults 18-64 as the stand-in for poor adults (poor adults are on average
younger, which would raise S_t slightly; the generous case covers this).

Population by single year of age: WDI 5-year age groups (UN WPP based) split
evenly within each group. Documented approximation: single-year WPP files were
not reachable from this environment (the UN data portal API needs a token and
IBGE SIDRA was blocked by the network proxy).
Run: python analysis/m2_exposure.py -> output/M2/exposure_share.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m2_data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "M2"

# Families receiving Bolsa Familia (December, millions). verified = found in a
# source during this run (MDS / Ipeadata series as reported by news and
# government pages); "approx" = not found, interpolated or taken from a target.
COVERAGE = {
    2003: (3.6, "verified"), 2004: (6.6, "verified"), 2005: (8.7, "verified"),
    2006: (11.0, "verified"), 2007: (11.0, "verified"), 2008: (10.6, "verified"),
    2009: (12.4, "verified"), 2010: (12.8, "approx: 2010 target 12.9"),
    2011: (13.4, "approx: interpolated"), 2012: (13.9, "verified"),
    2013: (14.1, "approx: interpolated"), 2014: (14.1, "verified"),
    2015: (13.9, "approx"), 2016: (13.6, "approx"), 2017: (13.8, "approx"),
    2018: (14.2, "verified"), 2019: (13.2, "verified"),
    2020: (14.3, "approx: Auxilio Brasil transition"), 2021: (14.5, "approx: Auxilio Brasil"),
    2022: (21.6, "verified: December"), 2023: (21.3, "verified: yearly average"),
    2024: (20.9, "verified: 20.86"),
}
# Predecessor Bolsa Escola (school-age children), generous case only. Not verified.
PREDECESSOR = {2001: 4.8, 2002: 5.0}
ELIGIBLE = 11.1
SCENARIOS = {"low": (0.5, False), "central": (0.7, False), "generous": (1.0, True)}
ADULT_AGES = range(18, 65)


def ramp(predecessor=False):
    r = {y: min(1.0, f / ELIGIBLE) for y, (f, _) in COVERAGE.items()}
    if predecessor:
        r.update({y: min(1.0, f / ELIGIBLE) for y, f in PREDECESSOR.items()})
    return r


def mechanical_ramp(years):
    """Coverage ramp used for the mechanical effect: 0 before 2004."""
    r = ramp()
    return np.array([r.get(y, 0.0) if y >= 2004 else 0.0 for y in years])


def cohort_exposure(b, reach, predecessor):
    r = ramp(predecessor)
    vals = [v for y, v in r.items() if b <= y <= b + 15]
    if b + 15 > max(r):          # still a child in the last data year
        vals.append(r[max(r)])
    return reach * (max(vals) if vals else 0.0)


def single_year_pop():
    """{year: {age: count}} for ages 0-79 from 5-year groups split evenly."""
    groups = m2_data.pop_by_group()
    out = {}
    for g, series in groups.items():
        if g == "80UP":
            continue
        a0 = int(g[:2])
        for y, v in series.items():
            for a in range(a0, a0 + 5):
                out.setdefault(y, {})[a] = v / 5.0
    return out


def exposure_shares(years=range(2000, 2025)):
    pop = single_year_pop()
    rows = []
    for t in years:
        row = {"year": t}
        w = np.array([pop[t][a] for a in ADULT_AGES])
        for name, (reach, pred) in SCENARIOS.items():
            p = np.array([cohort_exposure(t - a, reach, pred) for a in ADULT_AGES])
            row[f"S_{name}"] = float((w * p).sum() / w.sum())
        row["coverage_families_m"] = COVERAGE.get(t, (np.nan, ""))[0]
        row["coverage_source"] = COVERAGE.get(t, (np.nan, "none"))[1]
        row["mechanical_ramp"] = float(mechanical_ramp([t])[0])
        rows.append(row)
    return pd.DataFrame(rows)


def effect_paths(years, shares=None):
    """Log effects by year. Returns dict name -> array (log scale, negative = less poverty)."""
    if shares is None:
        shares = exposure_shares().set_index("year")
    yrs = np.asarray(years)
    out = {}
    m = mechanical_ramp(yrs)
    out[("mechanical", 0.15)] = np.log(1 - 0.15 * m)
    out[("mechanical", 0.25)] = np.log(1 - 0.25 * m)
    for sc in SCENARIOS:
        S = np.array([shares.loc[y, f"S_{sc}"] if y in shares.index else 0.0 for y in yrs])
        for th in (0.0, 0.05, 0.10, 0.20, 0.30):
            out[(f"longrun_{sc}", th)] = np.log(1 - th * S)
    return out


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    df = exposure_shares()
    df.to_csv(OUT / "exposure_share.csv", index=False, float_format="%.4f")
    print(df.round(3).to_string())
