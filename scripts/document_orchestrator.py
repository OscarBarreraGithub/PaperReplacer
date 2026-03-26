#!/usr/bin/env python3
"""Registry-backed scheduling helpers for the multi-document orchestrator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from document_pipeline import (
    DEFAULT_DOCUMENT_COVERAGE,
    DEFAULT_DOCUMENT_GAP_QUEUE,
    DEFAULT_DOCUMENT_REGISTRY,
    build_agent_lane_plan,
    load_document_registry,
    next_document_action,
    registry_is_complete,
    render_document_coverage,
    render_document_gap_queue,
    TERMINAL_DOCUMENT_STATUSES,
)


def queue_payload(registry: dict) -> dict:
    documents = list(registry["documents"])
    active = [doc for doc in documents if doc["status"] not in TERMINAL_DOCUMENT_STATUSES]
    return {
        "complete": registry_is_complete(registry),
        "active_document_count": len(active),
        "terminal_document_count": len(documents) - len(active),
        "global_backlog_count": len(registry.get("global_backlog", [])),
        "agent_plan": build_agent_lane_plan(registry),
        "active_documents": [
            {
                "doc_id": doc["doc_id"],
                "priority": doc["priority"],
                "status": doc["status"],
                "oracle_mode": doc["oracle_mode"],
                "next_action": next_document_action(doc),
                "last_checkpoint": doc.get("last_checkpoint"),
            }
            for doc in active
        ],
    }


def render_queue_markdown(payload: dict) -> str:
    lines = [
        "# Multi-Document Queue",
        "",
        f"- complete: `{str(payload['complete']).lower()}`",
        f"- active documents: `{payload['active_document_count']}`",
        f"- terminal documents: `{payload['terminal_document_count']}`",
        f"- cross-document backlog clusters: `{payload['global_backlog_count']}`",
        "",
        "## Active Documents",
        "",
    ]
    if not payload["active_documents"]:
        lines.append("- none")
    else:
        for doc in payload["active_documents"]:
            checkpoint = doc["last_checkpoint"] or "-"
            lines.append(
                f"- `{doc['doc_id']}`: `{doc['status']}` / `{doc['oracle_mode']}` / checkpoint `{checkpoint}` / {doc['next_action']}"
            )
    lines.extend(
        [
            "",
            "## Agent Plan",
            "",
            json.dumps(payload["agent_plan"], indent=2),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(DEFAULT_DOCUMENT_REGISTRY))
    parser.add_argument("--coverage-out", default=str(DEFAULT_DOCUMENT_COVERAGE))
    parser.add_argument("--gap-queue-out", default=str(DEFAULT_DOCUMENT_GAP_QUEUE))
    parser.add_argument("--check-complete", action="store_true")
    parser.add_argument("--queue-json", action="store_true")
    parser.add_argument("--queue-markdown", action="store_true")
    parser.add_argument("--refresh-tracking", action="store_true")
    args = parser.parse_args()

    registry = load_document_registry(Path(args.registry))
    if args.refresh_tracking:
        Path(args.coverage_out).write_text(render_document_coverage(registry))
        Path(args.gap_queue_out).write_text(render_document_gap_queue(registry))

    payload = queue_payload(registry)

    if args.queue_markdown:
        print(render_queue_markdown(payload))
    elif args.queue_json or not args.check_complete:
        print(json.dumps(payload, indent=2))

    if args.check_complete:
        return 0 if payload["complete"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
