# Laguinge, Gasparini & Neidhoefer: long-run effects of Bolsa Familia

Read in full, 2026-11-11, from two versions:

- **CEDLAS WP 328** (dated March 2024, 26 pp.): `doc_cedlas328.pdf`.
- **ECINEQ WP 2025-684** (dated April 2025, issued May 2025, 26 pp. + appendix): `ECINEQ2025-684.pdf`.

The ZEW DP 25-022 PDF could not be fetched (ftp.zew.de refused / did not resolve through the proxy). It is dated 2025 and carries the same title and abstract as the ECINEQ version, so it is very likely identical; not verified. The UNU-WIDER WP 2026/14 version was not read.
Numbers below are from the ECINEQ 2025 version unless marked "(2024)". Where the two versions differ, both are given.
Page and table numbers refer to the ECINEQ version.

The previous draft of this note was built from abstracts and press summaries. Corrections to it are listed at the end.

## Data

- **Stage 1 sample: PNAD 2006** (supplement with direct BF receipt question). Households with children where *both parents are present*; N = 49,728. Logit of household BF receipt on: highest parental education (7 levels), father's and mother's occupational category (7 each), state of residence (27 dummies), urban/rural (Table A.1).
- **Stage 2 sample: PNAD 2014**, using the *mobility supplement* answered by a random sub-sample, which asks adults about circumstances **when they were 15 and living with their parents** (parents' education and occupation; the paper also mentions a retrospective "state of residence at age 15" question, which it does *not* use yet: p. 11-12, "in the next analytical steps").
- Age restriction: **25 to 40 in 2014**, i.e. birth cohorts **1974-1989** (16 cohorts).
- Weights: "inverse probability of selection" (survey weights).
- **No Census (2010 or 2022), no PNAD Continua, no linked administrative records (CadUnico, RAIS).** One cross-section of outcomes (2014).

## Exposure definition

- Predicted probability of household BF receipt from the 2006 logit, applied to the 2014 retrospective covariates.
- **Treated = predicted probability > 0.257**, the ROC cutpoint nearest to (0,1) (Liu 2012). At that cut: true-positive rate 0.75, false-positive rate 0.28, AUC 0.74 (Table 2). LASSO / Ridge / Elastic-net (linear and logit) give cutpoints 0.245-0.297 and the same AUC (0.73-0.74).
- **Post = born 1985 or later.** Rationale: Bolsa Escola started March 2001 and targeted children under 17, so only cohorts born 1985+ were eligible. BE and BF are treated as "one and the same program".
- Exposure is binary on both axes. No years-of-exposure dose, no state or municipal coverage, no use of BF's 2003-2006 rollout.
- Consequence of the window: the "post" cohorts are 1985-1989, aged 12-16 in 2001 and 14-18 at BF's launch (Oct 2003). They had at most a few eligible years, and only as teenagers. The paper's effect is a late-adolescence exposure effect.

## Estimating equation

y_it = a + b Treated_i + g Post_t + d Treated_i x Post_t + X_it' theta + e_it  (eq. 1)

- X: sex, age, age squared, household size, region of residence, urban/rural (all measured in 2014).
- **SEs clustered by municipality** (rationale: municipalities enrol families).
- Outcome means are for the treated group in pre-period cohorts.

## Main estimates (Table 3), d with clustered SE

| Outcome | No controls | With controls | Mean (treated, pre) | N |
|---|---|---|---|---|
| Years of schooling | 0.803 (0.171) | 0.784 (0.166) | 8.1 | 10,722 |
| Monthly labor income, "US$" | 250.2 (44.39) | 247.6 (45.40) | 581.5 | 8,189 |

- Labor income is in current US dollars (Table A.4 note: "current US$"); the conversion (exchange rate or PPP, and which month) is not stated. +250 on a base of 581.5 is a 43% effect, which is very large for a 1-5 year teenage exposure.
- Completion (Table 10, controls in col. 2): primary +0.0876 (0.0186), mean 0.61; secondary +0.0585 (0.0205), mean 0.43; tertiary +0.0216 (0.0165), n.s.; N = 10,754. Secondary: men +0.013 (0.032), women +0.105 (0.028).
- Current receipt of social transfers (Table 11): -0.0252 (0.0152) without controls, **-0.0370 (0.0153)** with; men -0.058 (0.019), women -0.013 (0.024); mean 0.26. "Receipt" is imputed: household non-labor "other income" between R$35 and R$336 (the 2014 BF min and max).
- By sex (Table 7): schooling men 0.773 (0.238), women 0.821 (0.227); labor income men 308.5 (85.8), women 191.3 (53.9).
- Subgroups (Table 8): schooling rural 1.297 (0.639), urban 0.517 (0.174), Afro-Brazilian 1.229 (0.536), other 0.742 (0.177); labor income rural 214.3 (164.9), urban 235.0 (46.0), **Afro-Brazilian 3.2 (108.0)**, other 263.5 (49.3). Women subgroups in Table 9.
- Mechanisms (Fig. 7; Table 13 in 2024): lower probability of working in fishing (-0.005) and "other community/personal services" (-0.022), higher in public administration (+0.023) and utilities (+0.011).
- **(2024 only) Household per-capita income**, household heads only (Table A.1, 2024): +124.5 (45.68) unconditional, **+83.24 (40.63)** conditional, mean 834.35, N = 5,100. Dropped from the 2025 version. This is the only household-income outcome in either version; it is total income, **not pre-transfer income and not poverty**.

## Robustness and falsification

1. **Pre-trend slope test** on cohorts 1974-1984 (Table 4): Treated x linear cohort = 0.0187 (0.0339) for schooling, 18.89 (13.30) for labor income.
2. **Event study** by cohort, base 1974 (Fig. 4; Fig. 5 in 2024): pre-1985 coefficients individually insignificant; "break in 1985" (2025) / "around 1984" (2024); only the **1989 cohort** is significant for both outcomes.
3. **Rambachan-Roth sensitivity** on the 1989 cohort only, 90% CI: schooling robust up to **M-bar = 0.25** (2024: 0.2); labor income up to **0.15** (2024: 0.10). I.e. a post-period violation a quarter (schooling) or a sixth (income) as large as the largest pre-period wiggle would erase significance. The previous note's guess that "15%" was a misclassification bound was wrong.
4. **Fake-period placebo** within 1974-1984 (Fig. 6; Table 5 in 2024): schooling none significant; labor income significant at 5% for fake breaks at **1982 (182.8, SE 91.1) and 1984 (163.9*, SE 88.1)** with controls (2024 table); the 2025 text mentions only 1982 as weakly significant.
5. **Leave-one-cohort-out** (Table 5): schooling 0.56-1.03, income 236-288, all p < 0.01.
6. **Placebo outcome, non-labor income** (pensions, rent, donations; Table 6): 9.82 (6.37) without and **10.93* (6.43)** with controls.
7. Alternative stage-1 algorithms (Table 2) and samples including single mothers or single fathers (Table A.3: schooling 0.763 / 1.123, income 255.7 / 270.6).

## Identifying assumption and weaknesses (my reading)

- Assumption: absent the program, the high- vs low-propensity gap would have been the same for 1985-1989 cohorts as for 1974-1984 cohorts.
- **Age and cohort are the same variable in a single 2014 cross-section.** The 1985-89 "post" cohorts are 25-29; the controls are 30-40. Low-propensity (higher-SES) people finish tertiary education later and have steeper early-career earnings profiles, so the treated-control gap is mechanically smaller at 25-29 than at 30-40. This biases d *upward* for both schooling and labor income, and age + age squared do not remove it, because the bias is in the group-specific age profile. The pre-trend tests use ages 30-40, where those profiles are flatter, so they have little power against this. This is the strongest single reason to re-estimate with several survey years (age and cohort separable).
- Binary exposure misclassifies 25% of beneficiaries and 28% of non-beneficiaries; attenuation and the 0.257 cut are not tied to coverage in the person's state or year.
- Controls are measured in adulthood (household size, region, urban/rural of residence in 2014) and can be outcomes of the program (migration, fertility).
- Clustering at municipality of *current* residence, not of childhood.
- Stage-1 uses state of residence in 2006 but stage 2 has only current (2014) region in the outcome equation; how stage-2 state is assigned (current state vs state at 15) is not stated.
- Results lean on the 1989 cohort; the fake-break income placebo fails at 1982 and 1984.

## What they did NOT do

- No pre-transfer poverty or market-income outcome (2024 has total household per-capita income for heads only; 2025 drops it).
- No exposure intensity: no years-eligible count and no state or municipal BF coverage. They did not exploit the 2003-2006 rollout across states.
- No Census, no PNAD Continua, no linked records; a single outcome year (2014), so no fixed-age comparison across cohorts.
- No cohorts born after 1989 (the most exposed, who were young children in 2003-2010).
- No national translation of the individual effect into aggregate poverty.
- No multiple-testing adjustment across the many outcomes and subgroups.

## Verdict on the M0 kill criterion

**Kill criterion not met; confirmed from the full text.** The criterion needs Laguinge et al. to use Census 2022 or linked records *and* a design at least as strong as M5's. They use two PNAD cross-sections (2006 for prediction, 2014 for outcomes), a binary propensity cut and a binary 1985 cohort cut, with no geographic dose. M5 remains an **extension**, not a replication.

How M5 should position itself against them (carried into `pap/M5.md`):

1. Different identifying variation: state-of-birth coverage x eligible childhood years (ITT dose), rather than predicted household propensity x cohort.
2. Several outcome years (PNAD Continua 2012-2025), so age and cohort are separated and outcomes can be compared at fixed ages.
3. Younger, more exposed cohorts (born up to the late 1990s).
4. A pre-transfer household poverty outcome, which neither version has.
5. Report their design's age-cohort confound as a reason the estimates may differ, and re-use the 1985 cohort boundary as a check.

Benchmarks for M5: schooling +0.8 years and labor income +43% are **treatment-on-the-(predicted)-treated** contrasts for teens exposed from age 12-16; the household per-capita income effect (2024) is +10% for household heads. An M5 ITT on all children in a state is diluted by state coverage (roughly 10-50%) and should be expected to be far smaller.

## Corrections to the previous (secondary-source) note

- Data: confirmed PNAD 2006 (stage 1) and **PNAD 2014 mobility supplement** (stage 2); previously "[R], not confirmed".
- Sample: ages 25-40 in 2014, cohorts 1974-1989, both parents present; previously unknown.
- Stage-1 predictors are **retrospective parental characteristics at age 15**, not adult characteristics. The old threat "(2) stage-1 uses adult characteristics that may be outcomes" was wrong; it applies only to the second-stage controls.
- Treated is a **binary cut at 0.257**, not a continuous propensity.
- "15%" is the Rambachan-Roth M-bar for labor income (0.10 in 2024), not a misclassification bound.
- Placebos and event study **do exist** (old note: "not confirmed").
- The UNU-WIDER brief figures (ages 10-15 at start; +1.3 / +1.9 years; BRL 2,300 / 1,450) do **not** appear in either version read. Treat them as from the WIDER 2026 version or the brief only, unverified.
- The 2024 version reports a household per-capita income effect for heads (+83 US$, +10%); the old note said no household-income outcome existed.
- The "+9 pp primary, +6 pp secondary" and "-3.7 pp transfer receipt" figures were correct.

## Other 2024-2026 long-run Bolsa Familia papers (links found by search, not opened)

- Britto, Fonseca, Pinotti, Sampaio, Warwar, "Do CCTs create conditions to thrive? Bolsa Familia and social mobility in Brazil", UNU-WIDER WP 2025/96: https://www.wider.unu.edu/sites/default/files/Publications/Working-paper/PDF/wp2025-96-do-ccts-create-conditions-thrive-bolsa-familia-social-mobility-Brazil.pdf . Linked admin records (CadUnico, RAIS); local opportunities mediate the gains. Main threat to M6.
- UNU-WIDER research brief "Can Bolsa Familia break the cycle of poverty?": https://www.wider.unu.edu/publication/can-bolsa-familia-break-cycle-poverty
- IMDS/Oppen Social, "Social mobility and CCT programs: The Bolsa Familia program in Brazil", World Development Perspectives 35 (2024), doi:10.1016/j.wdp.2024.100624. Descriptive: of children aged 7-16 in 2005, 64% had left social programmes and 45% had entered formal work by 2019. Not causal.
- "Do conditional cash transfers improve intergenerational gains in educational achievement? Evidence from Brazil's Bolsa Familia Program", World Development (2024): https://www.sciencedirect.com/science/article/abs/pii/S0305750X2400322X . Education only.
