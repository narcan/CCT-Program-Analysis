"""Thin client for the World Bank Poverty and Inequality Platform (PIP) API
and the WDI API, with raw-response caching.

Every response is written verbatim (as returned) to a JSON file under
``data/raw/pip/<pull_date>/`` together with the request URL and pull
timestamp. Analysis code reads those files, never the network, so a
rebuild uses exactly the pulled data.

API notes (checked against release 20260922):
- ``/pip/v1/versions`` lists data versions as
  ``<release>_<ppp round>_<...>_PROD``. ``/pip/v1/info`` does not exist
  (404), so the version list is the record of release and PPP round.
- ``/pip/v1/pip`` rounds ``povline`` to 2 decimals and returns headcount
  and poverty gap rounded to 4 decimals. Counterfactual queries inherit
  that rounding.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode

import requests

PIP_BASE = "https://api.worldbank.org/pip/v1"
WDI_BASE = "https://api.worldbank.org/v2"
REPO = Path(__file__).resolve().parents[2]
RAW_DIR = REPO / "data" / "raw" / "pip"

_session = requests.Session()


def _get(url: str, params: dict) -> tuple[str, object]:
    full = f"{url}?{urlencode(params)}"
    r = _session.get(url, params=params, timeout=120)
    r.raise_for_status()
    return full, r.json()


def save_raw(name: str, url: str, payload: object, pull_dir: Path) -> Path:
    pull_dir.mkdir(parents=True, exist_ok=True)
    out = pull_dir / f"{name}.json"
    rec = {
        "request_url": url,
        "pulled_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "response": payload,
    }
    out.write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    return out


def load_raw(path: Path) -> dict:
    return json.loads(Path(path).read_text())


def versions() -> tuple[str, list]:
    return _get(f"{PIP_BASE}/versions", {})


def latest_version(vers: list, ppp: str = "2021") -> dict:
    cands = [v for v in vers if v["ppp_version"] == ppp and v["identity"] == "PROD"]
    return max(cands, key=lambda v: v["release_version"])


def pip_query(country: str, year, version: str, povline: float | None = None,
              popshare: float | None = None, fill_gaps: bool = False) -> tuple[str, list]:
    params = {"country": country, "year": year, "version": version,
              "format": "json", "fill_gaps": str(fill_gaps).lower()}
    if povline is not None:
        params["povline"] = f"{povline:.2f}"
    if popshare is not None:
        params["popshare"] = popshare
    return _get(f"{PIP_BASE}/pip", params)


def wdi_query(country: str, indicator: str) -> tuple[str, list]:
    return _get(f"{WDI_BASE}/country/{country}/indicator/{indicator}",
                {"format": "json", "per_page": 200})


def cf_name(year: int, povline: float) -> str:
    """File stem for a single counterfactual PIP query."""
    return f"cf_{year}_{povline:.2f}".replace(".", "p")


def latest_pull_dir() -> Path:
    dirs = sorted(p for p in RAW_DIR.iterdir() if p.is_dir())
    if not dirs:
        raise FileNotFoundError("No PIP pulls found; run analysis/m3_pull.py")
    return dirs[-1]


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
