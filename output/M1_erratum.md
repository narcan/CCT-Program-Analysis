# M1 erratum: what changed in the 2012 thesis, and what survives

November 2026. Built by `python analysis/m1_replicate.py`; full tables in `output/M1/m1_summary.md`. This page adds to `ERRATA.md`.

## Reproduction

Tables 4, 5 and 6 reproduce exactly from the archived data (every printed coefficient, t statistic and N). Table 5 only matches with ordinary standard errors, even though its title says "Robust". Table 1 does not reproduce; its FGT1 rate-of-change row (mean -0.64) cannot be correct.

## What changed

1. **Labels.** The three "CCT stage" terms in Table 6 are cumulative steps that switch on in 2004, 2006 and 2008. They are not "before" and "after" phases. Read correctly, Brazil's headcount fell faster after 2003 than before. The extra fall in the annual rate of change reaches 11 points by 2008-09.
2. **Real surveys only.** Without the five interpolated years (1991, 1994, 2000, 2006, 2007), only four post-2003 observations remain: 2004, 2005, 2008 and 2009. The 2006 and 2008 steps can no longer be told apart. With survey years and annualized change between surveys, the single post-2003 dummy shrinks to -0.052 (p = 0.16) with the thesis's controls.
3. **Gini.** Dropping Gini change, which is probably a channel rather than a confounder, makes post-2003 terms larger: the single dummy becomes -0.077 (p = 0.043).
4. **Adoption dates.** Colombia (2001), Costa Rica (2006), the Dominican Republic (2005) and Paraguay (2005) all ran conditional transfers. Sources are in `output/M1/cct_adoption_recode.csv`. Ecuador's Bono de Desarrollo Humano (2003) had conditions on paper that were never enforced, so both codings are run. After recoding, the thesis's "Latin America without CCT" group is just Venezuela, or Venezuela and Ecuador. A CCT versus non-CCT comparison is no longer possible.
5. **Cross-country test.** In a pooled Latin American model with country fixed effects, a GDP control and wild cluster bootstrap p-values (14 countries), the post-adoption shift in the survey-year headcount change is -0.03 to -0.05 with p = 0.24 to 0.46 under either recoding. That is no evidence of a CCT effect. Under the thesis's own coding and interpolated data it was borderline (p of about 0.05 to 0.07).

## What survives

- GDP growth is strongly linked to faster poverty decline in Brazil (coefficient about -1.6, p = 0.003, survey years only).
- Net of GDP and Gini, Brazil's headcount fell unusually fast in the 2005-2008 and 2008-2009 intervals: about 9 points per year faster than the pre-2004 average (p < 0.001, also with small-sample HC3 errors). This rests on two observations. Still, of the 22 possible pairs of consecutive surveys, it is the most extreme. It is a real pattern in the data. Nothing here ties it to Bolsa Família rather than the minimum wage, pensions, the commodity boom, or anything else that changed in Brazil at the time.

## Verdicts on the pre-registered hypotheses

- **H1.1 ("after the fixes, no post-2003 coefficient is significant at 5%"): refuted.** The cumulative 2008-09 shift is significant in all four survey-year variants (FGT0 and FGT1, with and without Gini). The single post-2003 dummy is not significant with the thesis's controls (p = 0.16), but it is without Gini (p = 0.043).
- **H1.2 ("2003 does not rank in the top 3 of placebo break years"): refuted.** In the primary test (headcount, survey years, GDP and Gini controls) 2003 ranks 2nd of 14 break years by t statistic (t = -1.45; 1997 ranks 1st). It ranks in the top 3 in all eight variants. But the 2003 break is not itself significant in the primary test.

## Bottom line

The thesis's labels, standard errors, sample rules and country coding were wrong. Once they are fixed, there is still a post-2003 speed-up in Brazilian poverty decline beyond what GDP explains. It is concentrated in 2005-2009 and stands out against placebo breaks. There is no cross-country evidence that CCT adoption caused faster poverty decline, and the design cannot attribute Brazil's speed-up to Bolsa Família. The thesis's claims about long-term CCT effects remain unsupported.
