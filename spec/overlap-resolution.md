# Overlap Resolution

## Purpose

This document defines how to handle new topics that overlap existing graph content.

The graph should not duplicate local neighborhoods just because a new batch is framed differently. Every candidate node should be classified relative to existing graph content before merge.

## Allowed Dispositions

- `reuse_existing`
- `alias_existing`
- `new_distinct`
- `part_of_existing`
- `ambiguous`

## Decision Order

For each candidate node, ask these questions in order:

1. Is there already an existing node with the same meaning for current query purposes?
   If yes: `reuse_existing`.
2. Is this the same concept under a different label?
   If yes: `alias_existing`.
3. Is this best modeled as a structural subtopic of an existing node?
   If yes: `part_of_existing`.
4. Is it genuinely distinct, but overlapping in background?
   If yes: `new_distinct`.
5. If none of the above can be defended clearly:
   mark it `ambiguous` and escalate.

## Practical Reading of the Outcomes

### `reuse_existing`

- no new node is created
- the batch points to the existing node id

### `alias_existing`

- no new canonical node is created
- the new label should be attached to the existing node as an alias

### `new_distinct`

- create a new node
- reuse shared prerequisites instead of duplicating background structure

### `part_of_existing`

- create a new node
- add a structural `part_of` edge to the larger topic

### `ambiguous`

- do not auto-merge
- require review of the possible matches and the proposed distinction

## Evidence of Overlap

Useful signals include:

- exact or near-exact label match
- explicit synonymy in source material
- indistinguishable dependency behavior in current queries
- same role in paper-facing manifests
- same downstream uses with no meaningful semantic distinction

These signals are suggestive, not decisive.

## Validator Heuristics

The validator may use cheap heuristics to flag overlap risk:

- exact label match
- normalized-label match
- candidate label matching an existing alias

These heuristics should create warnings, not silent merges.

## Required Overlap Review Fields

Each node proposal should include or be accompanied by:

- `overlap_disposition`
- `possible_existing_matches`
- a short rationale for the chosen disposition

## Escalation Triggers

Escalate when:

- two nodes appear to have the same meaning but different ids,
- a proposal has no clear distinction from an existing node,
- a candidate looks like a subtopic but no defensible `part_of` claim is available,
- or overlap would materially change existing query outputs.
