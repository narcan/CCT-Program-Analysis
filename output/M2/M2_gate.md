# M2 gate: could national poverty data ever show the long-run effect?

Run date: 2026-11-10. Rebuild: `python analysis/m2_data.py && python analysis/m2_noise.py && python analysis/m2_exposure.py && python analysis/m2_power.py` (the simulation takes about 45 seconds).

## Decision

**H2.1 is confirmed. The kill criterion is met: stop all national time-series work on the long-run effect.** In the main design (PIP $3.00 headcount, survey years 1995-2024, main noise), the mechanical effect of about 15% is detected 91% of the time. The long-run effect is not. Take the top of the plausible range: a 30% cut in adult poverty among exposed adults, with every poor adult under 37 counted as exposed (the generous case). Power is then 16% by 2024, 17% by 2019 and 14% by 2015. With the central exposure case it is 10%. That is below 20% at every plausible size, as H2.1 predicted, and far below the 50% kill line. Even when the test does fire, it overstates the effect about 2 to 3 times (Type M 2.2 to 3.0 at 30%, 3 to 8 at 10-20%), and at 5-10% between a sixth and a third of significant results have the wrong sign. Under pessimistic noise even the mechanical effect is mostly invisible (22% power by 2024). Every realistic design stays under 50%. The best is a long 1981-2024 series with noisy 1980s and calm later years, at 26%. Only one design passes 50%: a 1981 start that assumes the 1980s were as calm as post-1995 (72%). The data contradict that assumption (residual SD 0.19 log points before 1995, 0.05 after), so it does not count. M3 stays descriptive, and M7's cross-country items stay parked. The long-run question goes to the cohort design in M5.

## Key numbers (size-adjusted power, alpha 0.05, 4,000 simulations per cell)

| Design | Mechanical 15% | Long-run 30%, central | Long-run 30%, generous |
|---|---|---|---|
| Main noise, 1995-2015 | 0.58 | 0.10 | 0.14 |
| Main noise, 1995-2019 | 0.80 | 0.11 | 0.17 |
| Main noise, 1995-2024 | 0.91 | 0.10 | 0.16 |
| Pessimistic noise, 1995-2024 | 0.22 | 0.05 | 0.06 |
| Mixed noise, 1981-2024 | 0.87 | 0.16 | 0.26 |
| Main noise, 1981-2024 (not realistic) | 0.98 | 0.43 | 0.72 |

National effect implied by 2024: central 8.6%, generous 13.0% less poverty at the 30% individual effect.

Exposure share (share of adults 18-64 who were exposed as children, as stand-in for poor adults): 2015: 0.16 central (0.25 generous); 2019: 0.22 (0.34); 2024: 0.29 (0.43).

Full grid: `results.csv` (columns `power` size-adjusted, `power_nominal` textbook critical value, `type_s`, `type_m`, `true_coef`). Noise fits: `noise.csv`. Exposure by year: `exposure_share.csv`. Figure: `power_curves.png`.

## What was done

1. **Noise.** Log headcount at survey years regressed on a trend, GDP per capita growth (WDI), slope changes at 2003 and 2014 and a 2012 survey-break dummy. The errors are AR(1) on the calendar clock, which handles the gap years exactly, fitted by maximum likelihood.
   - Main case (PIP, 1995-2019): residual SD 0.044 log points, rho 0.13. Year-to-year change SD is 1.06 pp, close to the plan's 1.2 pp.
   - Pessimistic case (PIP, 1981-2019): SD 0.120, rho 0.16. Change SD is 3.9 pp.
   - Thesis data ($2 line): SD 0.043 (1995-2009) and 0.078 (1981-2009).
   - AIC slightly prefers white noise, so rho is weakly identified. A sensitivity case with rho 0.5 lowers long-run power further.
   - Adding 2022-2024 to the noise fit gives rho 0.83 and SD 0.17. That is the 2023 Bolsa Familia reform showing up as "noise", so the noise windows stop at 2019.
2. **Effects.**
   - Mechanical: 15% (and 25% for extreme poverty), phased in with coverage (0.60, 0.78, 0.99 of the 11.1M target in 2004-2006).
   - Long-run: national effect = individual effect x exposure share, with an individual-effect grid of 0, 5, 10, 20 and 30%.
   - A person counts as exposed if their family was enrolled by age 15, which leaves at least 3 covered years of age 0-17.
3. **Simulation.** The interrupted time series has a pre-trend, GDP growth, a post-shift that follows the coverage ramp and a post-slope from 2004. It uses Newey-West SEs. Fixed seeds, 4,000 draws per cell, 1,188 cells in about 41 seconds.
   - The long-run test is the post-slope, run with the mechanical effect present, because the shift absorbs the mechanical step.
   - A second test drops the mechanical effect and asks whether any break at all shows up (joint Wald test). It does no better.
   - Newey-West with about 20 points rejects a true null 8-28% of the time (median 18%) instead of 5%. Power is therefore reported at a size-adjusted critical value, simulated under the null from independent draws. Nominal power is in the CSV, but it is not real power.

## Assumptions (least sure first)

1. **Individual effect range.** 0-30% less adult poverty among the exposed. Anchors:
   - Laguinge, Gasparini & Neidhofer (CEDLAS WP 328, 2024; ZEW DP 25-022, 2025) report about 0.8 more years of schooling and a positive, significant effect on labor income. Verified from abstracts only: the labor income size and the poverty effect were not checked, because the PDFs were blocked from this environment.
   - With a return of 8-10% per year of schooling, that implies roughly 6-8% higher earnings. A plausible poverty effect is therefore around 5-20%, so 30% is a generous upper bound. This mapping is my reasoning, not a published estimate.
   - Parker & Vogl (Economic Journal 133(655), 2023) find large earnings gains for women and insignificant ones for men. Verified from the NBER working paper summary, not the published tables.
2. **Exposure share.**
   - All adults 18-64 stand in for poor adults.
   - Reach is the share of today's poor adults whose childhood family was in the target group and actually enrolled: 0.5 (low), 0.7 (central) or 1.0 (generous). These values are assumptions, not estimates.
   - Enrollment is treated as permanent once reached.
   - The generous case also counts Bolsa Escola 2001-2002 (about 5M families, not verified).
3. **Coverage series** (December families).
   - Verified from MDS / Ipeadata figures as reported by government and news pages: 3.6M (2003), 6.6M (2004), 8.7M (2005), 11.0M (2006), 11.0M (2007), 10.6M (2008), 12.4M (2009), 13.9M (2012), 14.1M (2014), 14.2M (2018), 13.2M (2019), 21.6M (2022), 21.3M (2023 average), 20.86M (2024).
   - The other years are approximate or interpolated (flagged in `analysis/m2_exposure.py`). Since coverage is capped at the 11.1M target after 2006, these gaps do not affect the results.
4. **Mechanical effect size.** 15% / 25% is taken from Souza, Osorio, Paiva & Soares (2019, IPEA TD 2499) as stated in the plan. It was not re-verified in this run. It is held flat after 2006, which ignores the larger benefits after 2023.
5. **Population.** Single-year ages come from WDI 5-year groups (UN WPP based), split evenly within each group. Single-year WPP and IBGE files could not be downloaded here.
6. **Noise process.** Stationary AR(1) around a linear trend. The extreme-poverty (25%) row reuses the $3.00 noise.
   - The synthetic world has no other post-2004 slope changes, such as the commodity boom, minimum wage rises or the 2015-16 recession. In real data these would load on the same post-slope.
   - So the simulated long-run power is an upper bound, and Type S risk in real data is higher.
7. **Sample.** Survey years only, with 2020-2021 dropped (COVID emergency aid). The 2022-2024 points are treated as ordinary years. In reality they carry the 2023 reform, which is a further confound.
8. **PIP release.** 20260922, 2021 PPP, $3.00 line, national, survey estimates only. Raw pulls are in `output/M2/raw/` with pull dates.

## Sources checked in this run

- Bolsa Familia coverage: agenciagov.ebc.com.br (2023 and 2024 averages), folhape.com.br (21.45M at 20 years), congressoemfoco.com.br (2006 target, 2019 low), news tables citing Ipeadata/MDS for 2004-2019. Not fetched directly: Ipeadata, MDS.
- Laguinge, Gasparini & Neidhofer: CEDLAS WP 328 and ZEW DP 25-022 listing pages and abstracts.
- Parker & Vogl: NBER w24303 and the NBER Digest summary.
- Gelman & Carlin (2014) for Type S and Type M definitions.
