# Query Semantics

## Purpose

This document defines the MVP query behavior for the HEP-TH prerequisite graph.

All query execution must be parameterized by a machine-readable batch contract. The contract, not informal prose, determines:

- which relations are traversable,
- which composition rules are allowed,
- whether context is fixed,
- whether composite expansion is enabled,
- and how prerequisite-set style queries are interpreted.

## Core Rule

Source data stores asserted facts only.

Derived ancestors, closures, and query outputs are computed at query time and must be labeled as derived rather than asserted.

## Allowed Default Traversal

In the MVP:

- prerequisite queries traverse dependency relations only,
- `part_of` is not traversed unless composite expansion is explicitly enabled,
- assumed-background overlays do not rewrite intrinsic dependency structure,
- disputed edges are excluded from default traversal,
- and heterogeneous dependency composition is forbidden unless the batch contract explicitly allows it.

## Query 1: Prerequisites

Signature:

```text
prerequisites(target, relation_type, expand_composites=false, profile=null)
```

Meaning:

- return all ancestors of `target` under the selected dependency relation,
- using the composition rules from the batch contract,
- with every derived step traceable to asserted source edges.

Required output metadata:

- selected relation type
- batch contract id or version
- whether composites were expanded
- context filters used
- which results are asserted vs derived

## Query 2: Contract-Defined Prerequisite Set

Signature:

```text
prerequisite_set(target, semantics, relation_type, expand_composites=false, profile=null)
```

Meaning:

- return one or more prerequisite sets according to the semantics named in the batch contract,
- not according to an implicit global notion of "minimal prerequisites."

Allowed MVP semantics:

- `ancestral_frontier`
- `policy_selected_frontier`

Formal MVP definitions:

- `ancestral_frontier`: the subset of prerequisite ancestors with no incoming edge from another returned ancestor under the same traversed relation type.
- `policy_selected_frontier`: for the MVP, the same frontier set as `ancestral_frontier`, returned under a deterministic selection policy because alternative support-set semantics are not yet implemented.

Required output metadata:

- semantics used
- whether the result is unique
- whether alternatives were suppressed by tie-breaking
- any warnings about incomparability or low-confidence support

## Query 3: Intrinsic vs Profile-Adjusted View

Signature:

```text
intrinsic_vs_profile_adjusted(target, relation_type, profile)
```

Meaning:

- show intrinsic prerequisites under dependency relations,
- then show which nodes are treated as already presumed by the selected overlay or profile,
- without erasing the underlying intrinsic structure.

Required output sections:

- intrinsic prerequisites
- presumed-by-profile nodes
- remaining unmet prerequisites after adjustment

## Query 4: Expanded Topic Slice

Signature:

```text
expanded_slice(target, relation_type, expand_composites=true, profile=null)
```

Meaning:

- show the relevant dependency neighborhood for a target,
- optionally expanding composite nodes through `part_of`,
- while keeping structural and dependency edges visually distinct.

## Query 5: Shortest Path

Signature:

```text
shortest_path(source, target, relation_type)
```

Meaning:

- return a path only when explicitly requested,
- never present it as recommended pedagogy by default,
- and always label it as a path under the chosen semantics, not as canonical learning order.

## Composition Policy

The MVP should use conservative composition:

- homogeneous dependency composition is allowed only when enabled by contract,
- heterogeneous dependency composition is forbidden by default,
- composition never crosses `part_of`,
- composition never crosses a context change unless explicitly allowed,
- and disputed edges poison the chain unless explicitly included.

For the seed implementation:

- `allowed_relation_chains` is interpreted as a whitelist of adjacent relation-type pairs that may compose during closure,
- `necessity_propagation: min` means take the weakest necessity along the path using the order `helpful < typical < necessary`,
- and `confidence_propagation: min` means take the minimum numeric confidence on the path.

## Reporting Requirements

Every nontrivial query result should be accompanied by:

- output set
- derivation provenance
- relation-composition trace
- confidence bottlenecks
- semantic warnings

This is part of the core product, not optional debugging output.
