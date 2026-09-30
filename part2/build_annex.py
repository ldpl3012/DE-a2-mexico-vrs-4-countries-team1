"""Build the Part II annex (annex/annex.html) from proposal.md. Requires pandoc.

Print it to PDF with Chrome (see part2/README.md). File links point to the team repository,
so they keep working inside the PDF.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = "https://github.com/ldpl3012/DE-a2-mexico-vrs-4-countries-team1"
BLOB, TREE = f"{REPO}/blob/master/part2/", f"{REPO}/tree/master/part2/"


def main():
    md = (HERE / "proposal.md").read_text(encoding="utf-8")
    # The annex has its own title block, so skip the working-document header of proposal.md.
    md = md[md.index("**Guiding question.**"):]
    html = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"], input=md,
                          capture_output=True, text=True, check=True).stdout
    # In print the full pipeline is too small to read; the compact version keeps the text legible.
    html = html.replace('src="diagrams/pipeline.svg"', 'src="diagrams/pipeline_compact.svg" class="compact"')
    html = re.sub(r'src="(diagrams|charts)/', r'src="../\1/', html)
    html = re.sub(r'href="((?:wipo/|evidence_log\.csv|diagrams/|charts/)[^"]*)"',
                  lambda m: f'href="{TREE if m.group(1).endswith("/") else BLOB}{m.group(1)}"', html)
    template = (HERE / "annex" / "_template.html").read_text(encoding="utf-8")
    target = HERE / "annex" / "annex.html"
    target.write_text(template.replace("%%BODY%%", html), encoding="utf-8")
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
