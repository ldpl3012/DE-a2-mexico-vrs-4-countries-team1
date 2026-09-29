"""Reproducible acquisition and analysis for Team 1 Digital Economy Lab."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
RAW, PROCESSED, DASH = ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "dashboard"
COUNTRIES = {"MEX": "Mexico", "KOR": "South Korea", "FIN": "Finland", "BRA": "Brazil", "IND": "India"}
# Category, source attribution, and any transformation before normalising.
INDICATORS = {
    "fixed_broadband_per_100": ("IT.NET.BBND.P2", "Infrastructure / connectivity", "ITU DataHub (published through World Bank WDI)", "subscriptions per 100 people", "none"),
    "mobile_subscriptions_per_100": ("IT.CEL.SETS.P2", "Infrastructure / connectivity", "ITU DataHub (published through World Bank WDI)", "subscriptions per 100 people", "none"),
    "internet_users_pct": ("IT.NET.USER.ZS", "Access / use", "ITU DataHub (published through World Bank WDI)", "% of population", "none"),
    "secure_servers_per_million": ("IT.NET.SECR.P6", "Quality / affordability", "World Bank WDI", "per 1 million people", "none"),
    "ict_service_exports_pct": ("BX.GSR.CCIS.ZS", "Digital economic activity", "World Bank WDI", "% of service exports", "none"),
    "high_tech_exports_pct": ("TX.VAL.TECH.MF.ZS", "Digital economic activity", "World Bank WDI", "% of manufactured exports", "none"),
    "rd_expenditure_pct_gdp": ("GB.XPD.RSDV.GD.ZS", "Technological capacity / innovation", "World Bank WDI", "% of GDP", "none"),
    "resident_patent_applications": ("IP.PAT.RESD", "Technological capacity / innovation", "WIPO IP Statistics (published through World Bank WDI)", "count", "ln(1 + x) before normalisation"),
}
BASE = "https://api.worldbank.org/v2/country/{countries}/indicator/{code}?format=json&per_page=1000"
ORIGIN_URL = {
    "ITU DataHub (published through World Bank WDI)": "https://datahub.itu.int/",
    "World Bank WDI": "https://data.worldbank.org/indicator/",
    "WIPO IP Statistics (published through World Bank WDI)": "https://www.wipo.int/en/web/ip-statistics",
}

def get_json(url: str):
    with urlopen(url, timeout=60) as response:
        return json.load(response)

def latest_by_country(records):
    chosen = {}
    for row in records:
        code = row.get("countryiso3code")
        value = row.get("value")
        if code in COUNTRIES and value is not None and code not in chosen:
            chosen[code] = {"value": float(value), "year": int(row["date"])}
    return chosen

def minmax(values):
    lo, hi = min(values), max(values)
    return [0.5] * len(values) if math.isclose(lo, hi) else [(v - lo) / (hi - lo) for v in values]

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)

def main():
    RAW.mkdir(parents=True, exist_ok=True); PROCESSED.mkdir(parents=True, exist_ok=True); DASH.mkdir(parents=True, exist_ok=True)
    gathered, provenance = {}, []
    country_query = ";".join(COUNTRIES)
    for slug, (code, category, provider, unit, transform) in INDICATORS.items():
        url = BASE.format(countries=country_query, code=code)
        raw_file = RAW / f"world_bank_{code}.json"
        # Preserve an already-downloaded original rather than silently replacing it.
        payload = json.loads(raw_file.read_text(encoding="utf-8")) if raw_file.exists() else get_json(url)
        if not raw_file.exists():
            raw_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        selected = latest_by_country(payload[1])
        missing = sorted(set(COUNTRIES) - set(selected))
        if missing:
            raise RuntimeError(f"{slug}: missing official observation for {missing}; no imputation is permitted.")
        gathered[slug] = selected
        provenance.append({"variable": slug, "official_indicator": payload[1][0]["indicator"]["value"], "indicator_code": code,
                           "category": category, "unit": unit, "official_source": provider, "api_endpoint": url,
                           "origin_url": ORIGIN_URL[provider],
                           "accessed_utc": "Generated when build_analysis.py runs", "observation_years": "; ".join(f"{COUNTRIES[c]}: {selected[c]['year']}" for c in COUNTRIES),
                           "method": "World Bank Indicators API JSON download; latest non-null observation per country", "transformation": transform,
                           "missing_data_treatment": "Complete-case check; stop pipeline rather than invent/impute values"})
    rows = []
    for code, country in COUNTRIES.items():
        row = {"country_code": code, "country": country}
        for slug in INDICATORS:
            row[slug] = gathered[slug][code]["value"]
            row[f"{slug}_year"] = gathered[slug][code]["year"]
        rows.append(row)
    # Equal weights prevent a subjective sectoral priority; patents are log-scaled only to reduce count skew.
    scores = {}
    for slug in INDICATORS:
        vals = [r[slug] for r in rows]
        if slug == "resident_patent_applications": vals = [math.log1p(v) for v in vals]
        scores[slug] = minmax(vals)
    for i, row in enumerate(rows):
        for slug in INDICATORS: row[f"{slug}_norm"] = round(scores[slug][i], 6)
        row["digital_readiness_score"] = round(sum(scores[s][i] * 0.125 for s in INDICATORS), 6)
    rows.sort(key=lambda r: r["digital_readiness_score"], reverse=True)
    fields = list(rows[0])
    write_csv(PROCESSED / "digital_economy_clean.csv", rows, fields)
    write_csv(ROOT / "source_log.csv", provenance, list(provenance[0]))
    dictionary = [{"variable": "country_code", "definition": "ISO 3166-1 alpha-3 country code", "unit": "code", "source": "World Bank API"},
                  {"variable": "country", "definition": "Country name", "unit": "text", "source": "World Bank API"},
                  {"variable": "digital_readiness_score", "definition": "Mean of the eight oriented min–max normalised indicator scores", "unit": "0–1", "source": "Team calculation"}]
    dictionary += [{"variable": p["variable"], "definition": p["official_indicator"], "unit": p["unit"], "source": p["official_source"]} for p in provenance]
    write_csv(ROOT / "data_dictionary.csv", dictionary, list(dictionary[0]))
    build_dashboard(rows)
    print(f"Created {PROCESSED / 'digital_economy_clean.csv'} with {len(rows)} countries and 8 indicators.")

def build_dashboard(rows):
    data = json.dumps(rows, ensure_ascii=False)
    labels = json.dumps(list(INDICATORS), ensure_ascii=False)
    template = (DASH / "_template.html").read_text(encoding="utf-8")
    html = template.replace("%%DATA%%", data).replace("%%LABELS%%", labels)
    (DASH / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__": main()
