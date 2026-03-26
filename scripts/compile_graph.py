#!/usr/bin/env python3
"""Compile authored graph data into normalized and queryable artifacts."""

from __future__ import annotations

import argparse
import json

from kg_core import (
    ALL_AUTHORED_BATCH_ID,
    compile_batch,
    compiled_bundle_path,
    load_all_authored_records,
    load_batch_records,
    validate_batch_records,
    validation_report_path,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--batch", help="Batch id to compile")
    group.add_argument(
        "--all-authored",
        action="store_true",
        help="Compile one synthetic bundle from all authored batches",
    )
    args = parser.parse_args()

    if args.all_authored:
        records = load_all_authored_records()
    else:
        records = load_batch_records(args.batch)
    report = validate_batch_records(records)
    write_json(validation_report_path(records.batch_id), report)
    if not report["valid"]:
        print(json.dumps(report, indent=2))
        return 1

    bundle = compile_batch(records)
    output_path = compiled_bundle_path(records.batch_id)
    write_json(output_path, bundle)
    print(
        json.dumps(
            {
                "compiled_to": str(output_path),
                "batch_id": records.batch_id,
                "all_authored": records.batch_id == ALL_AUTHORED_BATCH_ID,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
