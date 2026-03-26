#!/usr/bin/env python3
"""Render document coverage and queue dashboards from the central registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from document_pipeline import (
    DEFAULT_DOCUMENT_COVERAGE,
    DEFAULT_DOCUMENT_GAP_QUEUE,
    DEFAULT_DOCUMENT_REGISTRY,
    load_document_registry,
    render_document_coverage,
    render_document_gap_queue,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(DEFAULT_DOCUMENT_REGISTRY))
    parser.add_argument("--coverage-out", default=str(DEFAULT_DOCUMENT_COVERAGE))
    parser.add_argument("--gap-queue-out", default=str(DEFAULT_DOCUMENT_GAP_QUEUE))
    args = parser.parse_args()

    registry = load_document_registry(Path(args.registry))
    coverage_path = Path(args.coverage_out)
    gap_queue_path = Path(args.gap_queue_out)
    coverage_path.write_text(render_document_coverage(registry))
    gap_queue_path.write_text(render_document_gap_queue(registry))
    print(
        json.dumps(
            {
                "registry": str(Path(args.registry)),
                "coverage_out": str(coverage_path),
                "gap_queue_out": str(gap_queue_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
