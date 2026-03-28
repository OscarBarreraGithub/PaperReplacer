#!/usr/bin/env python3
"""Serve the local interactive graph UI and JSON APIs."""

from __future__ import annotations

import argparse
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import webbrowser

import yaml

from kg_core import (
    ALL_AUTHORED_BATCH_ID,
    BATCHES_DIR,
    expanded_slice,
    extended_neighborhood_slice,
    intrinsic_vs_profile_adjusted,
    load_batch_contract,
    load_or_compile_bundle,
    prerequisites,
)


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "ui"
PAPERS_DIR = ROOT / "data" / "papers"


class GraphUIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api(parsed)
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def handle_api(self, parsed) -> None:
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/health":
                self.send_json({"ok": True})
                return
            if path == "/api/papers":
                self.send_json(list_papers())
                return
            if path == "/api/paper-graph":
                paper_dir = _required(query, "paper_dir")
                self.send_json(load_paper_graph(paper_dir))
                return
            if path == "/api/batches":
                self.send_json(list_batches())
                return
            if path.startswith("/api/batch/"):
                batch_id = path.removeprefix("/api/batch/")
                self.send_json(load_or_compile_bundle(batch_id))
                return
            if path == "/api/neighborhood":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(expanded_slice(bundle, target, relation_type))
                return
            if path == "/api/extended-neighborhood":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(
                    extended_neighborhood_slice(bundle, target, relation_type)
                )
                return
            if path == "/api/prereqs":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(prerequisites(bundle, target, relation_type))
                return
            if path == "/api/intrinsic-vs-profile":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                audience_profile = _required(query, "audience_profile")
                subfield = _required(query, "subfield")
                task_type = query.get("task_type", [None])[0]
                profile = {
                    "audience_profile": audience_profile,
                    "subfield": subfield,
                }
                if task_type:
                    profile["task_type"] = task_type
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(
                    intrinsic_vs_profile_adjusted(bundle, target, relation_type, profile)
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

    def send_json(self, payload, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _required(query: dict[str, list[str]], key: str) -> str:
    value = query.get(key, [None])[0]
    if value is None or value == "":
        raise ValueError(f"Missing required query parameter: {key}")
    return value


def list_batches() -> list[dict[str, str]]:
    batches = [
        {
            "batch_id": ALL_AUTHORED_BATCH_ID,
            "description": "Synthetic connected view combining all authored batches.",
        }
    ]
    for batch_dir in sorted(path for path in BATCHES_DIR.iterdir() if path.is_dir()):
        contract_path = batch_dir / "batch_contract.yaml"
        description = ""
        if contract_path.exists():
            contract = load_batch_contract(batch_dir.name)
            description = contract.get("description", "")
        batches.append(
            {
                "batch_id": batch_dir.name,
                "description": description,
            }
        )
    return batches


def list_papers() -> list[dict[str, object]]:
    if not PAPERS_DIR.exists():
        return []
    return [
        {
            "paper_dir": paper_dir.name,
            "has_analysis": (paper_dir / "analysis.yaml").exists(),
        }
        for paper_dir in sorted(path for path in PAPERS_DIR.iterdir() if path.is_dir())
    ]


def load_paper_graph(paper_dir_name: str) -> dict[str, object]:
    paper_dir = resolve_paper_dir(paper_dir_name)
    analysis_path = paper_dir / "analysis.yaml"
    if not analysis_path.exists():
        raise FileNotFoundError(f"Missing analysis.yaml for paper_dir={paper_dir_name}")

    with analysis_path.open("r", encoding="utf-8") as handle:
        analysis = yaml.safe_load(handle) or {}
    if not isinstance(analysis, dict):
        raise ValueError(f"Expected mapping in {analysis_path}")

    paper_concepts = analysis.get("paper_concepts") or []
    in_graph_entries = concept_entries(
        paper_concepts,
        label_key="concept",
        classification="in_graph",
    )
    gap_entries = concept_entries(
        paper_concepts,
        label_key="concept",
        classification="gap",
    )
    if not gap_entries:
        gap_entries = concept_entries(analysis.get("gaps") or [], label_key="concept")
    gap_entries = backfill_matched_node_ids(
        gap_entries,
        analysis.get("prerequisites") or [],
    )

    novel_entries = dedupe_concept_entries(
        concept_entries(
            paper_concepts,
            label_key="concept",
            classification="novel",
        )
        + concept_entries(
            analysis.get("novel_contributions") or [],
            label_key="contribution",
        )
    )

    gap_node_ids = matched_node_ids(gap_entries)
    for gap in analysis.get("gaps") or []:
        if not isinstance(gap, dict):
            continue
        for related in gap.get("related_graph_nodes") or []:
            if not isinstance(related, dict):
                continue
            node_id = str(related.get("id", "")).strip()
            if node_id:
                gap_node_ids.append(node_id)
    gap_node_ids = unique_preserving_order(gap_node_ids)

    in_graph_node_ids = matched_node_ids(in_graph_entries)
    novel_node_ids = matched_node_ids(novel_entries)

    return {
        "paper_dir": paper_dir.name,
        "matched_node_ids": unique_preserving_order(
            in_graph_node_ids + gap_node_ids + novel_node_ids
        ),
        "in_graph_node_ids": in_graph_node_ids,
        "gap_node_ids": gap_node_ids,
        "novel_node_ids": novel_node_ids,
        "gap_concepts": gap_entries,
        "novel_concepts": novel_entries,
    }


def resolve_paper_dir(paper_dir_name: str) -> Path:
    paper_dir = (PAPERS_DIR / paper_dir_name).resolve()
    papers_root = PAPERS_DIR.resolve()
    if paper_dir.parent != papers_root or not paper_dir.is_dir():
        raise ValueError(f"Unknown paper_dir: {paper_dir_name}")
    return paper_dir


def concept_entries(
    records: list[object], *, label_key: str, classification: str | None = None
) -> list[dict[str, str | None]]:
    entries: list[dict[str, str | None]] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        if classification is not None and record.get("classification") != classification:
            continue
        label = str(record.get(label_key, "")).strip()
        if not label:
            continue
        matched_node_id = str(record.get("matched_node_id", "")).strip() or None
        entries.append(
            {
                "concept": label,
                "matched_node_id": matched_node_id,
            }
        )
    return dedupe_concept_entries(entries)


def dedupe_concept_entries(entries: list[dict[str, str | None]]) -> list[dict[str, str | None]]:
    deduped: list[dict[str, str | None]] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        label = str(entry.get("concept", "")).strip()
        node_id = str(entry.get("matched_node_id") or "").strip()
        if not label:
            continue
        key = (label.casefold(), node_id)
        if key in seen:
            continue
        seen.add(key)
        deduped.append({"concept": label, "matched_node_id": node_id or None})
    return deduped


def matched_node_ids(entries: list[dict[str, str | None]]) -> list[str]:
    return unique_preserving_order(
        [
            str(entry.get("matched_node_id") or "").strip()
            for entry in entries
            if str(entry.get("matched_node_id") or "").strip()
        ]
    )


def backfill_matched_node_ids(
    entries: list[dict[str, str | None]],
    records: list[object],
) -> list[dict[str, str | None]]:
    exact_matches: dict[str, str] = {}
    partial_matches: list[tuple[str, str]] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        label = str(record.get("topic") or record.get("concept") or "").strip()
        node_id = str(record.get("matched_node_id") or "").strip()
        if not label or not node_id:
            continue
        normalized = normalize_label(label)
        exact_matches[normalized] = node_id
        partial_matches.append((normalized, node_id))

    enriched: list[dict[str, str | None]] = []
    for entry in entries:
        label = str(entry.get("concept", "")).strip()
        node_id = str(entry.get("matched_node_id") or "").strip() or None
        if not label:
            continue
        if node_id is None:
            normalized = normalize_label(label)
            node_id = exact_matches.get(normalized)
            if node_id is None:
                for candidate_label, candidate_node_id in partial_matches:
                    if normalized in candidate_label or candidate_label in normalized:
                        node_id = candidate_node_id
                        break
        enriched.append({"concept": label, "matched_node_id": node_id})
    return dedupe_concept_entries(enriched)


def normalize_label(value: str) -> str:
    return " ".join(
        "".join(char if char.isalnum() else " " for char in value.casefold()).split()
    )


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="Open the UI in a browser")
    args = parser.parse_args()

    handler = partial(GraphUIHandler)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Serving graph UI at {url}")
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
