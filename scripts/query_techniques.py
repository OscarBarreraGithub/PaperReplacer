#!/usr/bin/env python3
"""Suggest techniques from the compiled knowledge graph for a free-text problem."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
from math import log
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GRAPH_PATH = ROOT / "data" / "generated" / "compiled" / "all_authored.graph.json"
TECHNIQUE_PREFIX = "technique."
UNLOCK_EDGE_RELATIONS = {
    "unlocks",
    "requires_for_use",
    "requires_for_derive",
    "requires_for_recognize",
}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "because",
    "by",
    "do",
    "evaluate",
    "for",
    "from",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "me",
    "much",
    "need",
    "of",
    "on",
    "or",
    "should",
    "so",
    "stuck",
    "that",
    "the",
    "than",
    "their",
    "then",
    "this",
    "to",
    "try",
    "use",
    "using",
    "what",
    "when",
    "where",
    "which",
    "with",
    "x",
}
NUMBER_WORDS = {"one", "two", "three", "four", "five", "six"}
TOKEN_ALIASES = {
    "analytically": "analytic",
    "asymptotics": "asymptotic",
    "denominators": "denominator",
    "energies": "energy",
    "expansions": "expansion",
    "externally": "external",
    "integrals": "integral",
    "loops": "loop",
    "masses": "mass",
    "momenta": "momentum",
    "parameters": "parameter",
    "regions": "region",
    "scales": "scale",
    "smaller": "small",
    "larger": "large",
}
GENERIC_TOKENS = {
    "analysis",
    "approach",
    "basic",
    "calculation",
    "computation",
    "derive",
    "evaluation",
    "framework",
    "general",
    "method",
    "problem",
    "result",
    "theory",
    "tool",
    "toolkit",
}


@dataclass(frozen=True)
class QueryTerms:
    tokens: tuple[str, ...]
    phrases: tuple[str, ...]


@dataclass(frozen=True)
class NodeSearchEntry:
    node_id: str
    label: str
    summary: str
    search_text: str
    token_set: frozenset[str]


@dataclass(frozen=True)
class NodeMatch:
    node_id: str
    label: str
    summary: str
    token_hits: tuple[str, ...]
    phrase_hits: tuple[str, ...]
    keyword_hits: int
    keyword_score: float


@dataclass(frozen=True)
class GraphIndex:
    nodes: dict[str, dict[str, Any]]
    entries: dict[str, NodeSearchEntry]
    concept_ids: tuple[str, ...]
    technique_ids: tuple[str, ...]
    token_idf: dict[str, float]
    unlock_edges_by_target: dict[str, tuple[dict[str, Any], ...]]


def _normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[_./-]+", " ", text)
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _canonicalize_token(token: str) -> str:
    token = token.lower().strip()
    return TOKEN_ALIASES.get(token, token)


def _tokenize(text: str) -> list[str]:
    return [
        _canonicalize_token(token)
        for token in _normalize_text(text).split()
        if token.strip()
    ]


def _should_keep_keyword(token: str) -> bool:
    if not token or token in STOPWORDS:
        return False
    if token in NUMBER_WORDS:
        return False
    return len(token) > 1


def _ranked_unique(values: list[str]) -> tuple[str, ...]:
    counts = Counter(values)
    return tuple(
        value
        for value, _ in sorted(
            counts.items(),
            key=lambda item: (-item[1], -len(item[0]), item[0]),
        )
    )


def _build_query_terms(problem_text: str) -> QueryTerms:
    raw_tokens = _tokenize(problem_text)
    content_tokens = [token for token in raw_tokens if _should_keep_keyword(token)]
    phrases: list[str] = []
    for size in (2, 3):
        for index in range(len(content_tokens) - size + 1):
            phrase = " ".join(content_tokens[index : index + size])
            if len(phrase.split()) >= 2:
                phrases.append(phrase)

    content_set = set(content_tokens)
    if "loop" in content_set and "integral" in content_set:
        phrases.extend(["loop integral", "feynman integral"])
    if content_set & {"small", "large"} and content_set & {"mass", "momentum", "scale", "energy"}:
        phrases.extend(["scale separation", "asymptotic expansion"])
        content_tokens.append("multiscale")
    if {"loop", "integral"} <= content_set and (
        content_set & {"mass", "momentum", "scale", "small", "large", "hierarchy", "multiscale"}
    ):
        phrases.extend(["multiscale integral", "method of regions"])
        content_tokens.append("multiscale")
    if {"external", "momentum"} <= content_set:
        phrases.append("external momentum")

    filtered_tokens = [token for token in content_tokens if token not in GENERIC_TOKENS]
    filtered_phrases = [
        phrase
        for phrase in phrases
        if any(part not in GENERIC_TOKENS for part in phrase.split())
    ]
    return QueryTerms(
        tokens=_ranked_unique(filtered_tokens),
        phrases=_ranked_unique(filtered_phrases),
    )


def _node_entry(node: dict[str, Any]) -> NodeSearchEntry:
    label = str(node.get("label", ""))
    summary = str(node.get("summary", ""))
    search_text = _normalize_text(" ".join([str(node.get("id", "")), label, summary]))
    token_set = frozenset(token for token in _tokenize(search_text) if _should_keep_keyword(token))
    return NodeSearchEntry(
        node_id=str(node.get("id", "")),
        label=label,
        summary=summary,
        search_text=search_text,
        token_set=token_set,
    )


@lru_cache(maxsize=8)
def _load_graph_index(graph_path: str) -> GraphIndex:
    path = Path(graph_path)
    graph = json.loads(path.read_text())
    nodes = {str(node["id"]): node for node in graph.get("nodes", []) if isinstance(node, dict) and node.get("id")}
    entries = {node_id: _node_entry(node) for node_id, node in nodes.items()}

    document_frequency: Counter[str] = Counter()
    for entry in entries.values():
        document_frequency.update(entry.token_set)
    total_documents = max(len(entries), 1)
    token_idf = {
        token: 1.0 + log((1 + total_documents) / (1 + frequency))
        for token, frequency in document_frequency.items()
    }

    unlock_edges_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph.get("dependencies", []):
        if not isinstance(edge, dict):
            continue
        from_id = str(edge.get("from", ""))
        to_id = str(edge.get("to", ""))
        relation_type = str(edge.get("relation_type", ""))
        if not from_id.startswith(TECHNIQUE_PREFIX):
            continue
        if to_id.startswith(TECHNIQUE_PREFIX):
            continue
        if relation_type not in UNLOCK_EDGE_RELATIONS:
            continue
        unlock_edges_by_target[to_id].append(edge)

    technique_ids = tuple(sorted(node_id for node_id in nodes if node_id.startswith(TECHNIQUE_PREFIX)))
    concept_ids = tuple(sorted(node_id for node_id in nodes if not node_id.startswith(TECHNIQUE_PREFIX)))
    return GraphIndex(
        nodes=nodes,
        entries=entries,
        concept_ids=concept_ids,
        technique_ids=technique_ids,
        token_idf=token_idf,
        unlock_edges_by_target={key: tuple(value) for key, value in unlock_edges_by_target.items()},
    )


def _score_phrase(phrase: str, token_idf: dict[str, float]) -> float:
    parts = [_canonicalize_token(part) for part in phrase.split()]
    if not parts:
        return 0.0
    return 1.5 + sum(token_idf.get(part, 1.0) for part in parts) / len(parts)


def _match_entry(
    entry: NodeSearchEntry,
    terms: QueryTerms,
    token_idf: dict[str, float],
) -> NodeMatch | None:
    token_hits = tuple(sorted(token for token in terms.tokens if token in entry.token_set))
    haystack = f" {entry.search_text} "
    phrase_hits = tuple(
        sorted(phrase for phrase in terms.phrases if f" {phrase} " in haystack)
    )
    if not phrase_hits and len(token_hits) < 2:
        return None
    keyword_score = sum(token_idf.get(token, 1.0) for token in token_hits)
    keyword_score += sum(_score_phrase(phrase, token_idf) for phrase in phrase_hits)
    return NodeMatch(
        node_id=entry.node_id,
        label=entry.label,
        summary=entry.summary,
        token_hits=token_hits,
        phrase_hits=phrase_hits,
        keyword_hits=len(token_hits) + len(phrase_hits),
        keyword_score=round(keyword_score, 4),
    )


def _sorted_matches(matches: list[NodeMatch]) -> list[NodeMatch]:
    return sorted(
        matches,
        key=lambda match: (
            -match.keyword_score,
            -match.keyword_hits,
            match.label.lower(),
            match.node_id,
        ),
    )


def _coerce_top_n(value: int) -> int:
    if value < 1:
        raise ValueError("top_n must be at least 1")
    return value


def query_techniques(
    problem_text: str,
    graph_path: str | Path = DEFAULT_GRAPH_PATH,
    top_n: int = 20,
) -> list[dict[str, Any]]:
    """Return ranked technique suggestions for the given problem text."""

    problem_text = problem_text.strip()
    if not problem_text:
        raise ValueError("Problem text must not be empty.")

    top_n = _coerce_top_n(top_n)
    index = _load_graph_index(str(Path(graph_path).resolve()))
    terms = _build_query_terms(problem_text)

    concept_match_buffer: list[NodeMatch] = []
    for node_id in index.concept_ids:
        match = _match_entry(index.entries[node_id], terms, index.token_idf)
        if match is not None:
            concept_match_buffer.append(match)
    concept_matches = _sorted_matches(concept_match_buffer)
    direct_match_buffer: list[NodeMatch] = []
    for node_id in index.technique_ids:
        technique_match = _match_entry(index.entries[node_id], terms, index.token_idf)
        if technique_match is not None:
            direct_match_buffer.append(technique_match)
    direct_technique_matches = {
        match.node_id: match for match in _sorted_matches(direct_match_buffer)
    }

    technique_scores: dict[str, dict[str, Any]] = {}

    for match in concept_matches:
        for edge in index.unlock_edges_by_target.get(match.node_id, ()):
            technique_id = str(edge["from"])
            technique_node = index.nodes.get(technique_id)
            if technique_node is None:
                continue
            bucket = technique_scores.setdefault(
                technique_id,
                {
                    "id": technique_id,
                    "label": str(technique_node.get("label", technique_id)),
                    "summary": str(technique_node.get("summary", "")),
                    "matched_keywords": set(),
                    "keyword_hits": 0,
                    "keyword_score": 0.0,
                    "unlock_edge_count": 0,
                    "unlock_confidence": 0.0,
                    "unlocked_concepts": [],
                },
            )
            edge_confidence = float(edge.get("confidence", 0.0) or 0.0)
            concept_payload = {
                "id": match.node_id,
                "label": match.label or match.node_id,
                "score": round(match.keyword_score, 4),
                "keyword_hits": match.keyword_hits,
                "matched_keywords": list(match.token_hits + match.phrase_hits),
                "edge_confidence": round(edge_confidence, 4),
                "relation_type": str(edge.get("relation_type", "")),
            }
            bucket["unlock_edge_count"] += 1
            bucket["unlock_confidence"] += edge_confidence
            bucket["keyword_score"] += match.keyword_score
            bucket["matched_keywords"].update(match.token_hits)
            bucket["matched_keywords"].update(match.phrase_hits)
            bucket["unlocked_concepts"].append(concept_payload)

    for technique_id, match in direct_technique_matches.items():
        technique_node = index.nodes.get(technique_id)
        if technique_node is None:
            continue
        bucket = technique_scores.setdefault(
            technique_id,
            {
                "id": technique_id,
                "label": str(technique_node.get("label", technique_id)),
                "summary": str(technique_node.get("summary", "")),
                "matched_keywords": set(),
                "keyword_hits": 0,
                "keyword_score": 0.0,
                "unlock_edge_count": 0,
                "unlock_confidence": 0.0,
                "unlocked_concepts": [],
            },
        )
        bucket["keyword_score"] += match.keyword_score
        bucket["matched_keywords"].update(match.token_hits)
        bucket["matched_keywords"].update(match.phrase_hits)

    results: list[dict[str, Any]] = []
    for bucket in technique_scores.values():
        matched_keywords = sorted(bucket["matched_keywords"])
        unique_concepts = {
            concept["id"]: concept for concept in bucket["unlocked_concepts"]
        }
        unlocked_concepts = sorted(
            unique_concepts.values(),
            key=lambda concept: (-concept["score"], concept["label"].lower(), concept["id"]),
        )
        keyword_hits = len(matched_keywords)
        final_score = (
            bucket["keyword_score"]
            + 2.0 * bucket["unlock_edge_count"]
            + bucket["unlock_confidence"]
        )
        results.append(
            {
                "id": bucket["id"],
                "label": bucket["label"],
                "summary": bucket["summary"],
                "score": round(final_score, 4),
                "keyword_hits": keyword_hits,
                "matched_keywords": matched_keywords,
                "unlock_edge_count": bucket["unlock_edge_count"],
                "unlock_confidence": round(bucket["unlock_confidence"], 4),
                "unlocked_concepts": unlocked_concepts,
            }
        )

    results.sort(
        key=lambda result: (
            -float(result["score"]),
            -int(result["keyword_hits"]),
            -int(result["unlock_edge_count"]),
            result["label"].lower(),
            result["id"],
        )
    )
    return results[:top_n]


def format_markdown_results(problem_text: str, results: list[dict[str, Any]]) -> str:
    if not results:
        return f"# Technique Suggestions\n\nProblem: {problem_text}\n\nNo matching techniques found."

    lines = ["# Technique Suggestions", "", f"Problem: {problem_text}", ""]
    for index, result in enumerate(results, start=1):
        lines.append(
            f"{index}. **{result['label']}** (`{result['id']}`) — score {result['score']:.2f}"
        )
        if result.get("summary"):
            lines.append(f"   {result['summary']}")
        if result.get("matched_keywords"):
            lines.append(
                "   Matched keywords: " + ", ".join(result["matched_keywords"][:12])
            )
        unlocked_concepts = result.get("unlocked_concepts", [])
        if unlocked_concepts:
            concept_fragments = [
                f"{concept['label']} ({concept['edge_confidence']:.2f})"
                for concept in unlocked_concepts[:6]
            ]
            lines.append("   Unlocks matched concepts: " + ", ".join(concept_fragments))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _load_problem_text(args: argparse.Namespace) -> str:
    if args.problem:
        return args.problem.strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise ValueError("Provide --problem or pipe problem text on stdin.")


def _make_handler(graph_path: Path, default_top_n: int):
    class QueryTechniquesHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                self._send_json({"ok": True})
                return
            self._send_json(
                {"ok": False, "message": f"Unknown route: {parsed.path}"},
                status=HTTPStatus.NOT_FOUND,
            )

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path != "/api/query-techniques":
                self._send_json(
                    {"ok": False, "message": f"Unknown route: {parsed.path}"},
                    status=HTTPStatus.NOT_FOUND,
                )
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                raw_body = self.rfile.read(length) if length > 0 else b"{}"
                payload = json.loads(raw_body.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("Request body must be a JSON object.")
                problem_text = str(payload.get("problem", "")).strip()
                top_n = int(payload.get("top_n", default_top_n))
                results = query_techniques(problem_text, graph_path, top_n=top_n)
                self._send_json(
                    {
                        "ok": True,
                        "problem": problem_text,
                        "top_n": top_n,
                        "results": results,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                self._send_json(
                    {
                        "ok": False,
                        "error": type(exc).__name__,
                        "message": str(exc),
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(status.value)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return QueryTechniquesHandler


def serve(graph_path: str | Path, host: str = "127.0.0.1", port: int = 8770, top_n: int = 20) -> int:
    graph_path = Path(graph_path).resolve()
    handler = _make_handler(graph_path, top_n)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving query API at http://{host}:{port}/api/query-techniques")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", help="Free-text problem description.")
    parser.add_argument("--graph-path", default=str(DEFAULT_GRAPH_PATH))
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    parser.add_argument("--serve", action="store_true", help="Start a small HTTP API server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8770)
    args = parser.parse_args()

    if args.serve:
        return serve(args.graph_path, host=args.host, port=args.port, top_n=args.top_n)

    problem_text = _load_problem_text(args)
    results = query_techniques(problem_text, args.graph_path, top_n=args.top_n)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_markdown_results(problem_text, results), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
