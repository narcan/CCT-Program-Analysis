"""Poverty decompositions and the log-normal growth-elasticity benchmark.

Datt & Ravallion (1992)
-----------------------
Write a poverty measure as P(mu, L): the mean and the Lorenz curve. For a
spell t1 -> t2 the change is split into

- growth: change in P from moving the mean with the Lorenz curve fixed;
- redistribution: change in P from moving the Lorenz curve with the mean
  fixed.

Because P(mu, L) depends on the distribution only through z / mu given L,
"year t1 distribution with year t2 mean" equals "year t1 distribution at
line z * mu1 / mu2". So P(mu2, L1) is one PIP query for year t1 at the
scaled line, and P(mu1, L2) is one query for year t2 at z * mu2 / mu1.

The original method fixes the reference period (t1) and leaves a
residual. We report that and the Shapley version (average over both
reference periods), which is exact.

Bourguignon (2003)
------------------
If welfare is log-normal with mean mu and log standard deviation sigma,
headcount is H = Phi(ln(z/mu)/sigma + sigma/2), and sigma follows from
the Gini: G = 2 Phi(sigma / sqrt 2) - 1. The growth elasticity of H is
-phi(a) / (sigma * Phi(a)) with a the argument above; it rises in
absolute value as z/mu falls, so proportional declines speed up
mechanically as poverty falls into the thinner tail.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm


def datt_ravallion(p11: float, p22: float, p21: float, p12: float) -> dict:
    """p_ab = poverty with mean of year a and Lorenz curve of year b.

    p11 = P(mu1, L1) observed t1; p22 observed t2;
    p21 = P(mu2, L1) (t1 distribution scaled to t2 mean);
    p12 = P(mu1, L2) (t2 distribution scaled to t1 mean).
    """
    total = p22 - p11
    g_base1 = p21 - p11
    r_base1 = p12 - p11
    g_base2 = p22 - p12
    r_base2 = p22 - p21
    return {
        "change": total,
        "growth_dr": g_base1,
        "redistribution_dr": r_base1,
        "residual_dr": total - g_base1 - r_base1,
        "growth_shapley": 0.5 * (g_base1 + g_base2),
        "redistribution_shapley": 0.5 * (r_base1 + r_base2),
    }


def sigma_from_gini(gini) -> np.ndarray:
    return np.sqrt(2.0) * norm.ppf((np.asarray(gini) + 1.0) / 2.0)


def lognormal_headcount(z, mu, sigma) -> np.ndarray:
    a = np.log(np.asarray(z) / np.asarray(mu)) / sigma + sigma / 2.0
    return norm.cdf(a)


def lognormal_gap(z, mu, sigma) -> np.ndarray:
    a = np.log(np.asarray(z) / np.asarray(mu)) / sigma + sigma / 2.0
    return norm.cdf(a) - (np.asarray(mu) / np.asarray(z)) * norm.cdf(a - sigma)


def lognormal_growth_elasticity(z, mu, sigma) -> np.ndarray:
    a = np.log(np.asarray(z) / np.asarray(mu)) / sigma + sigma / 2.0
    return -norm.pdf(a) / (sigma * norm.cdf(a))


def annualized_log_change(x0: float, x1: float, years: float) -> float:
    """Annual proportional change, 100 * ln(x1/x0) / years."""
    return 100.0 * np.log(x1 / x0) / years
