# Team 1 — Digital Economy Intelligence Lab

This repository delivers Activity 2, Part I for **Mexico, South Korea, Finland, Brazil, and India**, focused on telecommunications.

Run `python build_analysis.py` from the project root. It downloads official observations to `data/raw/`, creates `data/processed/digital_economy_clean.csv`, and rebuilds the dashboard and documentation files.

The notebook at `notebooks/Digital_Economy_Analysis.ipynb` contains the reproducible analysis narrative and calls the same pipeline. Data use is restricted to official World Bank WDI API observations whose metadata identifies the ITU and WIPO series used. The source log documents original-provider attribution, indicator definitions, units, years, endpoint, and transformations.

## Chosen eight indicators

1. Fixed broadband subscriptions (per 100 people) — connectivity
2. Mobile cellular subscriptions (per 100 people) — connectivity
3. Individuals using the Internet (% of population) — use
4. Secure Internet servers (per 1 million people) — quality/security proxy
5. ICT service exports (% of service exports) — digital economic activity
6. High-technology exports (% of manufactured exports) — digital economic activity
7. R&D expenditure (% of GDP) — technological capacity
8. Patent applications, residents (count) — innovation capacity

The DRS uses min–max normalization, equal weights (0.125), positive orientation for every selected measure, and a complete-case check. It is a descriptive comparison, not a causal estimate.

## Original sources and indicator traceability

The downloadable observations were obtained from the official **World Bank World Development Indicators (WDI) API**. WDI republishes several indicators originally reported by the **International Telecommunication Union (ITU)** and the **World Intellectual Property Organization (WIPO)**. The original provider is explicitly recorded below and in `source_log.csv`; this prevents presenting a WDI delivery endpoint as if it were the original producer.

| Clean-data variable | WDI indicator code | Original provider | Original source | Raw download file |
|---|---|---|---|---|
| `fixed_broadband_per_100` | `IT.NET.BBND.P2` | ITU | [ITU DataHub](https://datahub.itu.int/) | `data/raw/world_bank_IT.NET.BBND.P2.json` |
| `mobile_subscriptions_per_100` | `IT.CEL.SETS.P2` | ITU | [ITU DataHub](https://datahub.itu.int/) | `data/raw/world_bank_IT.CEL.SETS.P2.json` |
| `internet_users_pct` | `IT.NET.USER.ZS` | ITU | [ITU DataHub](https://datahub.itu.int/) | `data/raw/world_bank_IT.NET.USER.ZS.json` |
| `secure_servers_per_million` | `IT.NET.SECR.P6` | World Bank WDI | [World Bank Open Data](https://data.worldbank.org/indicator/IT.NET.SECR.P6) | `data/raw/world_bank_IT.NET.SECR.P6.json` |
| `ict_service_exports_pct` | `BX.GSR.CCIS.ZS` | World Bank WDI | [World Bank Open Data](https://data.worldbank.org/indicator/BX.GSR.CCIS.ZS) | `data/raw/world_bank_BX.GSR.CCIS.ZS.json` |
| `high_tech_exports_pct` | `TX.VAL.TECH.MF.ZS` | World Bank WDI | [World Bank Open Data](https://data.worldbank.org/indicator/TX.VAL.TECH.MF.ZS) | `data/raw/world_bank_TX.VAL.TECH.MF.ZS.json` |
| `rd_expenditure_pct_gdp` | `GB.XPD.RSDV.GD.ZS` | World Bank WDI | [World Bank Open Data](https://data.worldbank.org/indicator/GB.XPD.RSDV.GD.ZS) | `data/raw/world_bank_GB.XPD.RSDV.GD.ZS.json` |
| `resident_patent_applications` | `IP.PAT.RESD` | WIPO | [WIPO IP Statistics](https://www.wipo.int/en/web/ip-statistics) | `data/raw/world_bank_IP.PAT.RESD.json` |

### How to track any value

1. Start with a value in `data/processed/digital_economy_clean.csv`. The column name is the clean-data variable; its matching `<variable>_year` column gives the observation year used for that country.
2. Find that variable in `source_log.csv`. This record gives the official indicator name, unit, original provider, original-source link, WDI indicator code, full API endpoint, transformation, and exact observation year for all five countries.
3. Open the matching JSON file in `data/raw/`. Look for the country ISO code (`MEX`, `KOR`, `FIN`, `BRA`, or `IND`), the `date`, and `value`. That is the untouched official API observation from which the clean value was selected.
4. To verify or refresh a series, open the `api_endpoint` from its source-log row in a browser, or rerun `python build_analysis.py`. The endpoint format is: `https://api.worldbank.org/v2/country/MEX;KOR;FIN;BRA;IND/indicator/INDICATOR_CODE?format=json&per_page=1000`.

The build script selects the most recent non-null observation per country and retains the year instead of treating different years as identical. It does not impute missing data. The complete transformation record is in `source_log.csv`; only resident patent applications are transformed (`ln(1 + x)`) before DRS normalisation.
