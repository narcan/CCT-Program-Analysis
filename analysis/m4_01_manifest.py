"""M4 step 1: map the IBGE file tree for PNAD annual and PNAD Continua
annual-visit microdata and write data/raw/MANIFEST_M4.md.

Run: python analysis/m4_01_manifest.py
"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cct import pnad  # noqa: E402

OUT = pnad.ROOT / "data" / "raw" / "MANIFEST_M4.md"


def table(base: str, sub: str, depth: int = 0) -> list[str]:
    rows = []
    for name, mod, size in pnad.list_dir(base + sub):
        if name.endswith("/"):
            if depth > 0:
                rows += table(base, sub + name, depth - 1)
            continue
        rows.append(f"| {sub}{name} | {size} | {mod} |")
    return rows


def main() -> None:
    today = dt.date.today().isoformat()
    lines = [
        "# MANIFEST for M4 raw data (IBGE microdata)",
        "",
        f"Directory listing pulled {today} from the official IBGE server",
        "(ftp.ibge.gov.br, served over HTTPS). Sizes and dates are as listed by",
        "the server. Raw files are downloaded one year at a time into",
        "`data/raw/ibge/<survey><year>/`, the needed columns are saved as",
        "parquet in `data/clean/ibge/`, and the raw zip and text are deleted.",
        "Nothing from the downloads is executed: the SAS input programs are",
        "parsed as text only, to get column positions.",
        "",
        "## PNAD annual (2001-2015)",
        "",
        f"Base URL: `{pnad.PNAD_BASE}`",
        "",
        "Files used by the pipeline (`src/cct/pnad.py`, `PNAD_URLS`): 2001-2012",
        "come from `reponderacao_2001_2012/` (weights recalibrated to the",
        "population projection based on the 2010 Census, comparable with",
        "2013-2015). There was no PNAD in 2010 (Census year). Each reweighted",
        "zip holds data (PES/DOM txt), SAS input files and dictionaries.",
        "2013-2015 come from the year folders (data zip plus a separate",
        "dictionary/input zip).",
        "",
        "| Path (relative to base) | Size | Modified |",
        "|---|---|---|",
    ]
    lines += table(pnad.PNAD_BASE, "reponderacao_2001_2012/")
    for y in (2011, 2012, 2013, 2014, 2015):
        lines += table(pnad.PNAD_BASE, f"{y}/")
    lines += [
        "",
        "Also on the server but not used: `reponderacao_2001_2009/` (older",
        "reweighting to the 2000-Census-based projection) and 1976-1999 folders.",
        "",
        "## PNAD Continua, annual visit files (1st and 5th visits)",
        "",
        f"Base URL: `{pnad.PNADC_BASE}`",
        "",
        "Visit 1 covers 2012-2019 and 2022 onward; visit 5 covers 2016 onward",
        "(2020 and 2021 were collected in visit 5 because of the pandemic).",
        "Visit 2 exists for 2020, 2021, 2023, 2024 (not used). Visits 3 and 4",
        "have no annual files.",
        "",
        "| Path (relative to base) | Size | Modified |",
        "|---|---|---|",
    ]
    for sub in ("Visita_1/Dados/", "Visita_1/Documentacao/",
                "Visita_5/Dados/", "Visita_5/Documentacao/",
                "Documentacao_Geral/"):
        lines += table(pnad.PNADC_BASE, sub)
    lines += [
        "",
        "## Price index",
        "",
        "INPC monthly index (Dec 1993 = 100), IBGE:",
        "`https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip`",
        "(file inside: `inpc_202609SerieHist.xls` at pull time).",
        "",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
