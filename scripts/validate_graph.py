#!/usr/bin/env python3
"""Validate authored graph data against schemas and contract rules."""

from __future__ import annotations

import argparse
import json

from kg_core import load_batch_records, validate_batch_records, validation_report_path, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, help="Batch id to validate")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write a JSON report into data/generated/reports/",
    )
    args = parser.parse_args()

    report = validate_batch_records(load_batch_records(args.batch))
    print(json.dumps(report, indent=2))
    if args.write_report:
        write_json(validation_report_path(args.batch), report)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
