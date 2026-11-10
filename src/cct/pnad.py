"""Readers for IBGE household survey microdata (PNAD annual, 2001-2015).

The raw files are fixed-width text. IBGE ships SAS "input" programs that
give the start column, name and width of each variable. We parse those
programs as plain text (never execute anything from the download) and
read only the columns we need.

Downloaded files are untrusted data. Everything here treats them as bytes
to slice, nothing more.
"""
from __future__ import annotations

import html
import re
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "ibge"
CLEAN = ROOT / "data" / "clean" / "ibge"

FTP = "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
PNAD_BASE = FTP + "Pesquisa_Nacional_por_Amostra_de_Domicilios_anual/microdados/"
PNADC_BASE = FTP + "Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/"

# Official PNAD annual files. 2001-2012 use the files reweighted to the 2010
# Census population projection (folder reponderacao_2001_2012), which IBGE
# recommends for comparisons with 2013-2015. No PNAD in 2010 (Census year).
PNAD_URLS = {
    2001: "reponderacao_2001_2012/PNAD_reponderado_2001.zip",
    2002: "reponderacao_2001_2012/PNAD_reponderado_2002.zip",
    2003: "reponderacao_2001_2012/PNAD_reponderado_2003_20150814.zip",
    2004: "reponderacao_2001_2012/PNAD_reponderado_2004.zip",
    2005: "reponderacao_2001_2012/PNAD_reponderado_2005.zip",
    2006: "reponderacao_2001_2012/PNAD_reponderado_2006.zip",
    2007: "reponderacao_2001_2012/PNAD_reponderado_2007_20150814.zip",
    2008: "reponderacao_2001_2012/PNAD_reponderado_2008.zip",
    2009: "reponderacao_2001_2012/PNAD_reponderado_2009_20171228.zip",
    2011: "reponderacao_2001_2012/PNAD_reponderado_2011_20150814.zip",
    2012: "reponderacao_2001_2012/PNAD_reponderado_2012_20150814.zip",
    2013: ["2013/Dados_20170807.zip", "2013/Dicionarios_e_input_20170807.zip"],
    2014: ["2014/Dados_20170323.zip", "2014/Dicionarios_e_input_20170323.zip"],
    2015: ["2015/Dados_20170517.zip", "2015/Dicionarios_e_input_20170517.zip"],
}


# --------------------------------------------------------------------------
# FTP helpers
# --------------------------------------------------------------------------
def curl(url: str, dest: Path | None = None, timeout: int = 1800) -> str:
    """Fetch a URL with curl (honours the session proxy). Returns text if
    dest is None, else writes the file and returns its path."""
    args = ["curl", "-sS", "-f", "-L", "--retry", "3", "-m", str(timeout)]
    if dest is None:
        r = subprocess.run(args + [url], capture_output=True, check=True)
        return r.stdout.decode("latin-1")
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(args + ["-o", str(dest), url], check=True)
    return str(dest)


def list_dir(url: str) -> list[tuple[str, str, str]]:
    """List an IBGE FTP-over-HTTPS directory: (name, modified, size)."""
    text = curl(url)
    out = []
    for row in re.findall(r"<tr>(.*?)</tr>", text, re.S):
        a = re.search(r'href="([^"?/][^"]*)"', row)
        if not a or a.group(1).startswith("http"):
            continue
        cells = [re.sub("<[^>]+>", "", c).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        cells = [html.unescape(c) for c in cells if c and c != "&nbsp;"]
        name = html.unescape(a.group(1))
        mod = cells[1] if len(cells) > 1 else ""
        size = cells[2] if len(cells) > 2 else ""
        out.append((name, mod, size))
    return out


# --------------------------------------------------------------------------
# SAS input layout parsing
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Field:
    name: str
    start: int  # 1-based
    width: int
    char: bool
    decimals: int


_SAS = re.compile(r"@\s*0*(\d+)\s+([A-Za-z_][A-Za-z0-9_]*)\s+(\$?)\s*(\d+)\.(\d*)")


def parse_sas_input(text: str) -> dict[str, Field]:
    """Parse an IBGE SAS INPUT program into {name: Field}.

    Lines look like ``@00637  V1272  $1.   /* label */`` or
    ``@00096  V4605   12.10``. A ``w.d`` informat means d implied decimals
    when the field has no decimal point. Duplicates (e.g. UF inside V0102)
    are kept under their own names.
    """
    fields: dict[str, Field] = {}
    for m in _SAS.finditer(text):
        start, name, dollar, width, dec = m.groups()
        name = name.upper()
        if name in fields:
            continue
        fields[name] = Field(name, int(start), int(width), dollar == "$",
                             int(dec) if dec else 0)
    return fields


def read_fwf(path: Path, layout: dict[str, Field], cols: list[str],
             encoding: str = "latin-1", numeric: bool = True) -> pd.DataFrame:
    """Read selected columns of a fixed-width file.

    Numeric fields become float (NaN for blanks); character fields stay str.
    Columns missing from the layout are skipped with no error, so callers
    can ask for year-specific variables and check what came back.
    """
    use = [layout[c] for c in cols if c in layout]
    colspecs = [(f.start - 1, f.start - 1 + f.width) for f in use]
    df = pd.read_fwf(path, colspecs=colspecs, names=[f.name for f in use],
                     dtype=str, encoding=encoding, header=None)
    if numeric:
        for f in use:
            if f.char:
                continue
            s = df[f.name].str.strip()
            v = pd.to_numeric(s, errors="coerce")
            if f.decimals:
                has_point = s.str.contains(".", regex=False).fillna(False)
                v = v.where(has_point, v / 10 ** f.decimals)
            df[f.name] = v
    return df


# --------------------------------------------------------------------------
# PNAD annual: download, locate files, extract needed columns
# --------------------------------------------------------------------------
PERSON_COLS = [
    "V0101", "UF", "V0102", "V0103", "V0301", "V0302", "V8005", "V0401",
    "V0402", "V0403",
    # income items (monthly values, reference month September)
    "V1252", "V1255", "V1258", "V1261", "V1264", "V1267", "V1270",
    "V1272", "V1273", "V4718", "V4719", "V4720", "V4721", "V4742",
    "V4729", "V4732", "V4745",
]
HOUSEHOLD_COLS = [
    "V0101", "UF", "V0102", "V0103", "V0104", "V0105", "V4105", "V4602",
    "V4611", "V4614", "V4617", "V4618", "V4619", "V4620", "V4621", "V4741",
    "V4742",
    # 2004 and 2006 supplement items on social programmes (household level)
    "V2401", "V2402", "V2403", "V2404", "V2405", "V2406", "V2407", "V2408",
    "V2409",
]


def _find(members: list[str], *patterns: str) -> str:
    for pat in patterns:
        rx = re.compile(pat, re.I)
        hits = [m for m in members if rx.search(m)]
        if hits:
            return hits[0]
    raise FileNotFoundError(f"no member matching {patterns}")


def download_pnad(year: int) -> list[Path]:
    """Download the zip(s) for one PNAD year into data/raw/ibge/pnad{year}/."""
    rel = PNAD_URLS[year]
    rels = rel if isinstance(rel, list) else [rel]
    d = RAW / f"pnad{year}"
    paths = []
    for r in rels:
        p = d / Path(r).name
        if not p.exists():
            curl(PNAD_BASE + r, p)
        paths.append(p)
    return paths


def _read_member_text(zf: zipfile.ZipFile, name: str) -> str:
    raw = zf.read(name)
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def _open_nested(paths: list[Path], workdir: Path) -> dict[str, Path]:
    """Extract the data and input files we need. Some years nest zips
    inside zips; we only ever extract, never run, their contents."""
    workdir.mkdir(parents=True, exist_ok=True)
    found: dict[str, Path] = {}
    queue = list(paths)
    while queue:
        z = queue.pop()
        with zipfile.ZipFile(z) as zf:
            for m in zf.namelist():
                low = m.lower()
                base = Path(m).name
                if not base or not re.search(r"\.(txt|zip)$", low):
                    continue
                keep = (re.search(r"(pes|dom)\d{4}", base, re.I)
                        or "input" in low or low.endswith(".zip"))
                if not keep or "leitura" in low or "/cv/" in low:
                    continue
                target = workdir / base
                with zf.open(m) as src, open(target, "wb") as dst:
                    while chunk := src.read(1 << 22):
                        dst.write(chunk)
                if low.endswith(".zip"):
                    queue.append(target)
                else:
                    found[base] = target
    return found


def extract_pnad(year: int, keep_raw: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (persons, households) DataFrames with the M4 columns for one
    PNAD year. Downloads if needed; deletes raw text afterwards unless
    keep_raw."""
    zips = download_pnad(year)
    work = RAW / f"pnad{year}" / "x"
    files = _open_nested(zips, work)
    names = list(files)
    pes_txt = files[_find(names, rf"^PES{year}\.txt$", r"^PES\d{4}\.txt$")]
    dom_txt = files[_find(names, rf"^DOM{year}\.txt$", r"^DOM\d{4}\.txt$")]
    pes_in = files[_find(names, r"input.*pes", r"pes.*input")]
    dom_in = files[_find(names, r"input.*dom", r"dom.*input")]
    lay_p = parse_sas_input(pes_in.read_text(encoding="latin-1"))
    lay_d = parse_sas_input(dom_in.read_text(encoding="latin-1"))
    pes = read_fwf(pes_txt, lay_p, PERSON_COLS)
    dom = read_fwf(dom_txt, lay_d, HOUSEHOLD_COLS)
    meta = {"pes_input": pes_in.name, "dom_input": dom_in.name,
            "pes_cols": [c for c in PERSON_COLS if c in lay_p],
            "dom_cols": [c for c in HOUSEHOLD_COLS if c in lay_d]}
    pes.attrs["meta"] = meta
    if not keep_raw:
        for p in work.iterdir():
            p.unlink()
        work.rmdir()
    return pes, dom


def pnad_to_parquet(year: int, keep_zip: bool = False) -> tuple[Path, Path]:
    """Build data/clean/ibge/pnad{year}_{pes,dom}.parquet and clean up."""
    CLEAN.mkdir(parents=True, exist_ok=True)
    pes, dom = extract_pnad(year)
    pp = CLEAN / f"pnad{year}_pes.parquet"
    dp = CLEAN / f"pnad{year}_dom.parquet"
    pes.attrs = {}
    pes.to_parquet(pp, index=False)
    dom.to_parquet(dp, index=False)
    if not keep_zip:
        for z in (RAW / f"pnad{year}").glob("*.zip"):
            z.unlink()
    return pp, dp


def load_pnad(year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    pp = CLEAN / f"pnad{year}_pes.parquet"
    dp = CLEAN / f"pnad{year}_dom.parquet"
    if not (pp.exists() and dp.exists()):
        pnad_to_parquet(year)
    return pd.read_parquet(pp), pd.read_parquet(dp)


# --------------------------------------------------------------------------
# Household income aggregates
# --------------------------------------------------------------------------
MISSING_INCOME = 999_999_999_999  # IBGE code for "not declared"


def clean_income(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    return s.where(s < 1e11)  # 999999999999 and similar codes -> NaN


def household_members(pes: pd.DataFrame) -> pd.Series:
    """Members counted in household per-capita income (IBGE definition):
    excludes pensioners (V0401=6), domestic workers (7) and their relatives (8)."""
    cond = pd.to_numeric(pes["V0401"], errors="coerce")
    return cond.between(1, 5)
