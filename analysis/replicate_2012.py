"""
Replication and re-check of the 2012 thesis
"An Analysis of CCT Programs and Poverty" (Avila, Columbia QMSS, 2012).

This script reads the archived dataset (Data/ThesisDataCSV.csv), rebuilds the
variables the way Data/ThesisDataCoding.do built them, and re-runs the models
from Data/ThesisDataAnalysis.do. It prints:

  1. Brazil data coverage (which years are observed and which are interpolated)
  2. Table 6 reproduced, with the original labels and the corrected labels
  3. A simpler model with a single post-2003 dummy
  4. Table 5 with the standard errors the code actually used and with robust ones
  5. Table 1 recomputed from the data, next to the published numbers
  6. Country coding and sample-rule checks

Run from the repository root:
    python analysis/replicate_2012.py

Standard errors: Stata's `reg ..., robust` is HC1, with p-values from a
t distribution with n - k degrees of freedom. We use the same here
(cov_type="HC1", use_t=True), so t statistics and stars match Stata.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "Data" / "ThesisDataCSV.csv"


def stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""


def fmt(model, term):
    b, t, p = model.params[term], model.tvalues[term], model.pvalues[term]
    return f"{b:9.4f}{stars(p):3s} (t={t:6.2f}, p={p:.3f})"


def header(text):
    print("\n" + "=" * 78 + "\n" + text + "\n" + "=" * 78)


# ---------------------------------------------------------------------------
# Load data and rebuild variables (mirrors Data/ThesisDataCoding.do)
# ---------------------------------------------------------------------------
raw = pd.read_csv(DATA, encoding="latin1", low_memory=False)
d = raw.sort_values(["country", "year"]).reset_index(drop=True).copy()


def rate_of_change(df, var):
    """(x_t - x_{t-1}) / x_{t-1}, using Stata's L. operator semantics:
    the lag is missing unless the previous row is exactly year - 1."""
    prev = df.groupby("country")[var].shift(1)
    prev_year = df.groupby("country")["year"].shift(1)
    return pd.Series(
        np.where(prev_year == df["year"] - 1, (df[var] - prev) / prev, np.nan),
        index=df.index,
    )


new_cols = {
    "rcfgt0": rate_of_change(d, "ifgt0"),  # poverty headcount ratio (FGT0)
    "rcfgt1": rate_of_change(d, "ifgt1"),  # depth of poverty (FGT1)
    "rcgovgdpppp": rate_of_change(d, "igovgdpppp"),
    "rcgovgini": rate_of_change(d, "igovgini"),
}

# ThesisDataCoding.do, line 157:
#   recode yearfromcct (min/0 .=0) (1/2=1) (3/4=2) (5/max=3), gen(cctstage)
# Four stages, not three: 0 = up to CCT year, 1 = years 1-2, 2 = years 3-4, 3 = year 5+.
y = d["yearfromcct"]
cctstage = np.select([y.isna() | (y <= 0), y <= 2, y <= 4], [0, 1, 2], default=3)
new_cols["cctstage"] = cctstage

# ThesisDataAnalysis.do: mkspline before 1 phase1 2 phase2 = cctstage
# Stata's mkspline with knots at 1 and 2 gives
#   before = min(x, 1); phase1 = max(min(x, 2) - 1, 0); phase2 = max(x - 2, 0)
# Because cctstage only takes values 0..3, these are step dummies:
#   before = 1 if cctstage >= 1  (year 1+ after CCT start)
#   phase1 = 1 if cctstage >= 2  (year 3+)
#   phase2 = 1 if cctstage >= 3  (year 5+)
new_cols["before"] = np.minimum(cctstage, 1)
new_cols["phase1"] = np.clip(cctstage - 1, 0, 1)
new_cols["phase2"] = np.maximum(cctstage - 2, 0)
new_cols["post"] = (y > 0).astype(int)  # single post-CCT dummy

d = pd.concat([d, pd.DataFrame(new_cols, index=d.index)], axis=1)
bra = d[d["country"] == "Brazil"].copy()

# ---------------------------------------------------------------------------
# 1. Brazil coverage
# ---------------------------------------------------------------------------
header("1. Brazil poverty data coverage")
observed = bra.loc[bra["fgt0ppp2"].notna(), "year"]
interp = bra.loc[bra["fgt0ppp2"].isna() & bra["ifgt0"].notna(), "year"]
est = bra.dropna(subset=["rcfgt0", "rcgovgdpppp", "rcgovgini"])
print(f"Observed FGT0 years: {observed.min()}-{observed.max()} ({len(observed)} surveys)")
print(f"Linearly interpolated years: {interp.tolist()}")
print(f"Last year with any poverty value: {bra.loc[bra['ifgt0'].notna(), 'year'].max()}")
print(f"Regression sample: {est['year'].min()}-{est['year'].max()}, N = {len(est)}")

# ---------------------------------------------------------------------------
# 2. Table 6
# ---------------------------------------------------------------------------
header("2. Table 6 reproduced (Brazil, robust OLS)")
f6 = "{} ~ rcgovgdpppp + rcgovgini + before + phase1 + phase2"
m6 = {o: smf.ols(f6.format(o), data=bra).fit(cov_type="HC1", use_t=True)
      for o in ["rcfgt0", "rcfgt1"]}

labels = [
    ("rcgovgdpppp", "Rate of Change of GDP", "Rate of change of GDP"),
    ("rcgovgini", "Rate of Change in Gini", "Rate of change of Gini"),
    ("before", "Before CCT Program", "Shift from 2004 on (year 1+)"),
    ("phase1", "Immediately After CCT Program", "Extra shift from 2006 on (year 3+)"),
    ("phase2", "Intermediate Phases of CCT", "Extra shift from 2008 on (year 5+)"),
    ("Intercept", "intercept", "Pre-2004 mean (net of controls)"),
]
print(f"{'Thesis label':32s}{'Correct meaning':36s}{'FGT0 (headcount)':34s}FGT1 (depth)")
for term, old, new in labels:
    print(f"{old:32s}{new:36s}{fmt(m6['rcfgt0'], term):34s}{fmt(m6['rcfgt1'], term)}")
print(f"N = {int(m6['rcfgt0'].nobs)}, {int(m6['rcfgt1'].nobs)}")

print("\nYears in the regression sample that switch each dummy on:")
for term in ["before", "phase1", "phase2"]:
    print(f"  {term:7s}: {est.loc[est[term] == 1, 'year'].tolist()}")

print("\nCumulative post-2003 shift by period, relative to pre-2004 (sum of dummies):")
for o in ["rcfgt0", "rcfgt1"]:
    m = m6[o]
    for label, expr in [("2004-05", "before = 0"),
                        ("2006-07", "before + phase1 = 0"),
                        ("2008-09", "before + phase1 + phase2 = 0")]:
        tt = m.t_test(expr)
        est_val = float(np.squeeze(tt.effect))
        print(f"  {o} {label}: {est_val:8.4f}  (p={float(tt.pvalue):.3f})")

# ---------------------------------------------------------------------------
# 3. Single post dummy
# ---------------------------------------------------------------------------
header("3. Simpler model: one post-2003 dummy (Brazil, robust OLS)")
for o in ["rcfgt0", "rcfgt1"]:
    m = smf.ols(f"{o} ~ rcgovgdpppp + rcgovgini + post", data=bra).fit(
        cov_type="HC1", use_t=True)
    print(f"  {o}: post = {fmt(m, 'post')}, N = {int(m.nobs)}")

# ---------------------------------------------------------------------------
# 4. Table 5
# ---------------------------------------------------------------------------
header("4. Table 5: naive trend on year (classical SEs as coded vs robust SEs)")
groups = {
    "Brazil": d["country"] == "Brazil",
    "Latin America CCT": (d["eventualcct"] == 1) & (d["region"] == "Latin America"),
    "Latin America non-CCT": (d["eventualcct"] == 0) & (d["region"] == "Latin America"),
}
for o in ["rcfgt0", "rcfgt1"]:
    print(f"  {o}")
    for name, mask in groups.items():
        sub = d[mask]
        classical = smf.ols(f"{o} ~ year", data=sub).fit()
        robust = smf.ols(f"{o} ~ year", data=sub).fit(cov_type="HC1", use_t=True)
        print(f"    {name:22s} N={int(classical.nobs):3d}  "
              f"classical {fmt(classical, 'year')}   robust {fmt(robust, 'year')}")

# ---------------------------------------------------------------------------
# 5. Table 1
# ---------------------------------------------------------------------------
header("5. Table 1 recomputed (Brazil)")
published = {
    "ifgt0": (31, 23.37, 6.99, 9.87, 36.08),
    "ifgt1": (31, 8.84, 3.23, 3.22, 14.96),
    "rcfgt0": (30, -0.03, 0.11, -0.43, 0.19),
    "rcfgt1": (30, -0.64, 0.06, -0.81, -0.51),
}
print(f"{'variable':8s} {'source':10s} {'N':>4s} {'mean':>8s} {'sd':>7s} {'min':>8s} {'max':>8s}")
for v, pub in published.items():
    s = bra[v].dropna()
    print(f"{v:8s} {'thesis':10s} {pub[0]:4d} {pub[1]:8.2f} {pub[2]:7.2f} {pub[3]:8.2f} {pub[4]:8.2f}")
    print(f"{'':8s} {'data':10s} {len(s):4d} {s.mean():8.3f} {s.std():7.3f} {s.min():8.3f} {s.max():8.3f}")
first, last = bra["ifgt1"].dropna().iloc[[0, -1]]
print(f"\nSanity check: FGT1 went from {first:.2f} to {last:.2f}. Annual falls of 51% or more "
      f"for 28 years would leave {first * 0.49 ** 28:.1e}, so the published FGT1 row cannot be right.")

# ---------------------------------------------------------------------------
# 6. Country coding and sample rules
# ---------------------------------------------------------------------------
header("6. Country coding and the stated exclusion rules (Latin America and Caribbean)")
lac = d[d["region"].isin(["Latin America", "Caribbean"])]
rows = []
for c, g in lac.groupby("country"):
    progs = g["program"].dropna().unique()
    rows.append({
        "country": c,
        "eventualcct": int(g["eventualcct"].max()),
        "program_column": "; ".join(progs) if len(progs) else "",
        "program_from": g.loc[g["program"].notna(), "year"].min(),
        "fgt0_obs": int(g["fgt0ppp2"].notna().sum()),
        "fgt0_obs_after_cct": int((g["fgt0ppp2"].notna() & (g["yearfromcct"] > 0)).sum()),
    })
tab = pd.DataFrame(rows)
print(tab.to_string(index=False))
print("\nNamed in the program column but coded eventualcct = 0:")
print("  " + ", ".join(tab.loc[(tab["eventualcct"] == 0) & (tab["program_column"] != ""), "country"]))
print("Coded eventualcct = 1 but fewer than 5 FGT0 observations, or fewer than 3 after the CCT start:")
bad = tab[(tab["eventualcct"] == 1) & ((tab["fgt0_obs"] < 5) | (tab["fgt0_obs_after_cct"] < 3))]
print("  " + ", ".join(f"{r.country} ({r.fgt0_obs} total, {r.fgt0_obs_after_cct} after)"
                       for r in bad.itertuples()))
