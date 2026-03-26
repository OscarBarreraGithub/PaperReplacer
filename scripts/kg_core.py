#!/usr/bin/env python3
"""Core helpers for loading, validating, compiling, and querying the graph."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
import ast
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
AUTHORED_DIR = ROOT / "data" / "authored"
BATCHES_DIR = ROOT / "data" / "batches"
GENERATED_DIR = ROOT / "data" / "generated"
ALL_AUTHORED_BATCH_ID = "all_authored"

NECESSITY_ORDER = {"helpful": 0, "typical": 1, "necessary": 2}


class YamlSubsetError(ValueError):
    """Raised when a file uses YAML beyond the supported subset."""


def normalize_label(text: str) -> str:
    return "".join(char.lower() for char in text if char.isalnum())


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    chars: list[str] = []
    for char in line:
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            break
        chars.append(char)
    return "".join(chars).rstrip()


def _looks_like_key_value(text: str) -> bool:
    if ":" not in text:
        return False
    key, _ = text.split(":", 1)
    return bool(key.strip())


def _parse_scalar(text: str) -> Any:
    text = text.strip()
    if text == "":
        return ""
    if text in {"true", "True"}:
        return True
    if text in {"false", "False"}:
        return False
    if text in {"null", "None", "~"}:
        return None
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        try:
            return ast.literal_eval(text)
        except (SyntaxError, ValueError):
            return text[1:-1]
    if text.startswith("[") or text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return ast.literal_eval(text)
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def _prepare_lines(text: str) -> list[tuple[int, str]]:
    prepared: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        if "\t" in raw_line:
            raise YamlSubsetError("Tabs are not supported in YAML subset parser.")
        cleaned = _strip_comment(raw_line)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        prepared.append((indent, cleaned.lstrip(" ")))
    return prepared


def _parse_mapping(
    lines: list[tuple[int, str]], start: int, indent: int
) -> tuple[dict[str, Any], int]:
    mapping: dict[str, Any] = {}
    index = start
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent != indent or text.startswith("- "):
            break
        if ":" not in text:
            raise YamlSubsetError(f"Expected mapping at line: {text}")
        key, raw_value = text.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        index += 1
        if raw_value == "":
            if index < len(lines) and lines[index][0] > indent:
                value, index = _parse_block(lines, index, lines[index][0])
            else:
                value = None
        else:
            value = _parse_scalar(raw_value)
        mapping[key] = value
    return mapping, index


def _parse_sequence(
    lines: list[tuple[int, str]], start: int, indent: int
) -> tuple[list[Any], int]:
    items: list[Any] = []
    index = start
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent != indent or not text.startswith("- "):
            break
        remainder = text[2:].strip()
        index += 1
        if remainder == "":
            value, index = _parse_block(lines, index, lines[index][0])
            items.append(value)
            continue
        if _looks_like_key_value(remainder):
            key, raw_value = remainder.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            item: dict[str, Any] = {}
            if raw_value == "":
                if index < len(lines) and lines[index][0] > indent:
                    value, index = _parse_block(lines, index, lines[index][0])
                else:
                    value = None
            else:
                value = _parse_scalar(raw_value)
            item[key] = value
            if index < len(lines) and lines[index][0] > indent:
                extra, index = _parse_mapping(lines, index, lines[index][0])
                item.update(extra)
            items.append(item)
            continue
        items.append(_parse_scalar(remainder))
    return items, index


def _parse_block(
    lines: list[tuple[int, str]], start: int, indent: int
) -> tuple[Any, int]:
    if start >= len(lines):
        raise YamlSubsetError("Unexpected end of document.")
    current_indent, text = lines[start]
    if current_indent < indent:
        raise YamlSubsetError("Invalid indentation.")
    if text.startswith("- "):
        return _parse_sequence(lines, start, indent)
    if ":" not in text:
        return _parse_scalar(text), start + 1
    return _parse_mapping(lines, start, indent)


def load_yaml_subset(path: Path) -> Any:
    text = path.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    lines = _prepare_lines(text)
    if not lines:
        return None
    value, index = _parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise YamlSubsetError(f"Unparsed trailing content in {path}.")
    return value


def load_json(path: Path) -> Any:
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_schema(name: str) -> dict[str, Any]:
    return load_json(SCHEMAS_DIR / name)


def _validate_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def validate_value_against_schema(
    value: Any, schema: dict[str, Any], path: str
) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not _validate_type(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in enum {schema['enum']}")
    if isinstance(value, str) and "minLength" in schema and len(value) < schema["minLength"]:
        errors.append(f"{path}: string shorter than minLength {schema['minLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if schema.get("uniqueItems") and len(value) != len(
            {json.dumps(item, sort_keys=True) for item in value}
        ):
            errors.append(f"{path}: duplicate items not allowed")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(
                    validate_value_against_schema(item, item_schema, f"{path}[{index}]")
                )
    if isinstance(value, dict):
        allowed = set(schema.get("properties", {}))
        if schema.get("additionalProperties") is False:
            extra_keys = set(value) - allowed
            for key in sorted(extra_keys):
                errors.append(f"{path}: unexpected property {key!r}")
        for field in schema.get("required", []):
            if field not in value:
                errors.append(f"{path}: missing required field {field!r}")
        for key, item_schema in schema.get("properties", {}).items():
            if key in value:
                errors.extend(
                    validate_value_against_schema(value[key], item_schema, f"{path}.{key}")
                )
    return errors


def load_batch_contract(batch_id: str) -> dict[str, Any]:
    return load_yaml_subset(BATCHES_DIR / batch_id / "batch_contract.yaml")


def load_batch_brief(batch_id: str) -> str:
    return (BATCHES_DIR / batch_id / "brief.md").read_text()


@dataclass
class BatchRecords:
    batch_id: str
    contract: dict[str, Any]
    nodes: list[dict[str, Any]]
    dependencies: list[dict[str, Any]]
    partonomy: list[dict[str, Any]]
    overlays: list[dict[str, Any]]


def load_batch_records(batch_id: str) -> BatchRecords:
    contract = load_batch_contract(batch_id)
    nodes = load_yaml_subset(AUTHORED_DIR / "nodes" / f"{batch_id}.yaml") or []
    dependencies = (
        load_yaml_subset(AUTHORED_DIR / "dependencies" / f"{batch_id}.yaml") or []
    )
    partonomy = load_yaml_subset(AUTHORED_DIR / "partonomy" / f"{batch_id}.yaml") or []
    overlays = load_yaml_subset(AUTHORED_DIR / "overlays" / f"{batch_id}.yaml") or []
    for label, payload in {
        "nodes": nodes,
        "dependencies": dependencies,
        "partonomy": partonomy,
        "overlays": overlays,
    }.items():
        if not isinstance(payload, list):
            raise ValueError(f"{label} file for {batch_id} must contain a list.")
    return BatchRecords(
        batch_id=batch_id,
        contract=contract,
        nodes=nodes,
        dependencies=dependencies,
        partonomy=partonomy,
        overlays=overlays,
    )


def _load_authored_payload(kind: str) -> list[tuple[str, list[dict[str, Any]]]]:
    records: list[tuple[str, list[dict[str, Any]]]] = []
    directory = AUTHORED_DIR / kind
    for path in sorted(directory.glob("*.yaml")):
        payload = load_yaml_subset(path) or []
        if not isinstance(payload, list):
            raise ValueError(f"{kind} file for {path.stem} must contain a list.")
        records.append((path.stem, payload))
    return records


def _merge_nodes_for_global_bundle(
    node_batches: list[tuple[str, list[dict[str, Any]]]]
) -> tuple[list[dict[str, Any]], list[str]]:
    merged: dict[str, dict[str, Any]] = {}
    origin_by_id: dict[str, str] = {}
    warnings: list[str] = []
    for batch_id, payload in node_batches:
        for node in payload:
            if not isinstance(node, dict) or "id" not in node:
                continue
            node_id = node["id"]
            existing = merged.get(node_id)
            if existing is None:
                merged[node_id] = dict(node)
                origin_by_id[node_id] = batch_id
                continue
            if existing != node:
                warnings.append(
                    "global merge warning: conflicting duplicate node definition for "
                    f"{node_id} between batches {origin_by_id[node_id]} and {batch_id}; "
                    "kept first definition"
                )
    return _sorted_records(list(merged.values()), ["id"]), warnings


def _dedupe_records(
    record_batches: list[tuple[str, list[dict[str, Any]]]],
    sort_keys: list[str],
) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for _, payload in record_batches:
        for record in payload:
            if not isinstance(record, dict):
                continue
            fingerprint = json.dumps(record, sort_keys=True)
            deduped.setdefault(fingerprint, dict(record))
    return _sorted_records(list(deduped.values()), sort_keys)


def load_all_authored_records() -> BatchRecords:
    node_batches = _load_authored_payload("nodes")
    dependency_batches = _load_authored_payload("dependencies")
    partonomy_batches = _load_authored_payload("partonomy")
    overlay_batches = _load_authored_payload("overlays")

    nodes, merge_warnings = _merge_nodes_for_global_bundle(node_batches)
    dependencies = _dedupe_records(dependency_batches, ["relation_type", "from", "to"])
    partonomy = _dedupe_records(partonomy_batches, ["parent", "child"])
    overlays = _dedupe_records(overlay_batches, ["target_topic", "presumed_node"])

    allowed_relations = sorted(
        {
            edge.get("relation_type")
            for edge in dependencies
            if isinstance(edge, dict) and edge.get("relation_type")
        }
    )
    contract = {
        "description": "Synthetic global bundle combining all authored batches.",
        "allowed_relations": allowed_relations,
        "closure": {
            "exclude_statuses": ["disputed"],
        },
        "_merge_warnings": merge_warnings,
    }
    return BatchRecords(
        batch_id=ALL_AUTHORED_BATCH_ID,
        contract=contract,
        nodes=nodes,
        dependencies=dependencies,
        partonomy=partonomy,
        overlays=overlays,
    )


def load_authored_nodes_by_batch(exclude_batch_id: str | None = None) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    nodes_dir = AUTHORED_DIR / "nodes"
    for path in sorted(nodes_dir.glob("*.yaml")):
        batch_id = path.stem
        if exclude_batch_id and batch_id == exclude_batch_id:
            continue
        payload = load_yaml_subset(path) or []
        if not isinstance(payload, list):
            continue
        for node in payload:
            if isinstance(node, dict):
                copied = dict(node)
                copied["_batch_id"] = batch_id
                collected.append(copied)
    return collected


def _status_requires_evidence(status: str) -> bool:
    return status in {"asserted", "reviewed"}


def _cycle_path(graph: dict[str, list[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visiting:
            cycle_start = stack.index(node)
            return stack[cycle_start:] + [node]
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for child in graph.get(node, []):
            cycle = visit(child)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def validate_batch_records(records: BatchRecords) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = list(records.contract.get("_merge_warnings", []))

    node_schema = load_schema("node.schema.json")
    dependency_schema = load_schema("dependency.schema.json")
    partonomy_schema = load_schema("partonomy.schema.json")
    overlay_schema = load_schema("overlay.schema.json")

    for index, node in enumerate(records.nodes):
        errors.extend(validate_value_against_schema(node, node_schema, f"nodes[{index}]"))
    for index, edge in enumerate(records.dependencies):
        errors.extend(
            validate_value_against_schema(edge, dependency_schema, f"dependencies[{index}]")
        )
    for index, edge in enumerate(records.partonomy):
        errors.extend(
            validate_value_against_schema(edge, partonomy_schema, f"partonomy[{index}]")
        )
    for index, overlay in enumerate(records.overlays):
        errors.extend(
            validate_value_against_schema(overlay, overlay_schema, f"overlays[{index}]")
        )

    node_ids = [node["id"] for node in records.nodes if isinstance(node, dict) and "id" in node]
    duplicate_ids = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    for node_id in duplicate_ids:
        errors.append(f"duplicate node id: {node_id}")

    node_id_set = set(node_ids)
    existing_nodes = load_authored_nodes_by_batch(exclude_batch_id=records.batch_id)
    for node in records.nodes:
        node_label = node.get("label")
        if not node_label:
            continue
        normalized = normalize_label(node_label)
        aliases = [normalize_label(alias) for alias in node.get("aliases", [])]
        for existing in existing_nodes:
            if existing.get("id") == node.get("id"):
                continue
            existing_label = existing.get("label", "")
            existing_aliases = existing.get("aliases", []) or []
            if node_label == existing_label:
                warnings.append(
                    "overlap risk: label match between "
                    f"{node.get('id')} and {existing.get('id')} "
                    f"(batch {existing.get('_batch_id')})"
                )
                continue
            existing_normalized = normalize_label(existing_label)
            if normalized and normalized == existing_normalized:
                warnings.append(
                    "overlap risk: normalized label match between "
                    f"{node.get('id')} and {existing.get('id')} "
                    f"('{node_label}' ~ '{existing_label}')"
                )
                continue
            existing_alias_norm = [normalize_label(alias) for alias in existing_aliases]
            if normalized in existing_alias_norm or any(
                alias in {existing_normalized, *existing_alias_norm} for alias in aliases
            ):
                warnings.append(
                    "overlap risk: alias/label match between "
                    f"{node.get('id')} and {existing.get('id')} "
                    f"(batch {existing.get('_batch_id')})"
                )

    allowed_relations = set(records.contract.get("allowed_relations", []))
    for edge in records.dependencies:
        from_id = edge.get("from")
        to_id = edge.get("to")
        if from_id == to_id and from_id is not None:
            errors.append(f"dependency self-loop: {from_id} -> {to_id}")
        if from_id not in node_id_set:
            errors.append(f"dependency references missing from-node: {from_id}")
        if to_id not in node_id_set:
            errors.append(f"dependency references missing to-node: {to_id}")
        if edge.get("relation_type") not in allowed_relations:
            errors.append(
                "dependency relation not allowed by contract: "
                f"{edge.get('relation_type')}"
            )
        if _status_requires_evidence(edge.get("status", "")) and not edge.get("evidence"):
            errors.append(
                "asserted dependency edge must include non-empty evidence: "
                f"{from_id} -> {to_id}"
            )

    partonomy_graph: dict[str, list[str]] = {}
    for edge in records.partonomy:
        parent = edge.get("parent")
        child = edge.get("child")
        if parent == child and parent is not None:
            errors.append(f"partonomy self-loop: {parent} -> {child}")
        if parent not in node_id_set:
            errors.append(f"partonomy references missing parent node: {parent}")
        if child not in node_id_set:
            errors.append(f"partonomy references missing child node: {child}")
        partonomy_graph.setdefault(parent, []).append(child)
    cycle = _cycle_path(partonomy_graph)
    if cycle:
        errors.append(f"part_of cycle detected: {' -> '.join(cycle)}")

    for overlay in records.overlays:
        target = overlay.get("target_topic")
        presumed = overlay.get("presumed_node")
        if target not in node_id_set:
            errors.append(f"overlay references missing target topic: {target}")
        if presumed not in node_id_set:
            errors.append(f"overlay references missing presumed node: {presumed}")

    report = {
        "batch_id": records.batch_id,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "nodes": len(records.nodes),
            "dependencies": len(records.dependencies),
            "partonomy": len(records.partonomy),
            "overlays": len(records.overlays),
        },
        "errors": sorted(errors),
        "warnings": sorted(warnings),
        "valid": not errors,
    }
    return report


def _sorted_records(records: list[dict[str, Any]], keys: list[str]) -> list[dict[str, Any]]:
    def key_func(item: dict[str, Any]) -> tuple[Any, ...]:
        return tuple(item.get(key, "") for key in keys)

    return sorted(records, key=key_func)


def compile_batch(records: BatchRecords) -> dict[str, Any]:
    node_by_id = {node["id"]: node for node in records.nodes}
    dependencies = _sorted_records(
        records.dependencies,
        ["relation_type", "from", "to"],
    )
    partonomy = _sorted_records(records.partonomy, ["parent", "child"])
    overlays = _sorted_records(records.overlays, ["target_topic", "presumed_node"])

    bundle = {
        "batch_id": records.batch_id,
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "contract": records.contract,
        "nodes": _sorted_records(records.nodes, ["id"]),
        "dependencies": dependencies,
        "partonomy": partonomy,
        "overlays": overlays,
        "indexes": {
            "node_ids": sorted(node_by_id),
            "children_by_parent": _group_partonomy_children(partonomy),
            "parents_by_child": _group_partonomy_parents(partonomy),
        },
    }
    return bundle


def _group_partonomy_children(partonomy: list[dict[str, Any]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for edge in partonomy:
        grouped.setdefault(edge["parent"], []).append(edge["child"])
    for value in grouped.values():
        value.sort()
    return grouped


def _group_partonomy_parents(partonomy: list[dict[str, Any]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for edge in partonomy:
        grouped.setdefault(edge["child"], []).append(edge["parent"])
    for value in grouped.values():
        value.sort()
    return grouped


def compiled_bundle_path(batch_id: str) -> Path:
    return GENERATED_DIR / "compiled" / f"{batch_id}.graph.json"


def validation_report_path(batch_id: str) -> Path:
    return GENERATED_DIR / "reports" / f"{batch_id}.validation.json"


def load_or_compile_bundle(batch_id: str) -> dict[str, Any]:
    path = compiled_bundle_path(batch_id)
    if path.exists():
        return load_json(path)
    if batch_id == ALL_AUTHORED_BATCH_ID:
        records = load_all_authored_records()
    else:
        records = load_batch_records(batch_id)
    report = validate_batch_records(records)
    if not report["valid"]:
        raise ValueError(json.dumps(report, indent=2))
    bundle = compile_batch(records)
    write_json(path, bundle)
    return bundle


def _contract_excluded_statuses(bundle: dict[str, Any]) -> set[str]:
    return set(bundle["contract"].get("closure", {}).get("exclude_statuses", []))


def _match_optional_context(edge: dict[str, Any], profile: dict[str, Any] | None) -> bool:
    if not profile:
        return True
    for field in ("audience_profile", "subfield", "task_type"):
        edge_value = edge.get(field)
        profile_value = profile.get(field)
        if edge_value and profile_value and edge_value != profile_value:
            return False
    return True


def _filtered_dependencies(
    bundle: dict[str, Any],
    relation_type: str,
    profile: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    excluded_statuses = _contract_excluded_statuses(bundle)
    return [
        edge
        for edge in bundle["dependencies"]
        if edge["relation_type"] == relation_type
        and edge["status"] not in excluded_statuses
        and _match_optional_context(edge, profile)
    ]


def _aggregate_confidence(path: list[dict[str, Any]]) -> float:
    return min(edge["confidence"] for edge in path)


def _aggregate_necessity(path: list[dict[str, Any]]) -> str:
    return min(path, key=lambda edge: NECESSITY_ORDER[edge["necessity"]])["necessity"]


def prerequisites(
    bundle: dict[str, Any],
    target: str,
    relation_type: str,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    nodes = {node["id"]: node for node in bundle["nodes"]}
    if target not in nodes:
        raise KeyError(f"Unknown target node: {target}")

    incoming: dict[str, list[dict[str, Any]]] = {}
    for edge in _filtered_dependencies(bundle, relation_type, profile):
        incoming.setdefault(edge["to"], []).append(edge)

    best_paths: dict[str, list[dict[str, Any]]] = {}
    queue: deque[tuple[str, list[dict[str, Any]]]] = deque([(target, [])])
    while queue:
        current, path_to_target = queue.popleft()
        for edge in incoming.get(current, []):
            prereq = edge["from"]
            new_path = [edge] + path_to_target
            prior = best_paths.get(prereq)
            if prior is None or len(new_path) < len(prior):
                best_paths[prereq] = new_path
                queue.append((prereq, new_path))

    results = []
    for node_id, path in sorted(best_paths.items(), key=lambda item: (len(item[1]), item[0])):
        results.append(
            {
                "node_id": node_id,
                "label": nodes[node_id]["label"],
                "asserted_direct": len(path) == 1,
                "derived": len(path) > 1,
                "distance": len(path),
                "path_edges": [
                    {
                        "from": edge["from"],
                        "to": edge["to"],
                        "relation_type": edge["relation_type"],
                        "confidence": edge["confidence"],
                        "necessity": edge["necessity"],
                    }
                    for edge in path
                ],
                "relation_composition_trace": [edge["relation_type"] for edge in path],
                "aggregated_confidence": _aggregate_confidence(path),
                "aggregated_necessity": _aggregate_necessity(path),
            }
        )

    return {
        "target": target,
        "relation_type": relation_type,
        "profile": profile or {},
        "results": results,
    }


def prerequisite_set(
    bundle: dict[str, Any],
    target: str,
    relation_type: str,
    semantics: str,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if semantics not in {"ancestral_frontier", "policy_selected_frontier"}:
        raise ValueError(f"Unsupported prerequisite set semantics: {semantics}")

    prereq_result = prerequisites(bundle, target, relation_type, profile)
    ancestors = {item["node_id"] for item in prereq_result["results"]}
    edges = _filtered_dependencies(bundle, relation_type, profile)

    frontier = sorted(
        node_id
        for node_id in ancestors
        if not any(edge["to"] == node_id and edge["from"] in ancestors for edge in edges)
    )
    payload = {
        "target": target,
        "relation_type": relation_type,
        "semantics": semantics,
        "unique": True,
        "alternatives_suppressed": False,
        "sets": [frontier],
    }
    if semantics == "policy_selected_frontier":
        payload["policy"] = "lexicographic_on_frontier_ids"
    return payload


def intrinsic_vs_profile_adjusted(
    bundle: dict[str, Any],
    target: str,
    relation_type: str,
    profile: dict[str, Any],
) -> dict[str, Any]:
    intrinsic = prerequisites(bundle, target, relation_type, profile=None)
    intrinsic_ids = {item["node_id"] for item in intrinsic["results"]}
    presumed = sorted(
        overlay["presumed_node"]
        for overlay in bundle["overlays"]
        if overlay["target_topic"] == target
        and overlay["overlay_type"] == "assumed_background"
        and _match_optional_context(overlay, profile)
        and overlay["presumed_node"] in intrinsic_ids
    )
    remaining = sorted(intrinsic_ids - set(presumed))
    return {
        "target": target,
        "relation_type": relation_type,
        "profile": profile,
        "intrinsic_prerequisites": sorted(intrinsic_ids),
        "presumed_by_profile": presumed,
        "remaining_unmet_prerequisites": remaining,
    }


def expanded_slice(
    bundle: dict[str, Any],
    target: str,
    relation_type: str,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prereq_result = prerequisites(bundle, target, relation_type, profile)
    included = {target} | {item["node_id"] for item in prereq_result["results"]}
    dependency_edges = [
        edge
        for edge in _filtered_dependencies(bundle, relation_type, profile)
        if edge["from"] in included and edge["to"] in included
    ]
    partonomy_edges = [
        edge
        for edge in bundle["partonomy"]
        if edge["parent"] in included or edge["child"] in included
    ]
    included |= {edge["parent"] for edge in partonomy_edges}
    included |= {edge["child"] for edge in partonomy_edges}
    return {
        "target": target,
        "relation_type": relation_type,
        "nodes": sorted(included),
        "dependencies": dependency_edges,
        "partonomy": partonomy_edges,
    }


def render_mermaid(
    bundle: dict[str, Any],
    target: str,
    relation_type: str,
    profile: dict[str, Any] | None = None,
) -> str:
    slice_payload = expanded_slice(bundle, target, relation_type, profile)
    nodes = {node["id"]: node["label"] for node in bundle["nodes"]}
    lines = ["graph TD"]
    for node_id in slice_payload["nodes"]:
        label = nodes.get(node_id, node_id).replace('"', "'")
        lines.append(f'  "{node_id}"["{label}"]')
    for edge in slice_payload["dependencies"]:
        lines.append(f'  "{edge["from"]}" --> "{edge["to"]}"')
    for edge in slice_payload["partonomy"]:
        lines.append(f'  "{edge["child"]}" -.-> "{edge["parent"]}"')
    return "\n".join(lines)
