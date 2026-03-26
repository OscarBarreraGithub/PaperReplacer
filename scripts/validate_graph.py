#!/usr/bin/env python3
"""Validate authored graph data against schemas and contract rules."""

from __future__ import annotations

import argparse
import json

from kg_core import (
    ALL_AUTHORED_BATCH_ID,
    load_all_authored_records,
    load_batch_records,
    validate_batch_records,
    validation_report_path,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--batch", help="Batch id to validate")
    group.add_argument(
        "--all-authored",
        action="store_true",
        help="Validate one synthetic bundle from all authored batches",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write a JSON report into data/generated/reports/",
    )
    args = parser.parse_args()

    if args.all_authored:
        records = load_all_authored_records()
    else:
        records = load_batch_records(args.batch)
    report = validate_batch_records(records)
    print(json.dumps(report, indent=2))
    if args.write_report:
        write_json(validation_report_path(records.batch_id), report)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
