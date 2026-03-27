#!/usr/bin/env python3
"""Generate a condensed LaTeX reading version of a paper."""

from __future__ import annotations

import argparse
from pathlib import Path

from paper_pipeline_common import (
    DEFAULT_GRAPH_PATH,
    build_prerequisite_appendix_items,
    condense_whitespace,
    derive_gap_explanation,
    ensure_title_and_author_commands,
    escape_latex_text,
    extract_abstract,
    is_probably_novel_section,
    load_analysis,
    load_main_tex,
    load_metadata,
    normalize_candidate_text,
    parse_top_level_sections,
    split_body_and_bibliography,
    split_document,
    summarize_section_with_graph,
    write_structured_prompt,
)


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate a condensed LaTeX document that keeps novel sections in full "
            "and compresses background to graph-linked summaries."
        )
    )
    parser.add_argument("--paper-dir", required=True, help="Directory containing main.tex, metadata.yaml, and analysis.yaml")
    parser.add_argument("--out", required=True, help="Output path for condensed.tex")
    parser.add_argument(
        "--graph",
        default=str(DEFAULT_GRAPH_PATH),
        help="Compiled graph JSON to use when summarizing background sections",
    )
    return parser


def section_mentions_term(section_text: str, term: str) -> bool:
    """Return whether a section likely mentions a concept."""

    normalized_section = normalize_candidate_text(section_text)
    normalized_term = normalize_candidate_text(term)
    return bool(normalized_term and normalized_term in normalized_section)


def section_is_novel(section, analysis: dict) -> bool:
    """Decide whether a section should be kept in full."""

    if is_probably_novel_section(section):
        return True
    for contribution in analysis.get("novel_contributions") or []:
        concept = str(contribution.get("concept", "")).strip()
        if concept and section_mentions_term(section.full_tex, concept):
            return True
    return False


def prerequisite_notes_for_section(section, analysis: dict) -> list[str]:
    """Collect gap explanations relevant to a novel section."""

    notes: list[str] = []
    seen: set[str] = set()
    for gap in analysis.get("gaps") or []:
        concept = str(gap.get("concept", "")).strip()
        if not concept:
            continue
        if not section_mentions_term(section.full_tex, concept):
            continue
        explanation = derive_gap_explanation(gap)
        if explanation in seen:
            continue
        seen.add(explanation)
        related = gap.get("related_graph_nodes") or []
        related_refs = ", ".join(
            f"{item.get('label', item.get('id', ''))} ({item.get('id', '')})"
            for item in related[:3]
            if item.get("id")
        )
        if related_refs:
            notes.append(f"{explanation} Related graph nodes: {related_refs}.")
        else:
            notes.append(explanation)
    return notes


def render_minimal_background(notes: list[str]) -> str:
    """Render minimal prerequisite notes as a LaTeX paragraph."""

    if not notes:
        return ""
    body = " ".join(escape_latex_text(condense_whitespace(note)) for note in notes)
    return f"\\paragraph{{Minimal background.}} {body}\n"


def render_background_summary(section, graph_path: str | Path) -> str:
    """Render a condensed summary for a background section."""

    summary = summarize_section_with_graph(section, graph_path=graph_path, limit=3)
    return (
        f"{section.heading_tex}\n\n"
        f"\\noindent\\textit{{Condensed background.}} {escape_latex_text(summary)}\n"
    )


def render_novel_section(section, analysis: dict) -> str:
    """Render a novel section with inline prerequisite notes."""

    notes = prerequisite_notes_for_section(section, analysis)
    pieces = [section.heading_tex, ""]
    minimal_background = render_minimal_background(notes)
    if minimal_background:
        pieces.append(minimal_background.rstrip())
        pieces.append("")
    pieces.append(section.content_tex.strip())
    return "\n".join(piece for piece in pieces if piece is not None).rstrip() + "\n"


def build_reading_guide(sections, analysis: dict) -> str:
    """Build the condensed paper's reading guide."""

    kept = sum(section_is_novel(section, analysis) for section in sections)
    condensed = max(len(sections) - kept, 0)
    gap_count = len(analysis.get("gaps") or [])
    return (
        "This version keeps sections that appear to contain the paper's main contributions in full, "
        f"while condensing {condensed} background sections into graph-linked summaries. "
        f"It also inserts minimal prerequisite notes for {gap_count} uncovered concepts so the novel parts are easier to read in one pass."
    )


def append_prerequisites_appendix(analysis: dict) -> str:
    """Render the knowledge-graph prerequisite appendix."""

    items = build_prerequisite_appendix_items(analysis)
    if not items:
        return "\\appendix\n\\section*{Prerequisites from knowledge graph}\nNo graph-backed prerequisites were identified.\n"
    lines = ["\\appendix", "\\section*{Prerequisites from knowledge graph}", "\\begin{itemize}"]
    for item in items:
        lines.append(f"\\item {escape_latex_text(item)}")
    lines.append("\\end{itemize}")
    return "\n".join(lines) + "\n"


def condense_paper(
    paper_dir: str | Path,
    out_path: str | Path,
    graph_path: str | Path = DEFAULT_GRAPH_PATH,
) -> Path:
    """Generate a condensed LaTeX document for a staged paper."""

    paper_path = Path(paper_dir)
    metadata = load_metadata(paper_path)
    analysis = load_analysis(paper_path)
    tex = load_main_tex(paper_path)

    preamble, body = split_document(tex)
    body = body.rsplit(r"\end{document}", 1)[0]
    abstract_env = extract_abstract(body)
    body = body.replace(abstract_env, "", 1) if abstract_env else body
    body, bibliography = split_body_and_bibliography(body)
    sections = parse_top_level_sections(body)

    preamble = ensure_title_and_author_commands(
        preamble,
        str(metadata.get("title", "Untitled paper")),
        [str(author) for author in metadata.get("authors", [])],
    )

    rendered_sections: list[str] = []
    for section in sections:
        if section_is_novel(section, analysis):
            rendered_sections.append(render_novel_section(section, analysis))
        else:
            rendered_sections.append(render_background_summary(section, graph_path))

    guide = build_reading_guide(sections, analysis)
    appendix = append_prerequisites_appendix(analysis)

    pieces = [
        preamble.rstrip(),
        "",
        "\\begin{document}",
        "\\maketitle",
        "",
    ]
    if abstract_env:
        pieces.extend([abstract_env.strip(), ""])
    pieces.extend(
        [
            "\\section*{Reading guide}",
            escape_latex_text(guide),
            "",
            *rendered_sections,
            appendix.rstrip(),
        ]
    )
    if bibliography.strip():
        pieces.extend(["", bibliography.strip()])
    pieces.extend(["", "\\end{document}", ""])
    rendered = "\n".join(piece for piece in pieces if piece is not None)

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

    prompt_payload = {
        "task": "Review and improve a condensed paper LaTeX draft",
        "paper_dir": str(paper_path),
        "condensed_output": str(output),
        "instructions": [
            "Keep novel sections intact unless there is clear background-only material inside them.",
            "Strengthen the reading guide and condensed background summaries.",
            "Make prerequisite notes minimal but sufficient to read the kept sections.",
        ],
        "analysis": {
            "gaps": analysis.get("gaps") or [],
            "novel_contributions": analysis.get("novel_contributions") or [],
        },
        "required_output_schema": {
            "reading_guide": "string",
            "background_section_summaries": [
                {
                    "section_title": "string",
                    "summary": "string",
                }
            ],
            "prerequisite_notes": [
                {
                    "section_title": "string",
                    "notes": ["string"],
                }
            ],
        },
    }
    write_structured_prompt(paper_path, "condense_review", prompt_payload)
    return output


def main() -> int:
    """CLI entrypoint."""

    args = build_parser().parse_args()
    output = condense_paper(args.paper_dir, args.out, args.graph)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
