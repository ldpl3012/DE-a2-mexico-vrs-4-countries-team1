"""Reproducible acquisition and analysis for Team 1 Digital Economy Lab."""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
RAW, PROCESSED, DASH = ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "dashboard"
DOWNLOAD_LOG = ROOT / "data" / "download_log.csv"
COUNTRIES = {"MEX": "Mexico", "KOR": "South Korea", "FIN": "Finland", "BRA": "Brazil", "IND": "India"}
# Code, category, unit, and the original producer's portal.
INDICATORS = {
    "fixed_broadband_per_100": ("IT.NET.BBND.P2", "Infrastructure / connectivity", "subscriptions per 100 people", "https://datahub.itu.int/"),
    "mobile_subscriptions_per_100": ("IT.CEL.SETS.P2", "Infrastructure / connectivity", "subscriptions per 100 people", "https://datahub.itu.int/"),
    "internet_users_pct": ("IT.NET.USER.ZS", "Access / use", "% of population", "https://datahub.itu.int/"),
    "secure_servers_per_million": ("IT.NET.SECR.P6", "Quality / affordability (quality proxy)", "per 1 million people", "https://data.worldbank.org/indicator/IT.NET.SECR.P6"),
    "ict_service_exports_pct": ("BX.GSR.CCIS.ZS", "Digital economic activity", "% of service exports", "https://data.worldbank.org/indicator/BX.GSR.CCIS.ZS"),
    "high_tech_exports_pct": ("TX.VAL.TECH.MF.ZS", "Digital economic activity", "% of manufactured exports", "https://data.worldbank.org/indicator/TX.VAL.TECH.MF.ZS"),
    "rd_expenditure_pct_gdp": ("GB.XPD.RSDV.GD.ZS", "Technological capacity / innovation", "% of GDP", "https://data.worldbank.org/indicator/GB.XPD.RSDV.GD.ZS"),
    "resident_patent_applications": ("IP.PAT.RESD", "Technological capacity / innovation", "count", "https://www.wipo.int/en/web/ip-statistics"),
}
BASE = "https://api.worldbank.org/v2/country/{countries}/indicator/{code}?format=json&per_page=1000"
META = "https://api.worldbank.org/v2/indicator/{code}?format=json"
DELIVERY = "World Bank World Development Indicators API"
# The reference year is the latest one reported by at least this many of the five economies,
# so at most one economy is compared on an older observation.
MIN_REPORTING = 4
# An indicator whose max/min ratio across the five economies exceeds this is log-scaled (ln(1 + x))
# before normalising, so one extreme value does not squeeze the other four towards 0.
LOG_RATIO = 100

def read_download_log():
    if not DOWNLOAD_LOG.exists():
        return {}
    with DOWNLOAD_LOG.open(encoding="utf-8", newline="") as fh:
        return {row["file"]: row for row in csv.DictReader(fh)}

def fetch_raw(url: str, path: Path, log: dict):
    """Return the parsed JSON, downloading it once and keeping the response bytes untouched."""
    if not path.exists():
        with urlopen(url, timeout=60) as response:
            path.write_bytes(response.read())
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        log[path.relative_to(ROOT).as_posix()] = {"file": path.relative_to(ROOT).as_posix(), "url": url, "accessed_utc": stamp,
                                                  "note": "Downloaded by build_analysis.py; response bytes saved unmodified"}
    return json.loads(path.read_text(encoding="utf-8"))

def select_observations(records):
    series = {code: {} for code in COUNTRIES}
    for row in records:
        code, value = row.get("countryiso3code"), row.get("value")
        # None means "not available"; an observed 0 is kept as a real value.
        if code in COUNTRIES and value is not None:
            series[code][int(row["date"])] = float(value)
    coverage = Counter(year for years in series.values() for year in years)
    reference = max((year for year, n in coverage.items() if n >= MIN_REPORTING), default=None)
    chosen = {}
    for code, years in series.items():
        eligible = [year for year in years if reference is not None and year <= reference]
        if eligible:
            chosen[code] = {"value": years[max(eligible)], "year": max(eligible)}
    return reference, chosen

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
    log = read_download_log()
    gathered, log_scaled, provenance = {}, {}, []
    country_query = ";".join(COUNTRIES)
    for slug, (code, category, unit, origin_url) in INDICATORS.items():
        url, meta_url = BASE.format(countries=country_query, code=code), META.format(code=code)
        raw_file = RAW / f"world_bank_{code}.json"
        payload = fetch_raw(url, raw_file, log)
        meta = fetch_raw(meta_url, RAW / f"world_bank_metadata_{code}.json", log)[1][0]
        reference, selected = select_observations(payload[1])
        missing = sorted(set(COUNTRIES) - set(selected))
        if missing:
            raise RuntimeError(f"{slug}: missing official observation for {missing}; no imputation is permitted.")
        gathered[slug] = selected
        values = [selected[c]["value"] for c in COUNTRIES]
        ratio = max(values) / min(values) if min(values) > 0 else math.inf
        log_scaled[slug] = ratio > LOG_RATIO
        transform = f"ln(1 + x) before normalisation (max/min = {ratio:.0f} > {LOG_RATIO})" if log_scaled[slug] else f"none (max/min = {ratio:.1f} <= {LOG_RATIO})"
        exceptions = [f"{COUNTRIES[c]}: {selected[c]['year']} (latest available; {reference} not reported)" for c in COUNTRIES if selected[c]["year"] != reference]
        provenance.append({"variable": slug, "official_indicator": meta["name"], "indicator_code": code, "category": category,
                           "definition": " ".join(meta["sourceNote"].split()), "unit": unit,
                           "original_producer": " ".join(meta["sourceOrganization"].split()), "delivery_channel": DELIVERY,
                           "api_endpoint": url, "metadata_endpoint": meta_url, "origin_url": origin_url,
                           "raw_file": raw_file.relative_to(ROOT).as_posix(),
                           "accessed_utc": log.get(raw_file.relative_to(ROOT).as_posix(), {}).get("accessed_utc", "not recorded"),
                           "reference_year": reference,
                           "observation_years": "; ".join(f"{COUNTRIES[c]}: {selected[c]['year']}" for c in COUNTRIES),
                           "year_exceptions": "; ".join(exceptions) or "none",
                           "method": f"World Bank Indicators API JSON download; common reference year = latest year reported by at least {MIN_REPORTING} of 5 economies; an economy without it uses its latest earlier observation",
                           "transformation": transform,
                           "missing_data_treatment": "Null = not available and never replaced; 0 = observed zero. Complete-case check: stop the pipeline rather than invent/impute values"})
    write_csv(DOWNLOAD_LOG, sorted(log.values(), key=lambda r: r["file"]), ["file", "url", "accessed_utc", "note"])
    rows = []
    for code, country in COUNTRIES.items():
        row = {"country_code": code, "country": country}
        for slug in INDICATORS:
            row[slug] = gathered[slug][code]["value"]
            row[f"{slug}_year"] = gathered[slug][code]["year"]
        rows.append(row)
    # Equal weights prevent a subjective sectoral priority; log scaling only tames extreme max/min ratios.
    scores = {}
    for slug in INDICATORS:
        vals = [r[slug] for r in rows]
        if log_scaled[slug]: vals = [math.log1p(v) for v in vals]
        scores[slug] = minmax(vals)
    for i, row in enumerate(rows):
        for slug in INDICATORS: row[f"{slug}_norm"] = round(scores[slug][i], 6)
        row["digital_readiness_score"] = round(sum(scores[s][i] * 0.125 for s in INDICATORS), 6)
    rows.sort(key=lambda r: r["digital_readiness_score"], reverse=True)
    fields = list(rows[0])
    write_csv(PROCESSED / "digital_economy_clean.csv", rows, fields)
    write_csv(ROOT / "source_log.csv", provenance, list(provenance[0]))
    write_csv(ROOT / "data_dictionary.csv", build_dictionary(fields, provenance), ["variable", "definition", "type", "unit", "source"])
    build_dashboard(rows)
    print(f"Created {PROCESSED / 'digital_economy_clean.csv'} with {len(rows)} countries and 8 indicators.")

def build_dictionary(fields, provenance):
    by_slug = {p["variable"]: p for p in provenance}
    entries = {"country_code": ("ISO 3166-1 alpha-3 country code", "categorical (text)", "code", "World Bank API"),
               "country": ("Country name", "categorical (text)", "text", "World Bank API"),
               "digital_readiness_score": ("Digital Readiness Score: equal-weight (1/8) sum of the eight *_norm scores", "continuous", "0–1", "Team calculation")}
    for slug, p in by_slug.items():
        kind = "count (integer-valued)" if p["unit"] == "count" else "continuous (ratio)"
        entries[slug] = (f"{p['official_indicator']}. {p['definition']}", kind, p["unit"], f"{p['original_producer']} (via {DELIVERY})")
        entries[f"{slug}_year"] = (f"Observation year of {slug} for this country (reference year {p['reference_year']})", "integer (year)", "year", "World Bank API 'date' field")
        entries[f"{slug}_norm"] = (f"Min–max normalised {slug} across the five economies (0 = lowest, 1 = highest); transformation before scaling: {p['transformation']}",
                                   "continuous", "0–1", "Team calculation")
    return [dict(zip(["variable", "definition", "type", "unit", "source"], (f, *entries[f]))) for f in fields]

def build_dashboard(rows):
    data = json.dumps(rows, ensure_ascii=False)
    labels = json.dumps(list(INDICATORS), ensure_ascii=False)
    template = (DASH / "_template.html").read_text(encoding="utf-8")
    html = template.replace("%%DATA%%", data).replace("%%LABELS%%", labels)
    (DASH / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__": main()
