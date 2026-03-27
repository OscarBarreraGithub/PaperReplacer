#!/usr/bin/env python3
"""Insert background annotations into a paper's LaTeX source."""

from __future__ import annotations

import argparse
from pathlib import Path

from paper_pipeline_common import (
    derive_gap_explanation,
    ensure_usepackage,
    escape_latex_text,
    find_best_insertion_line,
    find_document_body_start_line,
    load_analysis,
    load_main_tex,
    write_structured_prompt,
)


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Insert blue background explanations after the first mention of each "
            "gap concept listed in analysis.yaml."
        )
    )
    parser.add_argument("--paper-dir", required=True, help="Directory containing main.tex and analysis.yaml")
    parser.add_argument("--out", required=True, help="Output path for the annotated LaTeX file")
    return parser


def build_annotation_block(explanation: str) -> str:
    """Format a gap explanation as a blue LaTeX annotation."""

    return rf"\textcolor{{blue}}{{\small [Background: {escape_latex_text(explanation)}]}}"


def annotate_paper(paper_dir: str | Path, out_path: str | Path) -> Path:
    """Annotate a paper with background notes after the first mention of each gap."""

    paper_path = Path(paper_dir)
    tex = ensure_usepackage(load_main_tex(paper_path), "xcolor")
    analysis = load_analysis(paper_path)

    lines = tex.splitlines()
    body_start = find_document_body_start_line(lines)
    insertions: dict[int, list[str]] = {}
    unresolved: list[dict[str, str]] = []

    for gap in analysis.get("gaps") or []:
        concept = str(gap.get("concept", "")).strip()
        if not concept:
            continue
        explanation = derive_gap_explanation(gap)
        target_line = find_best_insertion_line(lines, concept, start_index=body_start)
        if target_line is None:
            target_line = body_start
            unresolved.append({"concept": concept, "explanation": explanation})
        insertions.setdefault(target_line, []).append(build_annotation_block(explanation))

    rendered_lines: list[str] = []
    for index, line in enumerate(lines):
        rendered_lines.append(line)
        for block in insertions.get(index, []):
            rendered_lines.append(block)
            rendered_lines.append("")

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(rendered_lines).rstrip() + "\n", encoding="utf-8")

    prompt_payload = {
        "task": "Rewrite and tighten inline background annotations for a LaTeX paper",
        "paper_dir": str(paper_path),
        "annotated_output": str(output),
        "instructions": [
            "For each gap concept, keep the annotation concise and faithful to nearby graph summaries.",
            "Return one polished annotation string per gap concept.",
            "Do not remove the LaTeX wrapper; only improve the explanation text inside it.",
        ],
        "gaps": analysis.get("gaps") or [],
        "unresolved_mentions": unresolved,
        "required_output_schema": {
            "annotations": [
                {
                    "concept": "string",
                    "annotation_text": "string",
                }
            ]
        },
    }
    write_structured_prompt(paper_path, "annotation_review", prompt_payload)
    return output


def main() -> int:
    """CLI entrypoint."""

    args = build_parser().parse_args()
    output = annotate_paper(args.paper_dir, args.out)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
