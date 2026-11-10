# MANIFEST for M4 raw data (IBGE microdata)

Directory listing pulled 2026-11-10 from the official IBGE server
(ftp.ibge.gov.br, served over HTTPS). Sizes and dates are as listed by
the server. Raw files are downloaded one year at a time into
`data/raw/ibge/<survey><year>/`, the needed columns are saved as
parquet in `data/clean/ibge/`, and the raw zip and text are deleted.
Nothing from the downloads is executed: the SAS input programs are
parsed as text only, to get column positions.

## PNAD annual (2001-2015)

Base URL: `https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_anual/microdados/`

Files used by the pipeline (`src/cct/pnad.py`, `PNAD_URLS`): 2001-2012
come from `reponderacao_2001_2012/` (weights recalibrated to the
population projection based on the 2010 Census, comparable with
2013-2015). There was no PNAD in 2010 (Census year). Each reweighted
zip holds data (PES/DOM txt), SAS input files and dictionaries.
2013-2015 come from the year folders (data zip plus a separate
dictionary/input zip).

| Path (relative to base) | Size | Modified |
|---|---|---|
| reponderacao_2001_2012/PNAD_reponderado_2001.zip | 23M | 2016-08-17 11:43 |
| reponderacao_2001_2012/PNAD_reponderado_2002.zip | 24M | 2016-08-17 11:43 |
| reponderacao_2001_2012/PNAD_reponderado_2003_20150814.zip | 28M | 2016-08-17 11:43 |
| reponderacao_2001_2012/PNAD_reponderado_2004.zip | 27M | 2017-12-14 13:56 |
| reponderacao_2001_2012/PNAD_reponderado_2005.zip | 27M | 2018-07-04 15:30 |
| reponderacao_2001_2012/PNAD_reponderado_2006.zip | 27M | 2016-08-17 11:43 |
| reponderacao_2001_2012/PNAD_reponderado_2007_20150814.zip | 33M | 2016-08-17 11:43 |
| reponderacao_2001_2012/PNAD_reponderado_2008.zip | 43M | 2016-08-17 11:44 |
| reponderacao_2001_2012/PNAD_reponderado_2009_20171228.zip | 38M | 2017-12-28 16:08 |
| reponderacao_2001_2012/PNAD_reponderado_2011_20150814.zip | 31M | 2016-08-17 11:43 |
| reponderacao_2001_2012/PNAD_reponderado_2012_20150814.zip | 30M | 2016-08-17 11:43 |
| reponderacao_2001_2012/nota_tecnica.pdf | 102K | 2016-08-17 11:44 |
| reponderacao_2001_2012/nota_tecnica_seguranca_alimentar_PNAD_2004.pdf | 24K | 2017-12-14 13:51 |
| 2011/Dados.zip | 24M | 2016-08-17 11:43 |
| 2011/Dicionarios.zip | 84K | 2016-08-17 11:43 |
| 2011/Leia_me_PNAD_2011.zip | 7.4K | 2016-08-17 11:43 |
| 2011/Leitura_em_R.zip | 2.7M | 2016-08-17 11:43 |
| 2011/Marca_de_imputacao.zip | 3.1M | 2016-08-17 11:43 |
| 2011/Metodologia.zip | 565K | 2016-08-17 11:43 |
| 2011/Questionario.zip | 2.3M | 2016-08-17 11:43 |
| 2011/atualizacoes.txt | 1.6K | 2016-08-17 11:43 |
| 2012/Dados.zip | 26M | 2016-08-17 11:43 |
| 2012/Dicionarios_e_input.zip | 83K | 2016-08-17 11:43 |
| 2012/Leia_me_PNAD_2012.zip | 7.2K | 2016-08-17 11:43 |
| 2012/Leitura_em_R.zip | 3.4M | 2016-08-17 11:43 |
| 2012/Marca_de_Imputacao.zip | 2.5M | 2016-08-17 11:43 |
| 2012/Metodologia.zip | 575K | 2016-08-17 11:43 |
| 2012/Questionario.zip | 1.7M | 2016-08-17 11:43 |
| 2013/Dados_20170807.zip | 27M | 2017-08-07 14:50 |
| 2013/Dicionarios_e_input_20170807.zip | 131K | 2017-08-07 14:50 |
| 2013/Leitura_em_R.zip | 3.4M | 2016-08-17 11:43 |
| 2013/Marca_de_Imputacao.zip | 2.5M | 2016-08-17 11:43 |
| 2013/Metodologia.zip | 793K | 2016-08-17 11:43 |
| 2013/Questionario_20151005.zip | 2.4M | 2016-08-17 11:43 |
| 2013/leia_me_PNAD2013.pdf | 20K | 2016-08-17 11:43 |
| 2013/nota_tecnica_variavel_seguranca_alimentar_20170807.pdf | 47K | 2017-08-07 15:05 |
| 2014/Dados_20170323.zip | 31M | 2017-03-23 10:01 |
| 2014/Dicionarios_e_input_20170323.zip | 207K | 2017-03-23 10:01 |
| 2014/Leitura_em_R_20170323.zip | 3.4M | 2017-03-23 10:01 |
| 2014/Marca_de_Imputacao_20170323.zip | 2.4M | 2017-03-23 10:01 |
| 2014/Metodologia_20170802.zip | 1.1M | 2017-08-02 13:01 |
| 2014/Questionario_20170323.zip | 1.6M | 2017-03-23 10:01 |
| 2014/leia_me_20170323.pdf | 23K | 2017-03-23 10:01 |
| 2015/Dados_20170517.zip | 29M | 2017-05-17 10:00 |
| 2015/Dicionarios_e_input_20170517.zip | 159K | 2017-05-17 10:00 |
| 2015/Leitura_em_R_20170517.zip | 3.4M | 2017-05-17 10:00 |
| 2015/Marca_de_Imputacao_20170517.zip | 2.3M | 2017-05-17 10:00 |
| 2015/Metodologia_20170517.zip | 792K | 2017-05-17 10:00 |
| 2015/Questionario_20170517.zip | 1.0M | 2017-05-17 10:00 |
| 2015/leia_me_PNAD_2015_20170517.pdf | 52K | 2017-05-17 10:00 |

Also on the server but not used: `reponderacao_2001_2009/` (older
reweighting to the 2000-Census-based projection) and 1976-1999 folders.

## PNAD Continua, annual visit files (1st and 5th visits)

Base URL: `https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/`

Visit 1 covers 2012-2019 and 2022 onward; visit 5 covers 2016 onward
(2020 and 2021 were collected in visit 5 because of the pandemic).
Visit 2 exists for 2020, 2021, 2023, 2024 (not used). Visits 3 and 4
have no annual files.

| Path (relative to base) | Size | Modified |
|---|---|---|
| Visita_1/Dados/PNADC_2012_visita1_20250822.zip | 170M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2013_visita1_20250822.zip | 178M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2014_visita1_20250822.zip | 182M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2015_visita1_20251210.zip | 184M | 2025-12-10 07:51 |
| Visita_1/Dados/PNADC_2016_visita1_20250822.zip | 186M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2017_visita1_20250822.zip | 186M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2018_visita1_20250822.zip | 186M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2019_visita1_20250822.zip | 184M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2022_visita1_20250822.zip | 162M | 2025-08-21 15:36 |
| Visita_1/Dados/PNADC_2023_visita1_20250822.zip | 168M | 2025-08-21 15:37 |
| Visita_1/Dados/PNADC_2024_visita1_20251119.zip | 169M | 2025-11-19 10:34 |
| Visita_1/Dados/PNADC_2025_visita1_20260923.zip | 181M | 2026-09-23 10:00 |
| Visita_1/Documentacao/Observacoes_PNADC_2015_2016_visita1.pdf | 112K | 2020-03-02 08:48 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2012_a_2014_visita1_20220224.xls | 233K | 2022-02-24 09:43 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2015_visita1_20220224.xls | 258K | 2022-02-24 09:43 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2016_visita1_20220224.xls | 256K | 2022-02-24 09:43 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2017_visita1_20220224.xls | 256K | 2022-02-24 09:43 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2018_visita1_20220224.xls | 257K | 2022-02-24 09:43 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2019_visita1_20230811.xls | 229K | 2025-07-24 11:57 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2022_visita1_20231129.xls | 239K | 2025-07-24 11:57 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2023_visita1_20241220.xls | 239K | 2025-07-24 11:57 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2024_visita1_20251119.xls | 261K | 2025-11-19 10:34 |
| Visita_1/Documentacao/dicionario_PNADC_microdados_2025_visita1_20260923.xls | 261K | 2026-09-23 10:00 |
| Visita_1/Documentacao/input_PNADC_2012_a_2014_visita1_20220224.txt | 25K | 2022-02-24 09:43 |
| Visita_1/Documentacao/input_PNADC_2015_visita1_20220224.txt | 28K | 2022-02-24 09:43 |
| Visita_1/Documentacao/input_PNADC_2016_visita1_20220224.txt | 27K | 2022-02-24 09:43 |
| Visita_1/Documentacao/input_PNADC_2017_visita1_20220224.txt | 28K | 2022-02-24 09:43 |
| Visita_1/Documentacao/input_PNADC_2018_visita1_20220224.txt | 28K | 2022-02-24 09:43 |
| Visita_1/Documentacao/input_PNADC_2019_visita1_20230811.txt | 28K | 2023-08-11 12:30 |
| Visita_1/Documentacao/input_PNADC_2022_visita1_20231129.txt | 28K | 2023-11-29 11:17 |
| Visita_1/Documentacao/input_PNADC_2023_visita1_20241220.txt | 28K | 2024-12-20 10:00 |
| Visita_1/Documentacao/input_PNADC_2024_visita1_20251119.txt | 28K | 2025-11-19 10:34 |
| Visita_1/Documentacao/input_PNADC_2025_visita1_20260923.txt | 28K | 2026-09-23 10:00 |
| Visita_5/Dados/PNADC_2016_visita5_20260520.zip | 185M | 2026-05-20 12:45 |
| Visita_5/Dados/PNADC_2017_visita5_20260520.zip | 186M | 2026-05-20 12:53 |
| Visita_5/Dados/PNADC_2018_visita5_20250822.zip | 185M | 2025-08-21 15:37 |
| Visita_5/Dados/PNADC_2019_visita5_20250822.zip | 185M | 2025-08-21 15:37 |
| Visita_5/Dados/PNADC_2020_visita5_20250822.zip | 148M | 2025-08-21 15:37 |
| Visita_5/Dados/PNADC_2021_visita5_20250822.zip | 141M | 2025-08-21 15:37 |
| Visita_5/Dados/PNADC_2022_visita5_20250822.zip | 168M | 2025-08-21 15:37 |
| Visita_5/Dados/PNADC_2023_visita5_20250822.zip | 166M | 2025-08-21 15:37 |
| Visita_5/Dados/PNADC_2024_visita5.zip | 172M | 2025-09-01 08:42 |
| Visita_5/Dados/PNADC_2025_visita5_20261016.zip | 170M | 2026-10-16 10:00 |
| Visita_5/Documentacao/Observacoes_PNADC_2016_visita5.pdf | 113K | 2020-03-02 08:48 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2016_visita5_20260921.xls | 278K | 2026-09-18 19:30 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2017_visita5_20260921.xls | 296K | 2026-09-18 19:30 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2018_visita5_20260921.xls | 299K | 2026-09-18 19:30 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2019_visita5_20260921.xls | 300K | 2026-09-18 19:30 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2020_visita5_20220224.xls | 238K | 2022-02-24 09:32 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2021_visita5.xls | 223K | 2022-06-10 10:23 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2022_visita5_20260921.xls | 285K | 2026-09-18 19:30 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2023_visita5_20250424.xls | 275K | 2025-04-24 14:35 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2024_visita5_24092025.xls | 279K | 2025-09-24 09:33 |
| Visita_5/Documentacao/dicionario_PNADC_microdados_2025_visita5_20261016.xls | 271K | 2026-10-16 10:00 |
| Visita_5/Documentacao/input_PNADC_2016_visita5_20231222.txt | 30K | 2023-12-22 13:03 |
| Visita_5/Documentacao/input_PNADC_2017_visita5_20231222.txt | 31K | 2023-12-22 13:03 |
| Visita_5/Documentacao/input_PNADC_2018_visita5_20231222.txt | 31K | 2023-12-22 13:03 |
| Visita_5/Documentacao/input_PNADC_2019_visita5_20231222.txt | 31K | 2023-12-22 13:03 |
| Visita_5/Documentacao/input_PNADC_2020_visita5_20220224.txt | 24K | 2022-02-24 09:32 |
| Visita_5/Documentacao/input_PNADC_2021_visita5.txt | 24K | 2022-06-10 10:23 |
| Visita_5/Documentacao/input_PNADC_2022_visita5_20231222.txt | 31K | 2023-12-22 13:03 |
| Visita_5/Documentacao/input_PNADC_2023_visita5_20250424.txt | 30K | 2025-04-24 14:35 |
| Visita_5/Documentacao/input_PNADC_2024_visita5.txt | 31K | 2025-09-01 08:37 |
| Visita_5/Documentacao/input_PNADC_2025_visita5_20261016.txt | 34K | 2026-10-16 10:00 |
| Documentacao_Geral/Chaves_PNADC.pdf | 108K | 2020-03-02 08:47 |
| Documentacao_Geral/Estrutura_Atividade_CNAE_Domiciliar_2_0.xls | 68K | 2020-03-02 08:47 |
| Documentacao_Geral/Estrutura_Ocupacao_COD.xls | 97K | 2020-03-02 08:47 |
| Documentacao_Geral/Grupamentos_ocupacionais_atividades_PNADC.pdf | 28K | 2020-03-02 08:47 |
| Documentacao_Geral/PNADcIBGE_Deflator_Anual_Visita.pdf | 483K | 2022-02-07 07:40 |
| Documentacao_Geral/Variaveis_PNADC_Anual_Visita.xls | 310K | 2026-10-16 10:00 |
| Documentacao_Geral/deflacionamento_PNADC_anual_visita.txt | 2.7K | 2020-03-02 08:47 |
| Documentacao_Geral/deflator_PNADC_2017.xls | 216K | 2020-03-02 08:47 |
| Documentacao_Geral/deflator_PNADC_2018.xls | 129K | 2020-03-02 08:47 |
| Documentacao_Geral/deflator_PNADC_2019.xls | 278K | 2020-05-06 10:01 |
| Documentacao_Geral/deflator_PNADC_2020.xls | 159K | 2021-11-30 08:18 |
| Documentacao_Geral/deflator_PNADC_2021.xls | 174K | 2022-06-10 11:07 |
| Documentacao_Geral/deflator_PNADC_2022.xls | 188K | 2023-05-11 09:44 |
| Documentacao_Geral/deflator_PNADC_2023.xls | 204K | 2024-04-19 10:00 |
| Documentacao_Geral/deflator_PNADC_2024.xls | 218K | 2025-05-10 19:27 |
| Documentacao_Geral/deflator_PNADC_2025.xls | 233K | 2026-05-08 10:00 |
| Documentacao_Geral/historico_temas_PNADC_anual_visita.txt | 4.5K | 2026-10-16 10:00 |

## Price index

INPC monthly index (Dec 1993 = 100), IBGE:
`https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip`
(file inside: `inpc_202609SerieHist.xls` at pull time).

