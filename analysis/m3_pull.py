"""M3 step 1: pull Brazil from PIP and WDI, save raw JSON with pull date.

Usage: python analysis/m3_pull.py
Writes data/raw/pip/<YYYY-MM-DD>/ and the M3 section of the raw-data
manifest. Stage 2 pulls the counterfactual headcounts needed by the
Datt-Ravallion decomposition (each survey year at a line scaled by the
ratio of survey means), so it depends on stage 1.
"""
from __future__ import annotations

import datetime as dt
import time

from m3_common import (COUNTRY, LINES, PPP_ROUND, REPO, WDI_INDICATORS, P,
                       main_name, spells, survey_table)


def fetch(fn, name, pull_dir, *args, **kw):
    path = pull_dir / f"{name}.json"
    if path.exists():
        return P.load_raw(path)["response"]
    for attempt in range(4):
        try:
            url, payload = fn(*args, **kw)
            break
        except Exception as e:  # network hiccup: back off and retry
            if attempt == 3:
                raise
            print("retry", name, e)
            time.sleep(2 ** attempt)
    P.save_raw(name, url, payload, pull_dir)
    return payload


def main():
    pull_dir = P.RAW_DIR / dt.date.today().isoformat()
    vers = fetch(P.versions, "pip_versions", pull_dir)
    v = P.latest_version(vers, PPP_ROUND)
    version = v["version"]
    print("PIP version", version)

    for z in LINES:
        fetch(P.pip_query, main_name(z), pull_dir, COUNTRY, "all", version, povline=z)
    for ind in WDI_INDICATORS:
        fetch(P.wdi_query, f"wdi_{COUNTRY}_{ind}", pull_dir, COUNTRY, ind)

    df = survey_table(pull_dir)
    mean = df[df["line"] == LINES[0]].set_index("year")["mean"]
    needed = set()
    for a, b, _ in spells(df):
        for z in LINES:
            needed.add((a, round(z * mean[a] / mean[b], 2)))
            needed.add((b, round(z * mean[b] / mean[a], 2)))
    print(len(needed), "counterfactual queries")
    for yr, zz in sorted(needed):
        fetch(P.pip_query, P.cf_name(yr, zz), pull_dir, COUNTRY, yr, version, povline=zz)

    write_manifest(pull_dir, v)


def write_manifest(pull_dir, v):
    files = sorted(pull_dir.glob("*.json"))
    main_files = [f for f in files if not f.name.startswith("cf_")]
    cf = [f for f in files if f.name.startswith("cf_")]
    lines = [
        "## M3: PIP and WDI pulls for Brazil",
        "",
        f"- Pull directory: `{pull_dir.relative_to(REPO)}/` (gitignored; rebuild with `python analysis/m3_pull.py`)",
        f"- Pull date: {pull_dir.name}",
        f"- PIP version: `{v['version']}` (release {v['release_version']}, PPP round {v['ppp_version']}, {v['identity']}).",
        "  Recorded from `/pip/v1/versions`; `/pip/v1/info` returns 404 in this release.",
        "- Lines: $3.00, $4.20, $8.30 per person per day, 2021 PPP. Survey years only (`fill_gaps=false`).",
        "- PIP rounds `povline` to 2 decimals and headcount/poverty gap to 4 decimals.",
        "- WDI: " + ", ".join(f"`{k}`" for k in WDI_INDICATORS) + " (api.worldbank.org/v2).",
        "- National line (Bolsa Familia extreme-poverty eligibility line, reais): NOT pulled.",
        "  No primary source (planalto.gov.br, camara.leg.br, senado.leg.br, gov.br/mds) is reachable",
        "  from this environment, and web-search snippets were incomplete and partly inconsistent",
        "  (e.g. the 2016 adjustment is reported as both R$82 and R$85). Skipped until verified.",
        "",
        "| file | sha256 (first 16) |",
        "|---|---|",
    ]
    lines += [f"| `{f.name}` | `{P.sha256(f)[:16]}` |" for f in main_files]
    lines += [f"| `cf_*.json` ({len(cf)} counterfactual single-year queries) | see files |", ""]
    text = "\n".join(lines) + "\n"
    manifest = REPO / "data" / "raw" / "MANIFEST.md"
    if manifest.exists():
        body = manifest.read_text()
        start = body.find("## M3: PIP and WDI pulls for Brazil")
        if start >= 0:
            nxt = body.find("\n## ", start + 5)
            body = body[:start] + text + (body[nxt + 1:] if nxt >= 0 else "")
        else:
            body = body.rstrip() + "\n\n" + text
        manifest.write_text(body)
    else:
        (REPO / "data" / "raw" / "MANIFEST_M3.md").write_text("# Raw data manifest (M3)\n\n" + text)


if __name__ == "__main__":
    main()
