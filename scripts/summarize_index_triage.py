#!/usr/bin/env python3
"""Summarize document or index triage reports into one backlog view."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from document_pipeline import REPORT_SECTIONS, render_triage_summary_markdown, summarize_triage_reports


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRIAGE_DIR = ROOT / "data" / "generated" / "index_triage"
DEFAULT_JSON = ROOT / "data" / "generated" / "extracted" / "schwartz_index_summary.json"
DEFAULT_MD = ROOT / "data" / "generated" / "extracted" / "schwartz_index_summary.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--triage-dir", default=str(DEFAULT_TRIAGE_DIR))
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    parser.add_argument("--title", default="Schwartz Index Summary")
    parser.add_argument("--report-glob", default="page_*.md")
    parser.add_argument("--report-pattern", default=r"page_(\d+)\.md$")
    parser.add_argument("--section", action="append", dest="sections")
    args = parser.parse_args()

    triage_dir = Path(args.triage_dir)
    sections = tuple(args.sections or REPORT_SECTIONS)
    payload = summarize_triage_reports(
        triage_dir,
        sections=sections,
        report_glob=args.report_glob,
        report_pattern=args.report_pattern,
    )

    json_out = Path(args.json_out)
    md_out = Path(args.md_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    json_out.write_text(json.dumps(payload, indent=2))
    md_out.write_text(render_triage_summary_markdown(args.title, payload, sections=sections))
    print(
        json.dumps(
            {
                "reports_parsed": payload["report_count"],
                "json_out": str(json_out),
                "md_out": str(md_out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
