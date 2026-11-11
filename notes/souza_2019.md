# Souza, Osorio, Paiva & Soares (2019): IPEA TD 2499

"Os efeitos do Programa Bolsa Família sobre a pobreza e a desigualdade: um balanço dos primeiros quinze anos." Texto para Discussão 2499, Ipea, Rio de Janeiro, August 2019, 46 pp. Originally a chapter in Silva (org.), *Bolsa Família 15 Anos (2003-2018)*, 2018. English version: "The effects of Brazil's Bolsa Família programme on poverty and inequality: an assessment of the first 15 years" (IPC-IG; same results).

Read in full on 2026-11-11 from the Ipea repository (item handle 11058/9356, `repositorio.ipea.gov.br`). Note: the link in `RESEARCH_PLAN.md` (handle 11058/15191) is **not** TD 2499; it resolves to Soares, Soares, Medeiros & Osorio (2006), IPC Working Paper 21, "Cash transfer programmes in Brazil: impacts on inequality and poverty".

Also read, as method sources: Souza, Osorio & Soares (2011), IPEA TD 1654, "Uma metodologia para simular o Programa Bolsa Família"; and IPC WP 21 (2006).

## Data

- PNAD 2001-2015 (annual, September reference month) and PNAD Contínua **1st-visit annual files for 2016 and 2017** only (the only PNADC years with full income data at the time).
- The two series are never spliced: charts leave a gap between 2015 and 2016, and the authors warn the 2015-2016 jumps are partly artificial (appendix 1.1, footnote 7).
- No use of PNADC 2012-2015.
- No correction for under-reporting: "optamos por utilizar apenas os dados brutos, sem nenhuma correção" (section 3). PNAD/PNADC count of beneficiary families is 30-35% below the administrative register (Gráfico 1).

## Sample filters (appendix 1.2)

- Drop pensioners ("pensionista"), domestic workers and their relatives, in both surveys.
- PNAD 2001-2015: drop **every person in a household where at least one member has any income item with value not declared (missing)**.
- PNADC: no such filter, "because IBGE imputes missing income in this survey". This implies they used IBGE's imputed income variables.
- PNAD 2001-2003 exclude the rural North (except Tocantins), as the survey did.

## Income concept

- Household per-capita income ("renda domiciliar per capita"), all members except the excluded categories above, all sources.
- Counterfactual: the same income minus identified BF income ("renda domiciliar per capita líquida do PBF").
- **Habitual vs effective (PNADC): not stated in the text.** The deflation rule (each quarter deflated using its middle month) and the "IBGE imputes" remark fit either VD5002 (effective) or VD5008 (habitual work + effective other income). The published 2016-2017 levels match effective income better than habitual (see `output/M4/M4_income_check.md`): 2017 extreme poverty without BF is 6.6% published vs 6.85% effective and 5.97% habitual in our pipeline. This is an inference from numbers, not a statement in the paper.
- Old PNAD: income in the September reference month; per-capita from the household total. No separate habitual/effective distinction.

## BF identification in PNAD 2001-2015 (appendix 1.3)

A variant of the "typical values" method, in two steps:

1. **BPC first:** any "outros rendimentos" (V1273) value between **98% and 102% of the minimum wage** in force that year is BPC.
2. **BF:** the remaining V1273 amounts are **summed over the household**, and the sum is classified as BF when it is **between the legal minimum and the legal maximum benefit for that family, given its demographic composition**.
3. **Up to 2006**, the predecessor programmes (Auxílio Gás, Bolsa Alimentação, Bolsa Escola Nacional) are included in the calculation (so "BF" before 2004 means the predecessors).

The paper does not print the bounds. Our implementation (`src/cct/mechanical.py`, rule `"souza2019"`) uses: minimum = smallest variable benefit (R$7 Auxílio Gás up to 2006); maximum = basic + variable × min(children 0-15, cap) + BVJ × min(youths 16-17, cap), taking the larger of the current and previous schedule in readjustment years; up to 2006, the larger of that and the predecessor maximum (15 × children 0-6 + 15 × children 6-15, capped at 3 each, + 7.50 + 50); in BSP years, at least the extreme-poverty eligibility line × household size (+R$2), and in 2012 only for families with children 0-6.

Precursor in TD 1654 (2011, for PNAD 2009): every household whose **sum of other income was ≤ R$200** (the 2009 maximum benefit) was classed as a BF household, and the whole sum taken as BF. TD 2499 refines this by removing BPC and using composition-specific bounds.

IPC WP 21 (2006) used a different method built on the 2004 supplement (households declaring receipt, splitting V1273 into BPC, other programmes and interest by minimum-wage multiples). Not the TD 2499 rule.

## BF in PNAD Contínua 2016-2017

Direct item (V5002A / V5002A2, "Bolsa Família"). The paper says the PNADC questions improved the capture of benefit values but not the count of beneficiaries.

## Deflator and poverty lines (appendix 1.4-1.5)

- Deflator: **INPC to June 2018** (following Corseuil & Foguel 2002, IPEA TD 897). PNADC: each quarter deflated using its middle month (February, May, August, November).
- Lines: **R$89 (extreme) and R$178 (poverty) per person per month, in June 2018 reais**, fixed in real terms. They equal the BF eligibility lines of 2018 and are used "only for monitoring", not to judge eligibility in any year.
- Also a relative cut (poorest 20%, before BF) for the targeting section.

Implied nominal lines (INPC, June 2018 base; September for PNAD, annual average for PNADC), computed with `cct.mechanical.deflate_line`:

| Year | Extreme | Poverty | | Year | Extreme | Poverty |
|---|---|---|---|---|---|---|
| 2001 | 30.57 | 61.15 | | 2009 | 52.85 | 105.69 |
| 2002 | 33.50 | 67.01 | | 2011 | 59.36 | 118.71 |
| 2003 | 39.37 | 78.74 | | 2012 | 62.67 | 125.33 |
| 2004 | 41.71 | 83.43 | | 2013 | 66.23 | 132.46 |
| 2005 | 43.80 | 87.60 | | 2014 | 70.60 | 141.19 |
| 2006 | 45.05 | 90.10 | | 2015 | 77.59 | 155.17 |
| 2007 | 47.27 | 94.53 | | 2016 | 83.59 | 167.18 |
| 2008 | 50.60 | 101.19 | | 2017 | 86.07 | 172.15 |

Our pipeline uses July 2018 as the base (Decreto 9.396/2018 took effect in July). The difference is 0.25% in the line and moves cuts by up to 1 point in years where many people sit near the line (2006).

## Published year-specific results

**Text.** In 2017 BF cut extreme poverty by about 25% and poverty by about 15%; it lifted "mais de 3,4 milhões" out of extreme poverty and 3.2 million above the poverty line. After 2004, BF lowers extreme poverty by 1.3 pp and poverty by 1.6 pp on average. Of the extremely poor before BF in 2017, 70% were in the programme, and 64% of those stayed extremely poor after the transfer. Average 2004-2017: P1/P0 64% before vs 51% after; P2/P0 53% vs 38%.

**Gráfico 6** (headcount, %, without BF / observed). Printed labels (rounded to 0.1):

| Year | Survey | Extreme without | Extreme with | Cut | Poverty without | Poverty with | Cut |
|---|---|---|---|---|---|---|---|
| 2001 | PNAD | 7.9 | 7.7 | 2.5% | 20.7 | 20.6 | 0.5% |
| 2003 | PNAD | 7.5 | 6.9 | 8.0% | 20.2 | 19.8 | 2.0% |
| 2005 | PNAD | 6.4 | 5.3 | 17.2% | 17.2 | 16.0 | 7.0% |
| 2007 | PNAD | 5.5 | 4.5 | 18.2% | 14.0 | 12.6 | 10.0% |
| 2009 | PNAD | 5.1 | 3.8 | 25.5% | 11.6 | 10.1 | 12.9% |
| 2011 | PNAD | 4.8 | 3.7 | 22.9% | 10.0 | 8.4 | 16.0% |
| 2013 | PNAD | 4.8 | 3.4 | 29.2% | 8.8 | 7.1 | 19.3% |
| 2015 | PNAD | 4.1 | 2.8 | 31.7% | 8.2 | 6.7 | 18.3% |
| 2017 | PNADC | 6.6 | 4.9 | 25.8% | 10.6 | 9.1 | 14.2% |

Unlabelled years read from the chart's vector paths (calibrated on the labels; extreme panel accurate to about ±0.07 pp, poverty panel to about ±0.25 pp, so cuts to about ±1.5 and ±3 points):

| Year | Extreme without / with | Cut | Poverty without / with | Cut |
|---|---|---|---|---|
| 2002 | 7.14 / 6.62 | 7.3% | 19.93 / 19.56 | 1.9% |
| 2004 | 7.32 / 5.95 | 18.7% | 19.16 / 18.00 | 6.1% |
| 2006 | 5.71 / 4.42 | 22.6% | 15.17 / 13.59 | 10.4% |
| 2008 | 5.15 / 3.82 | 25.8% | 11.89 / 10.54 | 11.4% |
| 2012 | 4.35 / 3.07 | 29.4% | 9.15 / 7.21 | 21.2% |
| 2014 | 3.59 / 2.28 | 36.5% | 7.21 / 5.62 | 22.1% |
| 2016 | 6.01 / 4.28 | 28.8% | n/a | n/a |

The headline "15% / 25%" is a round summary across years, not a single-year figure. Year-specific extreme-poverty cuts range from about 18% (2005-2007) to 37% (2014).

## Other results (not used for M4)

- BF is about 0.5% of GDP and 0.7% of PNAD household income; about 70% of BF money reaches the poorest 20% (pre-transfer).
- Gini: BF explains about 10% of the 2001-2015 fall and almost 17% of the 2001-2006 fall; minimum-wage-linked transfers (pensions, BPC) about 18% and 13%.
- The binding constraint on the poverty effect is the size of the benefit, not targeting.
