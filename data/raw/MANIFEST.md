# Raw data manifest

Every file in `data/raw/` is a download saved exactly as pulled. Never edit a raw file by hand.
Raw files are gitignored; this manifest is the committed record of what was pulled, when, and from where.
Milestone-specific manifests (`MANIFEST_M3.md`, ...) follow the same format.

| File (path under data/raw/) | Source / URL or API call | Release / version (e.g. PIP PPP round, data version) | Pull date (YYYY-MM-DD) | SHA-256 | Pulled by (script) | Notes |
|---|---|---|---|---|---|---|
| _example_: `pip/brazil_2.15.csv` | `https://api.worldbank.org/pip/v1/pip?country=BRA&povline=2.15` | PPP 2017, data version 20240627_2017_01_02_PROD | 2026-11-10 | `abc123...` | `src/cct/pip.py` | template row, delete when the first real file is added |

M1 uses only the archived 2012 dataset `Data/ThesisDataCSV.csv`, which is committed in the repository and needs no download.
