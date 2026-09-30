# Part II — From Data to Digital Transformation

**Team 1:** Valeria Hernandez, Lorena Perez, Gustavo Fuentes, Jose Pech, Julio de Aquino, Ricardo Horta · **Professor:** Jose Francisco Perez Alcocer

Telecommunications · Proposal: **ConectaMapa**, a connectivity demand map that helps regional ISPs decide which underserved locality to connect next.

Part II builds on the Part I diagnosis: Mexico has 21.7 fixed broadband subscriptions per 100 people, 4th of 5. Part I files stay at the repository root; everything for Part II lives in this folder.

## Files

| File | Content |
|---|---|
| [`brief/Team1_Digital_Economy_Brief.pdf`](brief/Team1_Digital_Economy_Brief.pdf) | **Digital Economy Brief** (2 pages). Source: [`brief/brief.html`](brief/brief.html) |
| [`annex/Team1_Part2_Annex.pdf`](annex/Team1_Part2_Annex.pdf) | **Annex** (9 pages): the full analysis with all 13 sections, including the five-sector matrix, four-level analysis, business model, platform and scalability. Generated from `proposal.md` by [`build_annex.py`](build_annex.py) |
| [`proposal.md`](proposal.md) | Source text for the annex (all 13 sections); the brief is condensed from it. **Edit here, then rebuild the annex** |
| [`evidence_log.csv`](evidence_log.csv) | Every external figure used, with source, period, URL and access date (IDs `E1`–`E15`) |
| [`diagrams/pipeline.svg`](diagrams/pipeline.svg) | Pipeline diagram (full version); `pipeline_compact.svg` is the version used in the brief |
| [`charts/`](charts/) | Evidence chart: fixed broadband 2014–2024, Mexico vs Brazil and peers (full + brief versions) |
| [`build_charts.py`](build_charts.py) | Rebuilds the charts from the Part I raw data (`python part2/build_charts.py`, standard library only) |
| [`wipo/`](wipo/) | Mandatory WIPO IP Statistics query: exact query, screenshots, data (CSV) and results |

## Deliverables checklist

- [x] Digital Economy Brief, PDF, max. 2 pages
- [x] Digital transformation pipeline diagram
- [x] Comparative matrix of the five sectors (annex §1)
- [x] Four-level analysis: descriptive, diagnostic, predictive, prescriptive (annex §4, brief §4)
- [x] Business model, platform, network effects and scalability (annex §6–§8, brief §6–§8)
- [x] Evidence of the WIPO query (`wipo/`: query, 5 screenshots, data CSV, results; brief §5, annex §10)
- [x] Complementary visualization (fixed broadband, Mexico vs Brazil)

## Regenerating the PDFs

1. `python part2/build_charts.py` (charts) and `python part2/build_annex.py` (annex HTML from `proposal.md`; needs [pandoc](https://pandoc.org/)).
2. Open `part2/brief/brief.html` and `part2/annex/annex.html` in Chrome → Print → Save as PDF (Letter, no headers/footers). Or run it headless, e.g.:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --allow-file-access-from-files --print-to-pdf=part2/annex/Team1_Part2_Annex.pdf part2/annex/annex.html`
