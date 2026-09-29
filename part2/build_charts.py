"""Build Part II evidence charts from the Part I raw data (standard library only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = Path(__file__).resolve().parent / "charts"

YEARS = list(range(2014, 2025))
NAMES = {"MEX": "Mexico", "BRA": "Brazil", "KOR": "South Korea", "FIN": "Finland", "IND": "India"}
# Highlighted series use validated categorical slots 1-2; peers stay in muted gray for context.
COLORS = {"MEX": "#2a78d6", "BRA": "#eb6834"}
CONTEXT = "#c3c2b7"
INK, INK_2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"


def series(code: str) -> dict[str, dict[int, float]]:
    rows = json.loads((RAW / f"world_bank_{code}.json").read_text(encoding="utf-8"))[1]
    out: dict[str, dict[int, float]] = {c: {} for c in NAMES}
    for r in rows:
        c, v = r["countryiso3code"], r["value"]
        if c in out and v is not None and int(r["date"]) in YEARS:
            out[c][int(r["date"])] = float(v)
    return out


def fixed_broadband_chart(compact: bool = False) -> str:
    """Full chart with title, or a compact variant (no title, larger text) for the 2-page brief."""
    data = series("IT.NET.BBND.P2")
    w, h = (470, 290) if compact else (760, 430)
    left, right, top, bottom = (34, 140, 34, 26) if compact else (48, 150, 92, 44)
    fs = 1.18 if compact else 1.0  # font scale
    pw, ph = w - left - right, h - top - bottom
    ymax = 50
    x = lambda yr: left + (yr - YEARS[0]) / (YEARS[-1] - YEARS[0]) * pw
    y = lambda v: top + ph - v / ymax * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
             'font-family="system-ui, -apple-system, \'Segoe UI\', Arial, sans-serif" role="img" '
             'aria-labelledby="t d">',
             '<title id="t">Since 2021, Brazil has pulled ahead of Mexico in fixed broadband</title>',
             '<desc id="d">Line chart of fixed broadband subscriptions per 100 people, 2014 to 2024, for Mexico, '
             'Brazil, South Korea, Finland and India.</desc>',
             f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>']
    if not compact:
        parts += [f'<text x="{left}" y="30" font-size="17" font-weight="700" fill="{INK}">'
                  'Since 2021, Brazil has pulled ahead of Mexico in fixed broadband</text>',
                  f'<text x="{left}" y="52" font-size="12.5" fill="{INK_2}">'
                  'Fixed broadband subscriptions per 100 people, 2014–2024</text>']
    ly = 14 if compact else 72
    # Legend (identity never relies on colour alone: end labels repeat the names).
    lx = left
    for label, color, width in (("Mexico", COLORS["MEX"], 2.5), ("Brazil", COLORS["BRA"], 2.5), ("Other peers", CONTEXT, 2)):
        parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 18}" y2="{ly}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
        parts.append(f'<text x="{lx + 24}" y="{ly + 4}" font-size="{12 * fs:.1f}" fill="{INK_2}">{label}</text>')
        lx += 24 + len(label) * 7 * fs + 22
    # Grid and axes (hairline, recessive).
    for v in range(0, ymax + 1, 10):
        stroke = AXIS if v == 0 else GRID
        parts.append(f'<line x1="{left}" y1="{y(v):.1f}" x2="{left + pw}" y2="{y(v):.1f}" stroke="{stroke}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 8}" y="{y(v) + 4:.1f}" font-size="{11 * fs:.1f}" fill="{MUTED}" text-anchor="end" '
                     f'style="font-variant-numeric: tabular-nums">{v}</text>')
    for yr in YEARS[::2]:
        parts.append(f'<text x="{x(yr):.1f}" y="{top + ph + 18 * fs:.1f}" font-size="{11 * fs:.1f}" fill="{MUTED}" text-anchor="middle" '
                     f'style="font-variant-numeric: tabular-nums">{yr}</text>')
    # Context lines first, highlighted lines on top with a surface ring for legibility.
    order = ["KOR", "FIN", "IND", "BRA", "MEX"]
    for c in order:
        pts = " ".join(f"{x(yr):.1f},{y(data[c][yr]):.1f}" for yr in YEARS if yr in data[c])
        color = COLORS.get(c, CONTEXT)
        if c in COLORS:
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{SURFACE}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{2.5 if c in COLORS else 2}" '
                     'stroke-linejoin="round" stroke-linecap="round"/>')
    # End markers and direct labels (value at the end of each line, text in ink).
    ends = {c: data[c][YEARS[-1]] for c in order}
    label_y = {c: y(v) for c, v in ends.items()}
    gap = 16 * fs
    if abs(label_y["BRA"] - label_y["MEX"]) < gap:  # keep the two close labels readable
        mid = (label_y["BRA"] + label_y["MEX"]) / 2
        label_y["BRA"], label_y["MEX"] = mid - gap / 2, mid + gap / 2
    for c in order:
        ex, ey = x(YEARS[-1]), y(ends[c])
        color = COLORS.get(c, CONTEXT)
        parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{color}" stroke="{SURFACE}" stroke-width="2"/>')
        weight = "700" if c in COLORS else "400"
        ink = INK if c in COLORS else INK_2
        parts.append(f'<text x="{ex + 10:.1f}" y="{label_y[c] + 4:.1f}" font-size="{12 * fs:.1f}" font-weight="{weight}" fill="{ink}">'
                     f'{NAMES[c]} {ends[c]:.1f}</text>')
    if not compact:  # the brief prints the source in its own caption
        parts.append(f'<text x="{left}" y="{h - 8}" font-size="10.5" fill="{MUTED}">'
                     'Source: ITU via World Bank WDI (IT.NET.BBND.P2), Part I raw data. Chart: Team 1.</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, compact in (("fixed_broadband_2014_2024.svg", False), ("fixed_broadband_2014_2024_brief.svg", True)):
        target = OUT / name
        target.write_text(fixed_broadband_chart(compact), encoding="utf-8")
        print(f"Wrote {target}")


if __name__ == "__main__":
    main()
