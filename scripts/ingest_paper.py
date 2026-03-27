#!/usr/bin/env python3
"""Download an arXiv paper source bundle and stage it for analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from paper_pipeline_common import default_paper_dir, extract_arxiv_id, extract_source_to_directory


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Download an arXiv paper's LaTeX source, locate the main document, "
            "and write metadata.yaml plus main.tex into a paper directory."
        )
    )
    parser.add_argument(
        "--arxiv",
        required=True,
        help="arXiv identifier or URL, for example 2401.12345 or https://arxiv.org/abs/2401.12345",
    )
    parser.add_argument(
        "--out-dir",
        help="Output directory. Defaults to data/papers/<arxiv_id>/",
    )
    return parser


def ingest_paper(arxiv_value: str, out_dir: str | Path | None = None) -> Path:
    """Download and stage a paper into the requested output directory."""

    arxiv_id = extract_arxiv_id(arxiv_value)
    destination = Path(out_dir) if out_dir else default_paper_dir(arxiv_id)
    extract_source_to_directory(arxiv_id, destination)
    return destination


def main() -> int:
    """CLI entrypoint."""

    args = build_parser().parse_args()
    destination = ingest_paper(args.arxiv, args.out_dir)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
