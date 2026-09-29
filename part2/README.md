# Part II — From Data to Digital Transformation

Team 1 · Telecommunications · Proposal: **ConectaMapa**, a connectivity demand map that helps regional ISPs decide which underserved locality to connect next.

Part II builds on the Part I diagnosis: Mexico has 21.7 fixed broadband subscriptions per 100 people, 4th of 5. Part I files stay at the repository root; everything for Part II lives in this folder.

## Files

| File | Content |
|---|---|
| [`brief/Team1_Digital_Economy_Brief.pdf`](brief/Team1_Digital_Economy_Brief.pdf) | **Digital Economy Brief** (2 pages). Source: [`brief/brief.html`](brief/brief.html) |
| [`proposal.md`](proposal.md) | Full working document with all 13 sections; the brief is condensed from it |
| [`evidence_log.csv`](evidence_log.csv) | Every external figure used, with source, period, URL and access date (IDs `E1`–`E11`) |
| [`diagrams/pipeline.svg`](diagrams/pipeline.svg) | Pipeline diagram (full version); `pipeline_compact.svg` is the version used in the brief |
| [`charts/`](charts/) | Evidence chart: fixed broadband 2014–2024, Mexico vs Brazil and peers (full + brief versions) |
| [`build_charts.py`](build_charts.py) | Rebuilds the charts from the Part I raw data (`python part2/build_charts.py`, standard library only) |
| [`wipo/`](wipo/) | Mandatory WIPO IP Statistics query: exact query, link and evidence |

## Deliverables checklist

- [x] Digital Economy Brief, PDF, max. 2 pages (draft; the WIPO figures are still pending)
- [x] Digital transformation pipeline diagram
- [x] Comparative matrix of the five sectors (`proposal.md` §1)
- [x] Four-level analysis: descriptive, diagnostic, predictive, prescriptive (`proposal.md` §4, brief §4)
- [x] Business model, platform, network effects and scalability (`proposal.md` §6–§8, brief §5–§7)
- [ ] **Evidence of the WIPO query**: the query is set up, but the WIPO server returned an error on 2026-09-29 (see `wipo/README.md`)
- [x] Complementary visualization (fixed broadband, Mexico vs Brazil)

## Regenerating the brief PDF

1. `python part2/build_charts.py`
2. Open `part2/brief/brief.html` in Chrome → Print → Save as PDF (Letter, no headers/footers). Or run it headless:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --allow-file-access-from-files --print-to-pdf=part2/brief/Team1_Digital_Economy_Brief.pdf part2/brief/brief.html`

The drafts still need team review before they are final.
