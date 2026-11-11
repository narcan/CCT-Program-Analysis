# M4 summary: microdata pipeline and the mechanical effect of Bolsa Familia

Date: 2026-11-11 (corrected; first version 2026-11-10). Code: `src/cct/pnad.py`, `src/cct/pnadc.py`, `src/cct/mechanical.py`, `analysis/m4_*.py`. Data: official IBGE microdata (`data/raw/MANIFEST_M4.md`). Method source: Souza, Osorio, Paiva and Soares (2019), IPEA TD 2499 (`notes/souza_2019.md`).

## What changed in this correction

The first version used the wrong rule to find Bolsa Familia (BF) income in the annual PNAD, and habitual income in PNAD Continua. After reading TD 2499 (`output/M4/M4_income_check.md`) we switched to their method, which is now the primary specification:

- **PNAD 2001-2015.** BF has no item of its own and sits in the catch-all "other income" item (V1273). Values within 98-102% of the minimum wage are treated as BPC. The rest is summed over the household and counted as BF if the sum lies between the smallest and largest benefit that family could get, given its makeup. (Old rule: match each person's value to a list of benefit amounts. Kept as a sensitivity.)
- **PNAD Continua 2012-2025.** Direct BF question. Income is **effective** income (VD5002). Habitual income (VD5008) is kept as a labelled sensitivity.
- **Poverty lines.** R$89 (extreme) and R$178 (poverty) per person per month at June 2018 prices, moved with the INPC.

## Kill criterion

Rule: our percentage cut must be within 2 points of Souza et al. **Verdict: passes.** In all 9 years they print (2001, 2003, ..., 2015, 2017) the gap is at most 1.4 points for extreme poverty and 1.3 for poverty. In the 7 years read off their chart, all gaps are within 2.0 except poverty in 2014 (+2.4), which is inside the chart-reading error. The old specification fails in 6 of the 9 printed years (`output/M4/benchmark_souza2019.csv`).

**Be honest about what this means.** We chose the rule after seeing the mismatch. It is the rule the paper describes, but the bounds it uses are not printed, so our version is a reconstruction tuned while looking at their numbers. Treat this as a fix that makes the pipeline do what Souza et al. did, not as an independent result.

## Checks

1. **Direct questions, 2006.** 86% of people in households that said they got BF are flagged; 87% of people flagged are in such households.
2. **2012-2015 overlap.** Cut in extreme poverty, PNAD vs PNAD Continua: 30 vs 30%, 30 vs 38%, 39 vs 39%, 33 vs 34%. Recipients: 9.7 to 11.3 million vs 9.7 to 10.2 million.
3. **Surveys vs spending.** Surveys capture about 68 to 82% of what the government spends: 0.72 to 0.82 in 2013-2015, 0.68 in 2024 (R$114 billion vs R$168.3 billion). Only the 2024 spending figure is from an official source (`output/M4/survey_vs_admin.csv`).

## Results: percentage cut in the poverty rate from BF income

| Year | Survey | Extreme (primary) | Poverty (primary) | Extreme, habitual / old rule |
|---|---|---|---|---|
| 2006 | PNAD | 21% | 11% | 23% (old rule) |
| 2009 | PNAD | 27% | 14% | 28% (old rule) |
| 2015 | PNAD | 33% | 19% | 35% (old rule) |
| 2015 | PNAD Continua | 34% | 18% | 38% (habitual) |
| 2017 | PNAD Continua | 26% | 15% | 29% (habitual) |
| 2019 | PNAD Continua | 23% | 14% | 27% (habitual) |
| 2023 | PNAD Continua | 72% | 47% | 74% (habitual) |
| 2025 | PNAD Continua | 71% | 47% | 73% (habitual) |

In 2017 BF lifted 3.6 million people out of extreme poverty and 3.3 million out of poverty (Souza et al.: 3.4 and 3.2). In 2025: 9.6 and 9.1 million. Full series: `output/M4/series_main.csv`. Leave out 2020-2021 (most families got the Auxilio Emergencial, which this item misses) and 2001-2003 (no rural North in the PNAD).

## H4.1 verdict

H4.1 said the cut in extreme poverty would be 20-30% in 2015 and larger after the 2023 relaunch.

- **2015 part: rejected, by less than before.** The primary estimate is 33% (PNAD) or 34% (PNAD Continua), down from 34-38%. It is still above the band, and Souza et al.'s own 2015 figure (31.7%) is above it too. 2015 is the peak of the BSP top-up, which targets almost exactly our extreme line.
- **Post-2023 part: supported.** The cut is about 71-72% in 2023-2025, roughly double the 2015 level.
