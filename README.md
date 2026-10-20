# CCT-Program-Analysis

Code, data and text for my 2012 Columbia master's thesis, "An Analysis of CCT Programs and Poverty". The thesis uses World Bank poverty data and time-series regressions to ask whether Brazil's Bolsa Família and other conditional cash transfer (CCT) programs are associated with faster declines in poverty. The thesis is archived at the [Columbia Academic Commons](https://academiccommons.columbia.edu/doi/10.7916/D80Z79FW).

> **The 2012 conclusions are under revision.** A 2026 re-review found errors in how the main results were labeled, interpreted and summarized. See [ERRATA.md](ERRATA.md) for what is wrong and what still holds, and [RESEARCH_PLAN.md](RESEARCH_PLAN.md) for the follow-up work. The thesis files themselves are kept as originally submitted.

## Repository layout

- `Thesis - Avila (2012) - An Analysis of CCT Programs and Poverty.pdf`: the thesis as submitted
- `Thesis v6-FINAL.docx`: Word source of the thesis
- `Data/`: dataset (`ThesisDataCSV.csv`, `.dta`, `.xlsx`) and the original Stata code (`ThesisDataCoding.do` builds the variables, `ThesisDataAnalysis.do` runs the models)
- `Graphs/`, `Images/`: figures produced for the thesis
- `ThesisInR/`: early R exploration
- `analysis/`: 2026 Python replication (`replicate_2012.py`, `requirements.txt`)
- `ERRATA.md`: known errors in the thesis
- `RESEARCH_PLAN.md`: plan for revisiting the question

## Running the replication

From the repository root, with Python 3:

```
pip install -r analysis/requirements.txt
python analysis/replicate_2012.py
```

The script rebuilds the thesis variables from `Data/ThesisDataCSV.csv`, reproduces Table 6, and prints the checks referenced in `ERRATA.md`.
