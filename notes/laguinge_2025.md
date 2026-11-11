# Laguinge, Gasparini & Neidhoefer: long-run effects of Bolsa Familia

Versions: CEDLAS WP 328 (2024), ZEW DP 25-022 (2025), ECINEQ 2025-684 (2025), UNU-WIDER WP 2026/14, SSRN 5251109.

**Source caveat.** None of the PDFs could be opened from this session: the network proxy blocked cedlas.econo.unlp.edu.ar, ftp.zew.de, ecineq.org, econstor.eu, wider.unu.edu, ideas.repec.org and gov.br. Everything below comes from abstracts, search-engine excerpts of the PDFs, the Brazilian ministry (MDS / Agencia Gov) press summary of Sept 2024 and the UNU-WIDER research brief. Items marked [R] are reconstructed or inferred and must be checked against the full text before anyone cites them.

## Data and years
- PNAD, the annual national household survey. Exact survey rounds and whether PNAD Continua is also used: [R], not confirmed.
- No sign of Census 2010/2022 or linked administrative records (CadUnico, RAIS). The abstract justifies the method by the *lack* of longitudinal data, which strongly suggests no linked records.

## Exposure definition
- Two-sample two-stage (TS2S) approach. Stage 1 predicts the probability of childhood programme participation from household characteristics in a sample where receipt is observed. Stage 2 uses that predicted probability to sort adults into likely-treated and likely-control groups. [R: exact predictors and which PNAD rounds hold the receipt question]
- Age eligibility: the transfer (Bolsa Escola, the predecessor) started in March 2001, so only people born in 1985 or later could receive it as children. Older cohorts are the unexposed comparison.
- Design: cohort difference-in-differences, (born 1985 or later) x (high predicted participation).
- Unlike M5, exposure is individual-level predicted participation, not childhood eligible years x birth-state coverage. No evidence of a state-coverage dose term. [R]

## Identifying assumption and main threats
- Assumption: absent the programme, the gap between high- and low-propensity people would have evolved the same way across the 1985 cohort boundary.
- Threats: (1) other cohort-specific shocks hitting poor youth after 2001 (FUNDEF/FUNDEB school funding, the minimum-wage boom, the 2000s formalisation wave), which load on exactly the high-propensity group; (2) stage-1 prediction uses adult characteristics that may themselves be outcomes of the programme; (3) a binary cohort cutoff ignores years of exposure, so the effect mixes 1-year and 10-year exposure.

## Main estimates (as reported in excerpts and summaries)
- Schooling: +0.8 years for former beneficiaries, similar for men and women. Primary completion +9 pp and secondary completion +6 pp (MDS summary).
- Labor income: about +US$250 per month, larger for men. A secondary source puts this at about one third of a minimum wage. This is a scaled-up per-beneficiary (treated) effect, not an intent-to-treat effect, and the currency basis (PPP or nominal) is [R]. Treat it as an upper-range anchor.
- Current receipt of social transfers in adulthood: about -3.7 pp.
- UNU-WIDER brief: the largest and most consistent gains are for those aged 10 to 15 at programme start (schooling +1.3 years for boys, +1.9 for girls; formal-work earnings about BRL 2,300 for men and BRL 1,450 for women). How the brief's figures map onto paper tables is [R].
- Relative anchors for M5: +0.8 years is roughly 10 to 12 percent of mean schooling in poor Brazilian cohorts [R: denominator is my assumption, not theirs]. Per-beneficiary effects must be divided by participation probability x coverage to compare with an M5 ITT.

## Robustness and falsification
- Excerpts mention a sensitivity bound ("maximum threshold for a significant effect is 15%"), probably a test of how much stage-1 misclassification the results survive [R]. Placebo cohort cutoffs, pre-trend or event-study checks: not confirmed [R].
- Heterogeneity: by sex (income effect larger for men); the WIDER version stresses that gains are unevenly distributed across groups.

## What they did NOT do (as far as can be verified)
- No pre-transfer (counterfactual market income) poverty outcome. They report current transfer receipt, not poverty net of transfers.
- No Census 2022 (and the full microdata are not yet out). No linked administrative records.
- No exposure-intensity dose (years eligible x state or municipal coverage).
- No national translation (aggregate poverty or inequality change implied by the effects).

## Verdict on the M0 kill criterion
**M5 survives. It is not a replication.** The kill condition needs Census 2022 or linked records *and* a design at least as strong as M5's. Laguinge et al. have neither: PNAD only, a binary cohort cutoff and a predicted-participation contrast. M5 adds (a) a continuous ITT dose from eligible years x birth-state coverage, which enables dose-response and event-study checks; (b) pre-transfer poverty; (c) a national translation. But M5 must position itself against this paper explicitly, reuse its 1985 cohort boundary as a check, and treat its +0.8 years as a benchmark. This verdict rests on secondary sources; confirm in the full PDF that no state-coverage interaction or Census data appear.

**Watch Britto et al. as the bigger threat to M6.** They link CadUnico and RAIS (and tax data) and analyse place effects, so municipal heterogeneity is partly covered.

## Other 2024-2026 long-run Bolsa Familia papers (links found by search, not opened)
- Britto, Fonseca, Pinotti, Sampaio, Warwar, "Do CCTs create conditions to thrive? Bolsa Familia and social mobility in Brazil", UNU-WIDER WP 2025/96: https://www.wider.unu.edu/sites/default/files/Publications/Working-paper/PDF/wp2025-96-do-ccts-create-conditions-thrive-bolsa-familia-social-mobility-Brazil.pdf . Linked admin records (CadUnico, RAIS); local opportunities mediate the gains. 2025 author list only partly confirmed.
- UNU-WIDER research brief "Can Bolsa Familia break the cycle of poverty?": https://www.wider.unu.edu/publication/can-bolsa-familia-break-cycle-poverty
- IMDS/Oppen Social, "Social mobility and CCT programs: The Bolsa Familia program in Brazil", World Development Perspectives 35 (2024), doi:10.1016/j.wdp.2024.100624: https://www.sciencedirect.com/science/article/pii/S2452292924000614 . Descriptive admin-data follow-up of children aged 7 to 16 in 2005: by 2019, 64% had left social programmes and 45% had entered formal work. Not causal.
- "Do conditional cash transfers improve intergenerational gains in educational achievement? Evidence from Brazil's Bolsa Familia Program", World Development (2024): https://www.sciencedirect.com/science/article/abs/pii/S0305750X2400322X . Education outcome only.
- USP doctoral thesis (2025, cited in search results, link not verified): positive effects on schooling and formal work, mixed on earnings.
