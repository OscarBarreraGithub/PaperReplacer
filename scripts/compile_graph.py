#!/usr/bin/env python3
"""Compile authored graph data into normalized and queryable artifacts."""

from __future__ import annotations

import argparse
import json

from kg_core import (
    compile_batch,
    compiled_bundle_path,
    load_batch_records,
    validate_batch_records,
    validation_report_path,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, help="Batch id to compile")
    args = parser.parse_args()

    records = load_batch_records(args.batch)
    report = validate_batch_records(records)
    write_json(validation_report_path(args.batch), report)
    if not report["valid"]:
        print(json.dumps(report, indent=2))
        return 1

    bundle = compile_batch(records)
    output_path = compiled_bundle_path(args.batch)
    write_json(output_path, bundle)
    print(json.dumps({"compiled_to": str(output_path), "batch_id": args.batch}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
