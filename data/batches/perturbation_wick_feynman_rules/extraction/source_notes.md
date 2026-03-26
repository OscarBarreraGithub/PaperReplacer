# Source Notes: Perturbation, Wick, and Feynman-Rule Structure

These notes are batch-specific extraction context, not canonical graph facts.

## Central Constraint

Keep the batch on the operator-expansion to diagrammatics trunk.
Do not expand into free-field quantization, renormalization, or a full S-matrix chapter.

## Main Question

What is the smallest defensible prerequisite slice needed to move from interaction-picture
evolution to Dyson expansion, Wick theorem, and Feynman rules?

## Likely High-Value Additions

Possible additions include:

- interaction picture
- time-ordered exponential
- Dyson series
- time-ordered products
- normal ordering
- contractions
- Wick theorem
- Feynman rules
- symmetry factors
- propagator lines as rule ingredients

## Overlap Guidance

Strong reuse candidates:

- `qm.unitary_evolution`
- `qft.time_ordering`
- `qft.time_ordered_product`
- `qft.feynman_propagator`

The batch should reuse these shared canonical nodes instead of cloning them into perturbation-local
variants.

## Domain Anti-Patterns

Avoid:

- broad `QFT` or `S-matrix` umbrella nodes
- a second Dyson-series or Wick-theorem node with only a textual label change
- importing free-field quantization as a proxy for the perturbation trunk
- collapsing Feynman rules into a generic "perturbation theory" node

## Evidence Guidance

Useful evidence forms include:

- standard operator-evolution statements that write the interaction-picture evolution as a
  time-ordered exponential
- Wick-theorem formulas that expand time-ordered products into contractions
- diagrammatic rules that associate propagator lines, vertices, and symmetry factors with the
  Dyson/Wick expansion
- explicit references to the interaction-picture unitary evolution operator
