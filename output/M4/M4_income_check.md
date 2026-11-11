# M4 income check: does the pipeline measure income the way Souza et al. (2019) do?

Date: 2026-11-11. Source read: IPEA TD 2499 in full (`notes/souza_2019.md`). Data: the existing parquet files in `data/clean/ibge/` (PNAD 2001-2015, PNADC 2016-2017 visit 1); nothing was rebuilt.

## Short answer

1. **Base income, PNAD 2001-2015: matches.** TD 2499 uses household per-capita income from all sources, excluding pensioners, domestic workers and their relatives, and drops households with any undeclared income. That is what `pnad_person_frame` does (V4721 / members, V4721 missing dropped). Our without-BF and with-BF headcounts are within about 0.1 pp of the printed values in most years.
2. **BF identification in PNAD: did not match. Now fixed.** TD 2499 removes BPC first (values within 98-102% of the minimum wage), then **sums the remaining "other income" over the household** and counts the sum as BF if it lies between the legal minimum and maximum benefit for that family's composition. Our M4 rule matched **person-level** values against an exact list of benefit amounts (`tv`), plus a loose top-up rule from 2012 (`tvb`). The M4 rule overstates the cut in 2001, 2002, 2005, 2012-2015 by 3-6 points. The TD 2499 rule is now in `src/cct/mechanical.py` as rule `"souza2019"` (tests in `tests/test_mechanical_souza2019.py`). The existing rules and defaults are unchanged.
3. **PNADC: the paper does not say habitual or effective.** Its 2016-2017 numbers match **effective** income (VD5002), not habitual (VD5008). With effective income every gap is under 2 points; with habitual income extreme-poverty cuts miss by 3.6 (2017) and 4.1 (2016, read off the chart) points. This is an inference from the numbers. M4 used habitual as its first choice.
4. **Poverty-line base: June 2018, not July 2018.** TD 2499 deflates to June 2018. Our lines use July 2018. It changes cuts by up to 1 point (2006), usually by under 0.3.

## Does the M4 kill criterion pass?

Criterion: our percentage reduction must be within 2 points of Souza et al.

**Not unconditionally.** It passes in every year they publish **only** with the TD 2499 household rule for PNAD and effective income for PNADC:

- With `souza2019` + effective, June 2018 lines: all 9 years with printed numbers (2001, 2003, ..., 2015, 2017) are within 1.4 points for extreme poverty and 1.3 points for poverty. The 7 years read off the chart are within 2.0 points, except poverty in 2014 (+2.4), which is inside the chart-reading error (about ±3 points for the poverty panel).
- With the rules M4 actually reported (`tv`/`tvb` + habitual), it **fails** in 5 of 9 printed years for extreme poverty: 2001 (+4.4), 2005 (+2.9), 2009 (+2.2), 2013 (+4.0), 2015 (+2.9), plus 2017 (+3.6).

So `output/M4/series_main.csv`, `pnad_poverty.csv` and the M4 summary's year table overstate the PNAD-era extreme-poverty cut by up to 6 points in some years, and the 2017 habitual figure by 3.6. Two things remain to be done by the owners of `analysis/m4_04_*` and `analysis/m4_05_*`: switch PNAD's main rule to `"souza2019"`, and make `"effective"` the main PNADC concept for the Souza comparison (or report both). Until then, the pass rests on this check, not on the published M4 series. For M5, which uses pre-transfer income, this matters: use the `souza2019` rule for any PNAD year, and fix the income concept in the PAP.

## Comparison, every year Souza et al. publish

Percentage cut in the headcount from BF income. Lines R$89 / R$178 at June 2018 prices (INPC). "Published" for odd years = printed labels in Gráfico 6 (rounded to 0.1 pp, so the published cut itself is only known to about ±1.5 points); for even years = values read from the chart's vector paths (extreme panel ±0.07 pp, poverty panel ±0.25 pp). Gap = ours minus published.

### Extreme poverty (R$89)

| Year | Source | Published cut | M4 rule (tv / tvb / habitual) | Gap | TD 2499 rule / effective | Gap |
|---|---|---|---|---|---|---|
| 2001 | label | 2.5 | 6.9 | +4.4 | 3.3 | +0.8 |
| 2002 | chart | 7.3 | 10.3 | +3.0 | 7.2 | -0.1 |
| 2003 | label | 8.0 | 8.8 | +0.8 | 7.7 | -0.3 |
| 2004 | chart | 18.7 | 19.5 | +0.8 | 16.9 | -1.8 |
| 2005 | label | 17.2 | 20.1 | +2.9 | 17.1 | -0.0 |
| 2006 | chart | 22.6 | 22.8 | +0.2 | 21.3 | -1.3 |
| 2007 | label | 18.2 | 19.6 | +1.5 | 18.5 | +0.3 |
| 2008 | chart | 25.8 | 27.0 | +1.2 | 26.1 | +0.3 |
| 2009 | label | 25.5 | 27.7 | +2.2 | 26.8 | +1.4 |
| 2011 | label | 22.9 | 21.8 | -1.2 | 22.6 | -0.3 |
| 2012 | chart | 29.4 | 35.7 | +6.3 | 29.9 | +0.5 |
| 2013 | label | 29.2 | 33.2 | +4.0 | 29.6 | +0.5 |
| 2014 | chart | 36.5 | 41.1 | +4.6 | 38.5 | +2.0 |
| 2015 | label | 31.7 | 34.6 | +2.9 | 33.1 | +1.4 |
| 2016 | chart | 28.8 | 32.9 (habitual) | +4.1 | 30.5 (effective) | +1.7 |
| 2017 | label | 25.8 | 29.4 (habitual) | +3.6 | 25.7 (effective) | -0.1 |

### Poverty (R$178)

| Year | Source | Published cut | M4 rule (tv / tvb / habitual) | Gap | TD 2499 rule / effective | Gap |
|---|---|---|---|---|---|---|
| 2001 | label | 0.5 | 1.8 | +1.3 | 1.0 | +0.5 |
| 2002 | chart | 1.9 | 2.9 | +1.0 | 1.6 | -0.3 |
| 2003 | label | 2.0 | 3.0 | +1.0 | 2.5 | +0.5 |
| 2004 | chart | 6.1 | 7.0 | +1.0 | 5.8 | -0.3 |
| 2005 | label | 7.0 | 7.6 | +0.6 | 6.3 | -0.7 |
| 2006 | chart | 10.4 | 11.2 | +0.8 | 10.9 | +0.4 |
| 2007 | label | 10.0 | 9.3 | -0.7 | 8.7 | -1.3 |
| 2008 | chart | 11.4 | 13.8 | +2.5 | 13.1 | +1.7 |
| 2009 | label | 12.9 | 14.8 | +1.8 | 13.9 | +1.0 |
| 2011 | label | 16.0 | 16.3 | +0.3 | 17.0 | +1.0 |
| 2012 | chart | 21.2 | 24.8 | +3.6 | 22.3 | +1.1 |
| 2013 | label | 19.3 | 20.9 | +1.6 | 19.6 | +0.3 |
| 2014 | chart | 22.1 | 25.2 | +3.1 | 24.5 | +2.4 |
| 2015 | label | 18.3 | 19.2 | +0.9 | 19.2 | +0.9 |
| 2017 | label | 14.2 | 16.2 (habitual) | +2.0 | 14.6 (effective) | +0.5 |

### Levels, PNADC (headcount %, without BF / with BF)

| | Extreme 2016 | Extreme 2017 | Poverty 2016 | Poverty 2017 |
|---|---|---|---|---|
| Published | 6.0 / 4.3 (chart) | 6.6 / 4.9 | n/a | 10.6 / 9.1 |
| Effective (VD5002) | 6.19 / 4.30 | 6.85 / 5.09 | 10.46 / 8.74 | 11.01 / 9.40 |
| Habitual (VD5008) | 5.47 / 3.67 | 5.97 / 4.22 | 9.69 / 7.97 | 10.06 / 8.43 |

Effective is closer in every extreme-poverty level. For poverty the two concepts straddle the published values, but only effective gets the cut within 2 points. People lifted in 2017 (effective): 3.60 million out of extreme poverty and 3.30 million out of poverty, against 3.4 and 3.2 million published.

### With July 2018 lines (the current pipeline base)

The verdict is the same. With `souza2019` + effective the largest gaps are 2014 (+2.2 extreme, +2.5 poverty, both chart-read years), 2004 (-2.0, chart), 2015 (+2.0 extreme, printed), 2016 (+2.0, chart); all printed years are within 2.0.

## What the remaining gaps are

- **2014 and 2015 run about +1.5 to +2.5 points high** with the TD 2499 rule. Both are BSP years, where the legal maximum is not a fixed number. Our bound (eligibility line x household size) is generous. TD 2499 does not print its bound, so this cannot be tied down further.
- **2004 and 2006 run about 1.5 points low** (chart-read years). These are transition years with predecessor programmes; our predecessor bounds are a reconstruction.
- The persons-lifted figures are not compared year by year because TD 2499 prints them only for 2017.

## Code used for this check

Run from the repository root with the parquet files in place. It uses only `src/cct` functions; the `souza2019` rule is the change made here.

```python
import sys
sys.path.insert(0, "src")
import pandas as pd
from cct import mechanical as m, pnad, pnadc

LAB = {2001: (7.9, 7.7, 20.7, 20.6), 2003: (7.5, 6.9, 20.2, 19.8), 2005: (6.4, 5.3, 17.2, 16.0),
       2007: (5.5, 4.5, 14.0, 12.6), 2009: (5.1, 3.8, 11.6, 10.1), 2011: (4.8, 3.7, 10.0, 8.4),
       2013: (4.8, 3.4, 8.8, 7.1), 2015: (4.1, 2.8, 8.2, 6.7), 2017: (6.6, 4.9, 10.6, 9.1)}
DIG = {2002: (7.14, 6.62, 19.93, 19.56), 2004: (7.32, 5.95, 19.16, 18.00),
       2006: (5.71, 4.42, 15.17, 13.59), 2008: (5.15, 3.82, 11.89, 10.54),
       2012: (4.35, 3.07, 9.15, 7.21), 2014: (3.59, 2.28, 7.21, 5.62), 2016: (6.01, 4.28, None, None)}
BASE = (2018, 6)

def cuts(f, y, month):
    out = {}
    for k, z0 in (("ext", 89), ("pov", 178)):
        z = m.deflate_line(z0, y, month, BASE)
        out[k] = m.poverty_table(f.pc_with.values, f.pc_without.values, f.weight.values, {k: z}).iloc[0].pct_reduction
    return out

rows = []
for y in sorted(set(pnad.PNAD_URLS) | {2016, 2017}):
    pub = LAB.get(y) or DIG.get(y)
    if y <= 2015:
        pes, _ = pnad.load_pnad(y)
        old = "tvb" if y in m.BSP_YEARS else "tv"
        a, b = cuts(m.pnad_person_frame(pes, y, old), y, 9), cuts(m.pnad_person_frame(pes, y, "souza2019"), y, 9)
    else:
        df = pnadc.load_pnadc(y, 1)
        a, b = cuts(pnadc.person_frame(df, y, "habitual"), y, None), cuts(pnadc.person_frame(df, y, "effective"), y, None)
    for k, i in (("ext", 0), ("pov", 2)):
        p = 100 * (pub[i] - pub[i + 1]) / pub[i] if pub and pub[i] else None
        rows.append(dict(year=y, line=k, published=p, m4_rule=a[k], td2499_rule=b[k]))
print(pd.DataFrame(rows).round(1).to_string())
```
