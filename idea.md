# Idea: A Trustworthy Prerequisite Graph for HEP-TH

## 1. Goal

The project is to build a formal, queryable graph that represents the background needed to understand research topics in high-energy theoretical physics.

The graph should support workflows like:

- declaring assumed background for a paper,
- finding the minimal background needed to follow a topic,
- exposing the relevant slice of QFT behind a research concept,
- and giving LLMs a precise map of what knowledge is being assumed.

The key constraint is that the graph must be trustworthy, not merely easy to populate. A large concept map with vague arrows would be decorative but unreliable. The design should therefore prioritize semantic discipline over breadth.

## 2. Foundational Principle

We should not collapse all "comes before" relations into a single edge type.

At least four different notions must be kept distinct:

- epistemic dependency: what must already be understood to understand or use something else,
- didactic order: what is best taught first,
- sociological expectation: what a community usually assumes,
- plus a separate structural relation: partonomy or decomposition.

These do not behave the same way under inference.

For example:

- epistemic dependency is often directional and approximately transitive,
- pedagogical order is directional but only weakly transitive,
- sociological expectation is highly context-dependent and should not be treated as globally stable,
- partonomy is not an epistemic dependency at all.

This means relation types must be classified not only by meaning, but by formal behavior.

## 3. Formal Behavior of Relations

Before implementation, each relation class should be defined by how it behaves under queries.

### Dependency relations

These encode prerequisite claims relative to a competence target.

Core questions:

- Is the relation directional?
- Is it approximately transitive?
- Should it participate in minimal-prerequisite queries?
- Should it be allowed in shortest-path computations?
- Does it inherit through decomposition?
- Can it be aggregated across audiences?

Working semantics:

| Relation | Directional | Closure policy | Used in minimal prerequisite queries | Allowed in shortest-path style queries | Needs context |
| --- | --- | --- | --- | --- | --- |
| `requires_for_recognize` | yes | query-time only, inferred results marked derived | yes | yes, with care | optional |
| `requires_for_use` | yes | query-time only, within selected context | yes | yes | optional |
| `requires_for_derive` | yes | query-time only, within selected context | yes | yes | optional |
| `pedagogically_precedes` | yes | no closure by default | no by default | no by default | optional |
| `part_of` | yes | structural only | no | no | no |

This table is not just documentation. It should drive query implementation.

Assumed background is intentionally excluded from this table. For the MVP it should be modeled as a contextual overlay rather than as a traversable dependency relation.

### Operational closure policy

To avoid ambiguity, transitive consequences should not be stored as first-class source edges.

Working policy:

- source data stores only asserted dependency edges,
- transitive closure is computed only at query time,
- inferred ancestors are labeled as inferred rather than asserted,
- closure never crosses partonomy,
- closure does not cross context changes by default,
- disputed edges are excluded from closure unless explicitly requested.

## 4. Mastery-Relative Prerequisites

The graph should not have a single undifferentiated notion of "logical prerequisite."

Instead, prerequisite claims should be made relative to a target level of engagement with a topic.

Minimum mastery modes for MVP:

- `recognize`
- `use`
- `derive`

Interpretation:

- `recognize`: identify the object, parse standard statements involving it, and understand its role in the literature at a basic level.
- `use`: execute standard manipulations, computations, or inferential moves involving the topic without reconstructing its foundational derivation.
- `derive`: reproduce standard derivations and justify the formal underpinnings well enough to adapt or extend them in research.

Representation or notation fluency may enter already at the `recognize` level when the practical task is literature-facing rather than purely conceptual.

This matters immediately. The background needed to recognize `pinch singularities` is much smaller than the background needed to derive Landau conditions or analyze contour pinches rigorously.

Canonical edge reading:

- edge `(A, B, requires_for_use)` means `A` is required in order to use `B`.

So prerequisite edges should not be described in prose as "`A` requires `B`." The intended reading is always that the `from` node is a prerequisite for the `to` node at the specified mastery mode.

## 5. Keep Partonomy Separate from Dependency

Decomposition and prerequisite relations must not live in the same edge pool.

Examples:

- `propagators part_of QFT analytic structure`
- `contour deformation requires_for_use pinch singularities`

These are different kinds of facts.

If `part_of` is mixed with epistemic edges, path semantics become unreliable and queries silently return nonsense. Traversing across decomposition should always be a deliberate operation.

So the model should contain two distinct layers:

### Dependency layer

Used for prerequisite and pedagogical queries.

### Partonomy layer

Used for expanding composite nodes into children or collapsing detailed graphs into higher-level summaries.

Controlled inheritance rules should be defined explicitly. For example:

- children do not automatically inherit all prerequisites of the parent,
- a paper declaring a composite node as assumed background may optionally expand into selected children,
- minimal prerequisite queries should not traverse partonomy unless composite expansion is explicitly requested.

## 6. Treat Assumed Background as Contextual, Not Timeless

"Assumed background" is not an intrinsic relation in the same sense as epistemic dependency.

It depends on context such as:

- audience profile,
- subfield,
- era,
- venue,
- seminar or paper genre.

So the MVP should not treat assumed background as a timeless global edge.

Better options:

- represent it as a profile overlay,
- or require mandatory context fields on any assumed-background annotation.

Working recommendation for MVP:

- treat assumed background as a contextual overlay, not as a core dependency edge.

Example:

- in the context `hep_th_grad / amplitudes`, topic `Lorentz invariance` is presumed when discussing `pinch singularities`.

This prevents sociology from being mistaken for ontology.

## 7. Node Admissibility and Granularity Rules

Granularity cannot remain an informal policy. We need operational criteria for what counts as a valid node.

### A node is admissible if:

- it has a reasonably stable meaning across sources,
- it can participate in at least one nontrivial dependency claim,
- it is not so broad that interesting queries always terminate there,
- it is not so narrow that it appears only once as an artifact,
- its dependency behavior is not indistinguishable from that of its parent in all current use-cases,
- it can be summarized in one or two sentences without referring to a specific textbook chapter.

### Node schema should distinguish at least:

- `knowledge_kind`: concept / method / representation / formal_statement
- `granularity_level`: survey / intermediate / atomic
- `composite`: true or false
- `mastery_modes_supported`: recognize / use / derive

Examples:

- `Lorentz invariance`: concept
- `contour deformation`: method
- `spinor-helicity notation`: representation
- `LSZ reduction formula`: formal_statement

This is more stable than a flat type list mixing ontology, pedagogy, and skill level.

## 8. Dependency Metadata

The current idea of edge `strength` is too ambiguous. It mixes necessity with usefulness.

Instead, dependency annotations should separate:

- `necessity`: necessary / typical / helpful
- `confidence`: low / medium / high or numeric
- `context`: audience profile, subfield, task when relevant
- `rationale`: short free-text explanation

This keeps distinct:

- how necessary the dependency is,
- how certain we are about the annotation,
- and where the claim is supposed to apply.

## 9. Provenance Must Be First-Class

Provenance should not be optional metadata added later. It is necessary from the start.

Every dependency assertion should include:

- `provenance`: where the annotation came from,
- `evidence_type`: what kind of support is being offered.

These should not be conflated. An expert assertion, a textbook usage pattern, and a corpus observation are different kinds of support.

Typical evidence types:

- `expert_claim`
- `textual_evidence`
- `corpus_evidence`
- `inferred`

Typical provenance sources include:

- expert annotation,
- textbook citation,
- paper usage evidence,
- curriculum evidence,
- inferred from decomposition or an earlier reviewed edge.

Suggested edge lifecycle:

- `asserted`
- `reviewed`
- `disputed`

Without provenance, disagreements will become unresolvable and the graph will look more objective than it is.

## 10. Minimal Core Ontology for MVP

The MVP should be smaller and more typed than the earlier draft.

### Node categories

Only:

- `concept`
- `method`
- `representation`
- `formal_statement`

### Dependency relations

Only:

- `requires_for_recognize`
- `requires_for_use`
- `requires_for_derive`
- `pedagogically_precedes`

### Structural relations

Only:

- `part_of`

### Context fields

Only:

- `audience_profile`
- `subfield`

The schema should remain extensible for later contextual overlays such as artifact or genre, for example paper, seminar, or lecture notes.

### Evidence requirements

Mandatory:

- free-text rationale
- at least one provenance item

This is enough to test real queries without prematurely broadening the ontology.

## 11. Query Semantics Spec

No data should be seeded until the main queries are defined precisely.

### Query: "Show all prerequisites of X"

This must specify:

- which dependency relations are included,
- which mastery mode is targeted,
- whether composite nodes should be expanded,
- whether context filters are active.

Default proposal:

- interpret as all ancestors under one selected `requires_for_*` relation,
- with partonomy traversal disabled unless `expand_composites=true`.

### Query: "Minimal prerequisites for Y"

This is not a trivial graph traversal and must be defined carefully.

It should specify:

- target mastery mode,
- allowed relation types,
- whether context overlays are included,
- whether composites are expanded,
- what notion of minimality is being used.

Important note:

- there may be multiple incomparable minimal prerequisite sets.
- the system must not imply that one returned set is uniquely canonical unless uniqueness has actually been established under the chosen semantics.

So the system should be prepared to return either:

- one canonicalized set under a deterministic policy,
- or multiple minimal sets if the semantics support that.

Any answer to this query should report:

- the semantics used,
- whether the returned set is unique,
- and whether alternatives were suppressed by deterministic tie-breaking.

### Query: "What should a paper list as assumed background?"

This should not be derived from timeless global edges.

Instead it should be computed from:

- the paper's declared audience profile,
- the chosen topic nodes,
- and an assumed-background overlay or profile specification.

### Query: "Show the relevant slice of QFT behind topic X"

This should:

- expand composite nodes selectively,
- filter to dependency and partonomy relations appropriate for the requested mastery level,
- and avoid collapsing everything into the monolith node `QFT`.

### Query: "Shortest path from A to B"

This is dangerous and should be opt-in only.

If supported at all, it should:

- operate only on selected dependency relations,
- never be interpreted automatically as recommended pedagogy,
- and state that the result is merely a path under the chosen semantics.

## 12. Anti-Patterns

The plan should explicitly forbid the following:

- nodes that are really textbook chapter titles,
- prerequisite edges justified only by "usually taught before" unless relation type is pedagogical,
- broad subject nodes used as prerequisites when a finer decomposition already exists,
- assumed-background claims without context,
- shortest-path results being presented as pedagogy by default,
- mixing `part_of` with dependency edges in one traversal without explicit expansion rules.

## 13. Initial Seed Slice

The first seeded graph should be narrow and stress-test semantics instead of breadth.

Recommended seed area:

- complex analysis relevant to contour methods,
- relativistic kinematics,
- a minimal QFT analytic-structure slice,
- one research target: `pinch singularities`.

The purpose is to test whether the ontology can represent a real research-facing dependency problem without obvious nonsense.

To reduce decomposition risk, the seed should be staged.

### Seed A

- contour deformation
- poles vs branch points
- Feynman `i epsilon` prescription
- propagator singularities
- pinch singularities

### Seed B

- boundary values and distributions
- loop-momentum integration structure
- analytic continuation in kinematic invariants
- Landau singularity conditions

Potential seed nodes across both stages:

- contour deformation
- poles vs branch points
- boundary values and distributions
- Feynman `i epsilon` prescription
- propagator singularities
- loop-momentum integration structure
- analytic continuation in kinematic invariants
- Landau singularity conditions
- pinch singularities

These should be annotated at explicit mastery modes rather than placed in one vague concept chain.

## 14. Paper Workflow

One end goal remains the same: a paper should be able to declare structured assumed background instead of writing a diluted introduction.

Proposed workflow:

1. Author tags the paper with one or more topic nodes.
2. Author specifies an audience profile.
3. Tool computes the relevant dependency slice at a chosen mastery mode.
4. Tool proposes an assumed-background manifest from the contextual overlay and chosen nodes.
5. Author reviews, prunes, or augments that proposal.
6. Readers or LLMs inspect the missing prerequisites outside the paper itself.

Outputs could include:

- a short assumed-background section,
- a machine-readable manifest,
- an interactive graph view,
- a context-aware LLM prompt scaffold.

## 15. Storage and Validation

Recommended format strategy:

- author data in YAML,
- validate with JSON Schema or Pydantic,
- compile to canonical normalized JSON for querying.

Requirements:

- stable IDs from the beginning,
- IDs should be hierarchical enough to organize the graph,
- but not so semantically rigid that refactoring becomes painful.
- IDs should either support explicit rename migrations or be backed by tooling that preserves stable references across ontology refactors.

Example:

- `qft.propagator.feynman_prescription`

is acceptable if we are willing to build refactoring support later.

## 16. Example Schemas

### Node

```yaml
id: qft.pinch_singularities
label: Pinch singularities
knowledge_kind: concept
granularity_level: atomic
composite: false
mastery_modes_supported:
  - recognize
  - use
  - derive
summary: Singular configurations in which contour deformations are obstructed by competing singularities.
```

### Dependency edge

```yaml
from: complex_analysis.contour_deformation
to: qft.pinch_singularities
relation_type: requires_for_use
necessity: necessary
audience_profile: hep_th_grad
subfield: amplitudes
rationale: Understanding pinch singularities requires knowing when contour deformations fail because singularities trap the contour.
evidence_type: expert_claim
provenance:
  - kind: expert_annotation
    source: initial_seed
status: asserted
confidence: 0.85
```

### Partonomy relation

```yaml
parent: qft.analytic_structure
child: qft.pinch_singularities
```

## 17. Schema Invariants

The MVP should enforce a small set of invariants from the beginning:

- `part_of` relations must be acyclic.
- dependency relations must not create self-loops.
- every edge endpoint must reference an existing node.
- every dependency edge must encode mastery mode through its relation type.
- every contextual assumed-background annotation must specify context.
- every asserted dependency edge must include rationale, evidence type, and provenance.

## 18. Immediate Next Steps

The next work should proceed in this order:

1. Define query semantics for five concrete queries.
2. Define node admissibility and decomposition rules.
3. Define dependency and partonomy semantics, especially transitivity and context dependence.
4. Implement schema validation.
5. Seed one very small graph slice around contour methods, analytic structure, and pinch singularities.
6. Manually test whether the graph answers a few nontrivial paper-oriented questions without obvious semantic failure.

Only after that should we expand toward a broader backbone such as `math -> SR/QM -> QFT`.

## 19. Bottom Line

Four commitments should be treated as non-negotiable:

- prerequisites must be mastery-relative,
- partonomy must be separate from dependency,
- assumed background must be contextual,
- query semantics must be defined before large-scale population.

If those hold, this can become a rigorous prerequisite graph. If they do not, it will collapse into a sophisticated-looking but unreliable topic map.
