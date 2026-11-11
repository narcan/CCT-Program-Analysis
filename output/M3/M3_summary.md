# M3 summary: Brazil's poverty series with real survey years

Descriptive only. Nothing here identifies the effect of Bolsa Familia: 2003 also brought a new government, large minimum wage rises and a commodity boom, and a national series has no comparison group.

**Data.** World Bank PIP, version `20260922_2021_01_02_PROD` (release 2026-09-22, 2021 PPP), pulled 2026-11-10. Lines $3.00, $4.20 and $8.30 per person per day. Survey years only, income-based. Two series: PNAD 1981-2011 and PNAD Continua 2012-2024. Figures: `m3_fig_series.png`, `m3_fig_decomposition.png`. All numbers: `m3_tables.md` and the CSVs.

## What the series shows

At $3.00, the headcount fell from 19.5% (1995) to 16.2% (2002), then from 17.1% (2003) to 7.1% (2011). In PNAD Continua it fell from 6.4% (2012) to 4.8% (2014), rose to 7.0% by 2019 through the recession, dropped to 2.8% in 2020 (Auxilio Emergencial), jumped back to 7.5% in 2021, and fell to 3.0% by 2024. The poverty gap follows the same path. The other lines tell the same story.

**The post-2003 acceleration survives with survey years.** The proportional decline at $3.00 was 2.7% a year in 1995-2002, 11.0% a year in 2003-2011 (9.1% from 2002) and 14.6% a year in 2012-2014. In points, 0.47 a year before and 1.25 a year after.

The 2011 and 2012 values are from different surveys and are not joined. PIP has no overlap years (no PNAD 2012-2015), so the level shift between the two surveys cannot be shown here. M4 can measure it from the microdata.

## Decomposition (Datt-Ravallion, Shapley)

| $3.00 headcount, points | change | growth | redistribution |
|---|---|---|---|
| 1995-2002 | -3.3 | -2.1 | -1.2 |
| 2003-2011 | -10.0 | -5.6 | -4.4 |
| 2012-2014 | -1.6 | -0.6 | -1.0 |
| 2014-2019 | +2.3 | 0.0 | +2.3 |
| 2019-2024 | -4.0 | -0.8 | -3.2 |

Growth means the survey mean rising with the income distribution held fixed. Redistribution means the distribution changing with the mean held fixed. It is not the same as Bolsa Familia: minimum wage, pensions and labor markets all move it. From 1995-2002 to 2003-2011, the speed-up of 0.78 points a year splits roughly in half: 0.40 from faster growth and 0.38 from more redistribution. Since 2014, almost all movement is redistribution, including the 2020 drop and its 2021 reversal.

## Growth-elasticity benchmark (Bourguignon 2003)

As poverty falls into the thin tail, the same growth gives a bigger proportional drop. That effect is real but small here: the log-normal growth elasticity at $3.00 was -1.13 in 1995 and -1.26 in 2003. With inequality held fixed, log-normal growth predicts declines of 1.5% a year for 1995-2002 and 5.4% a year for 2003-2011 (4.5% using GDP per capita instead of the survey mean). Actual: 2.7% and 11.0%. So distribution-neutral growth plus the tail effect accounts for about half of the 2003-2011 decline. For 2012-2014 it predicts 5.7% against 14.6% actual, and survey mean growth (3.1% a year) far exceeded GDP per capita growth (0.9%).

## Verdict on H3.1

H3.1 says the 2003-2014 acceleration is mostly growth plus the mechanical transfer. **Growth alone does not do it: it explains about half.** The other half is falling inequality (4.4 of the 10.0-point drop at $3.00 in 2003-2011). H3.1 holds only if the mechanical Bolsa Familia effect covers most of that 4.4 points. That test is **pending M4**. As a rough guide only, Souza et al. (2019) report about 25% less extreme poverty from transfers at their national lines; applied to the 7.1% headcount of 2011 that is about 2 points, under half of the redistribution part. If M4 finds a number of that size, H3.1 fails and minimum wage, pensions and labor income would carry most of the redistribution.

## Caveats

- No national line. The Bolsa Familia extreme-poverty line in reais could not be verified: no primary legal source was reachable, and secondary snippets disagreed. Results rest on PPP lines only.
- 2020 and 2021 use PNAD Continua 5th-visit income; other PNADC years use the 1st visit.
- No PNAD in 2010 (census year). 1992-1993 survey means are measured under high inflation; the 1992-2002 baseline gives very different growth shares, so the 1995-2002 baseline is used for comparison.
- PIP rounds query lines to one cent and outputs to four decimals; the error is under 0.05 points.
- Log-normal levels overstate headcount by 10-20% at low lines; the benchmark uses only rates of change, and the empirical distribution-neutral path gives similar numbers.
