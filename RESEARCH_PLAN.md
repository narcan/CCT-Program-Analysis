# Research Plan: CCTs and Aggregate Poverty, Revisited

Status: draft v2 (after a hostile review), October 2026. Owner: Pedro Ávila.

## Objective

**Primary goal (guaranteed deliverable):** an honest correction of the 2012 thesis, plus a clear answer to "could national poverty data ever have shown what the thesis claimed?"

**Secondary goal (only if the gates below say go):** estimate whether Brazilians who were exposed to Bolsa Família as children are less poor as adults, **before counting any transfer they receive today**, and whether that effect is large enough to matter for national poverty.

Plain definitions used throughout:

1. **Mechanical effect.** The drop in measured poverty from adding transfer income to household income, holding everything else fixed. This is an accounting exercise, not a causal estimate: it ignores labor-supply responses and local multiplier effects.
2. **Long-run (human capital) effect.** The difference in adult outcomes (schooling, formal work, earnings, pre-transfer poverty) between people exposed and not exposed to the program as children. This is the claim the 2012 thesis was really testing.
3. **Detectability.** Whether an effect of plausible size could be seen in national time series at all.

**What this plan cannot answer.** It cannot separate the effect of the *conditions* from the effect of the *cash*. Every Brazilian beneficiary got both. Only designs like Baird, McIntosh & Özler (2011) can. The long-run effect here is the effect of the whole program.

**What is already known (do not rediscover it):**

| Question | Existing answer | Implication |
|---|---|---|
| Mechanical effect in Brazil | Souza, Osorio, Paiva & Soares (2019): about 15% less poverty and 25% less extreme poverty, PNAD 2001-2017 | Replicate it as a pipeline check. Not new. |
| Long-run effect of Bolsa Família on former child beneficiaries | Laguinge, Gasparini & Neidhöfer (2024/2025 working paper): gains in schooling and labor income, using a two-sample DiD | Any M5 result must be framed as a replication or extension of this paper, not a first answer |
| Descriptive outcomes of 2005 child beneficiaries | IMDS linked CadÚnico and RAIS: 64% had left CadÚnico by 2019 (descriptive, not causal) | Context only |
| Local spillovers | Gerard, Naritomi & Silva (2021): the expansion raised formal employment in more-exposed municipalities | Municipal comparisons (M6) include general-equilibrium effects by construction |
| Long-run CCT effects in general | Molina Millán et al. (2019); Parker & Vogl (2023) | Schooling gains are consistent; earnings effects are mixed |

**Where a contribution is plausible:** (a) a transparent, public replication of the long-run result with a pre-registered design and different data (Census 2022, released August 2026); (b) translating the long-run effect into national poverty terms, which none of the papers above does; (c) the power analysis itself, as a teaching piece on why the 2012 design could not work.

## Ground rules

- **Predictions first.** Each milestone opens with a dated `LOG.md` entry stating the expected result and why.
- **Pre-analysis plan before any causal estimate.** For M5 and M6, write `pap/M5.md` and `pap/M6.md` (template below) and commit them with a git tag *before* loading the outcome variables. Anything not in the plan is labeled exploratory.
- **One primary outcome per milestone.** Secondary outcomes are reported with multiple-testing adjustment (Romano-Wolf or Holm within each milestone's family).
- **No interpolated outcomes.** Survey years only. Interpolated covariates get a flag column.
- **Everything runs from raw data.** One command rebuilds every table. Raw downloads are saved with their pull date and never edited by hand. Pin the PIP API release (PPP round and data version) in the manifest.
- **Time box.** Each milestone gets an estimate in hours. If it runs past twice the estimate, stop and write a gate note before continuing.
- **Decision gates and kill criteria.** Each milestone ends with go / pivot / stop in `LOG.md`, judged against the kill criteria written below, not against how interesting the result looks.

## Milestones at a glance

| # | Milestone | Main output | Gate question |
|---|---|---|---|
| M0 | Setup, literature check, data access | Repo, environment, reading notes, Census 2022 access requested | Is the secondary goal still worth doing after reading Laguinge et al.? |
| M1 | Replicate and correct 2012 | Corrected Tables 1, 4-6 and a one-page erratum | What survives once the errors are fixed? |
| M2 | Power analysis | Power curves for national series | Could any plausible long-run effect be seen in national data? |
| M3 | Aggregate refresh (descriptive, capped at 15 hours) | Updated series and decomposition, no causal claim | Is the post-2003 pattern still there with real survey years? |
| M4 | Microdata pipeline and mechanical effect | Poverty with and without transfers, 2001 to latest | Does the pipeline reproduce Souza et al. (2019)? |
| M5 | Long-run effect, cohort design | Pre-registered cohort estimate | Are exposed cohorts less poor before transfers? |
| M6 | Municipal dose-response (conditional) | Pre-registered municipal estimate | Only if Census 2022 access is granted and M5 passes its checks |
| M7 | Optional extensions (parking lot) | Nothing by default | Only if time remains |
| M8 | Write-up | Paper or long blog post, replication package | Would a skeptical economist accept the main claim? |

**Why this order.** Information per hour, subject to dependencies. M0 now includes the literature check because a published working paper already covers the core long-run question; reading it first changes how M5 is framed. Census 2022 controlled access is requested in M0 because approval has lead time. M4 comes before M5 because the cohort analysis reuses the same microdata pipeline, and reproducing a known number (Souza et al.) is the cheapest way to find pipeline bugs. Cross-country work moved to a parking lot: adoption is endogenous, clean comparison countries are scarce, and M2 is likely to show it can't detect a long-run effect.

---

## M0. Setup, literature check, data access

**Why:** you've been out of grad school for 15 years, and the field moved. Two weeks of reading costs less than a month on a question someone already answered.

Tasks:

1. Layout: `data/raw/` (gitignored, with a manifest), `data/clean/`, `src/`, `analysis/` (one script per milestone), `pap/`, `output/`, `LOG.md`.
2. Environment: Python with `pandas`, `pyfixest` (fixed effects, event studies, wild bootstrap), `statsmodels`, `matplotlib`. Keep R available for `did` and `HonestDiD` if the Python ports fall short. Pin versions in `pyproject.toml`.
3. Port `Data/ThesisDataCoding.do` to Python. Keep the original `.do` files as the historical record.
4. Read Laguinge, Gasparini & Neidhöfer in full. Write half a page: their data, how they define exposure, their identifying assumption, and what they did not do.
5. Request Census 2022 controlled-tier microdata access (gov.br account and a signed agreement). Record the date. Check which geographic level the controlled tier identifies.
6. Read the "Start here" items.

**Kill criterion:** if Laguinge et al. already use Census 2022 or linked records with a design at least as strong as M5's, M5 becomes a replication only, and M6 becomes the main secondary contribution or is dropped.

Done when the environment builds from scratch and `LOG.md` has the first prediction entry and the literature note.

Reading, start here:

- Haughton & Khandker (2009), *Handbook on Poverty and Inequality*, World Bank. Chapters on FGT measures and poverty over time. [Link](https://openknowledge.worldbank.org/entities/publication/159a4bae-4817-5b0b-9d7f-9ba7b6b666cb)
- Huntington-Klein, *The Effect*. Chapters on causal diagrams, DiD, event studies and synthetic control. [Link](https://theeffectbook.net)
- Cunningham, *Causal Inference: The Mixtape*. DiD and synthetic control chapters. [Link](https://mixtape.scunning.com)
- Fiszbein & Schady et al. (2009), *Conditional Cash Transfers: Reducing Present and Future Poverty*, World Bank. Chapter 4. [Link](https://openknowledge.worldbank.org/entities/publication/db93c3fe-1810-5834-a9da-c1386caa0323)
- Laguinge, Gasparini & Neidhöfer, "The Long-Run Effects of Conditional Cash Transfers: The Case of Bolsa Familia in Brazil" (CEDLAS WP 328, 2024; ECINEQ WP 2025-684). The closest existing paper to M5. [Link](https://www.ecineq.org/milano/WP/ECINEQ2025-684.pdf)

---

## M1. Replicate and correct the 2012 analysis

**Why:** it sets the baseline. Table 6 has already been reproduced exactly from `Data/ThesisDataCSV.csv`.

Tasks:

1. Reproduce Tables 4, 5 and 6 in Python to three decimals.
2. Fix the spline labels. `mkspline` on the 0-3 `cctstage` code produces cumulative step indicators (post year 1, year 3, year 5). Relabel and report cumulative effects.
3. Recompute Table 1. The published FGT1 rate-of-change row (mean -0.64) is wrong; the data give about -0.039.
4. Re-run with survey-year outcomes only, dropping the interpolated 1991, 1994, 2000, 2006 and 2007. Use annualized change between surveys.
5. Placebo break years: move the break across every year from 1990 to 2002.
6. Re-code CCT adoption dates with a cited source per country. In the current data Colombia, Ecuador, Costa Rica, the Dominican Republic and Paraguay are all coded as never-CCT; check each. Re-run Table 5.
7. Drop Gini change from the controls (it's a mediator). Report both versions.
8. Write `output/M1_erratum.md`: one page on what changed and what survives.

**Hypotheses (written now, so they can be wrong):**
- H1.1: after fixes 2-4, no post-2003 coefficient is significant at 5%.
- H1.2: 2003 does not rank in the top 3 of the placebo break years by t-statistic.

**Falsification test:** the placebo distribution in task 5. If 2003 is not extreme relative to fake breaks, the thesis's main result is not distinguishable from noise.

**Kill criterion:** none. M1 always finishes; it is the guaranteed deliverable.

Reading:

- Bernal, Cummins & Gasparrini (2017), interrupted time series tutorial. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC5407170/)
- Simmons, Nelson & Simonsohn (2011), "False-Positive Psychology." [Link](https://journals.sagepub.com/doi/10.1177/0956797611417632)

---

## M2. Power analysis (decision gate)

**Why:** before asking "is there an effect?", ask "could I see one if it were there?"

Tasks:

1. Estimate the noise. In the thesis data, the SD of annual changes in Brazil's headcount (the $2 line) is about 2.5 percentage points, or about 9.5 log points. It is not stable: about 3.7 pp in 1982-1993 (hyperinflation years) and about 1.2 pp from 1995 on. Use the post-1995 noise as the main case and the full-period noise as a pessimistic case. Model autocorrelation; don't assume independent shocks.
2. Effect sizes:
   - **Mechanical:** Souza et al. (2019), about 15% (poverty) and 25% (extreme poverty), phased in with coverage 2004-2006.
   - **Long-run:** translate an individual-level effect into a national one. Exposed cohorts are only part of the adult population, so a national effect is roughly (individual effect) × (share of poor adults who were exposed). Build that share from population by birth year and coverage by year. Simulate a grid of individual effects anchored on Laguinge et al. and Parker & Vogl.
3. Simulate the M3 specification on synthetic series. Record power, Type S and Type M error by effect size and series length.
4. Write the gate decision.

**Hypothesis H2.1:** with realistic exposure shares, power to detect the long-run effect in national series is below 20% at any plausible size, while the mechanical effect is detectable.

**Kill criterion:** if power for the long-run effect is below 50% at the upper end of plausible sizes, stop all national time-series work on the long-run effect. M3 stays descriptive and M7's cross-country items stay parked.

Done when there is a power curve plot and a one-paragraph decision.

Reading:

- Gelman & Carlin (2014), "Beyond Power Calculations." [Link](https://sites.stat.columbia.edu/gelman/research/published/PPS551642_REV2.pdf)
- Souza, Osorio, Paiva & Soares (2019), IPEA TD 2499. Source of the mechanical anchors. [Link](https://repositorio.ipea.gov.br/handle/11058/9356)

---

## M3. Aggregate refresh (descriptive only, 15-hour cap)

**Why:** answers "did the 2012 pattern hold?" with real survey years. It makes no causal claim, because 2003 coincides with the Lula government, large minimum wage increases and the commodity boom, and the national series has no comparison group.

Tasks:

1. Pull Brazil from the World Bank PIP API. Save the raw JSON with pull date and PIP version. Use the 2021 PPP lines: $3.00, $4.20 and $8.30 (upper-middle-income line). Also report one national line (the Bolsa Família eligibility line in reais) so the result doesn't hinge on PPP revisions.
2. Plot the series and mark the breaks: 2012-2015 PNAD to PNAD Contínua (use the overlap years to show the level shift; never splice silently), 2015-16 recession, 2020 Auxílio Emergencial, Auxílio Brasil period, 2023 relaunch.
3. Datt-Ravallion growth vs redistribution decomposition per survey spell. Redistribution is not the same as Bolsa Família: minimum wage and pensions also move it. Combine with the M4 mechanical series to show how much of the redistribution part the transfer accounts for.
4. Compare with a growth-elasticity benchmark (Bourguignon 2003): percentage declines speed up mechanically as poverty falls into the thinner tail.

**Hypothesis H3.1:** after the growth-elasticity benchmark, the 2003-2014 acceleration is mostly explained by growth plus the mechanical transfer, leaving little to attribute to anything else.

Reading:

- Datt & Ravallion (1992). [Link](https://ideas.repec.org/a/eee/deveco/v38y1992i2p275-295.html)
- Bourguignon (2003), "The growth elasticity of poverty reduction." [Link](https://ideas.repec.org/p/del/abcdef/2002-03.html)
- World Bank, June 2025 update to the global poverty lines. [Link](https://www.worldbank.org/en/news/factsheet/2025/06/05/june-2025-update-to-global-poverty-lines)
- PIP data and API docs. [Link](https://pip.worldbank.org)

---

## M4. Microdata pipeline and mechanical effect

**Why:** M5 needs the same pipeline, and reproducing a known number is the best bug test.

Tasks:

1. Get PNAD (2001-2015) and PNAD Contínua (2012 on). Base dos Dados hosts cleaned versions on BigQuery.
2. **Know what each survey can identify.** Annual PNAD has no separate Bolsa Família income item: the transfer sits in a catch-all "interest, dividends and other income" variable. Receipt is asked directly only in supplements (2004 and 2006 confirmed; check others). Souza et al. impute it from typical benefit values; follow their method. PNAD Contínua collects "other income", including Bolsa Família, in the 1st and 5th visits; check the dictionary for the exact item and the first year it exists.
3. Reproduce Souza et al. (2019) for two years. **Kill criterion:** if the reproduction is off by more than 2 points of the percentage reduction after two weeks of debugging, stop and fix the pipeline before M5.
4. Extend the with/without-transfer series to the latest year, on both survey bases, showing the 2012-2015 overlap.
5. Report the known measurement problem: surveys under-report transfer income relative to administrative totals. Compare survey totals with program spending per year and report the ratio.

**Hypothesis H4.1:** the mechanical reduction in extreme poverty is between 20% and 30% in 2015 and larger after the 2023 relaunch.

Reading:

- Base dos Dados. [Link](https://basedosdados.org)

---

## M5. Long-run effect: cohort design

**Why:** this tests the actual hypothesis. It must now be framed against Laguinge et al.

**Design (intent-to-treat).** Exposure is defined by when and where you were a child, not by whether your family received the benefit, since adult surveys don't record childhood receipt.

- Exposure_i = (years of benefit-eligible childhood age during 2004-2010) × (Bolsa Família coverage in birth state in 2004-2006).
- Compare cohorts within states with cohort fixed effects and state-of-birth fixed effects. Use state of birth, not current state, because people migrate. Note that state of birth is coarse (27 units), so use wild cluster bootstrap.
- Outcomes, measured in PNAD Contínua and Census 2022: years of schooling (primary outcome), formal employment, labor income, **pre-transfer** household poverty.

**Hypotheses:**
- H5.1 (primary): a one-SD increase in exposure raises completed schooling. Expected size and sign written in the PAP.
- H5.2: the effect on pre-transfer poverty is negative but smaller in relative terms than the schooling effect.

**Falsification tests (all must pass before the main estimate is believed):**
- F5.1: cohorts too old to be exposed show no exposure-by-coverage gradient. This is the pre-trend test. Exposure started before 2003 through the predecessor Bolsa Escola (2001), so "too old" means too old for that program too (check its age rules; roughly born 1985 or earlier).
- F5.2: outcomes fixed before the program (e.g. parents' schooling, where observable) show no effect.
- F5.3: results don't depend on adding state-specific linear cohort trends. Brazil's schooling was rising for all cohorts, and early-coverage states were poorer states that may have been catching up anyway (the same spatial convergence Parker & Vogl found hard to separate for men).

**Threats specific to M5:** predecessor programs (Bolsa Escola, Bolsa Alimentação) blur the start date; age at observation differs by cohort (younger cohorts are measured earlier in their careers, which biases earnings effects toward zero; compare at fixed ages); other programs and reforms that hit the same cohorts and states; selective migration.

**Kill criterion:** if F5.1 fails, report the descriptive gradient and do not make a causal claim.

Done when the PAP is tagged, the estimate is reported with all three falsification tests, and the result is placed next to Laguinge et al.

Reading:

- Parker & Vogl (2023), *Economic Journal* 133(655). The template. [NBER version](https://www.nber.org/papers/w24303)
- Molina Millán, Barham, Macours, Maluccio & Stampini (2019), *World Bank Research Observer* 34(1). [IDB working paper version](https://publications.iadb.org/bitstream/handle/11319/7891/Long-term-Impacts-of-Conditional-Cash-Transfers-in-Latin-America-Review-of-the-Evidence.pdf)
- Cameron & Miller (2015), "A Practitioner's Guide to Cluster-Robust Inference." [Link](https://jhr.uwpress.org/content/50/2/317)

---

## M6. Municipal dose-response (conditional)

**Start only if:** Census 2022 controlled-tier access is granted and identifies municipality, and M5's falsification tests passed.

**Why it's weaker than v1 claimed.** Coverage was assigned by estimated poverty, so coverage and poverty are almost the same variable. Poor places also catch up for other reasons (mean reversion). Municipal effects include local multipliers (Gerard, Naritomi & Silva 2021) and migration between municipalities, so they are not the effect on a family. And 2010-2022 is not "mostly structural": the 2022 Census was taken in a year of large transfer changes and after COVID.

Tasks:

1. Check data first, before any design work:
   - Census 2022 sample microdata: released 31 August 2026 in three tiers (public files identify only the state; controlled tier needs a gov.br login and a signed agreement; restricted tier is on-site). Income for all residents is only in the sample questionnaire. Check whether social-program income can be separated from other non-labor income; if not, a pre-transfer poverty outcome is impossible in 2022.
   - Municipal Bolsa Família counts by year from 2004: confirm the source (MDS open data) and that the series really starts in 2004.
   - Atlas do Desenvolvimento Humano for 1991, 2000 and 2010.
2. Draw the causal diagram before any regression.
3. Treatment: average 2004-2010 coverage. Primary specification in the PAP, with 2000 poverty and its square as controls, region fixed effects.
4. Estimate 2000-2010 and 2010-2022 separately.

**Hypothesis H6.1:** conditional on 2000 poverty, higher coverage predicts a faster fall in pre-transfer poverty 2010-2022.

**Falsification tests:**
- F6.1: coverage does not predict 1991-2000 poverty change (pre-program placebo).
- F6.2: coverage does not predict outcomes the program could not affect (e.g. share of population over 70 in 2010, adjusted for the same controls).

**Kill criterion:** if F6.1 fails, stop and report the result as descriptive.

Reading:

- Atlas do Desenvolvimento Humano no Brasil. [Link](https://www.atlasbrasil.org.br)
- IBGE, Census 2022 microdata and documentation. [Link](https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Microdados_e_Areas_de_Ponderacao/)
- IPUMS International. [Link](https://international.ipums.org)
- Gerard, Naritomi & Silva (2021), "Cash Transfers and Formal Labor Markets: Evidence from Brazil," CEPR DP16286. [Link](https://ideas.repec.org/p/cpr/ceprdp/16286.html)

---

## M7. Optional extensions (parking lot)

Nothing here starts unless M8 is drafted and time remains. Each item needs its own gate note.

1. **Mexico's 2019 Prospera rollback.** Marquez-Padilla, Parker & Vogl (NBER w33527, 2025) already use it and find sharp enrollment drops. The rollback was not a pure cash removal: Becas Benito Juárez replaced it, so it changes targeting and conditions more than cash. A poverty-rate study may still be open; verify before investing. [Link](https://www.nber.org/papers/w33527)
2. **Cross-country staggered DiD and synthetic control.** Only if M2 says aggregate effects are detectable, which is unlikely. Read Roth et al. (2023) first. [Link](https://arxiv.org/abs/2201.01194)
3. **Brazil 2020-21** as an illustration of the mechanical channel, using the M4 series.

Further reading if any of these start: Callaway & Sant'Anna (2021) [Link](https://doi.org/10.1016/j.jeconom.2020.12.001); Goodman-Bacon (2021) [Link](https://doi.org/10.1016/j.jeconom.2021.03.014); Abadie (2021) [Link](https://doi.org/10.1257/jel.20191450); Bertrand, Duflo & Mullainathan (2004) [Link](https://www.nber.org/papers/w8841); Rambachan & Roth (2023) [Link](https://doi.org/10.1093/restud/rdad018); Baird, McIntosh & Özler (2011) [Link](https://doi.org/10.1093/qje/qjr032).

---

## M8. Write-up

A 10-15 page paper or long blog post, a replication package (`make all` rebuilds everything from raw data), and a section comparing predictions with results, including the ones that were wrong.

Done when someone else can clone the repo and reproduce every figure.

---

## Threats to validity

| Threat | Where it bites | Response |
|---|---|---|
| 2003 confounders (Lula, minimum wage, commodity boom, pensions) | M1, M3 | No causal claim from national series; decomposition plus mechanical series |
| Program scaled up 2003-2006, so timing is gradual | M1, M3, M5 | Use coverage, not an on/off date |
| Survey income under-reports transfers | M4, M5 | Compare with administrative totals; report the ratio |
| PNAD cannot identify Bolsa Família directly | M4 | Follow the Souza et al. imputation; use supplements to validate |
| PNAD to PNAD Contínua break (2012-2015) | M3, M4, M5 | Show overlap years; never splice silently |
| PPP revisions (2005 to 2017 to 2021 rounds) | M1, M3 | Report a national reais line alongside PPP lines; pin the PIP version |
| Spillovers and general equilibrium (local multipliers, migration, school supply) | M5, M6 | State that estimates include them; use state of birth in M5 |
| Mean reversion and targeting on need | M6 | Pre-program placebo; control for baseline poverty |
| Bad controls (Gini, current income, current residence) | All | Controls must be fixed before treatment |
| Cohort trends and age at observation | M5 | Cohort fixed effects, fixed-age comparisons, trend sensitivity |
| Multiple testing across lines, outcomes and milestones | All | One primary outcome per milestone; Romano-Wolf within families; report every test run |
| Researcher degrees of freedom | M5, M6 | Tagged pre-analysis plan before outcomes are loaded |
| Effects of conditions vs cash | All | Out of scope; stated as a limit |

## Pre-analysis plan template (`pap/M5.md`, `pap/M6.md`)

1. Question and primary hypothesis, with expected sign and size.
2. Data sources, versions and sample restrictions.
3. Treatment and exposure definition.
4. Primary outcome; list of secondary outcomes.
5. Primary specification, written as an equation, plus standard errors.
6. Falsification tests and what counts as passing.
7. Multiple-testing correction.
8. What result would change your mind, and what you will report if the main test fails.

Commit, tag (`pap-M5-v1`), and optionally post to OSF before loading outcome variables. Deviations go in a dated "changes from the plan" section, never silently.

---

## Open decisions

1. **Scope.** Commit to M0-M4 plus the erratum and power note as the project, with M5-M6 as a stretch? Recommended: yes.
2. **Census 2022 access.** Apply for the controlled tier (needs a gov.br account)? Recommended: yes in M0; without it, M6 is dropped and M5 uses PNAD Contínua only.
3. **Public pre-registration.** OSF or a git tag only? Recommended: git tag for all, OSF for M5.
4. **Time budget.** At about 5 hours a week: M0-M4 roughly 3-4 months; M5 another 2-3 months; M6 another 2-3 months.
