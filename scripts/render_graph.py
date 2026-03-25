#!/usr/bin/env python3
"""Render graph views from compiled artifacts."""

from __future__ import annotations

import argparse

from kg_core import load_or_compile_bundle, render_mermaid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, help="Batch id to render")
    parser.add_argument("target")
    parser.add_argument("relation_type")
    args = parser.parse_args()

    bundle = load_or_compile_bundle(args.batch)
    print(render_mermaid(bundle, args.target, args.relation_type))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
