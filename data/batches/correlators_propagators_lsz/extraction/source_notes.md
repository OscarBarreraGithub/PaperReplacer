# Source Notes: Correlators, Propagators, and LSZ Reduction

These notes are batch-specific extraction context, not canonical graph facts.

## Central Constraint

Build the smallest defensible trunk that connects time-ordered correlators to propagators and LSZ.
Do not expand into a general free-field or perturbation-theory chapter.

## Main Question

What structure is genuinely needed to read standard QFT formulas that move from time-ordered Green
functions to scattering amplitudes?

## Likely High-Value Additions

Possible additions include:

- time ordering
- time-ordered products
- time-ordered Green functions
- Feynman propagator
- propagator singularities as they appear in the propagator node
- amputation
- asymptotic one-particle states
- LSZ reduction formula

## Overlap Guidance

Strong reuse candidates:

- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.time_ordering`
- `qft.time_ordered_product`
- `qft.feynman_propagator`

The batch should treat these as shared canonical nodes, not as batch-local redefinitions.

## Domain Anti-Patterns

Avoid:

- broad `QFT` or `S-matrix` umbrella nodes
- free-field quantization as a surrogate for the correlator/LSZ slice
- creating separate "Green function" and "propagator" nodes with no query-visible distinction
- importing perturbative Feynman-rule machinery before the correlator/LSZ trunk is stable

## Evidence Guidance

Useful evidence forms include:

- standard textbook or paper definitions of time ordering and Green functions
- statements that the Feynman propagator is the two-point time-ordered Green function
- explicit LSZ formulas relating amputated Green functions to scattering amplitudes
- causal pole-placement language tied to the Feynman `i epsilon` convention
