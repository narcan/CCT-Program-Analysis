"""M4 step 2: build compact parquet files for each PNAD year.

Downloads one year at a time, keeps only the needed columns, deletes the
raw zip and text. Run: python analysis/m4_02_build_pnad.py [years...]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import pnad  # noqa: E402

years = [int(a) for a in sys.argv[1:]] or sorted(pnad.PNAD_URLS)
for y in years:
    pp = pnad.CLEAN / f"pnad{y}_pes.parquet"
    if pp.exists():
        print(y, "exists")
        continue
    p, d = pnad.pnad_to_parquet(y)
    print(y, p.stat().st_size // 1024, "KB", d.stat().st_size // 1024, "KB", flush=True)
