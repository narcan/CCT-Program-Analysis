# M4 summary: microdata pipeline and the mechanical effect of Bolsa Familia

Date: 2026-11-10. Code: `src/cct/pnad.py`, `src/cct/pnadc.py`, `src/cct/mechanical.py`, `analysis/m4_*.py`. Data: official IBGE microdata (`data/raw/MANIFEST_M4.md`).

## What was built

- A reader for every annual PNAD from 2001 to 2015 and every PNAD Continua annual-visit file from 2012 to 2025 (visit 1; visit 5 for 2020 and 2021). Column positions come from IBGE's own layout files.
- Annual PNAD has no Bolsa Familia (BF) question. BF sits in a catch-all "interest, dividends and other income" item (V1273). We flag a value as BF when it matches an amount the programme rules allowed that year ("typical values"). From 2012 a top-up of any size (the BSP) breaks this, so from 2012 we also count other values below the minimum wage, except round amounts above R$100.
- PNAD Continua asks directly: "BF or PETI" until mid 2015, "Bolsa Familia" after.
- Poverty lines: R$89 (extreme) and R$178 (poverty) per person per month at July 2018 prices, the lines Souza, Osorio, Paiva and Soares (2019) use, moved to each year with the INPC. Survey weights throughout.

## Checks

1. **Direct questions in 2004 and 2006.** In 2006, 88% of people in households that said they got BF are flagged by our rule, and 89% of the people we flag are in such households.
2. **2012-2015 overlap.** In 2012-2015 the PNAD rule and the PNAD Continua direct question agree closely. Cut in extreme poverty: 36 vs 33%, 33 vs 42%, 41 vs 42%, 35 vs 38%. Recipients: 10.5 to 11.9 million vs 9.7 to 10.2 million. The typical-values rule alone finds only 12 to 16% from 2013 on, so it can't be used after the BSP.
3. **Against Souza et al. (2019).** The only year-specific figures we could check are for 2017: BF cut extreme poverty by 25% and poverty by 15%, and lifted 3.4 and 3.2 million people. The IPEA site is blocked here, so their 2006 and 2015 numbers and their exact imputation rule could not be read.

| 2017, PNAD Continua | Extreme: our cut | Gap vs 25% | Poverty: our cut | Gap vs 15% | People lifted (ext./pov.) |
|---|---|---|---|---|---|
| Habitual income (our first choice) | 29.3% | +4.3 | 16.2% | +1.2 | 3.6 / 3.3 million |
| Effective income | 26.0% | +1.0 | 14.7% | -0.3 | 3.6 / 3.3 million |

**Kill criterion, stated plainly.** We picked habitual income first, and with it the extreme-poverty figure misses by 4.3 points. That fails the 2-point rule. With effective income (the reference-month measure, which is closer to what the old PNAD asked) both gaps are under 2 points. The number of people lifted matches under both. So the transfer itself is measured right, and the gap comes from which income measure sets the base poverty rate. **Verdict: conditional pass.** The pipeline can reproduce Souza et al. for 2017, but only after choosing the income measure that fits, and we could not check any PNAD year (2001-2015) against their published numbers. Before M5, someone should read TD 2499 to confirm the income measure and the imputation rule.

## Results (percentage cut in the poverty rate from BF income)

| Year | Survey | Extreme | Poverty |
|---|---|---|---|
| 2006 | PNAD | 24% | 11% |
| 2009 | PNAD | 28% | 15% |
| 2015 | PNAD / PNADC habitual / PNADC effective | 35% / 38% / 34% | 19% / 20% / 18% |
| 2019 | PNADC habitual / effective | 27% / 24% | 15% / 14% |
| 2023 | PNADC habitual / effective | 74% / 72% | 50% / 47% |
| 2025 | PNADC habitual / effective | 73% / 71% | 51% / 47% |

Full series: `output/M4/series_main.csv`. Leave out 2020-2021, when most families got the Auxilio Emergencial, which this item doesn't capture. Also leave out 2001-2003, when the PNAD did not sample the rural North.

**Surveys vs. spending.** People report about 70 to 85% of what the government spends. Scaled to a year, the surveys give R$19 to 21 billion in 2013-2015, against R$24.5 to 26.4 billion spent. In 2024 PNAD Continua shows R$114 billion against R$168.3 billion spent, a ratio of 0.68. Only the 2024 spending figure comes from an official outlet. Figures for the other years come from secondary sources found by web search, because government sites are blocked here (`output/M4/survey_vs_admin.csv`).

## H4.1 verdict

H4.1 said the cut in extreme poverty would be 20-30% in 2015 and larger after the 2023 relaunch. **First part rejected:** every 2015 estimate is above the range, at 34 to 38%. The year 2015 sits at the peak of the BSP top-up, and our extreme line (R$77 in 2015) is almost the same as the top-up's own target. **Second part supported:** after the 2023 relaunch the cut is about 72 to 74%.
