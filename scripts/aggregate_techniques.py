#!/usr/bin/env python3
"""Aggregate technique extractions across papers, deduplicate, and map to existing graph.

Usage:
    .venv/bin/python scripts/aggregate_techniques.py \
        --technique-files /tmp/techniques_*.yaml \
        --graph-nodes data/authored/nodes/ \
        --out data/researchers/schwartz_matt/technique_candidates.yaml

Reads extracted technique YAML files, deduplicates by semantic similarity
(using technique_id overlap and label fuzzy matching), and classifies each
technique against the existing graph as reuse_existing / alias_existing /
new_distinct / part_of_existing.
"""

import argparse
import glob
import os
import re
import sys
from collections import defaultdict
import yaml


def load_technique_files(patterns: list[str]) -> list[dict]:
    """Load all technique YAML files matching the given glob patterns."""
    all_techniques = []
    files_found = []
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            files_found.append(path)
            with open(path) as f:
                data = yaml.safe_load(f)
            if data is None:
                continue
            # Handle both top-level list and nested formats
            if isinstance(data, dict) and "techniques" in data:
                # Single-paper format from first extraction
                for t in data["techniques"]:
                    t.setdefault("source_paper", data.get("arxiv_id", "unknown"))
                    all_techniques.append(t)
            elif isinstance(data, dict) and "papers" in data:
                # Multi-paper format
                for paper in data["papers"]:
                    arxiv_id = paper.get("arxiv_id", "unknown")
                    for t in paper.get("techniques", []):
                        t.setdefault("source_paper", arxiv_id)
                        all_techniques.append(t)
            elif isinstance(data, list):
                all_techniques.extend(data)
    print(f"Loaded {len(all_techniques)} raw techniques from {len(files_found)} files", file=sys.stderr)
    return all_techniques


def normalize_id(technique_id: str) -> str:
    """Normalize a technique_id for dedup comparison."""
    s = technique_id.lower().strip()
    s = re.sub(r'[^a-z0-9_]', '_', s)
    s = re.sub(r'_+', '_', s)
    return s.strip('_')


def load_existing_node_ids(nodes_dir: str) -> set[str]:
    """Load all existing node IDs from authored graph."""
    node_ids = set()
    for path in glob.glob(os.path.join(nodes_dir, "*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None:
            continue
        nodes = data if isinstance(data, list) else data.get("nodes", [])
        if isinstance(nodes, list):
            for node in nodes:
                if isinstance(node, dict) and "id" in node:
                    node_ids.add(node["id"])
    return node_ids


def load_existing_labels(nodes_dir: str) -> dict[str, str]:
    """Load node_id -> label mapping from authored graph."""
    labels = {}
    for path in glob.glob(os.path.join(nodes_dir, "*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None:
            continue
        nodes = data if isinstance(data, list) else data.get("nodes", [])
        if isinstance(nodes, list):
            for node in nodes:
                if isinstance(node, dict) and "id" in node:
                    labels[node["id"]] = node.get("label", node["id"])
    return labels


def deduplicate_techniques(techniques: list[dict]) -> list[dict]:
    """Group techniques by normalized ID and merge."""
    groups = defaultdict(list)
    for t in techniques:
        key = normalize_id(t.get("technique_id", "unknown"))
        groups[key].append(t)

    merged = []
    for key, group in sorted(groups.items()):
        # Take the richest entry as base
        base = max(group, key=lambda t: len(str(t.get("description", ""))))
        source_papers = list(set(
            t.get("source_paper", "unknown") for t in group
        ))
        base["source_papers"] = sorted(source_papers)
        base["mention_count"] = len(group)
        if "source_paper" in base:
            del base["source_paper"]
        merged.append(base)

    return merged


def classify_against_graph(technique: dict, existing_ids: set[str],
                           existing_labels: dict[str, str]) -> str:
    """Classify a technique against the existing graph.

    Returns: reuse_existing, alias_existing, part_of_existing, or new_distinct
    """
    tid = technique.get("technique_id", "")
    label = technique.get("label", "").lower()

    # Check for exact ID match
    for eid in existing_ids:
        if tid in eid or eid.split(".")[-1] == tid:
            return "reuse_existing"

    # Check for label overlap with existing nodes
    label_words = set(re.findall(r'[a-z]+', label))
    best_overlap = 0
    best_match = None
    for eid, elabel in existing_labels.items():
        elabel_words = set(re.findall(r'[a-z]+', elabel.lower()))
        if not elabel_words:
            continue
        overlap = len(label_words & elabel_words) / max(len(label_words), 1)
        if overlap > best_overlap:
            best_overlap = overlap
            best_match = eid

    if best_overlap >= 0.7:
        technique["closest_existing_node"] = best_match
        return "alias_existing"
    elif best_overlap >= 0.4:
        technique["closest_existing_node"] = best_match
        return "part_of_existing"

    return "new_distinct"


def main():
    parser = argparse.ArgumentParser(description="Aggregate technique extractions")
    parser.add_argument("--technique-files", nargs="+", required=True,
                        help="Glob patterns for technique YAML files")
    parser.add_argument("--graph-nodes", default="data/authored/nodes/",
                        help="Path to authored graph nodes directory")
    parser.add_argument("--out", required=True, help="Output YAML path")
    args = parser.parse_args()

    # Load techniques
    techniques = load_technique_files(args.technique_files)

    # Load existing graph
    existing_ids = load_existing_node_ids(args.graph_nodes)
    existing_labels = load_existing_labels(args.graph_nodes)
    print(f"Existing graph: {len(existing_ids)} nodes", file=sys.stderr)

    # Deduplicate
    merged = deduplicate_techniques(techniques)
    print(f"After dedup: {len(merged)} unique techniques", file=sys.stderr)

    # Classify against graph
    classifications = defaultdict(list)
    for t in merged:
        classification = classify_against_graph(t, existing_ids, existing_labels)
        t["overlap_classification"] = classification
        classifications[classification].append(t["technique_id"])

    # Sort: new_distinct first (most interesting), then by mention count
    merged.sort(key=lambda t: (
        0 if t["overlap_classification"] == "new_distinct" else
        1 if t["overlap_classification"] == "part_of_existing" else 2,
        -t.get("mention_count", 1)
    ))

    # Summary
    print("\nClassification summary:", file=sys.stderr)
    for cls, ids in sorted(classifications.items()):
        print(f"  {cls}: {len(ids)}", file=sys.stderr)

    output = {
        "researcher": "schwartz_matt",
        "total_unique_techniques": len(merged),
        "classification_summary": {k: len(v) for k, v in classifications.items()},
        "techniques": merged,
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)

    print(f"\nWrote {len(merged)} techniques to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
