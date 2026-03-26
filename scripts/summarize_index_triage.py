#!/usr/bin/env python3
"""Summarize per-page Schwartz index triage reports into one backlog view."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRIAGE_DIR = ROOT / "data" / "generated" / "index_triage"
DEFAULT_JSON = ROOT / "data" / "generated" / "extracted" / "schwartz_index_summary.json"
DEFAULT_MD = ROOT / "data" / "generated" / "extracted" / "schwartz_index_summary.md"

SECTION_NAMES = {
    "covered_existing",
    "candidate_batch_expansion",
    "candidate_new_node",
    "skip_non_ontology",
}


def parse_report(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = defaultdict(list)
    current: str | None = None
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            name = line[3:].strip()
            current = name if name in SECTION_NAMES else None
            continue
        if line.startswith("| term | classification | best match / proposed namespace |"):
            current = "__three_column_table__"
            continue
        if line.startswith("| term | match |") or line.startswith("| term | best match |") or line.startswith("| term | proposed namespace |") or line.startswith("| term | reason |"):
            continue
        if line.startswith("| ---"):
            continue
        if current and line.startswith("- "):
            sections[current].append(line[2:].strip())
            continue
        if current in SECTION_NAMES and line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells and cells[0].lower() == "term":
                continue
            sections[current].append(" | ".join(cells))
            continue
        if current == "__three_column_table__" and line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) == 3:
                term, classification, match = cells
                classification = classification.strip()
                if classification in SECTION_NAMES:
                    sections[classification].append(f"{term} | {match}")
    return sections


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--triage-dir", default=str(DEFAULT_TRIAGE_DIR))
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args()

    triage_dir = Path(args.triage_dir)
    reports = sorted(triage_dir.glob("page_*.md"))

    payload: dict[str, object] = {
        "report_count": len(reports),
        "pages": {},
        "totals": {},
    }
    totals: dict[str, list[str]] = defaultdict(list)

    for report in reports:
        match = re.search(r"page_(\d+)\.md$", report.name)
        page = match.group(1) if match else report.stem
        parsed = parse_report(report)
        payload["pages"][page] = parsed
        for section, items in parsed.items():
            totals[section].extend(items)

    payload["totals"] = {key: len(value) for key, value in totals.items()}

    json_out = Path(args.json_out)
    md_out = Path(args.md_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    json_out.write_text(json.dumps(payload, indent=2))

    lines = [
        "# Schwartz Index Summary",
        "",
        f"- reports parsed: {len(reports)}",
        "",
        "## Totals",
    ]
    for section in sorted(SECTION_NAMES):
        lines.append(f"- `{section}`: {len(totals.get(section, []))}")
    lines.append("")
    lines.append("## Pages")
    for report in reports:
        match = re.search(r"page_(\d+)\.md$", report.name)
        page = match.group(1) if match else report.stem
        lines.append(f"- page {page}")
        parsed = payload["pages"][page]
        for section in sorted(SECTION_NAMES):
            count = len(parsed.get(section, []))
            lines.append(f"  - {section}: {count}")

    md_out.write_text("\n".join(lines) + "\n")
    print(
        json.dumps(
            {
                "reports_parsed": len(reports),
                "json_out": str(json_out),
                "md_out": str(md_out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
