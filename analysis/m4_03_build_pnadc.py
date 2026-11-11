"""M4: build compact parquet files for PNAD Continua annual-visit data.

Visit 1 for 2012-2019 and 2022 on; visit 5 for 2020-2021 (pandemic years,
no visit-1 file). One year at a time; raw zip and text are deleted.
Run: python analysis/m4_03_build_pnadc.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import pnadc  # noqa: E402

PLAN = [(y, 1) for y in range(2012, 2020)] + [(2020, 5), (2021, 5)] + \
       [(y, 1) for y in range(2022, 2026)]

if __name__ == "__main__":
    for y, v in PLAN:
        p = pnadc.pnadc_to_parquet(y, v)
        print(y, v, p.stat().st_size // 1024, "KB", flush=True)
