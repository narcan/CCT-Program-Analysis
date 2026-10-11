# Research Plan: CCTs and Aggregate Poverty, Revisited

Status: draft v1, October 2026. Owner: Pedro Ávila.

## Objective

Find out whether conditional cash transfer (CCT) programs leave a detectable mark on aggregate poverty **beyond the cash itself**. Use Brazil's Bolsa Família as the main case.

That one question breaks into three:

1. **Mechanical effect.** How much does poverty fall simply because transfer income is added to household income?
2. **Structural effect.** After the transfer is subtracted out, are adults who grew up in the program poorer or less poor than they would otherwise have been? This is the human capital channel, and it's the claim the 2012 thesis was really testing.
3. **Detectability.** Can a structural effect of plausible size be seen in national time series at all, or only in microdata?

Question 3 is checked early (Milestone 2) because the answer decides how much effort the cross-country work in Milestone 6 deserves.

## Ground rules

- **Write predictions down before running anything.** Each milestone opens with a dated entry in `LOG.md` saying what you expect to find and why. Comparing those predictions with the results later is how you build research taste.
- **Decide the specification before seeing new data.** Write down the outcome, treatment definition, controls and sample in `LOG.md` first. Anything added afterward is labeled exploratory.
- **No interpolated outcomes.** Use survey years only. Covariates may be interpolated, but they get a flag column.
- **Everything runs from raw data.** One command rebuilds every table. Raw downloads are saved with their pull date and never edited by hand.
- **Decision gates.** Each milestone ends with a short go / pivot / stop note in `LOG.md`.

## Milestones at a glance

| # | Milestone | Main output | Why it sits here | Gate question |
|---|---|---|---|---|
| M0 | Setup and refresher | Repo skeleton, environment, first readings done | Everything else depends on it | Can I explain FGT, DiD and parallel trends in two sentences each? |
| M1 | Replicate and correct 2012 | Corrected Tables 4–6 plus a one-page erratum | Cheapest step. It sets the baseline and teaches the old code. | What survives once the errors are fixed? |
| M2 | Power / design analysis | Simulation of what national series can detect | Stops months of work on a design that can't answer the question | Is a plausible structural effect detectable in aggregate data? |
| M3 | Brazil refresh, aggregate | ITS on current PIP data through the latest year, plus a growth-vs-redistribution decomposition | Quick answer to "did the 2012 pattern hold?" | Does the post-2003 break survive with more years and honest data? |
| M4 | Mechanical vs structural, microdata | Poverty with and without transfers; exposure-cohort analysis | Tests the actual hypothesis, not a proxy | Is there a structural effect net of the transfer? |
| M5 | Within-Brazil dose-response | Municipal coverage vs poverty change, Census 2000 → 2010 → 2022 | Strongest causal design available for free | Do municipalities with more coverage pull ahead after 2010? |
| M6 | Cross-country and natural experiments (optional) | Staggered DiD, synthetic control, Mexico's 2019 Prospera removal | Gives external validity, but identification is weakest | Only if M2 says aggregate signals are detectable |
| M7 | Write-up | Short paper or long blog post plus a replication package | Unpublished work doesn't count | Would a skeptical economist accept the main claim? |

**How the order was chosen:** expected information per hour of work, subject to dependencies. M1 and M2 are cheap and decide what follows. M4 and M5 are expensive but answer the question directly. M6 is last: CCT adoption across countries is endogenous (it coincides with left-wing governments and commodity booms), clean comparison countries are scarce, and that literature is already crowded.

---

## M0. Setup and refresher

**Why:** you've been out of grad school for 15 years. Two weeks of targeted reading costs less than a month spent on a wrong specification.

Tasks:

1. Create the layout: `data/raw/` (gitignored, plus a manifest file), `data/clean/`, `src/` (functions), `analysis/` (one script per milestone), `output/`, `LOG.md`.
2. Set up the environment: Python with `pandas`, `pyfixest` (fixed effects, event studies, wild bootstrap), `statsmodels`, `matplotlib`. Keep R available just for the `did` and `HonestDiD` packages if their Python ports fall short. Pin versions in `pyproject.toml`.
3. Port the cleaning steps in `Data/ThesisDataCoding.do` to Python. Keep the original `.do` files untouched as the historical record.
4. Read the "Start here" items below.

Done when the environment builds from scratch and `LOG.md` has its first prediction entry.

Reading, start here:

- Haughton & Khandker (2009), *Handbook on Poverty and Inequality*, World Bank. Free. Read the chapters on poverty measures (FGT) and poverty over time. [Link](https://openknowledge.worldbank.org/entities/publication/159a4bae-4817-5b0b-9d7f-9ba7b6b666cb)
- Huntington-Klein, *The Effect* (free online). Read the chapters on causal diagrams, difference-in-differences, event studies and synthetic control. It's the gentlest current refresher. [Link](https://theeffectbook.net)
- Cunningham, *Causal Inference: The Mixtape* (free online). Read the DiD and synthetic control chapters; it goes deeper than *The Effect*. [Link](https://mixtape.scunning.com)
- Fiszbein & Schady et al. (2009), *Conditional Cash Transfers: Reducing Present and Future Poverty*, World Bank. Chapter 4 covers consumption and poverty effects. It's the canonical reference that the thesis leaned on. [Link](https://openknowledge.worldbank.org/entities/publication/db93c3fe-1810-5834-a9da-c1386caa0323)

---

## M1. Replicate and correct the 2012 analysis

**Why:** it sets the baseline that every later result is compared against. It's mostly done already: the current session reproduced Table 6 exactly from `Data/ThesisDataCSV.csv`.

Tasks, in order:

1. Reproduce Tables 4, 5 and 6 in Python. Done when the numbers match to three decimals.
2. Fix the spline labels. `mkspline` on the 0–3 `cctstage` code produces step indicators: post ≥ year 1, ≥ year 3, ≥ year 5. Relabel the rows and report cumulative effects.
3. Recompute Table 1. The published FGT1 rate row (mean −0.64) is wrong; the data gives about −0.039.
4. Re-run with only survey-year outcomes, dropping the interpolated 1991, 1994, 2000, 2006 and 2007. Use annualized change between surveys.
5. Placebo tests. Move the break year across every year from 1990 to 2002 and check whether 2003 stands out from the fake breaks.
6. Re-code CCT adoption dates, with a cited source for each country. Known errors: Colombia is coded as non-CCT. Ecuador, Costa Rica, the Dominican Republic and Paraguay also need checking. Re-run Table 5 with the corrected coding.
7. Take Gini change out of the controls, since it's a mediator, and report both versions.
8. Write `output/M1_erratum.md`: one page listing what changed and what survives.

Done when the erratum exists and each table has a script that reproduces it.

Reading:

- Bernal, Cummins & Gasparrini (2017), "Interrupted time series regression for the evaluation of public health interventions: a tutorial." This is the correct name for what the thesis did, and the paper shows how to do it properly, including autocorrelation. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC5407170/)
- Simmons, Nelson & Simonsohn (2011), "False-Positive Psychology." Explains why choosing controls by significance inflates false positives. [Link](https://journals.sagepub.com/doi/10.1177/0956797611417632)

---

## M2. Power and design analysis (decision gate)

**Why:** this is the most important milestone for building taste. Before asking "is there an effect?", ask "could I see one if it were there?" If the answer is no, the national time-series approach should be dropped. That would itself be a finding.

Tasks:

1. Estimate the noise. From Brazil's survey-year series, get the SD of year-to-year changes in log FGT0 and FGT1, after removing GDP growth. The current data gives roughly 9 percentage points a year in the raw rate.
2. Set effect sizes to look for, anchored in the literature:
   - **Mechanical:** Souza et al. (2019) estimate that Bolsa Família transfers lowered poverty by about 15% and extreme poverty by about 25%.
   - **Structural:** much smaller. Simulate a grid such as 0.5, 1, 2 and 5% extra decline per year, starting 8–15 years after 2003, when exposed children reach working age.
3. Simulate. Generate synthetic series with that noise, add each effect, and run the M3 specification on them. Record power, Type S error (wrong sign) and Type M error (exaggeration ratio) for each effect size and series length.
4. Write the gate decision in `LOG.md`.

Done when there's a power curve plot and a one-paragraph go/pivot decision.

Reading:

- Gelman & Carlin (2014), "Beyond Power Calculations: Assessing Type S and Type M Errors." The key paper for this milestone, and short. [Link](https://sites.stat.columbia.edu/gelman/research/published/PPS551642_REV2.pdf)
- Souza, Osorio, Paiva & Soares (2019), "Os efeitos do Programa Bolsa Família sobre a pobreza e a desigualdade," IPEA TD 2499. The source of the effect-size anchors. An English version, "The effects of Brazil's Bolsa Família programme on poverty and inequality: an assessment of the first 15 years," exists via IPC-IG. [Link](https://repositorio.ipea.gov.br/handle/11058/15191)

---

## M3. Brazil refresh with current aggregate data

**Why:** it answers the obvious question, whether the 2012 pattern held, with 15 more years of data. It also brings in the decomposition that separates growth from redistribution.

Tasks:

1. Pull Brazil's series from the World Bank Poverty and Inequality Platform (PIP) API. Save the raw JSON with its pull date. Use the 2021 PPP lines: $3.00 (extreme), $4.20 and $8.30 (the upper-middle-income line, the relevant one for Brazil). The thesis's $2.00 line (2005 PPP) has no exact modern equivalent, so report all three lines.
2. Re-run the corrected M1 specification on the new data. Use autocorrelation-robust errors (Newey-West) or Prais-Winsten.
3. Mark the known structural breaks rather than averaging over them:
   - 2012: the switch from PNAD to PNAD Contínua
   - 2015–16: recession
   - 2020: Auxílio Emergencial
   - 2021: benefit cut
   - 2023: Bolsa Família relaunch
4. Run a Datt-Ravallion decomposition for each survey spell, splitting the change in poverty into a growth part (mean income) and a redistribution part (shape of the distribution). If the post-2003 drop is mostly growth, the CCT story weakens. If it's mostly redistribution, the transfer is a candidate cause, but so is the minimum wage.
5. Check against a growth-elasticity benchmark. The percentage drop in headcount should speed up as the poverty line moves into the thinner part of the distribution, even with growth that doesn't change the distribution's shape. Compare the actual acceleration to that benchmark.

Done when there are updated figures, a decomposition table, and a `LOG.md` entry comparing results with the M0 predictions.

Reading:

- Datt & Ravallion (1992), "Growth and redistribution components of changes in poverty measures," *Journal of Development Economics* 38(2). Its worked examples include Brazil. [Link](https://ideas.repec.org/a/eee/deveco/v38y1992i2p275-295.html)
- Bourguignon (2003), "The growth elasticity of poverty reduction." Explains why percentage poverty declines speed up mechanically. [Link](https://ideas.repec.org/p/del/abcdef/2002-03.html)
- World Bank, June 2025 update to the global poverty lines. Explains why the numbers differ from 2012's. [Link](https://www.worldbank.org/en/news/factsheet/2025/06/05/june-2025-update-to-global-poverty-lines)
- PIP data and API docs. [Link](https://pip.worldbank.org)

---

## M4. Mechanical vs structural effects (microdata)

**Why:** this tests the actual hypothesis. The thesis tried to infer human capital effects from the shape of an aggregate curve. Microdata let you subtract the transfer directly and follow exposed cohorts.

Tasks:

1. Get PNAD (2001–2015) and PNAD Contínua (2012 onward) microdata. Base dos Dados hosts cleaned versions on BigQuery, which is free within quota. Check which waves include transfer-income variables; PNAD identifies Bolsa Família income only indirectly, so this needs care.
2. Validate first. Reproduce the Souza et al. (2019) result (about −15% poverty, −25% extreme poverty from Bolsa Família) for one or two years before trusting the pipeline.
3. Extend that "poverty with and without transfers" series to the latest year. This gives the size of the mechanical channel over time.
4. Cohort analysis, following Parker & Vogl's design:
   - Compare adults born just early enough to have been exposed to Bolsa Família as school-age children with slightly older cohorts who aged out.
   - Outcomes: schooling, formal employment, labor income, and **pre-transfer** poverty.
   - Exposure varies by birth year and by state-level rollout speed.
5. Robustness: confirm results hold across cohort window widths and poverty lines, and check that the cohorts didn't already differ before the program.

Done when there's a mechanical-effect series and a cohort estimate, with confidence intervals and the M2 power context.

Reading:

- Parker & Vogl (2023), "Do Conditional Cash Transfers Improve Economic Outcomes in the Next Generation? Evidence from Mexico," *Economic Journal* 133(655). The template for this milestone. [NBER version](https://www.nber.org/papers/w24303)
- Molina Millán, Barham, Macours, Maluccio & Stampini (2019), "Long-term impacts of conditional cash transfers: review of the evidence," *World Bank Research Observer*. The state of the field: schooling gains are consistent, while earnings effects are unclear and often measured too early. [IDB working paper version](https://publications.iadb.org/bitstream/handle/11319/7891/Long-term-Impacts-of-Conditional-Cash-Transfers-in-Latin-America-Review-of-the-Evidence.pdf)
- Base dos Dados (Brazilian public data on BigQuery). [Link](https://basedosdados.org)

---

## M5. Within-Brazil municipal dose-response

**Why:** about 5,570 municipalities with different program coverage give far more statistical power than one national series. The 2022 Census is the first one late enough to capture children who grew up in the program.

Tasks:

1. Build the panel:
   - Municipal poverty from Census 2000, 2010 and 2022. Atlas do Desenvolvimento Humano has 2000 and 2010 already computed. Check how much of the 2022 microdata IBGE has released.
   - Bolsa Família coverage by municipality and year from MDS / Portal da Transparência.
   - Controls: 2000 income, schooling, urbanization, region.
2. Define treatment intensity: average 2004–2010 coverage relative to the estimated number of poor families.
3. Draw the confounding problem as a causal diagram before any regression. Coverage was targeted at poor places, and poor places tend to catch up regardless (mean reversion), so a naive regression will overstate the effect.
4. Look for variation in coverage that isn't driven by need. One idea, unverified: the federal government allocated municipal quotas from poverty estimates, and errors in those estimates could provide that variation.
5. Estimate 2000→2010 (mostly mechanical) and 2010→2022 (more structural) separately. Run a placebo using pre-program changes (1991→2000) as the outcome.

Done when there's a dose-response estimate with a placebo that passes.

Reading:

- Atlas do Desenvolvimento Humano no Brasil (municipal indicators, 1991/2000/2010). [Link](https://www.atlasbrasil.org.br)
- IPUMS International (harmonized census microdata, includes Brazil). [Link](https://international.ipums.org)
- Cameron & Miller (2015), "A Practitioner's Guide to Cluster-Robust Inference." Read before choosing standard errors. [Link](https://jhr.uwpress.org/content/50/2/317)

---

## M6. Cross-country and natural experiments (optional)

**Why:** external validity. Do only the parts M2 says are detectable.

Tasks:

1. Build a country-year panel: PIP poverty, a hand-coded CCT adoption year for each country with sources, and program size from the World Bank ASPIRE database (coverage and spending as % of GDP).
2. Staggered-adoption DiD using Callaway & Sant'Anna or Sun & Abraham, comparing against countries not yet treated. Plot the event study and check parallel trends with HonestDiD.
3. Synthetic control for Brazil and Mexico with a worldwide set of comparison countries.
4. Mexico's 2019 Prospera removal as a natural experiment. Did poverty or schooling outcomes reverse in former beneficiary areas? Data: ENIGH (biennial) and CONEVAL. The hard part is COVID in 2020. I found enrollment-effect work (Parker et al.) but no published poverty-rate estimate, so this may be the most original piece in the plan.
5. Brazil 2020–21 as a test of the mechanical channel: the size of Auxílio Emergencial, then its cut. Press and FGV reports show extreme poverty hitting a record low in 2020 and rebounding in 2021; quantify this with PNADC.

Reading:

- Roth, Sant'Anna, Bilinski & Poe (2023), "What's Trending in Difference-in-Differences?" *Journal of Econometrics*. The best single survey; read it before any staggered DiD. [Link](https://arxiv.org/abs/2201.01194)
- Callaway & Sant'Anna (2021), "Difference-in-Differences with Multiple Time Periods." [Link](https://doi.org/10.1016/j.jeconom.2020.12.001)
- Goodman-Bacon (2021), "Difference-in-differences with variation in treatment timing." Why the old pooled two-way fixed effects approach misleads. [Link](https://doi.org/10.1016/j.jeconom.2021.03.014)
- Abadie (2021), "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects," *JEL*. [Link](https://doi.org/10.1257/jel.20191450)
- Bertrand, Duflo & Mullainathan (2004), "How Much Should We Trust Differences-in-Differences Estimates?" On serial correlation and overly small standard errors. [Link](https://www.nber.org/papers/w8841)
- Rambachan & Roth (2023), "A More Credible Approach to Parallel Trends." [Link](https://doi.org/10.1093/restud/rdad018)
- Baird, McIntosh & Özler (2011), "Cash or Condition? Evidence from a Cash Transfer Experiment," *QJE*. Directly asks whether the condition matters, versus the cash. [Link](https://doi.org/10.1093/qje/qjr032)

---

## M7. Write-up

Tasks: a 10–15 page paper or a long blog post, a replication package (`make all` rebuilds everything from raw data), and a section comparing the M0 predictions with the results.

Done when someone else can clone the repo and reproduce every figure.

---

## Open decisions

1. **Language.** The plan assumes Python with `pyfixest`, falling back to R only for `did` and `HonestDiD`. Switch to all-R if you'd rather; R's econometrics tooling is still slightly ahead.
2. **Time budget.** Not set. At about 5 hours a week, M0–M3 is roughly 2–3 months, and M4–M5 is another 3–6 months.
3. **Microdata appetite.** M4 and M5 are where the answer is, but they mean real data engineering (PNAD weights, the 2012 survey break, municipal code crosswalks). If that's not appealing, stop after M3 plus M6.4 (Prospera).
