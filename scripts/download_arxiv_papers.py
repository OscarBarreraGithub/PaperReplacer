#!/usr/bin/env python3
"""Download arXiv papers (PDF) for a researcher from their papers.yaml.

Usage:
    .venv/bin/python scripts/download_arxiv_papers.py \
        --papers data/researchers/schwartz_matt/papers.yaml \
        --out-dir data/researchers/schwartz_matt/pdfs/ \
        --top 25

Downloads the top N papers by citation count that have arXiv IDs.
"""

import argparse
import os
import sys
import time
import urllib.request
import yaml


def download_pdf(arxiv_id: str, out_path: str) -> bool:
    """Download a PDF from arXiv. Returns True on success."""
    # Normalize old-style IDs
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    req = urllib.request.Request(url, headers={
        "User-Agent": "KnowledgeGraph-research-mapper/1.0 (academic research tool)"
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read()
            with open(out_path, "wb") as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"  FAILED {arxiv_id}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Download arXiv PDFs")
    parser.add_argument("--papers", required=True, help="Path to papers.yaml")
    parser.add_argument("--out-dir", required=True, help="Output directory for PDFs")
    parser.add_argument("--top", type=int, default=25, help="Download top N by citations")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip already downloaded PDFs")
    args = parser.parse_args()

    with open(args.papers) as f:
        data = yaml.safe_load(f)

    papers = data["papers"]
    # Filter to those with arXiv IDs
    papers_with_arxiv = [p for p in papers if p.get("arxiv_id")]
    papers_to_download = papers_with_arxiv[:args.top]

    os.makedirs(args.out_dir, exist_ok=True)

    downloaded = 0
    skipped = 0
    failed = 0

    for i, p in enumerate(papers_to_download):
        arxiv_id = p["arxiv_id"]
        safe_name = arxiv_id.replace("/", "_")
        out_path = os.path.join(args.out_dir, f"{safe_name}.pdf")

        if args.skip_existing and os.path.exists(out_path):
            print(f"  [{i+1}/{len(papers_to_download)}] SKIP (exists): {arxiv_id}", file=sys.stderr)
            skipped += 1
            continue

        print(f"  [{i+1}/{len(papers_to_download)}] Downloading {arxiv_id} ({p['citation_count']} cites)...",
              file=sys.stderr)
        if download_pdf(arxiv_id, out_path):
            downloaded += 1
        else:
            failed += 1

        time.sleep(3)  # arXiv rate limit: be polite

    print(f"\nDone: {downloaded} downloaded, {skipped} skipped, {failed} failed", file=sys.stderr)


if __name__ == "__main__":
    main()
