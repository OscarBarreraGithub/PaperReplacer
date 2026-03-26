#!/usr/bin/env python3
"""Summarize per-document triage reports into stable JSON and Markdown outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from document_pipeline import DEFAULT_ORACLE_ROOT, REPORT_SECTIONS, render_triage_summary_markdown, summarize_triage_reports


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--triage-dir")
    parser.add_argument("--json-out")
    parser.add_argument("--md-out")
    parser.add_argument("--title")
    parser.add_argument("--report-glob", default="*.md")
    parser.add_argument("--report-pattern", default=r"(.+)\.md$")
    parser.add_argument("--section", action="append", dest="sections")
    args = parser.parse_args()

    doc_root = DEFAULT_ORACLE_ROOT / args.doc_id
    triage_dir = Path(args.triage_dir) if args.triage_dir else doc_root / "triage"
    json_out = Path(args.json_out) if args.json_out else doc_root / "triage_summary.json"
    md_out = Path(args.md_out) if args.md_out else doc_root / "triage_summary.md"
    title = args.title or f"{args.doc_id} oracle triage summary"
    sections = tuple(args.sections or REPORT_SECTIONS)

    payload = summarize_triage_reports(
        triage_dir,
        sections=sections,
        report_glob=args.report_glob,
        report_pattern=args.report_pattern,
    )

    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2))
    md_out.write_text(render_triage_summary_markdown(title, payload, sections=sections))

    print(
        json.dumps(
            {
                "doc_id": args.doc_id,
                "triage_dir": str(triage_dir),
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
