# Raw data manifest (M3)

## M3: PIP and WDI pulls for Brazil

- Pull directory: `data/raw/pip/2026-11-10/` (gitignored; rebuild with `python analysis/m3_pull.py`)
- Pull date: 2026-11-10
- PIP version: `20260922_2021_01_02_PROD` (release 20260922, PPP round 2021, PROD).
  Recorded from `/pip/v1/versions`; `/pip/v1/info` returns 404 in this release.
- Lines: $3.00, $4.20, $8.30 per person per day, 2021 PPP. Survey years only (`fill_gaps=false`).
- PIP rounds `povline` to 2 decimals and headcount/poverty gap to 4 decimals.
- WDI: `NY.GDP.PCAP.KD`, `NY.GDP.PCAP.PP.KD` (api.worldbank.org/v2).
- National line (Bolsa Familia extreme-poverty eligibility line, reais): NOT pulled.
  No primary source (planalto.gov.br, camara.leg.br, senado.leg.br, gov.br/mds) is reachable
  from this environment, and web-search snippets were incomplete and partly inconsistent
  (e.g. the 2016 adjustment is reported as both R$82 and R$85). Skipped until verified.

| file | sha256 (first 16) |
|---|---|
| `pip_BRA_all_3p00.json` | `2c982fc7dc98207c` |
| `pip_BRA_all_4p20.json` | `9b3b6b0fdb49760e` |
| `pip_BRA_all_8p30.json` | `10669f03eb5b4f7d` |
| `pip_versions.json` | `f5a856f62997a7f6` |
| `wdi_BRA_NY.GDP.PCAP.KD.json` | `3bc3a8cd634fd8f9` |
| `wdi_BRA_NY.GDP.PCAP.PP.KD.json` | `7a04e1c51e411520` |
| `cf_*.json` (275 counterfactual single-year queries) | see files |

