# Team 1 — Digital Economy Intelligence Lab

**Team 1:** Valeria Hernandez, Lorena Perez, Gustavo Fuentes, Jose Pech, Julio de Aquino, Ricardo Horta  
**Professor:** Jose Francisco Perez Alcocer

This repository delivers Activity 2, Part I for **Mexico, South Korea, Finland, Brazil, and India**, focused on telecommunications. Part II (From Data to Digital Transformation) is in [`part2/`](part2/).

Run `python build_analysis.py` from the project root (standard library only). It downloads official observations and indicator metadata to `data/raw/` if they are missing, records access times in `data/download_log.csv`, creates `data/processed/digital_economy_clean.csv`, and rebuilds `source_log.csv`, `data_dictionary.csv` and the dashboard.

The notebook at `notebooks/Digital_Economy_Analysis.ipynb` calls the same pipeline and contains the full analysis: acquisition, traceability, temporal comparability, data exploration and preparation, concepts, DRS with robustness checks, four charts with their readings, correlations, digital gap, 4C framework and final diagnosis. It needs `pip install -r requirements.txt` (pandas, matplotlib, Jupyter). Data use is restricted to official World Bank WDI API observations; the API metadata identifies the original producer of each series (ITU, WIPO, and World Bank compilations of Netcraft, IMF, UN Comtrade and UNESCO data). The source log documents original-producer attribution, official definitions, units, years, endpoints, and transformations.

## Chosen eight indicators

1. Fixed broadband subscriptions (per 100 people) — connectivity
2. Mobile cellular subscriptions (per 100 people) — connectivity
3. Individuals using the Internet (% of population) — use
4. Secure Internet servers (per 1 million people) — quality/security proxy
5. ICT service exports (% of service exports) — digital economic activity
6. High-technology exports (% of manufactured exports) — digital economic activity
7. R&D expenditure (% of GDP) — technological capacity
8. Patent applications, residents (count) — innovation capacity

Each indicator uses a common reference year: the latest year reported by at least four of the five economies (the only exception is India's R&D, 2020 against 2023). The DRS uses ln(1 + x) for indicators whose max/min ratio exceeds 100 (secure servers and resident patents), min–max normalization, equal weights (0.125), positive orientation for every selected measure, and a complete-case check. It is a descriptive comparison, not a causal estimate.

## Original sources and indicator traceability

The downloadable observations were obtained from the official **World Bank World Development Indicators (WDI) API**. WDI republishes indicators originally produced by the **International Telecommunication Union (ITU)**, the **World Intellectual Property Organization (WIPO)** and other organisations compiled by the World Bank. The original producer, taken verbatim from the API metadata, is recorded below and in `source_log.csv`; this prevents presenting a WDI delivery endpoint as if it were the original producer.

| Clean-data variable | WDI indicator code | Original provider | Original source | Raw download file |
|---|---|---|---|---|
| `fixed_broadband_per_100` | `IT.NET.BBND.P2` | ITU | [ITU DataHub](https://datahub.itu.int/) | `data/raw/world_bank_IT.NET.BBND.P2.json` |
| `mobile_subscriptions_per_100` | `IT.CEL.SETS.P2` | ITU | [ITU DataHub](https://datahub.itu.int/) | `data/raw/world_bank_IT.CEL.SETS.P2.json` |
| `internet_users_pct` | `IT.NET.USER.ZS` | ITU | [ITU DataHub](https://datahub.itu.int/) | `data/raw/world_bank_IT.NET.USER.ZS.json` |
| `secure_servers_per_million` | `IT.NET.SECR.P6` | Netcraft, compiled by the World Bank | [World Bank Open Data](https://data.worldbank.org/indicator/IT.NET.SECR.P6) | `data/raw/world_bank_IT.NET.SECR.P6.json` |
| `ict_service_exports_pct` | `BX.GSR.CCIS.ZS` | IMF Balance of Payments, compiled by the World Bank | [World Bank Open Data](https://data.worldbank.org/indicator/BX.GSR.CCIS.ZS) | `data/raw/world_bank_BX.GSR.CCIS.ZS.json` |
| `high_tech_exports_pct` | `TX.VAL.TECH.MF.ZS` | UN Comtrade / WITS, compiled by the World Bank | [World Bank Open Data](https://data.worldbank.org/indicator/TX.VAL.TECH.MF.ZS) | `data/raw/world_bank_TX.VAL.TECH.MF.ZS.json` |
| `rd_expenditure_pct_gdp` | `GB.XPD.RSDV.GD.ZS` | UNESCO Institute for Statistics, compiled by the World Bank | [World Bank Open Data](https://data.worldbank.org/indicator/GB.XPD.RSDV.GD.ZS) | `data/raw/world_bank_GB.XPD.RSDV.GD.ZS.json` |
| `resident_patent_applications` | `IP.PAT.RESD` | WIPO | [WIPO IP Statistics](https://www.wipo.int/en/web/ip-statistics) | `data/raw/world_bank_IP.PAT.RESD.json` |

### How to track any value

1. Start with a value in `data/processed/digital_economy_clean.csv`. The column name is the clean-data variable; its matching `<variable>_year` column gives the observation year used for that country.
2. Find that variable in `source_log.csv`. This record gives the official indicator name and definition, unit, original producer, original-source link, WDI indicator code, full API and metadata endpoints, raw file, access date, reference year, exact observation year for all five countries, year exceptions, and transformation. `data_dictionary.csv` describes every column of the clean dataset.
3. Open the matching JSON file in `data/raw/`. Look for the country ISO code (`MEX`, `KOR`, `FIN`, `BRA`, or `IND`), the `date`, and `value`. That is the official API observation from which the clean value was selected. `data/download_log.csv` gives when each raw file was obtained.
4. To verify or refresh a series, open the `api_endpoint` from its source-log row in a browser, or rerun `python build_analysis.py`. The endpoint format is: `https://api.worldbank.org/v2/country/MEX;KOR;FIN;BRA;IND/indicator/INDICATOR_CODE?format=json&per_page=1000`.

The build script selects the common reference year for each indicator and retains each country's observation year instead of treating different years as identical. It does not impute missing data, and it treats `null` (not available) differently from an observed `0`. The complete transformation record is in `source_log.csv`; secure servers and resident patent applications are transformed (`ln(1 + x)`) before DRS normalisation.
