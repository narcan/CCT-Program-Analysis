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
