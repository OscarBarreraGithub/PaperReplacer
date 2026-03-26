#!/usr/bin/env python3
"""Helpers for multi-document registry, oracle extraction, and triage summaries."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Iterable

from kg_core import ROOT, load_yaml_subset, write_json


REF_MATERIAL_DIR = ROOT / "Ref material"
DEFAULT_DOCUMENT_REGISTRY = ROOT / "document-registry.yaml"
DEFAULT_DOCUMENT_COVERAGE = ROOT / "document-coverage.md"
DEFAULT_DOCUMENT_GAP_QUEUE = ROOT / "document-gap-queue.md"
DEFAULT_EXTRACTED_ROOT = ROOT / "data" / "generated" / "extracted"
DEFAULT_ORACLE_ROOT = ROOT / "data" / "generated" / "oracles"

DEFAULT_ORCHESTRATOR = {
    "max_active_agents": 8,
    "canonical_merge_lane": 1,
    "lane_budget": {
        "ingestion": 3,
        "content": 3,
        "review": 2,
    },
    "selection_priority": [
        "unblock active population batch",
        "merge a validated disjoint batch already prepared",
        "ingest next unstarted logical document",
        "promote a cross-document reusable backlog cluster",
        "perform explicit deferral classification for residue",
    ],
}

DOCUMENT_STATUSES = {
    "unstarted",
    "structure_scanned",
    "oracle_extracted",
    "triaged",
    "cross_document_reduced",
    "population_in_progress",
    "substantively_exhausted",
    "deferred",
    "blocked",
}

TERMINAL_DOCUMENT_STATUSES = {
    "substantively_exhausted",
    "deferred",
    "blocked",
}

ORACLE_MODES = {
    "index",
    "toc_fallback",
    "hybrid",
}

REPORT_SECTIONS = (
    "covered_existing",
    "candidate_batch_expansion",
    "candidate_new_node",
    "alias_candidate",
    "out_of_scope_or_non_ontology",
    "skip_non_ontology",
)

STATUS_TRANSITIONS = {
    "unstarted": {"structure_scanned", "blocked", "deferred"},
    "structure_scanned": {"oracle_extracted", "blocked", "deferred"},
    "oracle_extracted": {"triaged", "blocked", "deferred"},
    "triaged": {"cross_document_reduced", "blocked", "deferred"},
    "cross_document_reduced": {"population_in_progress", "substantively_exhausted", "blocked", "deferred"},
    "population_in_progress": {"cross_document_reduced", "substantively_exhausted", "blocked", "deferred"},
    "substantively_exhausted": set(),
    "deferred": set(),
    "blocked": {"structure_scanned", "oracle_extracted", "triaged", "cross_document_reduced", "population_in_progress", "deferred"},
}

REGISTRY_REQUIRED_FIELDS = {
    "doc_id",
    "title",
    "source_paths",
    "domain_family",
    "priority",
    "oracle_mode",
    "status",
    "assigned_wave",
    "last_checkpoint",
    "coverage_state",
    "blocking_issues",
    "next_actions",
}

STATUS_PRIORITY = {
    "population_in_progress": 0,
    "cross_document_reduced": 1,
    "triaged": 2,
    "oracle_extracted": 3,
    "structure_scanned": 4,
    "unstarted": 5,
    "blocked": 6,
    "deferred": 7,
    "substantively_exhausted": 8,
}


@dataclass(frozen=True)
class DocumentSpec:
    doc_id: str
    title: str
    source_patterns: tuple[str, ...]
    domain_family: str
    priority: int
    default_oracle_mode: str


DEFAULT_DOCUMENT_SPECS = (
    DocumentSpec(
        doc_id="schwartz_qft",
        title="Quantum Field Theory and the Standard Model (Schwartz)",
        source_patterns=("Schwartz QFT.pdf",),
        domain_family="qft",
        priority=1,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="peskin_qft",
        title="An Introduction to Quantum Field Theory (Peskin and Schroeder)",
        source_patterns=("Peskin.pdf",),
        domain_family="qft",
        priority=2,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="weinberg_qft_vol1",
        title="The Quantum Theory of Fields, Volume I (Weinberg)",
        source_patterns=("Weinberg/QFT I/*.pdf",),
        domain_family="qft",
        priority=3,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="weinberg_qft_vol2",
        title="The Quantum Theory of Fields, Volume II (Weinberg)",
        source_patterns=("Weinberg/QFT II/*.pdf",),
        domain_family="qft",
        priority=4,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="shankar_qm",
        title="Principles of Quantum Mechanics (Shankar)",
        source_patterns=("Shankar.pdf",),
        domain_family="qm",
        priority=5,
        default_oracle_mode="index",
    ),
    DocumentSpec(
        doc_id="jackson_em",
        title="Classical Electrodynamics (Jackson)",
        source_patterns=("Jackson.pdf",),
        domain_family="classical_em",
        priority=6,
        default_oracle_mode="index",
    ),
    DocumentSpec(
        doc_id="complex_analysis",
        title="Complex Analysis",
        source_patterns=("Complex Analysis.pdf",),
        domain_family="complex_analysis",
        priority=7,
        default_oracle_mode="index",
    ),
    DocumentSpec(
        doc_id="complex_variables",
        title="Complex Variables",
        source_patterns=("Complex Variables.pdf",),
        domain_family="complex_analysis",
        priority=8,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="tu_manifolds",
        title="An Introduction to Manifolds (Tu)",
        source_patterns=("Manifolds/Tu_AnIntroductionToManifolds.pdf",),
        domain_family="differential_geometry",
        priority=9,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="lee_smooth_manifolds",
        title="Introduction to Smooth Manifolds (Lee)",
        source_patterns=("Manifolds/lee_smooth_manifolds.pdf",),
        domain_family="differential_geometry",
        priority=10,
        default_oracle_mode="index",
    ),
    DocumentSpec(
        doc_id="axion_lecture_notes",
        title="Axion Lecture Notes",
        source_patterns=("Axion_Lecture_Notes_Physics253cr.pdf",),
        domain_family="axion_bsm",
        priority=11,
        default_oracle_mode="toc_fallback",
    ),
    DocumentSpec(
        doc_id="dodelson_modern_cosmology",
        title="Modern Cosmology (Dodelson and Schmidt)",
        source_patterns=("Scott Dodelson, Fabian Schmidt - Modern Cosmology-Academic Press (2020).pdf",),
        domain_family="cosmology",
        priority=12,
        default_oracle_mode="hybrid",
    ),
    DocumentSpec(
        doc_id="weinberg_qft_vol3",
        title="The Quantum Theory of Fields, Volume III (Weinberg)",
        source_patterns=("Weinberg/QFT III/*.pdf",),
        domain_family="supersymmetry",
        priority=13,
        default_oracle_mode="hybrid",
    ),
)


INITIAL_DOCUMENT_OVERRIDES: dict[str, dict[str, Any]] = {
    "schwartz_qft": {
        "status": "substantively_exhausted",
        "assigned_wave": "completed_seed",
        "last_checkpoint": "stage22_schwartz_refinement_p",
        "coverage_state": (
            "Substantive backlog exhausted; remaining residue is tracked as explicit deferrals in "
            "schwartz-gap-queue.md."
        ),
        "blocking_issues": [],
        "next_actions": [
            "Monitor for future cross-document alias reuse or overlap cleanup only.",
        ],
    },
    "weinberg_qft_vol3": {
        "coverage_state": (
            "Awaiting structure scan; likely overlap-sensitive because large parts of the volume sit in "
            "the current SUSY/SUGRA perimeter."
        ),
        "next_actions": [
            "Run structure scan and oracle extraction.",
            "Expect early explicit-deferral review for supersymmetry and supergravity branches.",
        ],
    },
}


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _relative_source_string(path: Path, base: Path = ROOT) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        if base != ROOT:
            return _relative_source_string(path, base=ROOT)
        return path.as_posix()


def _load_pdf_reader(path: Path) -> Any:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "pypdf is required for PDF extraction. Use .venv/bin/python for document oracle scripts."
        ) from exc
    return PdfReader(str(path))


def source_role(path: Path) -> str:
    name = path.name.lower()
    if "subject_index" in name or ("index" in name and "author_index" not in name and "subject" in name):
        return "subject_index"
    if "author_index" in name:
        return "author_index"
    if "contents" in name:
        return "contents"
    if "glossary" in name:
        return "glossary"
    if "frontmatter" in name or "preface" in name or "notation" in name:
        return "frontmatter"
    return "chapter"


def _clean_filename_stem(stem: str) -> str:
    cleaned = re.sub(r"^\d+\.\d+_", "", stem)
    cleaned = re.sub(r"^pp_[^_]+_", "", cleaned)
    cleaned = re.sub(r"^[0-9_]+", "", cleaned)
    cleaned = cleaned.replace("_", " ").strip(" -")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def chapter_title_from_path(path: Path) -> str:
    title = _clean_filename_stem(path.stem)
    if not title:
        title = path.stem
    return title.title()


def group_source_paths_by_document(
    paths: Iterable[Path],
    ref_root: Path = REF_MATERIAL_DIR,
    specs: tuple[DocumentSpec, ...] = DEFAULT_DOCUMENT_SPECS,
) -> dict[str, list[Path]]:
    normalized_paths = sorted({Path(path) for path in paths if path.suffix.lower() == ".pdf"})
    grouped: dict[str, list[Path]] = {}
    matched: set[Path] = set()
    for spec in specs:
        collected: list[Path] = []
        for pattern in spec.source_patterns:
            for candidate in sorted(ref_root.glob(pattern)):
                if candidate in normalized_paths:
                    collected.append(candidate)
                    matched.add(candidate)
        grouped[spec.doc_id] = sorted(collected)
    unexpected = sorted(path for path in normalized_paths if path not in matched)
    if unexpected:
        raise ValueError(
            "Unmapped reference PDFs found: " + ", ".join(str(path.relative_to(ref_root)) for path in unexpected)
        )
    return grouped


def resolve_logical_documents(
    ref_root: Path = REF_MATERIAL_DIR,
    specs: tuple[DocumentSpec, ...] = DEFAULT_DOCUMENT_SPECS,
) -> list[dict[str, Any]]:
    all_paths = sorted(path for path in ref_root.rglob("*.pdf") if path.is_file())
    grouped = group_source_paths_by_document(all_paths, ref_root=ref_root, specs=specs)
    documents: list[dict[str, Any]] = []
    for spec in sorted(specs, key=lambda item: item.priority):
        source_paths = grouped.get(spec.doc_id, [])
        documents.append(
            {
                "doc_id": spec.doc_id,
                "title": spec.title,
                "source_paths": [_relative_source_string(path, base=ref_root) for path in source_paths],
                "domain_family": spec.domain_family,
                "priority": spec.priority,
                "oracle_mode": spec.default_oracle_mode,
            }
        )
    return documents


def default_registry_entries(
    ref_root: Path = REF_MATERIAL_DIR,
    specs: tuple[DocumentSpec, ...] = DEFAULT_DOCUMENT_SPECS,
) -> list[dict[str, Any]]:
    entries = resolve_logical_documents(ref_root=ref_root, specs=specs)
    by_doc_id = {entry["doc_id"]: dict(entry) for entry in entries}
    for entry in by_doc_id.values():
        entry.setdefault("status", "unstarted")
        entry.setdefault("assigned_wave", None)
        entry.setdefault("last_checkpoint", None)
        entry.setdefault("coverage_state", "Awaiting structure scan and oracle extraction.")
        entry.setdefault("blocking_issues", [])
        entry.setdefault(
            "next_actions",
            [
                "Run structure scan and oracle extraction.",
                "Generate document-local triage from the extracted oracle.",
            ],
        )
    for doc_id, patch in INITIAL_DOCUMENT_OVERRIDES.items():
        if doc_id in by_doc_id:
            by_doc_id[doc_id].update(patch)
    return [by_doc_id[spec.doc_id] for spec in sorted(specs, key=lambda item: item.priority)]


def transition_document_status(entry: dict[str, Any], new_status: str) -> dict[str, Any]:
    if new_status not in DOCUMENT_STATUSES:
        raise ValueError(f"Unsupported document status: {new_status}")
    current = entry["status"]
    if new_status == current:
        return dict(entry)
    allowed = STATUS_TRANSITIONS.get(current, set())
    if new_status not in allowed:
        raise ValueError(f"Invalid document status transition: {current} -> {new_status}")
    updated = dict(entry)
    updated["status"] = new_status
    return updated


def next_document_action(entry: dict[str, Any]) -> str:
    next_actions = entry.get("next_actions") or []
    if next_actions:
        return str(next_actions[0])
    fallback = {
        "unstarted": "Run structure scan and oracle extraction.",
        "structure_scanned": "Complete oracle extraction.",
        "oracle_extracted": "Generate document-local triage and summarize it.",
        "triaged": "Reduce document-local pressure into cross-document backlog clusters.",
        "cross_document_reduced": "Promote the next reusable batch or record explicit deferrals.",
        "population_in_progress": "Validate and merge the next stable authored batch checkpoint.",
        "blocked": "Resolve the recorded blocker or convert it into an explicit deferral.",
        "deferred": "Monitor only; no active work unless overlap or reuse pressure changes.",
        "substantively_exhausted": "Monitor only; the document backlog is currently closed.",
    }
    return fallback[entry["status"]]


def is_overlap_sensitive(entry: dict[str, Any]) -> bool:
    signal_text = " ".join(
        [
            entry.get("coverage_state", ""),
            " ".join(str(issue) for issue in entry.get("blocking_issues", [])),
            " ".join(str(item) for item in entry.get("next_actions", [])),
            entry.get("domain_family", ""),
        ]
    ).lower()
    markers = (
        "overlap",
        "sensitive",
        "perimeter",
        "defer",
        "supersymmetry",
        "supergravity",
        "conflict",
    )
    return any(marker in signal_text for marker in markers)


def registry_is_complete(registry: dict[str, Any]) -> bool:
    documents = registry.get("documents", [])
    return bool(documents) and all(doc["status"] in TERMINAL_DOCUMENT_STATUSES for doc in documents)


def _registry_settings(payload: dict[str, Any]) -> dict[str, Any]:
    settings = dict(DEFAULT_ORCHESTRATOR)
    raw = payload.get("orchestrator") or {}
    lane_budget = dict(DEFAULT_ORCHESTRATOR["lane_budget"])
    lane_budget.update(raw.get("lane_budget") or {})
    settings.update(raw)
    settings["lane_budget"] = lane_budget
    if sum(int(count) for count in lane_budget.values()) > int(settings["max_active_agents"]):
        raise ValueError("document registry lane budget exceeds max_active_agents")
    return settings


def build_agent_lane_plan(registry: dict[str, Any]) -> dict[str, Any]:
    settings = _registry_settings(registry)
    documents = sorted(
        registry["documents"],
        key=lambda item: (STATUS_PRIORITY[item["status"]], item["priority"], item["doc_id"]),
    )
    assigned: set[str] = set()

    def pick(statuses: set[str], limit: int, predicate: Any | None = None) -> list[dict[str, Any]]:
        selected: list[dict[str, Any]] = []
        for doc in documents:
            if doc["doc_id"] in assigned:
                continue
            if doc["status"] not in statuses:
                continue
            if predicate is not None and not predicate(doc):
                continue
            selected.append(doc)
            assigned.add(doc["doc_id"])
            if len(selected) == limit:
                break
        return selected

    lane_budget = settings["lane_budget"]
    ingestion = pick({"unstarted", "structure_scanned"}, int(lane_budget["ingestion"]))
    content = pick(
        {"oracle_extracted", "triaged", "cross_document_reduced", "population_in_progress"},
        int(lane_budget["content"]),
    )
    review = pick(
        {"blocked", "triaged", "cross_document_reduced", "population_in_progress", "unstarted"},
        int(lane_budget["review"]),
        predicate=is_overlap_sensitive,
    )
    total_assigned = len(ingestion) + len(content) + len(review)
    return {
        "max_active_agents": int(settings["max_active_agents"]),
        "canonical_merge_lane": int(settings["canonical_merge_lane"]),
        "lane_budget": lane_budget,
        "selection_priority": list(settings["selection_priority"]),
        "lanes": {
            "ingestion": [
                {
                    "doc_id": doc["doc_id"],
                    "status": doc["status"],
                    "oracle_mode": doc["oracle_mode"],
                    "next_action": next_document_action(doc),
                }
                for doc in ingestion
            ],
            "content": [
                {
                    "doc_id": doc["doc_id"],
                    "status": doc["status"],
                    "oracle_mode": doc["oracle_mode"],
                    "next_action": next_document_action(doc),
                }
                for doc in content
            ],
            "review": [
                {
                    "doc_id": doc["doc_id"],
                    "status": doc["status"],
                    "oracle_mode": doc["oracle_mode"],
                    "next_action": next_document_action(doc),
                }
                for doc in review
            ],
        },
        "active_agents": total_assigned,
    }


def load_document_registry(path: Path = DEFAULT_DOCUMENT_REGISTRY) -> dict[str, Any]:
    payload = load_yaml_subset(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Document registry at {path} must be a mapping.")
    documents = payload.get("documents")
    if not isinstance(documents, list):
        raise ValueError(f"Document registry at {path} must contain a documents list.")
    normalized_documents: list[dict[str, Any]] = []
    seen_doc_ids: set[str] = set()
    seen_source_paths: dict[str, str] = {}
    for index, raw_entry in enumerate(documents):
        if not isinstance(raw_entry, dict):
            raise ValueError(f"documents[{index}] in {path} must be a mapping.")
        missing = sorted(REGISTRY_REQUIRED_FIELDS - set(raw_entry))
        if missing:
            raise ValueError(f"documents[{index}] in {path} is missing required fields: {', '.join(missing)}")
        entry = dict(raw_entry)
        entry["doc_id"] = str(entry["doc_id"])
        if entry["doc_id"] in seen_doc_ids:
            raise ValueError(f"Duplicate document id in {path}: {entry['doc_id']}")
        seen_doc_ids.add(entry["doc_id"])
        if entry["oracle_mode"] not in ORACLE_MODES:
            raise ValueError(f"Unsupported oracle_mode for {entry['doc_id']}: {entry['oracle_mode']}")
        if entry["status"] not in DOCUMENT_STATUSES:
            raise ValueError(f"Unsupported status for {entry['doc_id']}: {entry['status']}")
        source_paths = entry["source_paths"]
        if not isinstance(source_paths, list) or not source_paths:
            raise ValueError(f"{entry['doc_id']} in {path} must define a non-empty source_paths list.")
        normalized_paths: list[str] = []
        for raw_source_path in source_paths:
            source_path = Path(str(raw_source_path)).as_posix()
            owner = seen_source_paths.get(source_path)
            if owner is not None:
                raise ValueError(
                    f"Duplicate source path in {path}: {source_path} is assigned to both {owner} and {entry['doc_id']}"
                )
            seen_source_paths[source_path] = entry["doc_id"]
            normalized_paths.append(source_path)
        entry["source_paths"] = normalized_paths
        if not isinstance(entry["priority"], int):
            raise ValueError(f"Priority for {entry['doc_id']} must be an integer.")
        if not isinstance(entry["blocking_issues"], list):
            raise ValueError(f"blocking_issues for {entry['doc_id']} must be a list.")
        if not isinstance(entry["next_actions"], list):
            raise ValueError(f"next_actions for {entry['doc_id']} must be a list.")
        normalized_documents.append(entry)

    payload = dict(payload)
    payload["documents"] = sorted(
        normalized_documents,
        key=lambda item: (item["priority"], item["doc_id"]),
    )
    payload["orchestrator"] = _registry_settings(payload)
    payload["global_backlog"] = list(payload.get("global_backlog") or [])
    return payload


def _extract_page_text(reader: Any, page_index: int) -> str:
    return normalize_whitespace(reader.pages[page_index].extract_text() or "")


def scan_pdf_structure(path: Path, front_pages: int = 12, tail_pages: int = 12) -> dict[str, Any]:
    reader = _load_pdf_reader(path)
    page_count = len(reader.pages)
    front_indices = list(range(min(front_pages, page_count)))
    tail_indices = list(range(max(0, page_count - tail_pages), page_count))
    front_samples = [
        {"page_number": index + 1, "text": _extract_page_text(reader, index)}
        for index in front_indices
    ]
    tail_samples = [
        {"page_number": index + 1, "text": _extract_page_text(reader, index)}
        for index in tail_indices
    ]
    front_text = " ".join(sample["text"] for sample in front_samples).lower()
    tail_text = " ".join(sample["text"] for sample in tail_samples).lower()
    return {
        "path": str(path.as_posix()),
        "page_count": page_count,
        "source_role": source_role(path),
        "front_samples": front_samples,
        "tail_samples": tail_samples,
        "front_has_contents": "contents" in front_text or "table of contents" in front_text,
        "tail_has_index": "index" in tail_text and "author index" not in tail_text,
        "tail_has_bibliography": "bibliography" in tail_text or "references" in tail_text,
    }


def detect_oracle_mode(
    source_paths: Iterable[Path],
    scans: Iterable[dict[str, Any]] | None = None,
) -> str:
    source_path_list = [Path(path) for path in source_paths]
    roles = {source_role(path) for path in source_path_list}
    has_index = "subject_index" in roles
    has_toc = "contents" in roles or len(source_path_list) > 1
    if scans is not None:
        scan_list = list(scans)
        has_index = has_index or any(scan.get("tail_has_index") for scan in scan_list)
        has_toc = has_toc or any(scan.get("front_has_contents") for scan in scan_list)
    if has_index and has_toc:
        return "hybrid"
    if has_index:
        return "index"
    return "toc_fallback"


def _find_marker_page(
    path: Path,
    start_page: int,
    end_page: int,
    marker_pattern: str,
) -> int | None:
    reader = _load_pdf_reader(path)
    for index in range(max(0, start_page - 1), min(end_page, len(reader.pages))):
        text = _extract_page_text(reader, index)
        head = text[:500].lower()
        if re.search(marker_pattern, head):
            return index + 1
    return None


def _extract_page_range(path: Path, start_page: int, end_page: int) -> dict[str, Any]:
    reader = _load_pdf_reader(path)
    end_page = min(end_page, len(reader.pages))
    pages: list[dict[str, Any]] = []
    text_blocks: list[str] = []
    for page_number in range(start_page, end_page + 1):
        raw_text = reader.pages[page_number - 1].extract_text() or ""
        normalized_text = normalize_whitespace(raw_text)
        pages.append(
            {
                "page_number": page_number,
                "raw_text": raw_text,
                "normalized_text": normalized_text,
            }
        )
        text_blocks.append(f"=== PAGE {page_number} ===\n{raw_text.strip()}\n")
    return {
        "source_pdf": str(path.as_posix()),
        "pdf_page_count": len(reader.pages),
        "start_page": start_page,
        "end_page": end_page,
        "pages": pages,
        "text": "\n".join(text_blocks).strip() + ("\n" if text_blocks else ""),
    }


def _extract_full_pdf(path: Path) -> dict[str, Any]:
    reader = _load_pdf_reader(path)
    return _extract_page_range(path, 1, len(reader.pages))


def _clean_candidate_line(line: str) -> str:
    cleaned = line.strip()
    cleaned = re.sub(r"\.{2,}\s*\d+$", "", cleaned)
    cleaned = re.sub(r"\s+\d+$", "", cleaned)
    cleaned = re.sub(r"^\d+(\.\d+)*\s+", "", cleaned)
    cleaned = cleaned.strip(" -\t")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def candidate_phrases_from_lines(lines: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []
    for raw_line in lines:
        line = _clean_candidate_line(raw_line)
        if not line:
            continue
        if len(line.split()) < 2:
            continue
        lowered = line.lower()
        if lowered in {"contents", "table of contents", "index", "subject index", "author index"}:
            continue
        if not any(char.isalpha() for char in line):
            continue
        fingerprint = lowered
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        results.append(line)
    return results


def _contents_lines_from_payload(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for page in payload.get("pages", []):
        text = page.get("raw_text", "")
        for line in text.splitlines():
            if line.strip():
                lines.append(line)
    return lines


def extract_document_oracle(
    document: dict[str, Any],
    extracted_root: Path = DEFAULT_EXTRACTED_ROOT,
    oracle_root: Path = DEFAULT_ORACLE_ROOT,
) -> dict[str, Any]:
    doc_id = document["doc_id"]
    source_paths = [ROOT / path for path in document["source_paths"]]
    scans = [scan_pdf_structure(path) for path in source_paths]
    detected_oracle_mode = detect_oracle_mode(source_paths, scans=scans)
    declared_oracle_mode = document.get("oracle_mode")
    oracle_mode = declared_oracle_mode if declared_oracle_mode in ORACLE_MODES else detected_oracle_mode

    extracted_dir = extracted_root / doc_id
    oracle_dir = oracle_root / doc_id
    triage_dir = oracle_dir / "triage"
    extracted_dir.mkdir(parents=True, exist_ok=True)
    oracle_dir.mkdir(parents=True, exist_ok=True)
    triage_dir.mkdir(parents=True, exist_ok=True)

    source_manifest = {
        "doc_id": doc_id,
        "title": document["title"],
        "domain_family": document["domain_family"],
        "priority": document["priority"],
        "source_paths": [str(path.as_posix()) for path in source_paths],
        "source_roles": {str(path.as_posix()): source_role(path) for path in source_paths},
        "oracle_mode": oracle_mode,
        "declared_oracle_mode": declared_oracle_mode,
        "detected_oracle_mode": detected_oracle_mode,
    }
    write_json(extracted_dir / "source_manifest.json", source_manifest)
    write_json(extracted_dir / "structure_scan.json", {"doc_id": doc_id, "scans": scans})

    index_payloads: list[dict[str, Any]] = []
    toc_payloads: list[dict[str, Any]] = []

    for path in source_paths:
        role = source_role(path)
        if role == "subject_index":
            index_payloads.append(_extract_full_pdf(path))
        elif role == "contents":
            toc_payloads.append(_extract_full_pdf(path))

    if not index_payloads and oracle_mode in {"index", "hybrid"}:
        for path in source_paths:
            reader = _load_pdf_reader(path)
            page_count = len(reader.pages)
            start_page = _find_marker_page(
                path,
                max(1, page_count - 40),
                page_count,
                r"\b(subject\s+)?index\b",
            )
            if start_page is not None:
                index_payloads.append(_extract_page_range(path, start_page, page_count))
                break

    if not toc_payloads and oracle_mode in {"toc_fallback", "hybrid"}:
        for path in source_paths:
            reader = _load_pdf_reader(path)
            page_count = len(reader.pages)
            start_page = _find_marker_page(path, 1, min(20, page_count), r"\b(contents|table of contents)\b")
            if start_page is not None:
                toc_payloads.append(_extract_page_range(path, start_page, min(page_count, start_page + 4)))
                break

    chapter_titles = [
        chapter_title_from_path(path)
        for path in source_paths
        if source_role(path) == "chapter"
    ]
    chapter_titles = candidate_phrases_from_lines(chapter_titles)

    toc_lines: list[str] = []
    for payload in toc_payloads:
        toc_lines.extend(_contents_lines_from_payload(payload))

    toc_candidates = candidate_phrases_from_lines(toc_lines)
    seed_candidates = candidate_phrases_from_lines(chapter_titles + toc_candidates)

    if index_payloads:
        index_text = "\n".join(payload["text"] for payload in index_payloads)
        (extracted_dir / "index.txt").write_text(index_text)
        write_json(extracted_dir / "index.json", {"doc_id": doc_id, "segments": index_payloads})
    if toc_payloads:
        toc_text = "\n".join(payload["text"] for payload in toc_payloads)
        (extracted_dir / "toc.txt").write_text(toc_text)
        write_json(extracted_dir / "toc.json", {"doc_id": doc_id, "segments": toc_payloads})

    write_json(extracted_dir / "chapter_titles.json", {"doc_id": doc_id, "chapter_titles": chapter_titles})
    write_json(
        oracle_dir / "seed_candidates.json",
        {
            "doc_id": doc_id,
            "oracle_mode": oracle_mode,
            "chapter_title_candidates": chapter_titles,
            "toc_candidates": toc_candidates,
            "seed_candidates": seed_candidates,
        },
    )

    oracle_manifest = {
        "doc_id": doc_id,
        "title": document["title"],
        "oracle_mode": oracle_mode,
        "index_segments": len(index_payloads),
        "toc_segments": len(toc_payloads),
        "chapter_title_candidates": len(chapter_titles),
        "toc_candidates": len(toc_candidates),
        "seed_candidates": len(seed_candidates),
        "extracted_dir": str(extracted_dir),
        "oracle_dir": str(oracle_dir),
        "triage_dir": str(triage_dir),
    }
    write_json(oracle_dir / "oracle_manifest.json", oracle_manifest)
    return oracle_manifest


def parse_triage_report(
    path: Path,
    sections: tuple[str, ...] = REPORT_SECTIONS,
) -> dict[str, list[str]]:
    section_set = set(sections)
    parsed: dict[str, list[str]] = defaultdict(list)
    current: str | None = None
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current = line[3:].strip() if line[3:].strip() in section_set else None
            continue
        if line.startswith("| term | classification |"):
            current = "__table__"
            continue
        if line.startswith("| ---"):
            continue
        if current and current != "__table__" and line.startswith("- "):
            parsed[current].append(line[2:].strip())
            continue
        if current in section_set and line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells and cells[0].lower() == "term":
                continue
            parsed[current].append(" | ".join(cells))
            continue
        if current == "__table__" and line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 3 or cells[0].lower() == "term":
                continue
            term, classification, match = cells
            if classification in section_set:
                parsed[classification].append(f"{term} | {match}")
    return parsed


def summarize_triage_reports(
    triage_dir: Path,
    sections: tuple[str, ...] = REPORT_SECTIONS,
    report_glob: str = "*.md",
    report_pattern: str = r"(.+)\.md$",
) -> dict[str, Any]:
    reports = sorted(triage_dir.glob(report_glob))
    payload: dict[str, Any] = {
        "report_count": len(reports),
        "reports": {},
        "totals": {},
    }
    totals: dict[str, list[str]] = defaultdict(list)

    for report in reports:
        match = re.search(report_pattern, report.name)
        report_key = match.group(1) if match else report.stem
        parsed = parse_triage_report(report, sections=sections)
        payload["reports"][report_key] = parsed
        for section, items in parsed.items():
            totals[section].extend(items)

    payload["totals"] = {section: len(totals.get(section, [])) for section in sections}
    return payload


def render_triage_summary_markdown(title: str, payload: dict[str, Any], sections: tuple[str, ...] = REPORT_SECTIONS) -> str:
    lines = [
        f"# {title}",
        "",
        f"- reports parsed: {payload['report_count']}",
        "",
        "## Totals",
    ]
    for section in sections:
        lines.append(f"- `{section}`: {payload['totals'].get(section, 0)}")
    lines.append("")
    lines.append("## Reports")
    for report_key in sorted(payload["reports"]):
        lines.append(f"- {report_key}")
        parsed = payload["reports"][report_key]
        for section in sections:
            lines.append(f"  - {section}: {len(parsed.get(section, []))}")
    return "\n".join(lines) + "\n"


def render_document_coverage(registry: dict[str, Any]) -> str:
    documents = sorted(registry["documents"], key=lambda item: item["priority"])
    counts = Counter(doc["status"] for doc in documents)
    settings = _registry_settings(registry)
    lines = [
        "# Document Coverage Dashboard",
        "",
        f"- logical documents tracked: {len(documents)}",
        f"- exhausted: {counts.get('substantively_exhausted', 0)}",
        f"- deferred: {counts.get('deferred', 0)}",
        f"- blocked: {counts.get('blocked', 0)}",
        f"- active: {sum(counts.get(status, 0) for status in DOCUMENT_STATUSES if status not in TERMINAL_DOCUMENT_STATUSES)}",
        f"- max active agents: {settings['max_active_agents']}",
        "",
        "## Documents",
        "",
        "| Priority | Doc ID | Oracle | Status | Domain | Checkpoint | Next Action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for doc in documents:
        next_action = next_document_action(doc)
        checkpoint = doc.get("last_checkpoint") or "-"
        lines.append(
            f"| {doc['priority']} | `{doc['doc_id']}` | `{doc['oracle_mode']}` | `{doc['status']}` | "
            f"`{doc['domain_family']}` | `{checkpoint}` | {next_action} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- The orchestrator should treat `document-registry.yaml` as the source of truth.",
            "- `document-gap-queue.md` is the operational backlog view generated from the same registry.",
            "- `schwartz_qft` is already substantially exhausted and serves as the seeded calibration document.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_document_gap_queue(registry: dict[str, Any]) -> str:
    documents = sorted(registry["documents"], key=lambda item: item["priority"])
    active = [doc for doc in documents if doc["status"] not in TERMINAL_DOCUMENT_STATUSES]
    lane_plan = build_agent_lane_plan(registry)
    wave_groups = [active[index:index + 3] for index in range(0, len(active), 3)]
    backlog_clusters = list(registry.get("global_backlog") or [])

    lines = [
        "# Document Gap Queue",
        "",
        "This file is the cross-document source of truth for what the overnight orchestrator should do next.",
        "",
        "## Operating Rules",
        "",
        "- Read `document-registry.yaml` first on every run.",
        "- Keep one canonical merge lane.",
        "- Use at most `8` spawned agents at once.",
        "- Keep ingestion one or two documents ahead of active merge work.",
        "- Prefer reusable shared batches over document-local one-off nodes.",
        "",
        "## Agent Plan",
        "",
        f"- max active agents: `{lane_plan['max_active_agents']}`",
        f"- canonical merge lanes: `{lane_plan['canonical_merge_lane']}`",
        f"- currently assigned agents: `{lane_plan['active_agents']}`",
        "",
    ]
    for lane_name in ("ingestion", "content", "review"):
        lines.append(f"### {lane_name.title()} Lane")
        lines.append("")
        lane_items = lane_plan["lanes"][lane_name]
        if not lane_items:
            lines.append("- none scheduled")
        else:
            for item in lane_items:
                lines.append(
                    f"- `{item['doc_id']}`: `{item['status']}` / `{item['oracle_mode']}` / {item['next_action']}"
                )
        lines.append("")

    lines.extend(
        [
        "## Active Queue",
        "",
        ]
    )
    if not active:
        lines.append("- No active documents remain. The canonical document backlog is exhausted.")
    else:
        for wave_index, group in enumerate(wave_groups, start=1):
            lines.append(f"### Suggested Wave {wave_index}")
            lines.append("")
            for doc in group:
                next_action = next_document_action(doc)
                lines.append(
                    f"- `{doc['doc_id']}`: `{doc['status']}` / `{doc['oracle_mode']}` / `{doc['domain_family']}`"
                )
                lines.append(f"  next: {next_action}")
            lines.append("")

    lines.extend(
        [
            "## Reusable Backlog Clusters",
            "",
        ]
    )
    if not backlog_clusters:
        lines.append("- No cross-document backlog clusters are registered yet beyond the live document queue.")
        lines.append("- The orchestrator should add reusable clusters here once multiple documents point at the same missing branch.")
        lines.append("")
    else:
        for item in backlog_clusters:
            cluster_id = item.get("cluster_id", "unlabeled_cluster")
            summary = item.get("summary", "")
            status = item.get("status", "queued")
            docs = ", ".join(f"`{doc_id}`" for doc_id in item.get("documents", []))
            next_action = item.get("next_action", "")
            lines.append(f"- `{cluster_id}`: `{status}`")
            lines.append(f"  summary: {summary}")
            if docs:
                lines.append(f"  documents: {docs}")
            if next_action:
                lines.append(f"  next: {next_action}")
        lines.append("")

    lines.extend(
        [
            "## Cross-Document Cautions",
            "",
            "- Do not let textbook titles or chapter names become ontology nodes.",
            "- Do not duplicate existing canonical topics because a second book uses different language.",
            "- Split works such as the Weinberg volumes must be processed as one logical document each.",
            "- `author index` PDFs are never a coverage oracle.",
            "- `weinberg_qft_vol3` is expected to hit the current SUSY/SUGRA perimeter early and may end partially deferred.",
            "- `axion_lecture_notes` and `dodelson_modern_cosmology` can open same-graph expansion, but only when repeated pressure justifies reusable new branches.",
            "",
            "## Completion Rule",
            "",
            "- A document is done only when its substantive oracle residue is either promoted, covered by existing graph structure, or explicitly deferred.",
        ]
    )
    return "\n".join(lines) + "\n"
