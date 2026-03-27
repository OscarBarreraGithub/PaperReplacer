#!/usr/bin/env python3
"""Analyze a staged paper against the compiled knowledge graph."""

from __future__ import annotations

from collections import defaultdict
import argparse
from pathlib import Path
from typing import Any

from paper_pipeline_common import (
    DEFAULT_GRAPH_PATH,
    CandidateConcept,
    deduplicate_candidates,
    extract_candidate_concepts,
    extract_novel_contributions,
    graph_index,
    is_probably_novel_section,
    is_strong_graph_match,
    load_main_tex,
    match_text_against_graph,
    node_match_payload,
    normalize_candidate_text,
    parse_top_level_sections,
    snippet_from_text,
    split_document,
    tex_to_plain_text,
    utc_timestamp,
    write_structured_prompt,
    write_yaml_file,
)


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Extract concept coverage, gaps, likely novel contributions, and quiz "
            "questions for a paper using the compiled knowledge graph."
        )
    )
    parser.add_argument("--paper-dir", required=True, help="Directory containing main.tex and metadata.yaml")
    parser.add_argument(
        "--graph",
        default=str(DEFAULT_GRAPH_PATH),
        help="Compiled graph JSON to match against",
    )
    return parser


def section_level_matches(tex: str, graph_path: str | Path) -> list[CandidateConcept]:
    """Create graph-guided concept candidates from top-level sections."""

    _, body = split_document(tex)
    body = body.rsplit(r"\end{document}", 1)[0]
    sections = parse_top_level_sections(body)
    candidates: list[CandidateConcept] = []
    for section in sections:
        query_text = f"{section.title_text}\n{tex_to_plain_text(section.content_tex[:2200])}"
        for match in match_text_against_graph(query_text, graph_path=graph_path, top_n=4):
            label = match.label or match.node_id
            candidates.append(
                CandidateConcept(
                    concept=label,
                    context_snippet=snippet_from_text(section.full_tex),
                    source="section_graph_match",
                    weight=6.5 if is_probably_novel_section(section) else 5.5,
                    novelty_score=1.0 if is_probably_novel_section(section) else 0.0,
                )
            )
    return deduplicate_candidates(candidates)


def classify_candidate(
    candidate: CandidateConcept,
    graph_path: str | Path,
) -> dict[str, Any]:
    """Classify a candidate concept as in-graph, gap, or novel."""

    matches = match_text_against_graph(candidate.concept, graph_path=graph_path, top_n=3)
    strong_match = next((match for match in matches if is_strong_graph_match(candidate.concept, match, graph_path=graph_path)), None)
    lower_context = candidate.context_snippet.lower()
    novelty_cues = (
        candidate.novelty_score >= 1.0
        or any(marker in lower_context for marker in ("we propose", "we present", "we derive", "we prove", "we show", "our result"))
    )

    if strong_match is not None:
        payload = {
            "concept": candidate.concept,
            "classification": "in_graph",
            "matched_node_id": strong_match.node_id,
            "matched_node": node_match_payload(strong_match, graph_path=graph_path),
            "context_snippet": candidate.context_snippet,
            "source": candidate.source,
        }
        return payload

    related_nodes = [node_match_payload(match, graph_path=graph_path) for match in matches]
    if novelty_cues:
        description = candidate.context_snippet or f"The paper appears to introduce or extend {candidate.concept}."
        return {
            "concept": candidate.concept,
            "classification": "novel",
            "matched_node_id": None,
            "context_snippet": candidate.context_snippet,
            "source": candidate.source,
            "description": description,
            "related_graph_nodes": related_nodes,
        }

    labels = ", ".join(node["label"] for node in related_nodes[:3]) if related_nodes else "nearby prerequisites in the graph"
    summaries = " ".join(node["summary"] for node in related_nodes[:2] if node.get("summary"))
    suggested_explanation = (
        f"Briefly explain {candidate.concept} before it is used, and connect it to {labels}. {summaries}".strip()
    )
    why_needed = (
        f"The paper relies on {candidate.concept} in {candidate.source.replace('_', ' ')} context "
        f"without pausing to teach it. Readers need that prerequisite to follow the local argument."
    )
    return {
        "concept": candidate.concept,
        "classification": "gap",
        "matched_node_id": None,
        "context_snippet": candidate.context_snippet,
        "source": candidate.source,
        "why_needed": why_needed,
        "suggested_explanation": suggested_explanation,
        "related_graph_nodes": related_nodes,
    }


def merge_classifications(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate classified concept entries with a stable priority order."""

    priority = {"novel": 3, "gap": 2, "in_graph": 1}
    best_by_key: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if entry.get("classification") == "in_graph" and entry.get("matched_node_id"):
            key = f"in_graph::{entry['matched_node_id']}"
        else:
            key = f"{entry.get('classification')}::{normalize_candidate_text(str(entry.get('concept', '')))}"
        existing = best_by_key.get(key)
        if existing is None:
            best_by_key[key] = entry
            continue
        current_rank = (
            priority.get(str(entry.get("classification")), 0),
            len(str(entry.get("context_snippet", ""))),
            len(str(entry.get("concept", ""))),
        )
        existing_rank = (
            priority.get(str(existing.get("classification")), 0),
            len(str(existing.get("context_snippet", ""))),
            len(str(existing.get("concept", ""))),
        )
        if current_rank > existing_rank:
            best_by_key[key] = entry
    ordered = sorted(
        best_by_key.values(),
        key=lambda item: (
            {"in_graph": 0, "gap": 1, "novel": 2}.get(str(item.get("classification")), 3),
            str(item.get("concept", "")).lower(),
        ),
    )
    return ordered


def enrich_novel_contributions(
    raw_contributions: list[dict[str, str]],
    paper_concepts: list[dict[str, Any]],
    graph_path: str | Path,
) -> list[dict[str, str]]:
    """Merge heuristic novel contributions with classified novel concepts."""

    contributions: dict[str, dict[str, str]] = {}
    for contribution in raw_contributions:
        concept = contribution.get("concept", "").strip()
        if not concept:
            continue
        contributions[normalize_candidate_text(concept)] = {
            "concept": concept,
            "description": contribution.get("description", "").strip() or f"The paper contributes {concept}.",
        }
    for concept in paper_concepts:
        if concept.get("classification") != "novel":
            continue
        name = str(concept.get("concept", "")).strip()
        if not name:
            continue
        key = normalize_candidate_text(name)
        description = str(concept.get("description", "")).strip() or concept.get("context_snippet", "")
        if key not in contributions:
            contributions[key] = {
                "concept": name,
                "description": description,
            }
            continue
        if len(description) > len(contributions[key]["description"]):
            contributions[key]["description"] = description
    return sorted(contributions.values(), key=lambda item: item["concept"].lower())


def build_quiz_questions(
    paper_concepts: list[dict[str, Any]],
    novel_contributions: list[dict[str, str]],
) -> list[str]:
    """Generate 30 deterministic study questions from the analysis payload."""

    priority_buckets: list[tuple[str, str]] = []
    seen: set[str] = set()

    for contribution in novel_contributions:
        concept = contribution["concept"]
        key = normalize_candidate_text(concept)
        if key and key not in seen:
            priority_buckets.append((concept, "novel"))
            seen.add(key)

    for concept in paper_concepts:
        key = normalize_candidate_text(str(concept.get("concept", "")))
        if not key or key in seen:
            continue
        priority_buckets.append((str(concept["concept"]), str(concept["classification"])))
        seen.add(key)

    templates = {
        "novel": [
            "What is the paper's new claim or construction around {concept}?",
            "Which prerequisites does the reader need before {concept} becomes understandable?",
            "How does {concept} differ from the closest background already in the knowledge graph?",
        ],
        "gap": [
            "What background idea is missing when the paper first uses {concept}?",
            "How would you explain {concept} in two or three sentences before reading onward?",
            "Why does understanding {concept} matter for the paper's main argument?",
        ],
        "in_graph": [
            "How is {concept} used in this paper rather than in the abstract?",
            "What should a reader already know about {concept} from the knowledge graph?",
            "How does {concept} connect to the nearby derivation or section where it appears?",
        ],
    }

    questions: list[str] = []
    for concept, classification in priority_buckets:
        for template in templates.get(classification, templates["in_graph"]):
            questions.append(template.format(concept=concept))
            if len(questions) == 30:
                return questions

    fallback_concepts = [concept for concept, _ in priority_buckets] or ["the paper's central result"]
    fallback_index = 0
    while len(questions) < 30:
        concept = fallback_concepts[fallback_index % len(fallback_concepts)]
        questions.append(f"What part of the paper becomes clearer once you understand {concept}?")
        fallback_index += 1
    return questions


def build_prompt_payloads(
    paper_dir: Path,
    analysis_payload: dict[str, Any],
    graph_path: str | Path,
) -> dict[str, str]:
    """Write structured prompts for Codex-assisted review."""

    paper_concepts = analysis_payload["paper_concepts"]
    prompt_paths: dict[str, str] = {}

    analysis_prompt = {
        "task": "Review and refine paper concept classification against the knowledge graph",
        "paper_dir": str(paper_dir),
        "graph_path": str(Path(graph_path).resolve()),
        "instructions": [
            "Keep the schema exactly the same as analysis.yaml.",
            "Re-evaluate whether each concept is correctly labeled in_graph, gap, or novel.",
            "Tighten why_needed and suggested_explanation entries for gaps.",
            "Prefer graph-node references already surfaced in the related_graph_nodes fields.",
        ],
        "current_analysis": {
            "paper_concepts": paper_concepts,
            "gaps": analysis_payload["gaps"],
            "novel_contributions": analysis_payload["novel_contributions"],
        },
        "required_output_schema": {
            "paper_concepts": [
                {
                    "concept": "string",
                    "classification": "in_graph | gap | novel",
                    "matched_node_id": "string | null",
                    "context_snippet": "string",
                }
            ],
            "gaps": [
                {
                    "concept": "string",
                    "why_needed": "string",
                    "suggested_explanation": "string",
                }
            ],
            "novel_contributions": [
                {
                    "concept": "string",
                    "description": "string",
                }
            ],
        },
    }
    prompt_paths["analysis_review"] = str(
        write_structured_prompt(paper_dir, "analysis_review", analysis_prompt).relative_to(paper_dir)
    )

    quiz_prompt = {
        "task": "Generate 30 high-signal quiz questions for paper reading preparation",
        "paper_dir": str(paper_dir),
        "instructions": [
            "Write exactly 30 questions.",
            "Prioritize gap concepts and the paper's novel contributions.",
            "Questions should help a reader build the background needed to understand the paper.",
            "Avoid yes/no wording and avoid trivial citation questions.",
        ],
        "concepts_by_classification": defaultdict(list),
        "novel_contributions": analysis_payload["novel_contributions"],
        "current_questions": analysis_payload["quiz_questions"],
        "required_output_schema": {
            "quiz_questions": ["question 1", "question 2", "question 3"],
        },
    }
    for concept in paper_concepts:
        quiz_prompt["concepts_by_classification"][str(concept["classification"])].append(str(concept["concept"]))
    quiz_prompt["concepts_by_classification"] = dict(quiz_prompt["concepts_by_classification"])
    prompt_paths["quiz_generation"] = str(
        write_structured_prompt(paper_dir, "quiz_generation", quiz_prompt).relative_to(paper_dir)
    )
    return prompt_paths


def analyze_paper(paper_dir: str | Path, graph_path: str | Path = DEFAULT_GRAPH_PATH) -> dict[str, Any]:
    """Analyze a paper directory and write `analysis.yaml`."""

    paper_path = Path(paper_dir)
    tex = load_main_tex(paper_path)
    graph = graph_index(graph_path)
    _ = graph  # Enforce graph-load errors early.

    raw_candidates = extract_candidate_concepts(tex)
    raw_candidates.extend(section_level_matches(tex, graph_path))
    candidates = deduplicate_candidates(raw_candidates)[:80]

    classified_entries = [classify_candidate(candidate, graph_path) for candidate in candidates]
    paper_concepts = merge_classifications(classified_entries)

    raw_novel_contributions = extract_novel_contributions(tex, graph_path=graph_path)
    novel_contributions = enrich_novel_contributions(raw_novel_contributions, paper_concepts, graph_path=graph_path)

    gaps = [
        {
            "concept": entry["concept"],
            "why_needed": entry["why_needed"],
            "suggested_explanation": entry["suggested_explanation"],
            "context_snippet": entry["context_snippet"],
            "related_graph_nodes": entry.get("related_graph_nodes", []),
        }
        for entry in paper_concepts
        if entry.get("classification") == "gap"
    ]

    quiz_questions = build_quiz_questions(paper_concepts, novel_contributions)
    analysis_payload = {
        "generated_at": utc_timestamp(),
        "graph_path": str(Path(graph_path).resolve()),
        "paper_concepts": [
            {
                "concept": entry["concept"],
                "classification": entry["classification"],
                "matched_node_id": entry.get("matched_node_id"),
                "context_snippet": entry["context_snippet"],
                **({"matched_node": entry["matched_node"]} if entry.get("matched_node") else {}),
                **({"related_graph_nodes": entry["related_graph_nodes"]} if entry.get("related_graph_nodes") else {}),
                **({"description": entry["description"]} if entry.get("description") else {}),
                **({"source": entry["source"]} if entry.get("source") else {}),
            }
            for entry in paper_concepts
        ],
        "gaps": gaps,
        "novel_contributions": novel_contributions,
        "quiz_questions": quiz_questions,
    }
    analysis_payload["prompts"] = build_prompt_payloads(paper_path, analysis_payload, graph_path)
    write_yaml_file(paper_path / "analysis.yaml", analysis_payload)
    return analysis_payload


def main() -> int:
    """CLI entrypoint."""

    args = build_parser().parse_args()
    analyze_paper(args.paper_dir, args.graph)
    print(Path(args.paper_dir) / "analysis.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
