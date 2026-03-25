# Ontology Rules

## Node Admissibility

A node is admissible only if:

- it has a stable enough meaning across relevant sources,
- it participates in at least one nontrivial dependency or partonomy claim,
- it is not so broad that all interesting queries terminate there,
- it is not so narrow that it only appears as a one-off artifact,
- its dependency behavior is not indistinguishable from that of its parent in all current use-cases,
- and it can be summarized without referring to a textbook chapter boundary.

## Node Kinds

The MVP allows these `knowledge_kind` values:

- `concept`
- `method`
- `representation`
- `formal_statement`

## Granularity

The MVP allows these `granularity_level` values:

- `survey`
- `intermediate`
- `atomic`

Operational rule:

- if a broad node already exists and a downstream query depends on only one identifiable subpiece, split the node,
- otherwise prefer not to fragment the graph early.

## Overlap Rule

Closely related topics should not be handled by duplicating nodes under slightly different names.

Every candidate node must be classified relative to existing graph content as one of:

- `reuse_existing`
- `alias_existing`
- `new_distinct`
- `part_of_existing`

The detailed workflow lives in [overlap-resolution.md](/Users/emmy/Documents/KnowledgeGraph/spec/overlap-resolution.md).

Operational rule:

- if a candidate node has no meaningful distinction in dependency behavior from an existing node for current query purposes, do not add it as a new node.

## Dependency Edge Meaning

Canonical reading:

- edge `(A, B, requires_for_use)` means `A` is required in order to use `B`.

The `from` node is always the prerequisite. The `to` node is always the downstream topic.

## Dependency Relations

The MVP dependency relations are:

- `requires_for_recognize`
- `requires_for_use`
- `requires_for_derive`
- `pedagogically_precedes`

## Structural Relations

The MVP structural relation is:

- `part_of`

`part_of` is not a prerequisite relation and must not be mixed into default dependency traversal.

## Overlay Rules

Assumed background is modeled as contextual overlay data, not as intrinsic ontology.

Overlay annotations must include context such as:

- audience profile
- subfield

Later versions may add artifact or genre.

## Evidence Requirements

Every asserted dependency edge must include:

- a rationale
- an evidence record
- a status
- a confidence value

Each evidence record should say what kind of support is being offered, for example:

- `expert_claim`
- `textual_evidence`
- `corpus_evidence`
- `inferred`

## Edge Review Question

Every dependency proposal should answer this question explicitly:

- what concrete failure occurs if the prerequisite is absent?

Examples:

- cannot parse standard statement
- cannot interpret notation
- cannot execute contour deformation argument
- cannot justify derivation step

## Forbidden Patterns

Do not allow:

- chapter-title nodes
- global assumed-background claims without context
- prerequisite edges justified only by teaching order unless relation type is pedagogical
- broad umbrella nodes as prerequisites when a better decomposition already exists
- duplicate nodes that differ only by label while serving the same dependency role
- shortest-path output presented as pedagogy by default
- silent traversal across `part_of` in prerequisite queries
