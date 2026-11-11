# M4 variables: where Bolsa Familia income lives in the IBGE surveys

Source: the official IBGE SAS input programs and dictionaries shipped with
each microdata release (see `data/raw/MANIFEST_M4.md`). Variable names and
positions are read from those files by `src/cct/pnad.py` and
`src/cct/pnadc.py`; nothing is hard-coded by position.

## PNAD annual, 2001-2015 (person file PES, household file DOM)

| Variable | File | Meaning | Years |
|---|---|---|---|
| V1272 / V1273 | PES | Received / value of "juros de caderneta de poupanca e de outras aplicacoes, dividendos e outros rendimentos" in the reference month (September). The catch-all that holds Bolsa Familia, its predecessors, BPC and also true interest and dividends. | 2001-2015, same name every year |
| V4721 | PES | Monthly household income, all sources, all members | 2001-2015 |
| V4742 | PES | Monthly household per-capita income (IBGE) | 2004-2015 in the reweighted files (absent 2001-2003); used only as a cross-check |
| V0401 | PES | Condition in household. 1-5 are counted as members; 6 pensioner, 7 domestic worker, 8 relative of domestic worker are excluded from per-capita income, as IBGE does | 2001-2015 |
| V4729 | PES | Person weight | 2001-2015 |
| V0102 + V0103 | both | Household identifier (control number + serial number) | 2001-2015 |

Household per-capita income used here: V4721 divided by the number of
members (V0401 in 1-5). Households with undeclared income (V4721 missing or
coded 999999999999) are dropped. BF income is never separately reported, so
it is identified inside V1273 (see `src/cct/mechanical.py`).

### Supplements with direct questions on programme receipt

| Year | Variables (household file) | Content |
|---|---|---|
| 2004 | V2003 auxilio-gas, V2005 Bolsa Familia, V0620 Fome Zero / Cartao Alimentacao, V2007 Bolsa Alimentacao, V2012 Bolsa Escola, V2014 PETI, V1600 other programme | "Recebeu dinheiro do ..." in the reference period. Codes: yes = 1 for V2003, V2005, V2007; yes = 2 for V0620, V2012, V2014, V1600 |
| 2006 | V2403 Bolsa Familia (yes = 1, no = 3), V2404-V2406 BPC, V2407 PETI, V2409 other programme | "Algum morador recebeu dinheiro do ..." |
| 2014 | V33001-V33004 only | Whether anyone has heard of / tried / was interviewed for the Cadastro Unico. **No receipt question and no value.** |
| 2015 | none | No supplement on transfers |

The 2004 and 2006 supplements give receipt (yes/no) but not the amount, so
they validate the identification rule but cannot replace it.

## PNAD Continua, annual visit files

Income from sources other than work is collected once a year: in the 1st
visit (2012-2019, 2022 onward) and in the 5th visit (2016 onward; the only
annual file for 2020 and 2021).

| Variable | Meaning | Availability |
|---|---|---|
| V5010 / V50101 / V501011 | "Alguma pessoa do domicilio recebeu BF ou PETI" / this person received / value. Bolsa Familia shares the item with PETI (PETI cash was folded into BF in 2006, so PETI-only amounts are rare). | Old questionnaire: visit 1, 2012 to Q3 2015 |
| V5011 / V50111 / V501111 | "Outro programa social" (other programmes, not BF) | Old questionnaire: visit 1, 2012 to Q3 2015 |
| V5002A / V5002A2 | "Recebeu Bolsa Familia" / value received | New questionnaire, **first available Q4 2015** (full year from 2016) |
| V5001A / V5001A2 | BPC-LOAS receipt / value | Q4 2015 on |
| V5003A / V5003A2 | Other social programme receipt / value | Q4 2015 on |
| VD5008 | Habitual household per-capita income (habitual work income plus effective other income; excludes pensioners, domestic workers and their relatives) | all years |
| VD5002 | Effective household per-capita income | all years |
| V2005 | Condition in household (17-19 excluded from per-capita income) | all years |
| V1032 | Person weight (calibrated) | all years |
| UPA + V1008 + V1014 | Household identifier | all years |

Deflators: `deflator_PNADC_2025.xls` (IBGE), CO1 (habitual) and CO1e
(effective) bring income to average prices of the survey year.

Caveats on the BF item after 2019: the item keeps the label "Bolsa Familia"
in the dictionaries, but the programme was replaced by Auxilio Brasil from
November 2021 to February 2023, and in 2020-2021 most beneficiaries were
moved to the Auxilio Emergencial, which is not in V5002A2. Series for
2020-2022 are therefore not comparable with the rest.

## Implication for the 2012-2015 overlap

PNAD has no BF item (catch-all V1273 plus imputation). PNAD Continua has a
direct item in every year: "BF ou PETI" (V501011) until Q3 2015 and
"Bolsa Familia" (V5002A2) from Q4 2015. The overlap therefore compares an
imputed PNAD measure with a directly reported PNADC measure. (An earlier
draft of this note missed V5010 because its label abbreviates Bolsa
Familia as "BF".)
