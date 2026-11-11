"""M2 step 0: download raw inputs and save them with the pull date.

Sources (all public, no key):
  - World Bank PIP API, Brazil headcount at $3.00/day (2021 PPP), pinned release.
  - World Bank WDI API: GDP per capita growth (NY.GDP.PCAP.KD.ZG) and
    population by 5-year age group and sex (SP.POP.AAAA.{MA,FE}.5Y).
Raw JSON is written to output/M2/raw/ and never edited by hand.
Run: python analysis/m2_data.py   (skips files that already exist; --force to refetch)
"""
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "output" / "M2" / "raw"
PIP_VERSION = "20260922_2021_01_02_PROD"
AGE_GROUPS = ["0004", "0509", "1014", "1519", "2024", "2529", "3034", "3539",
              "4044", "4549", "5054", "5559", "6064", "6569", "7074", "7579", "80UP"]


def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def save(name, url, force):
    path = RAW / name
    if path.exists() and not force:
        return
    data = fetch(url)
    path.write_text(json.dumps({"url": url, "pulled": dt.date.today().isoformat(), "data": data}))
    print("saved", path.name)


def main(force=False):
    RAW.mkdir(parents=True, exist_ok=True)
    save("pip_bra_3usd.json",
         f"https://api.worldbank.org/pip/v1/pip?country=BRA&povline=3&version={PIP_VERSION}&format=json", force)
    wdi = "https://api.worldbank.org/v2/country/BRA/indicator/{}?format=json&per_page=200&date=1960:2025"
    save("wdi_gdppc_growth.json", wdi.format("NY.GDP.PCAP.KD.ZG"), force)
    # The 5-year age indicators are percent of the male/female population,
    # so the sex totals are needed to turn them into counts.
    save("wdi_pop_total_MA.json", wdi.format("SP.POP.TOTL.MA.IN"), force)
    save("wdi_pop_total_FE.json", wdi.format("SP.POP.TOTL.FE.IN"), force)
    for g in AGE_GROUPS:
        for s in ("MA", "FE"):
            ind = f"SP.POP.{g}.{s}.5Y"
            save(f"wdi_pop_{g}_{s}.json", wdi.format(ind), force)


def wdi_series(name):
    """Return {year: value} from a saved WDI file."""
    obj = json.loads((RAW / name).read_text())
    rows = obj["data"][1] or []
    return {int(r["date"]): r["value"] for r in rows if r["value"] is not None}


def pop_by_group():
    """Population counts by 5-year age group (both sexes): {group: {year: count}}."""
    out = {}
    tot = {s: wdi_series(f"wdi_pop_total_{s}.json") for s in ("MA", "FE")}
    for g in AGE_GROUPS:
        out[g] = {}
        for s in ("MA", "FE"):
            pct = wdi_series(f"wdi_pop_{g}_{s}.json")
            for y, v in pct.items():
                if y in tot[s]:
                    out[g][y] = out[g].get(y, 0.0) + v / 100.0 * tot[s][y]
    return out


def pip_rows():
    return json.loads((RAW / "pip_bra_3usd.json").read_text())["data"]


if __name__ == "__main__":
    main(force="--force" in sys.argv)
