# Errata: "An Analysis of CCT Programs and Poverty" (2012)

October 2026

The thesis PDF and Word file in this repository are kept exactly as submitted to Columbia in 2012. In a 2026 re-review I re-ran the original Stata code and data in Python and checked the text against them. This file lists the errors I found and confirmed. Each item says what the thesis says, what is correct, how it changes the conclusions, and how to reproduce the check.

All checks are in `analysis/replicate_2012.py`. Run it from the repository root:

```
pip install -r analysis/requirements.txt
python analysis/replicate_2012.py
```

The script reproduces Table 6 to every reported digit (coefficients and t statistics), so the data file and the model code are the ones behind the published results. Section numbers below refer to the script's printed output.

## 1. Table 6: the CCT-stage coefficients are mislabeled and misread

**What the thesis says.** Table 6 reports three coefficients labeled "Before CCT Program", "Immediately After CCT Program" and "Intermediate Phases of CCT Program". The text (p. 46-47) reads the first one as the trend "over the course of the two decades preceding the implementation of the program", and footnote 41 says the model has three stages: before, Phase 1 (first two years) and Phase 2 (after two years).

**What is correct.** `Data/ThesisDataCoding.do` builds `cctstage` with four values: 0 up to 2003, 1 for years 1-2 after the start, 2 for years 3-4, 3 for year 5 on. `Data/ThesisDataAnalysis.do` then runs `mkspline before 1 phase1 2 phase2 = cctstage`. Because `cctstage` only takes the values 0 to 3, the three spline terms are step dummies:

| Thesis label | Actual variable | FGT0 | FGT1 |
|---|---|---|---|
| Before CCT Program | 1 from 2004 on (year 1+) | -0.0093 (p=0.87) | -0.0366 (p=0.73) |
| Immediately After CCT Program | 1 from 2006 on (year 3+), extra to the above | -0.0568 (p=0.30) | -0.0028 (p=0.98) |
| Intermediate Phases | 1 from 2008 on (year 5+), extra to the above | -0.0415 (p=0.20) | -0.0796 (p=0.015) |

The pre-2003 baseline is the intercept, not the "Before" coefficient. The "Before" coefficient is the shift in 2004-2005. Each later coefficient is an additional shift on top of the earlier ones, so the effect in a given period is the sum. Read that way, the cumulative shift in the rate of change of FGT0 is -0.009 in 2004-05 (p=0.87), -0.066 in 2006-07 (p=0.012) and -0.108 in 2008-09 (p=0.001). For FGT1 it is -0.037, -0.039 and -0.119 (p<0.001).

A simpler model with one post-2003 dummy, plus the same GDP and Gini controls, gives -0.064 for FGT0 (p=0.036) and -0.069 for FGT1 (p=0.125).

**Impact.** The narrative on p. 47 ("dropped steadily by a statistically insignificant -.0093 over the course of the two decades preceding", "falls by more than six times to -.0568", "increased from -.0366 to -.00281") is wrong and should be disregarded. Equation 1 has the same labeling problem. The corrected reading shows a larger and more significant post-2003 drop in Brazil than the thesis reported, but see items 2 and 3 for why that drop cannot be attributed to Bolsa Família.

**Reproduce.** Script sections 2 and 3.

## 2. The Brazil data end in 2009, and several years are interpolated

**What the thesis says.** The analysis covers "1980 to 2011" (p. 10, p. 29 and p. 46), and the splines run "from 2005 to 2011" (p. 37).

**What is correct.** Brazil's poverty series (FGT0 and FGT1 at $2/day PPP) runs from 1981 to 2009. There are no poverty values for 1980, 2010 or 2011. The years 1991, 1994, 2000, 2006 and 2007 are linear interpolations, not surveys (`ipolate` in `ThesisDataCoding.do`). The regression sample is 1982-2009, N = 28.

After 2003 there are only four real surveys: 2004, 2005, 2008 and 2009. The "Intermediate Phases" dummy, the only CCT term the thesis reports as significant, is switched on by 2008 and 2009 alone. Its p-value is 0.015 with Stata's t distribution, consistent with the single star in Table 6. The "Immediately After" dummy is switched on by 2006 and 2007, which are interpolated, and the 2008 rate of change is computed from an interpolated 2007 value.

**Impact.** The post-2003 estimates rest on two to four data points per period. The 2006-07 estimates in particular describe a straight line drawn between 2005 and 2008, not observed poverty.

**Reproduce.** Script sections 1 and 2.

## 3. The method is not difference-in-differences, and the outcome is not a log difference

**What the thesis says.** The Brazil model is described as a "difference-in-differences analysis" (p. 10, 35 and 46), and Tables 5 and 6 are titled "Log-Differences of Poverty".

**What is correct.** The Brazil regressions use Brazil only (`if country=="Brazil"`). There is no control unit, so the design is a single-country before/after comparison (an interrupted time series on first differences). The outcome is the simple percentage change, `(x_t - x_{t-1}) / x_{t-1}` (`ThesisDataCoding.do`), not a log difference. Table 6 reproduces exactly with the percentage change.

**Impact.** Without a comparison unit, the post-2003 shift in item 1 captures anything that changed in Brazil after 2003, not only Bolsa Família. The thesis's causal language should be read as a before/after association at most. The log-difference mislabel does not change any number.

**Reproduce.** Script section 2; see the `rate_of_change` function.

## 4. Table 5 is labeled robust but uses classical standard errors

**What the thesis says.** Table 5 is titled "Naïve Robust OLS Regression". The text (p. 45) says there is a significant trend in Brazil and in CCT countries, "whereas the same cannot be said for countries without CCT programs".

**What is correct.** The Table 5 lines in `ThesisDataAnalysis.do` (`reg rcfgt0 year if ...`) have no `, robust` option. The published t statistics match classical standard errors exactly. With robust (HC1) standard errors:

| Group | FGT0 classical | FGT0 robust | FGT1 classical | FGT1 robust |
|---|---|---|---|---|
| Brazil | t=-2.06, p=0.049 | t=-1.80, p=0.084 | t=-1.75, p=0.092 | t=-1.63, p=0.115 |
| Latin America CCT | t=-5.66 | t=-5.13 | t=-4.62 | t=-4.60 |
| Latin America non-CCT | t=-1.74, p=0.085 | t=-1.99, p=0.049 | t=-1.86, p=0.065 | t=-2.37, p=0.019 |

**Impact.** With robust errors the Brazil trend is not significant and the non-CCT trend is. The contrast the text draws from Table 5 does not hold. The non-CCT group is also miscoded (item 6).

**Reproduce.** Script section 4.

## 5. Table 1 does not match the data

**What the thesis says.** Table 1 reports N = 31 for poverty levels and N = 30 for rates of change. For the rate of change in depth of poverty it reports mean -0.64, sd 0.06, min -0.81, max -0.51.

**What is correct.** From the archived data:

| Variable | Thesis N / mean / sd / min / max | Data N / mean / sd / min / max |
|---|---|---|
| FGT0 level | 31 / 23.37 / 6.99 / 9.87 / 36.08 | 29 / 23.91 / 6.53 / 9.87 / 36.08 |
| FGT1 level | 31 / 8.84 / 3.23 / 3.22 / 14.96 | 29 / 9.09 / 3.06 / 3.22 / 14.96 |
| FGT0 rate of change | 30 / -0.03 / 0.11 / -0.43 / 0.19 | 28 / -0.036 / 0.093 / -0.212 / 0.186 |
| FGT1 rate of change | 30 / -0.64 / 0.06 / -0.81 / -0.51 | 28 / -0.039 / 0.128 / -0.288 / 0.352 |

The published FGT1 row is impossible on its face: a fall of at least 51% every year for 28 years would take depth of poverty from 12.38 to nearly zero, but the data end at 3.22. No row reproduces exactly; the FGT0 rate-of-change row is close on the mean but not on the spread.

**Impact.** Descriptive only. The regressions do not use Table 1. But the text's description of the Brazilian data should be taken from the "Data" rows above.

**Reproduce.** Script section 5.

## 6. Several countries with CCT programs are coded as non-CCT

**What the thesis says.** The cross-country comparison (Table 5, Figures 15-21) splits countries by `eventualcct`. The text discusses Colombia's Familias en Acción as a CCT (p. 11 and p. 16).

**What is correct.** The dataset's own `program` column names a program for five Latin American and Caribbean countries that are coded `eventualcct = 0`:

| Country | Program in the `program` column | Listed from |
|---|---|---|
| Colombia | Familias en Acción | 2001 |
| Costa Rica | Avancemos | 2006 |
| Dominican Republic | Programa Solidaridad | 2005 |
| Ecuador | Bono de Desarrollo Humano | 2003 |
| Paraguay | Tekoporã | 2005 |

Colombia is a confirmed inconsistency: the thesis itself treats Familias en Acción as a CCT. For the other four, whether each program is a conditional transfer and when it reached national scale is **to verify** against an outside source. The six non-Latin American countries with a program listed and `eventualcct = 0` (Ethiopia, Kenya, Mozambique, South Africa, Sri Lanka, Tanzania) are also **to verify**; some of these may be unconditional transfers, in which case the coding is right. Separately, Brazil's `program` column lists Bolsa Escola from 1995, while the analysis dates the CCT from 2003; this choice of start year is **to verify**.

**Impact.** The "Latin America non-CCT" group in Table 5 and Figures 16-17 includes post-program years from countries that ran CCTs. Any CCT versus non-CCT contrast in the thesis is contaminated to an unknown degree.

**Reproduce.** Script section 6.

## 7. The stated sample rules were not applied

**What the thesis says.** Countries with fewer than five FGT0 or FGT1 observations, or fewer than three observations after the CCT start, "were dropped from the sample" (p. 30).

**What is correct.** No such filter exists in the code. Counting real (not interpolated) FGT0 surveys:

| Country | Total | After CCT start | Where it is used |
|---|---|---|---|
| Nicaragua | 4 | 2 | Own model block in the do-file; Latin America CCT group |
| Jamaica | 7 | 2 | Figure 14, discussed on p. 50-51 as supporting evidence |
| Peru | 9 | 2 | Latin America CCT group |
| El Salvador | 10 | 1 | Latin America CCT group |
| Panama | 10 | 1 | Latin America CCT group |

**Impact.** The Jamaica discussion rests on two post-program surveys (2002 and 2004). The pooled Latin America CCT group includes four countries that the stated rule would have dropped. Those results should be treated as anecdotal.

**Reproduce.** Script section 6.

## 8. The abstract contradicts the conclusion

**What the thesis says.** The abstract (and this repository's README until October 2026) says there is "little evidence that CCT programs promise to be as effective in combating poverty in the long term as many would like to believe". The conclusion chapter (p. 57) says the study "has provided more evidence that the long-term objectives of CCT programs are being met".

**What is correct.** These two statements point in opposite directions. Given items 1 to 7, neither is supported by the analysis. The analysis cannot speak to long-term effects: it has four post-2003 surveys for Brazil, the latest six years after the program started, and no control unit.

**Impact.** Neither the abstract's nor the conclusion's verdict on long-term effectiveness should be cited.

**Reproduce.** Compare the abstract with the last paragraph of the conclusion (p. 57) of the PDF.

## Bottom line

What survives is narrow. In Brazil, growth in GDP is strongly associated with faster falls in poverty (GDP coefficient about -1.7 for FGT0, p=0.001). Net of GDP and the Gini coefficient, Brazil's poverty rates fell faster after 2003 than before: with a single post-2003 dummy, the annual rate of change of the headcount ratio is about 6 percentage points lower after 2003 (p=0.036), and the shift reaches about 11 to 12 points in 2008-09. That is a real pattern in the data, and it is larger than the thesis reported. But it comes from one country, four post-2003 surveys, interpolated middle years and no comparison group, so it cannot be attributed to Bolsa Família rather than to anything else that changed in Brazil after 2003. The cross-country comparison is weakened by miscoded and under-sampled countries. The thesis does not support a conclusion either way on whether CCT programs reduce poverty in the long term. That question is being taken up again in [RESEARCH_PLAN.md](RESEARCH_PLAN.md).
