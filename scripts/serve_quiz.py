#!/usr/bin/env python3
"""Serve a lightweight paper knowledge-check UI and profile APIs."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import webbrowser

from annotate_paper import annotate_paper
from condense_paper import condense_paper
from paper_pipeline_common import (
    DEFAULT_GRAPH_PATH,
    derive_gap_explanation,
    expand_upstream_gaps,
    load_analysis,
    load_metadata,
    normalize_candidate_text,
    read_yaml_file,
    utc_timestamp,
    write_yaml_file,
)


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "ui"
PROFILE_FILENAME = "user_profile.yaml"
PERSONALIZED_ANALYSIS_FILENAME = "user_profile_analysis.yaml"
ANNOTATED_OUTPUT_FILENAME = "personalized_annotated.tex"
CONDENSED_OUTPUT_FILENAME = "personalized_condensed.tex"
KNOWN_THRESHOLD = 3
GAP_THRESHOLD = 2
RATING_LEVELS = [
    {
        "value": 1,
        "label": "Never heard of it",
        "short_label": "Never heard",
    },
    {
        "value": 2,
        "label": "Heard the name",
        "short_label": "Heard it",
    },
    {
        "value": 3,
        "label": "Could explain the idea",
        "short_label": "Could explain",
    },
    {
        "value": 4,
        "label": "Could use it in a calculation",
        "short_label": "Could use it",
    },
    {
        "value": 5,
        "label": "Could derive/prove it",
        "short_label": "Could derive",
    },
]
RATING_BY_VALUE = {entry["value"]: entry for entry in RATING_LEVELS}
IMPORTANCE_RANK = {
    "essential": 0,
    "important": 1,
    "supporting": 2,
}
IMPORTANCE_LABEL = {
    "essential": "Essential",
    "important": "Important",
    "supporting": "Supporting",
}


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description="Serve the knowledge-check UI and APIs for a staged paper directory.",
    )
    parser.add_argument("--paper-dir", required=True, help="Directory containing analysis.yaml and metadata.yaml")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8767)
    parser.add_argument("--open", action="store_true", help="Open the knowledge-check UI in a browser")
    return parser


def profile_path_for(paper_dir: Path) -> Path:
    """Return the saved knowledge-check profile path for a paper."""

    return paper_dir / PROFILE_FILENAME


def personalized_analysis_path_for(paper_dir: Path) -> Path:
    """Return the personalized analysis path for a paper."""

    return paper_dir / PERSONALIZED_ANALYSIS_FILENAME


def annotated_output_path_for(paper_dir: Path) -> Path:
    """Return the personalized annotated output path for a paper."""

    return paper_dir / ANNOTATED_OUTPUT_FILENAME


def condensed_output_path_for(paper_dir: Path) -> Path:
    """Return the personalized condensed output path for a paper."""

    return paper_dir / CONDENSED_OUTPUT_FILENAME


def paper_identity(paper_dir: Path) -> dict[str, str]:
    """Return stable paper metadata for API responses and profile files."""

    paper_id = paper_dir.name
    title = paper_dir.name
    metadata_path = paper_dir / "metadata.yaml"
    if metadata_path.exists():
        metadata = load_metadata(paper_dir)
        paper_id = str(metadata.get("arxiv_id", paper_id)).strip() or paper_id
        title = str(metadata.get("title", title)).strip() or title
    return {
        "paper_id": paper_id,
        "title": title,
    }


def to_repo_relative(path: Path) -> str:
    """Return a repo-relative display path when possible."""

    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def load_profile_if_exists(paper_dir: Path) -> dict[str, Any] | None:
    """Load the saved user profile if present."""

    path = profile_path_for(paper_dir)
    if not path.exists():
        return None
    payload = read_yaml_file(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


def normalize_prerequisites(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a UI-friendly prerequisite topic list."""

    raw_prerequisites = analysis.get("prerequisites")
    if not isinstance(raw_prerequisites, list) or not raw_prerequisites:
        raise ValueError("analysis.yaml does not contain a prerequisites list.")

    prerequisites: list[dict[str, Any]] = []
    for index, raw_item in enumerate(raw_prerequisites):
        entry = normalize_prerequisite(raw_item, index)
        if entry is not None:
            prerequisites.append(entry)
    if not prerequisites:
        raise ValueError("No usable prerequisites found in analysis.yaml.")
    return prerequisites


def normalize_prerequisite(raw_item: Any, index: int) -> dict[str, Any] | None:
    """Normalize one prerequisite topic record."""

    if isinstance(raw_item, str):
        topic = raw_item.strip()
        if not topic:
            return None
        return {
            "id": index,
            "topic": topic,
            "description": "",
            "importance": "important",
            "importance_label": IMPORTANCE_LABEL["important"],
            "importance_rank": IMPORTANCE_RANK["important"],
            "graph_node": None,
            "why_important": "",
        }

    if not isinstance(raw_item, dict):
        return None

    topic = str(raw_item.get("topic") or raw_item.get("concept") or raw_item.get("name") or "").strip()
    if not topic:
        return None
    description = str(
        raw_item.get("description")
        or raw_item.get("summary")
        or raw_item.get("one_line")
        or ""
    ).strip()
    importance = str(raw_item.get("importance") or "important").strip().lower() or "important"
    if importance not in IMPORTANCE_RANK:
        importance = "important"
    graph_node = str(raw_item.get("matched_node_id") or raw_item.get("graph_node") or "").strip() or None
    why_important = str(
        raw_item.get("why_important")
        or raw_item.get("why_needed")
        or raw_item.get("explanation")
        or description
    ).strip()
    return {
        "id": index,
        "topic": topic,
        "description": description,
        "importance": importance,
        "importance_label": IMPORTANCE_LABEL[importance],
        "importance_rank": IMPORTANCE_RANK[importance],
        "graph_node": graph_node,
        "why_important": why_important,
    }


def quiz_payload_for(paper_dir: Path) -> dict[str, Any]:
    """Build the GET /api/quiz response."""

    analysis = load_analysis(paper_dir)
    identity = paper_identity(paper_dir)
    prerequisites = normalize_prerequisites(analysis)
    profile = load_profile_if_exists(paper_dir)
    payload: dict[str, Any] = {
        "ok": True,
        **identity,
        "prerequisite_count": len(prerequisites),
        "prerequisites": prerequisites,
        "rating_levels": RATING_LEVELS,
        "profile_exists": profile is not None,
    }
    if profile is not None:
        payload["saved_profile"] = profile.get("summary")
        payload["generated_outputs"] = profile.get("generated_outputs")
    return payload


def normalize_submission_ratings(payload: dict[str, Any], prerequisite_count: int) -> list[dict[str, Any]]:
    """Validate and normalize the submitted rating list."""

    raw_ratings = payload.get("ratings")
    if not isinstance(raw_ratings, list):
        raw_ratings = payload.get("answers")
    if not isinstance(raw_ratings, list):
        raise ValueError("Expected ratings to be a list.")
    if len(raw_ratings) != prerequisite_count:
        raise ValueError(f"Expected {prerequisite_count} ratings, received {len(raw_ratings)}.")

    normalized: list[dict[str, Any] | None] = [None] * prerequisite_count
    seen_ids: set[int] = set()

    for index, raw_rating in enumerate(raw_ratings):
        if isinstance(raw_rating, int):
            prerequisite_id = index
            rating_value = raw_rating
        elif isinstance(raw_rating, str):
            prerequisite_id = index
            try:
                rating_value = int(raw_rating)
            except Exception as exc:  # noqa: BLE001
                raise ValueError(f"Invalid rating value: {raw_rating}") from exc
        elif isinstance(raw_rating, dict):
            raw_prerequisite_id = raw_rating.get("prerequisite_id", raw_rating.get("question_id", index))
            try:
                prerequisite_id = int(raw_prerequisite_id)
            except Exception as exc:  # noqa: BLE001
                raise ValueError(f"Invalid prerequisite_id: {raw_prerequisite_id}") from exc
            raw_value = raw_rating.get("rating", raw_rating.get("mastery", raw_rating.get("choice")))
            try:
                rating_value = int(raw_value)
            except Exception as exc:  # noqa: BLE001
                raise ValueError(f"Invalid rating value: {raw_value}") from exc
        else:
            raise ValueError("Each rating must be an integer or mapping.")

        if prerequisite_id < 0 or prerequisite_id >= prerequisite_count:
            raise ValueError(f"Prerequisite id out of range: {prerequisite_id}")
        if prerequisite_id in seen_ids:
            raise ValueError(f"Duplicate rating for prerequisite id {prerequisite_id}")
        if rating_value not in RATING_BY_VALUE:
            raise ValueError(f"Unknown rating value: {rating_value}")
        seen_ids.add(prerequisite_id)
        normalized[prerequisite_id] = {
            "prerequisite_id": prerequisite_id,
            "rating": rating_value,
        }

    if any(entry is None for entry in normalized):
        raise ValueError("Every prerequisite topic must have a rating.")
    return [entry for entry in normalized if entry is not None]


def build_profile_payload(
    paper_dir: Path,
    prerequisites: list[dict[str, Any]],
    normalized_ratings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble the saved user profile payload."""

    identity = paper_identity(paper_dir)
    responses: list[dict[str, Any]] = []

    for prerequisite, rating_entry in zip(prerequisites, normalized_ratings):
        rating = RATING_BY_VALUE[rating_entry["rating"]]
        known = rating["value"] >= KNOWN_THRESHOLD
        gap = rating["value"] <= GAP_THRESHOLD
        responses.append(
            {
                "prerequisite_id": prerequisite["id"],
                "topic": prerequisite["topic"],
                "description": prerequisite["description"],
                "importance": prerequisite["importance"],
                "importance_label": prerequisite["importance_label"],
                "importance_rank": prerequisite["importance_rank"],
                "graph_node": prerequisite["graph_node"],
                "why_important": prerequisite["why_important"],
                "rating": rating["value"],
                "rating_label": rating["label"],
                "rating_short_label": rating["short_label"],
                "known": known,
                "gap": gap,
            }
        )

    counts = Counter(response["rating"] for response in responses)
    total = len(responses)
    known_topics = sorted(
        [build_profile_topic_item(response) for response in responses if response["known"]],
        key=known_topic_sort_key,
    )
    gap_topics = sorted(
        [build_profile_topic_item(response) for response in responses if response["gap"]],
        key=gap_topic_sort_key,
    )
    summary = {
        "topic_count": total,
        "rated_topic_count": total,
        "known_count": len(known_topics),
        "gap_count": len(gap_topics),
        "rating_1_count": counts[1],
        "rating_2_count": counts[2],
        "rating_3_count": counts[3],
        "rating_4_count": counts[4],
        "rating_5_count": counts[5],
        "could_use_count": counts[4] + counts[5],
        "could_derive_count": counts[5],
        "summary_text": f"You rated {total} topics. {len(gap_topics)} gaps identified (rated 1-2).",
    }

    return {
        "saved_at": utc_timestamp(),
        "paper_dir": to_repo_relative(paper_dir),
        **identity,
        "knowledge_threshold": "rated_3_or_better",
        "gap_threshold": "rated_1_or_2",
        "summary": summary,
        "ratings": responses,
        "known_topics": known_topics,
        "gap_topics": gap_topics,
        "answers": responses,
        "strengths": known_topics,
        "gaps": gap_topics,
    }


def build_profile_topic_item(response: dict[str, Any]) -> dict[str, Any]:
    """Return a compact profile entry for known and gap topics."""

    return {
        "prerequisite_id": response["prerequisite_id"],
        "topic": response["topic"],
        "description": response["description"],
        "importance": response["importance"],
        "importance_label": response["importance_label"],
        "importance_rank": response["importance_rank"],
        "graph_node": response["graph_node"],
        "why_important": response["why_important"],
        "rating": response["rating"],
        "rating_label": response["rating_label"],
        "rating_short_label": response["rating_short_label"],
    }


def known_topic_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    """Sort known topics by importance first, then strongest rating."""

    return (
        int(item.get("importance_rank", IMPORTANCE_RANK["important"])),
        -int(item.get("rating", 0)),
        str(item.get("topic", "")).lower(),
    )


def gap_topic_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    """Sort gap topics by importance first, then weakest rating."""

    return (
        int(item.get("importance_rank", IMPORTANCE_RANK["important"])),
        int(item.get("rating", 0)),
        str(item.get("topic", "")).lower(),
    )


def extract_profile_gap_topics(profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Return saved gap topics from either the new or legacy profile schema."""

    gap_topics = profile.get("gap_topics")
    if isinstance(gap_topics, list):
        return [item for item in gap_topics if isinstance(item, dict)]
    legacy_gaps = profile.get("gaps")
    if isinstance(legacy_gaps, list):
        return [item for item in legacy_gaps if isinstance(item, dict)]
    return []


def build_personalized_analysis(analysis: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    """Derive a knowledge-check-personalized analysis payload."""

    personalized = deepcopy(analysis)
    personalized_gaps: list[dict[str, Any]] = []
    for topic in extract_profile_gap_topics(profile):
        matches = match_analysis_gaps(topic, analysis)
        if matches:
            for match in matches:
                gap = deepcopy(match)
                gap["source_analysis_concept"] = str(match.get("concept") or "").strip()
                gap["concept"] = str(topic.get("topic") or gap.get("concept") or "").strip()
                for field in (
                    "prerequisite_id",
                    "description",
                    "importance",
                    "importance_label",
                    "importance_rank",
                    "graph_node",
                    "why_important",
                    "rating",
                    "rating_label",
                    "rating_short_label",
                ):
                    if topic.get(field) is not None:
                        gap[field] = topic.get(field)
                if gap.get("why_important") and not gap.get("why_needed"):
                    gap["why_needed"] = gap["why_important"]
                if not gap.get("context_snippet"):
                    gap["context_snippet"] = str(topic.get("description") or topic.get("why_important") or "").strip()
                personalized_gaps.append(gap)
            continue
        personalized_gaps.append(build_synthetic_gap(topic, analysis))

    personalized["gaps"] = deduplicate_gaps(personalized_gaps)
    personalized["personalization"] = {
        "generated_at": utc_timestamp(),
        "knowledge_threshold": profile.get("knowledge_threshold", "rated_3_or_better"),
        "source_profile": PROFILE_FILENAME,
        "selected_gap_count": len(personalized["gaps"]),
        "summary": profile.get("summary", {}),
        "known_topics": profile.get("known_topics") or profile.get("strengths") or [],
    }
    return personalized


def match_analysis_gaps(answer: dict[str, Any], analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Find original analysis gaps that match a low-rated prerequisite topic."""

    answer_text = normalize_joined(
        answer.get("description"),
        answer.get("why_important"),
        answer.get("question"),
        answer.get("topic"),
        answer.get("graph_node"),
    )
    topic_text = normalize_joined(answer.get("topic"))
    answer_graph_node = str(answer.get("graph_node") or "").strip().lower()
    matches: list[dict[str, Any]] = []

    for gap in analysis.get("gaps") or []:
        if not isinstance(gap, dict):
            continue
        concept = str(gap.get("concept", "")).strip()
        concept_key = normalize_joined(concept)
        if concept_key and answer_text and concept_key in answer_text:
            matches.append(gap)
            continue
        if concept_key and topic_text and (concept_key in topic_text or topic_text in concept_key):
            matches.append(gap)
            continue
        related_ids = {
            str(item.get("id", "")).strip().lower()
            for item in gap.get("related_graph_nodes") or []
            if isinstance(item, dict)
        }
        if answer_graph_node and answer_graph_node in related_ids:
            matches.append(gap)
    return matches


def deduplicate_gaps(gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate gaps by normalized concept while preserving order."""

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for gap in gaps:
        concept = str(gap.get("concept", "")).strip()
        key = normalize_joined(concept)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(gap)
    return deduped


def build_synthetic_gap(answer: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    """Create a best-effort gap entry for a low-rated prerequisite topic."""

    answer_topic = str(answer.get("topic") or answer.get("question") or "paper concept").strip()
    _matched_name, matched_concept = find_best_concept_match(answer, analysis)
    concept_name = answer_topic or _matched_name
    why_important = str(answer.get("why_important", "")).strip()
    explanation_parts = [
        f"Briefly explain {concept_name} before it is used.",
    ]
    if why_important:
        explanation_parts.append(why_important)
    elif matched_concept is not None:
        role = str(matched_concept.get("role_in_paper") or matched_concept.get("description") or "").strip()
        if role:
            explanation_parts.append(role)

    related_nodes: list[dict[str, Any]] = []
    matched_node_id = str(matched_concept.get("matched_node_id") or "").strip() if matched_concept is not None else ""
    if matched_node_id:
        summary = str(matched_concept.get("role_in_paper") or matched_concept.get("description") or "").strip()
        related_nodes.append(
            {
                "id": matched_node_id,
                "label": concept_name,
                "summary": summary,
            }
        )
    elif answer.get("graph_node"):
        related_nodes.append(
            {
                "id": str(answer["graph_node"]),
                "label": concept_name,
                "summary": why_important,
            }
        )

    why_needed = why_important or f"The saved knowledge-check profile rated {concept_name} as a gap."
    return {
        "concept": concept_name,
        "source_analysis_concept": str(matched_concept.get("concept") or "").strip() if matched_concept is not None else "",
        "why_needed": why_needed,
        "suggested_explanation": " ".join(part.strip() for part in explanation_parts if part.strip()),
        "context_snippet": str(answer.get("description") or answer.get("question") or answer.get("topic") or "").strip(),
        "related_graph_nodes": related_nodes,
        "prerequisite_id": answer.get("prerequisite_id"),
        "description": answer.get("description"),
        "importance": answer.get("importance"),
        "importance_label": answer.get("importance_label"),
        "importance_rank": answer.get("importance_rank"),
        "graph_node": answer.get("graph_node"),
        "why_important": why_important,
        "rating": answer.get("rating"),
        "rating_label": answer.get("rating_label"),
        "rating_short_label": answer.get("rating_short_label"),
        "profile_topic": answer_topic,
    }


def find_best_concept_match(answer: dict[str, Any], analysis: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    """Find the paper concept that best corresponds to a prerequisite topic."""

    answer_text = normalize_joined(
        answer.get("description"),
        answer.get("why_important"),
        answer.get("question"),
        answer.get("topic"),
        answer.get("graph_node"),
    )
    topic_text = normalize_joined(answer.get("topic"))
    answer_graph_node = str(answer.get("graph_node") or "").strip()

    for concept in analysis.get("paper_concepts") or []:
        if not isinstance(concept, dict):
            continue
        concept_name = str(concept.get("concept", "")).strip()
        if not concept_name:
            continue
        concept_key = normalize_joined(concept_name)
        matched_node_id = str(concept.get("matched_node_id") or "").strip()
        if answer_graph_node and matched_node_id and matched_node_id == answer_graph_node:
            return concept_name, concept
        if concept_key and answer_text and concept_key in answer_text:
            return concept_name, concept
        if concept_key and topic_text and (concept_key in topic_text or topic_text in concept_key):
            return concept_name, concept

    fallback = str(answer.get("topic") or answer.get("question") or "paper concept").strip()
    return fallback, None


def normalize_joined(*parts: Any) -> str:
    """Normalize free text for fuzzy concept matching."""

    joined = " ".join(str(part).strip() for part in parts if str(part).strip())
    return normalize_candidate_text(joined)


def generate_personalized_outputs(paper_dir: Path) -> dict[str, Any]:
    """Generate personalized annotation and condensation outputs from a saved profile."""

    profile = load_profile_if_exists(paper_dir)
    if profile is None:
        raise FileNotFoundError("No saved knowledge-check profile found. Submit the knowledge check first.")

    analysis = load_analysis(paper_dir)
    personalized_analysis = build_personalized_analysis(analysis, profile)
    personalized_analysis["gaps"] = expand_upstream_gaps(
        personalized_analysis.get("gaps") or [],
        profile,
        DEFAULT_GRAPH_PATH,
    )
    for gap in personalized_analysis.get("gaps") or []:
        explanation = derive_gap_explanation(gap)
        gap["pedagogical_explanation"] = explanation
        gap["suggested_explanation"] = explanation
    analysis_path = personalized_analysis_path_for(paper_dir)
    write_yaml_file(analysis_path, personalized_analysis)

    annotated_path = annotate_paper(
        paper_dir,
        annotated_output_path_for(paper_dir),
        analysis_path=analysis_path,
    )
    condensed_path = condense_paper(
        paper_dir,
        condensed_output_path_for(paper_dir),
        analysis_path=analysis_path,
    )

    generated_outputs = {
        "generated_at": utc_timestamp(),
        "personalized_gap_count": len(personalized_analysis.get("gaps") or []),
        "analysis_path": to_repo_relative(analysis_path),
        "annotated_output": to_repo_relative(annotated_path),
        "condensed_output": to_repo_relative(condensed_path),
    }
    profile["generated_outputs"] = generated_outputs
    write_yaml_file(profile_path_for(paper_dir), profile)
    return generated_outputs


class QuizUIHandler(SimpleHTTPRequestHandler):
    """HTTP handler for the knowledge-check UI and JSON APIs."""

    def __init__(self, *args, paper_dir: Path, **kwargs):
        self.paper_dir = paper_dir
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_get_api(parsed.path)
            return
        if parsed.path == "/":
            self.path = "/quiz.html"
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self.send_json(
                {"ok": False, "message": f"Unknown route: {parsed.path}"},
                status=HTTPStatus.NOT_FOUND,
            )
            return
        self.handle_post_api(parsed.path)

    def handle_get_api(self, path: str) -> None:
        try:
            if path == "/api/health":
                self.send_json({"ok": True})
                return
            if path == "/api/quiz":
                self.send_json(quiz_payload_for(self.paper_dir))
                return
            if path == "/api/profile":
                profile = load_profile_if_exists(self.paper_dir)
                if profile is None:
                    self.send_json(
                        {"ok": False, "message": "No saved knowledge-check profile found."},
                        status=HTTPStatus.NOT_FOUND,
                    )
                    return
                self.send_json({"ok": True, "profile": profile})
                return
        except Exception as exc:  # noqa: BLE001
            self.send_json(
                {
                    "ok": False,
                    "error": type(exc).__name__,
                    "message": str(exc),
                },
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        self.send_json(
            {"ok": False, "message": f"Unknown API route: {path}"},
            status=HTTPStatus.NOT_FOUND,
        )

    def handle_post_api(self, path: str) -> None:
        try:
            payload = self.read_json_body()
            if path == "/api/submit-quiz":
                quiz_payload = quiz_payload_for(self.paper_dir)
                prerequisites = quiz_payload["prerequisites"]
                normalized_ratings = normalize_submission_ratings(payload, len(prerequisites))
                profile = build_profile_payload(self.paper_dir, prerequisites, normalized_ratings)
                write_yaml_file(profile_path_for(self.paper_dir), profile)
                self.send_json(
                    {
                        "ok": True,
                        "summary": profile["summary"],
                        "profile": profile,
                    }
                )
                return
            if path == "/api/generate-personalized-paper":
                generated_outputs = generate_personalized_outputs(self.paper_dir)
                self.send_json(
                    {
                        "ok": True,
                        "generated_outputs": generated_outputs,
                    }
                )
                return
        except FileNotFoundError as exc:
            self.send_json(
                {
                    "ok": False,
                    "error": type(exc).__name__,
                    "message": str(exc),
                },
                status=HTTPStatus.NOT_FOUND,
            )
            return
        except Exception as exc:  # noqa: BLE001
            self.send_json(
                {
                    "ok": False,
                    "error": type(exc).__name__,
                    "message": str(exc),
                },
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        self.send_json(
            {"ok": False, "message": f"Unknown API route: {path}"},
            status=HTTPStatus.NOT_FOUND,
        )

    def read_json_body(self) -> dict[str, Any]:
        """Read and decode a JSON request body."""

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            return {}
        raw_body = self.rfile.read(content_length)
        payload = json.loads(raw_body.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Expected a JSON object request body.")
        return payload

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        """Write a JSON response."""

        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    """CLI entrypoint."""

    args = build_parser().parse_args()
    paper_dir = Path(args.paper_dir).expanduser().resolve()
    if not paper_dir.exists():
        raise FileNotFoundError(f"Paper directory not found: {paper_dir}")

    handler = partial(QuizUIHandler, paper_dir=paper_dir)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Serving knowledge check UI for {paper_dir.name} at {url}")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
