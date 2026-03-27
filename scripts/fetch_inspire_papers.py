#!/usr/bin/env python3
"""Fetch a researcher's papers from INSPIRE-HEP and write structured YAML.

Usage:
    .venv/bin/python scripts/fetch_inspire_papers.py \
        --author "M.D.Schwartz.1" \
        --out data/researchers/schwartz_matt/papers.yaml

Uses the INSPIRE-HEP REST API (no API key required).
Only stdlib — no requests dependency.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import yaml  # PyYAML should be in .venv


INSPIRE_API = "https://inspirehep.net/api/literature"
PAGE_SIZE = 100  # max allowed by INSPIRE


def fetch_page(author_id: str, page: int, sort: str = "mostcited") -> dict:
    params = urllib.parse.urlencode({
        "sort": sort,
        "size": PAGE_SIZE,
        "page": page,
        "q": f"a {author_id}",
        "fields": "titles,abstracts,arxiv_eprints,inspire_categories,"
                  "citation_count,dois,publication_info,collaborations,"
                  "keywords,control_number",
    })
    url = f"{INSPIRE_API}?{params}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def extract_record(hit: dict) -> dict:
    meta = hit.get("metadata", {})
    titles = meta.get("titles", [])
    title = titles[0]["title"] if titles else "(no title)"

    abstracts = meta.get("abstracts", [])
    abstract = abstracts[0].get("value", "") if abstracts else ""

    arxiv = meta.get("arxiv_eprints", [])
    arxiv_id = arxiv[0].get("value", "") if arxiv else ""
    arxiv_cats = arxiv[0].get("categories", []) if arxiv else []

    dois = meta.get("dois", [])
    doi = dois[0].get("value", "") if dois else ""

    keywords_raw = meta.get("keywords", [])
    keywords = [k.get("value", "") for k in keywords_raw if k.get("value")]

    inspire_cats = meta.get("inspire_categories", [])
    categories = [c.get("term", "") for c in inspire_cats if c.get("term")]

    citation_count = meta.get("citation_count", 0)
    inspire_id = meta.get("control_number", "")

    collabs = meta.get("collaborations", [])
    collaboration = collabs[0].get("value", "") if collabs else ""

    pub_info = meta.get("publication_info", [])
    journal = ""
    year = ""
    if pub_info:
        journal = pub_info[0].get("journal_title", "")
        year = pub_info[0].get("year", "")

    return {
        "inspire_id": inspire_id,
        "title": title,
        "arxiv_id": arxiv_id,
        "arxiv_categories": arxiv_cats,
        "doi": doi,
        "citation_count": citation_count,
        "year": year if year else None,
        "journal": journal if journal else None,
        "collaboration": collaboration if collaboration else None,
        "categories": categories,
        "keywords": keywords,
        "abstract": abstract,
    }


def fetch_all(author_id: str) -> list[dict]:
    page = 1
    all_papers = []
    while True:
        print(f"  fetching page {page}...", file=sys.stderr)
        data = fetch_page(author_id, page)
        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", 0)
        for h in hits:
            all_papers.append(extract_record(h))
        if len(all_papers) >= total or not hits:
            break
        page += 1
        time.sleep(0.5)  # be polite
    return all_papers


def main():
    parser = argparse.ArgumentParser(description="Fetch INSPIRE-HEP papers for an author")
    parser.add_argument("--author", required=True, help="INSPIRE author ID, e.g. M.D.Schwartz.1")
    parser.add_argument("--out", required=True, help="Output YAML path")
    parser.add_argument("--min-citations", type=int, default=0,
                        help="Only include papers with at least this many citations")
    args = parser.parse_args()

    print(f"Fetching papers for {args.author}...", file=sys.stderr)
    papers = fetch_all(args.author)
    print(f"  fetched {len(papers)} papers total", file=sys.stderr)

    if args.min_citations > 0:
        papers = [p for p in papers if p["citation_count"] >= args.min_citations]
        print(f"  {len(papers)} papers with >= {args.min_citations} citations", file=sys.stderr)

    # Sort by citation count descending
    papers.sort(key=lambda p: p["citation_count"], reverse=True)

    output = {
        "author_id": args.author,
        "fetched": time.strftime("%Y-%m-%d"),
        "total_papers": len(papers),
        "papers": papers,
    }

    with open(args.out, "w") as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)

    print(f"Wrote {len(papers)} papers to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
