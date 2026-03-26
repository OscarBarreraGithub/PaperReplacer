#!/usr/bin/env python3
"""Extract structure and oracle artifacts for one or more logical documents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from document_pipeline import (
    DEFAULT_DOCUMENT_REGISTRY,
    DEFAULT_EXTRACTED_ROOT,
    DEFAULT_ORACLE_ROOT,
    default_registry_entries,
    extract_document_oracle,
    load_document_registry,
)


def load_documents(registry_path: Path) -> list[dict]:
    if registry_path.exists():
        registry = load_document_registry(registry_path)
        return list(registry["documents"])
    return default_registry_entries()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(DEFAULT_DOCUMENT_REGISTRY))
    parser.add_argument("--doc-id", action="append", dest="doc_ids")
    parser.add_argument("--all-docs", action="store_true")
    parser.add_argument("--extracted-root", default=str(DEFAULT_EXTRACTED_ROOT))
    parser.add_argument("--oracle-root", default=str(DEFAULT_ORACLE_ROOT))
    args = parser.parse_args()

    registry_path = Path(args.registry)
    documents = load_documents(registry_path)
    if args.all_docs:
        selected = documents
    else:
        requested = set(args.doc_ids or [])
        if not requested:
            parser.error("Provide --doc-id at least once or use --all-docs.")
        selected = [doc for doc in documents if doc["doc_id"] in requested]
        missing = sorted(requested - {doc["doc_id"] for doc in selected})
        if missing:
            parser.error(f"Unknown document ids: {', '.join(missing)}")

    extracted_root = Path(args.extracted_root)
    oracle_root = Path(args.oracle_root)
    payload = {
        "documents": [
            extract_document_oracle(doc, extracted_root=extracted_root, oracle_root=oracle_root)
            for doc in selected
        ]
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
