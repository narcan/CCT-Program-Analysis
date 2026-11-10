"""Readers for PNAD Continua annual-visit microdata (1st and 5th visits).

Income from sources other than work (pensions, BPC, Bolsa Familia, other
programmes, rents, etc.) is collected once a year, in the 1st visit
(2012-2019, 2022 on) or the 5th visit (2016 on; the only one for 2020-2021).

Bolsa Familia item:
  - 2012 to Q3 2015 (old questionnaire): no separate item. BF is inside
    V5011/V50111/V501111 "outro programa social" (any other social
    programme, which in practice is mostly BF).
  - From Q4 2015 (new questionnaire): V5002A "recebeu Bolsa Familia" and
    V5002A2 value; other programmes in V5003A/V5003A2; BPC in V5001A/A2.
    The label stays "Bolsa Familia" in later dictionaries, but the item
    captured Auxilio Brasil in 2022 (programme renamed Nov 2021 - Feb 2023).
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from .pnad import CLEAN, PNADC_BASE, RAW, curl, list_dir, parse_sas_input, read_fwf

COLS = [
    "Ano", "Trimestre", "UF", "UPA", "Estrato", "V1008", "V1014", "V1022",
    "V1032", "V2001", "V2003", "V2005", "V2009",
    # old questionnaire (2012-2015 Q3): household-level filter + person + value
    "V5009", "V50091", "V500911",   # BPC
    "V5011", "V50111", "V501111",   # other social programme (includes BF)
    # new questionnaire (2015 Q4 on)
    "V5001A", "V5001A2",            # BPC
    "V5002A", "V5002A2",            # Bolsa Familia
    "V5003A", "V5003A2",            # other social programme
    "VD4019", "VD4020", "VD4048", "VD4052",
    "VD5001", "VD5002", "VD5004", "VD5005", "VD5007", "VD5008",
    "VD5010", "VD5011",
]


def files_for(year: int, visit: int) -> tuple[str, str]:
    """(data zip URL, SAS input URL) for one year/visit, found by listing."""
    v = f"Visita_{visit}/"
    data = [n for n, _, _ in list_dir(PNADC_BASE + v + "Dados/")
            if re.match(rf"PNADC_{year}_visita{visit}.*\.zip$", n)]
    docs = [n for n, _, _ in list_dir(PNADC_BASE + v + "Documentacao/")
            if n.startswith("input_PNADC_") and n.endswith(".txt")]
    inp = [n for n in docs if re.match(rf"input_PNADC_{year}_visita{visit}", n)]
    if not inp:  # 2012-2014 share one layout
        for n in docs:
            m = re.match(r"input_PNADC_(\d{4})_a_(\d{4})_visita", n)
            if m and int(m.group(1)) <= year <= int(m.group(2)):
                inp = [n]
    if not data or not inp:
        raise FileNotFoundError(f"PNADC {year} visit {visit}: data={data} input={inp}")
    return (PNADC_BASE + v + "Dados/" + sorted(data)[-1],
            PNADC_BASE + v + "Documentacao/" + sorted(inp)[-1])


def pnadc_to_parquet(year: int, visit: int) -> Path:
    out = CLEAN / f"pnadc{year}_v{visit}.parquet"
    if out.exists():
        return out
    CLEAN.mkdir(parents=True, exist_ok=True)
    d = RAW / f"pnadc{year}_v{visit}"
    d.mkdir(parents=True, exist_ok=True)
    zurl, iurl = files_for(year, visit)
    zp = d / Path(zurl).name
    ip = d / Path(iurl).name
    if not zp.exists():
        curl(zurl, zp)
    if not ip.exists():
        curl(iurl, ip)
    layout = parse_sas_input(ip.read_text(encoding="latin-1"))
    layout = {k.upper(): v for k, v in layout.items()}
    with zipfile.ZipFile(zp) as zf:
        txt = [n for n in zf.namelist() if n.lower().endswith(".txt")]
        name = max(txt, key=lambda n: zf.getinfo(n).file_size)
        target = d / Path(name).name
        zf.extract(name, d)
        extracted = d / name
        if extracted != target:
            extracted.rename(target)
    cols = [c.upper() for c in COLS]
    df = read_fwf(target, layout, cols)
    df.columns = [c.upper() for c in df.columns]
    df.to_parquet(out, index=False)
    for p in sorted(d.rglob("*"), reverse=True):
        p.unlink() if p.is_file() else p.rmdir()
    d.rmdir()
    return out


def load_pnadc(year: int, visit: int) -> pd.DataFrame:
    return pd.read_parquet(pnadc_to_parquet(year, visit))


# --------------------------------------------------------------------------
# Deflators (IBGE, deflator_PNADC_<latest>.xls): CO1 brings habitual income
# to average prices of the survey year itself.
# --------------------------------------------------------------------------
DEFLATOR_URL = PNADC_BASE + "Documentacao_Geral/deflator_PNADC_2025.xls"


def deflators() -> pd.DataFrame:
    p = RAW / "pnadc_doc" / "deflator_PNADC_2025.xls"
    if not p.exists():
        curl(DEFLATOR_URL, p)
    d = pd.read_excel(p)
    d.columns = [c.lower() for c in d.columns]
    return d


def person_frame(df: pd.DataFrame, year: int, concept: str = "habitual") -> pd.DataFrame:
    """Household members with per-capita income with and without BF.

    Income concept (default "habitual"): VD5008, IBGE's habitual household per-capita income
    (habitual work income plus effective income from other sources),
    excluding pensioners, domestic workers and their relatives, and
    converted to average prices of the survey year with deflator CO1.
    concept="effective" uses VD5002 with deflator CO1e instead.
    BF: V5002A2 where the new item exists; otherwise (2012-2015 Q1-Q3)
    V501111 "other social programme" as the closest available proxy.
    """
    x = df.copy()
    for c in ("TRIMESTRE", "UF"):
        x[c] = pd.to_numeric(x[c], errors="coerce")
    cond = pd.to_numeric(x["V2005"], errors="coerce")
    x = x[cond.between(1, 16)].copy()  # 17-19: pensioner, domestic worker, relative
    x["hh"] = x["UPA"].astype(str) + x["V1008"].astype(str) + x["V1014"].astype(str)
    defl = deflators()
    dcol = "co1" if concept == "habitual" else "co1e"
    defl = defl[defl["ano"] == year][["trim", "uf", dcol]].rename(columns={dcol: "co1"})
    x = x.merge(defl, left_on=["TRIMESTRE", "UF"], right_on=["trim", "uf"], how="left")
    bf_new = x["V5002A2"] if "V5002A2" in x else pd.Series(np.nan, index=x.index)
    bf_old = x["V501111"] if "V501111" in x else pd.Series(np.nan, index=x.index)
    has_new = bf_new.notna().groupby(x["hh"]).transform("any") | (
        x["V5002A"].notna() if "V5002A" in x else False)
    x["bf_item"] = np.where(has_new, "V5002A2", "V501111")
    x["bf_value"] = np.where(has_new, bf_new.fillna(0), bf_old.fillna(0))
    x["bpc_value"] = (x["V5001A2"] if "V5001A2" in x else 0)
    x["n_members"] = x.groupby("hh")["hh"].transform("size")
    x["hh_bf"] = x.groupby("hh")["bf_value"].transform("sum")
    # habitual: VD5008; effective: VD5002 (effective work income in the
    # reference month plus effective income from other sources)
    pc = x["VD5008"] if concept == "habitual" else x["VD5002"]
    x["pc_with"] = pc * x["co1"]
    x["pc_without"] = (pc - x["hh_bf"] / x["n_members"]).clip(lower=0) * x["co1"]
    x["weight"] = x["V1032"]
    keep = x["pc_with"].notna() & x["weight"].notna()
    return x.loc[keep, ["hh", "UF", "TRIMESTRE", "weight", "n_members", "bf_item",
                        "bf_value", "hh_bf", "pc_with", "pc_without", "co1"]]
