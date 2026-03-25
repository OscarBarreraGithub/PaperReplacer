# Source Notes: Pinch Singularities Deep

These notes are batch-specific extraction context, not canonical graph facts.

## Central Constraint

Do not create a second node for pinch singularities.

The target of this batch is the existing canonical node:

- `qft.pinch_singularities`

This batch should deepen the graph around that node, not split the topic into "surface" and "deep" variants.

## Main Question

What additional local structure is genuinely needed to move from the seed calibration slice toward a more realistic research-facing graph neighborhood?

## Likely High-Value Additions

Possible additions include:

- loop-energy or loop-momentum integration structure
- boundary values and distributions
- analytic continuation in invariants
- Landau singularity conditions

These should be added only if they sharpen the graph around the same target rather than broadening it aimlessly.

## Overlap Guidance

The batch is expected to overlap heavily with the existing seed slice.

Strong reuse candidates:

- `complex_analysis.contour_deformation`
- `complex_analysis.poles_vs_branch_points`
- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.pinch_singularities`

When a candidate looks similar to something already in the graph, use the overlap workflow:

- `reuse_existing`
- `alias_existing`
- `new_distinct`
- `part_of_existing`
- `ambiguous`

## Domain Anti-Patterns

Avoid:

- broad "all of QFT" prerequisites
- a second pinch-singularities node with a new id
- importing unrelated amplitude or renormalization machinery without direct evidence
- forcing `Landau singularity conditions` into the same node as `pinch singularities`

## Evidence Guidance

Useful evidence forms include:

- explicit contour-trapping arguments
- statements about pole placement and obstruction to deformation
- uses of Landau conditions as a distinct but overlapping analytic tool
- distributional or boundary-value machinery when it is directly required for interpretation or derivation
