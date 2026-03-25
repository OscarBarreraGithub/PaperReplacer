# Review Policy

## Purpose

This document defines the exception-driven human review policy for graph changes.

## Review Statuses

Every proposed item should end in one of these states:

- `auto_accepted`
- `accepted`
- `needs_revision`
- `disputed`
- `deferred`

## Default Policy

Low-risk items should be merged automatically by the orchestrator when they satisfy the active batch contract.

Human review is reserved for exceptions.

## What Must Be Reviewed

For each batch, the orchestrator should present exception packets covering:

- newly proposed nodes
- newly proposed dependency edges
- newly proposed `part_of` relations
- overlay proposals
- low-confidence items
- ontology drift risks
- duplicate or near-duplicate concepts
- overlap-disposition ambiguities
- any contract violations or warnings

## Automatic Merge Rule

An item may be auto-accepted into canonical authored graph data when:

- schema and invariant checks pass,
- confidence is above the batch threshold,
- no ontology drift warning is present,
- no unresolved duplicate-risk warning is present,
- no disputed dependency is involved,
- and the query probe reports no blocking semantic warning.

## Human Review Rule

Only `accepted` or `auto_accepted` items may move into canonical authored graph data.

`disputed` items must remain out of default compiled results unless a future parallel-view system is added.

## Minimum Review Packet for Dependency Edges

Every dependency edge review should show:

- `from`
- `to`
- relation type
- rationale
- evidence summary
- confidence
- the concrete failure if the prerequisite is absent

## Query Review Packet

Every batch query report should include:

- the contract and semantics used
- asserted vs derived results
- warnings about context mixing
- warnings about suppressed alternatives
- warnings about disputed-edge adjacency

## Escalation Rule

Escalate for human decision when:

- a prerequisite edge could plausibly be inverted,
- a proposed node duplicates an existing node's dependency behavior,
- a node's overlap disposition is ambiguous or weakly justified,
- a proposal changes the intended decomposition of an existing composite,
- an overlay appears to hide intrinsic structure that readers should still see,
- a query result looks authoritative but depends on low-confidence or inferred links,
- the batch contract's warning threshold is exceeded,
- or a forbidden heuristic is triggered.
