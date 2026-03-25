#!/usr/bin/env python3
"""Run contract-aware queries against compiled graph artifacts."""

from __future__ import annotations

import argparse
import json

from kg_core import (
    expanded_slice,
    intrinsic_vs_profile_adjusted,
    load_or_compile_bundle,
    prerequisite_set,
    prerequisites,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, help="Batch id to query")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prereqs_parser = subparsers.add_parser("prereqs")
    prereqs_parser.add_argument("target")
    prereqs_parser.add_argument("relation_type")

    prereq_set_parser = subparsers.add_parser("prereq-set")
    prereq_set_parser.add_argument("target")
    prereq_set_parser.add_argument("relation_type")
    prereq_set_parser.add_argument(
        "--semantics",
        default="ancestral_frontier",
        choices=["ancestral_frontier", "policy_selected_frontier"],
    )

    profile_parser = subparsers.add_parser("intrinsic-vs-profile")
    profile_parser.add_argument("target")
    profile_parser.add_argument("relation_type")
    profile_parser.add_argument("--audience-profile", required=True)
    profile_parser.add_argument("--subfield", required=True)
    profile_parser.add_argument("--task-type")

    slice_parser = subparsers.add_parser("expanded-slice")
    slice_parser.add_argument("target")
    slice_parser.add_argument("relation_type")

    args = parser.parse_args()
    bundle = load_or_compile_bundle(args.batch)

    if args.command == "prereqs":
        result = prerequisites(bundle, args.target, args.relation_type)
    elif args.command == "prereq-set":
        result = prerequisite_set(
            bundle,
            args.target,
            args.relation_type,
            args.semantics,
        )
    elif args.command == "intrinsic-vs-profile":
        profile = {
            "audience_profile": args.audience_profile,
            "subfield": args.subfield,
        }
        if args.task_type:
            profile["task_type"] = args.task_type
        result = intrinsic_vs_profile_adjusted(
            bundle,
            args.target,
            args.relation_type,
            profile,
        )
    else:
        result = expanded_slice(bundle, args.target, args.relation_type)

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
