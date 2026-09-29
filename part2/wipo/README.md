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

**Direct link to the results** (opens the same query):
<https://www3.wipo.int/ipstats/ips-search/search-result?type=IPS&selectedTab=patent&indicator=17&reportType=13&fromYear=2014&toYear=2024&ipsOffSelValues=&ipsOriSelValues=MX,KR,FI,BR,IN&ipsTechSelValues=3,4,6,7>

## Status (2026-09-29)

- `01_query_form_fields_2026-09-29.jpg`: the query form filled in, showing the selected fields of technology.
- Running the search returned WIPO's page "Technical error — Sorry. Some technical error found on our server, please try later." The server responded HTTP 500. It was tried 3 times: 2014–2024, 2014–2023 and 2020–2023.
- **Pending:**
  - retry the link above;
  - take screenshots of the results table;
  - download the data (export button on the results page) into this folder, e.g. `wipo_patents_by_tech_origin.csv`.
