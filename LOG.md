# Project log

Dated entries, newest last. Each milestone opens with a prediction entry and closes with a go / pivot / stop gate note,
judged against the kill criteria in `RESEARCH_PLAN.md`.

## Owner predictions

TBD

## 2026-11-10: M1 opened

M1 opened; hypotheses H1.1 and H1.2 as committed in RESEARCH_PLAN.md (git 84dedda).

- H1.1: after fixes 2-4 (spline labels, Table 1, survey-year outcomes only), no post-2003 coefficient is significant at 5%.
- H1.2: 2003 does not rank in the top 3 of the placebo break years (1990-2002) by t-statistic.

## 2026-11-10: M0 setup (tasks 1-3)

Layout, `.gitignore`, pinned `pyproject.toml`, and `src/cct/clean_2012.py` (port of `ThesisDataCoding.do`).
`tests/test_clean_2012.py` checks the port against the interpolated columns of `Data/ThesisDataCSV.csv`.
Every cell matches except a documented list in which the archive's raw columns were edited after interpolation:
the Kenya 2004-2010 row block (corrupted), Ukraine 1989-1995 poverty, Brazil and Mexico population revisions, and a few rounded consumption values.
None of these is a Brazil regression input. The CSV interpolates through raw poverty values of 0 (Chile 2009, Kyrgyz 1988) and then sets those cells to missing.
The port reproduces this, and it is needed to get the published Table 5 N of 189.

## 2026-11-10: M1 results and gate

- Tables 4, 5 and 6 reproduced to every printed digit (Table 5 with classical SEs, as coded).
- H1.1 **refuted**. With survey years only, the cumulative 2008-09 shift is significant in all four variants (FGT0 with Gini: -0.088, p < 0.001 HC1, p = 0.0004 HC3).
  The single post-2003 dummy is -0.052 (p = 0.16) with Gini and -0.077 (p = 0.043) without it.
- H1.2 **refuted**. 2003 ranks 2nd of 14 break years by t in the primary variant (t = -1.45, p = 0.16), and in the top 3 in all eight variants.
- Exploratory: in a two-observation placebo, the 2008-09 pair is the most extreme of 22 consecutive-survey pairs.
- The CCT recode leaves at most two never-CCT Latin American countries. With country FE and wild cluster bootstrap, the pooled post-adoption effect on survey-year headcount change is -0.03 to -0.05, p = 0.24 to 0.46.
- Adoption dates were sourced by web search. The ECLAC database host could not be reached from this environment, so ECLAC dates come from search-engine copies of the records.
  Ecuador's classification is contested (conditions not enforced), so both codings are reported.
- Gate: **go** (M1 has no kill criterion). The post-2003 Brazil pattern is real but rests on two to four observations, which is the question M2 (power) and M3 (refresh with real survey years) take up.

## 2026-11-10: M0 literature gate

- Laguinge, Gasparini & Neidhöfer read from abstracts and summaries only (full text blocked here); see `notes/laguinge_2025.md`.
- They use PNAD only, with no Census 2022 or linked records; exposure is predicted participation x a born-1985+ cutoff. Kill criterion **not met**: M5 stays an extension, not a replication. Confirm against the PDF before writing `pap/M5.md`.
- Competitor for M6: Britto et al., WIDER WP 2025/96 (CadÚnico x RAIS, place effects).

## 2026-11-10: M2 gate

- H2.1 **confirmed**. Size-adjusted power on PIP $3.00 survey years 1995-2024: mechanical 15% effect 91%; long-run effect at the top plausible size 10% (central exposure) to 16% (generous). Significant results overstate the effect 2-3x.
- Kill criterion **met**: stop national time-series work on the long-run effect. Cross-country items stay parked. See `output/M2/M2_gate.md`.

## 2026-11-10: M3 gate

- The post-2003 acceleration survives on survey years: -2.7%/yr (1995-2002), -11.0%/yr (2003-2011), -14.6%/yr (2012-2014).
- Datt-Ravallion at $3.00, 2003-2011: 10.0 points total, 5.6 growth, 4.4 redistribution. Log-normal benchmark predicts 5.4%/yr vs 11.0% actual.
- H3.1 **not supported so far**: growth explains about half; the transfer would need to cover most of the 4.4 redistribution points, and M4 suggests roughly 2. See `output/M3/M3_summary.md`.

## 2026-11-10: M4 gate

- Pipeline reproduces Souza et al. (2019) for 2017 only with effective income (gaps +1.0 / -0.3 points); habitual income fails on extreme poverty (+4.3). Kill criterion **passes conditionally**: read TD 2499 to confirm their income concept before M5.
- H4.1: 2015 part **refuted** (extreme-poverty cut 34-38%, above the 20-30% band); post-2023 part **supported** (about 72-74%).
- Surveys capture about 70-85% of program spending. See `output/M4/M4_summary.md`.

## 2026-11-11: M4 correction

- Primary specification changed to the TD 2499 method: PNAD uses the household rule `souza2019` (BPC removed, household sum of other income within the family's legal benefit bounds); PNAD Continua uses effective income (VD5002); lines at June 2018 prices. The old person-level rule (tv/tvb) and habitual income are kept as labelled sensitivities. Series, overlap and survey-vs-spending tables regenerated.
- Kill criterion **passes**: all 9 printed Souza et al. years within 1.4 points (extreme) and 1.3 (poverty); the old specification fails 6 of 9. The rule was chosen after seeing the mismatch, so this is a pipeline fix, not an independent result.
- New cuts in extreme poverty: 33% (PNAD) / 34% (PNADC) in 2015; 26% in 2017; 71% in 2025.
- H4.1: 2015 part still **refuted** (33-34%, above the 20-30% band, as is Souza et al.'s own 31.7%); post-2023 part **supported** (71-72%). See `output/M4/M4_summary.md`.
