# WIPO IP Statistics query (evidence for §10 Patents)

The Part II instructions make the WIPO query **mandatory** for the patents section. This folder holds the evidence.

## Query

| Field | Value |
|---|---|
| Portal | [WIPO IP Statistics Data Center](https://www3.wipo.int/ipstats/) → PATENT |
| Indicator | 4a - Patent publications by technology |
| Report type | Total count by applicant's origin |
| Years | 2014–2024 |
| Origins | Mexico, Republic of Korea, Finland, Brazil, India |
| Fields of technology | 3 Telecommunications · 4 Digital communication · 6 Computer technology · 7 IT methods for management |
| Database | "Source: WIPO statistics database. Last updated: May 2026" |
| Consulted | 2026-09-29 |

**Direct link to the results** (opens the same query):
<https://www3.wipo.int/ipstats/ips-search/search-result?type=IPS&selectedTab=patent&indicator=17&reportType=13&fromYear=2014&toYear=2024&ipsOffSelValues=&ipsOriSelValues=MX,KR,FI,BR,IN&ipsTechSelValues=3,4,6,7>

## Files

| File | Content |
|---|---|
| `01_query_form_fields_2026-09-29.jpg` | Query form filled in (selected fields of technology) |
| `02_results_query_metadata.jpg` | Results page: indicator, report type, year range, database date |
| `03_results_table_rows01-11_2014-2019.jpg` | Results table, rows 1–11, years 2014–2019 |
| `04_results_table_rows04-20_2014-2019.jpg` | Results table, rows 4–20, years 2014–2019 |
| `05_results_table_rows04-20_2014-2024.jpg` | Results table scrolled right: rows 4–20, years 2014–2024 |
| `wipo_patent_publications_by_tech_origin_2014_2024.csv` | All 20 rows (5 origins × 4 fields × 11 years), copied from the results table and checked against the screenshots |
| `world_bank_SP.POP.TOTL_2021_2024.json` | Population (World Bank API, `SP.POP.TOTL`), used to express counts per million people |

## Results (team calculation)

Sum of the four digital fields, average of 2021–2023:

| Origin | Publications per year | Per million people | Telecom + digital communication (fields 3–4) per million | Trend vs 2014–2016 average |
|---|---|---|---|---|
| Republic of Korea | 54,245 | 1,048.9 | 371.3 | up |
| Finland | 3,941 | 708.7 | 572.5 | ≈ flat |
| India | 5,501 | 3.9 | 1.1 | about ×2.1 (2,663 → 5,501) |
| Brazil | 315 | 1.5 | 0.4 | −21% (400 → 315) |
| **Mexico** | **89** | **0.7** | **0.2** | **−21% (113 → 89)** |

**Reading and caveats**
- **2024 is excluded from the averages.** Brazil, India and Mexico show sharp drops in 2024, most likely because the latest year is still incomplete. India also has an irregular 2022.
- **What is counted:** publications of patent applications, attributed to the **applicant's origin**. That is not necessarily where the invention was developed, and it says nothing about quality, use or commercial success.
- **What it shows:** Mexico's patenting in the digital and telecom fields is very small and not growing. This is consistent with the Part I finding that resident patents were one of Mexico's weakest indicators.
