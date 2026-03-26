# Source Notes: Cross Sections, Decay Rates, and Phase Space

These notes are batch-local extraction guidance, not canonical graph facts.

## Main Reading Question

What is the smallest reusable neighborhood that turns amplitudes into observable scattering and decay formulas while staying close to Schwartz chapter 4-7 usage?

## Core Reuse

Reuse the existing canonical ids that already anchor the trunk:

- `qft.lsz_reduction_formula`
- `relativity.lorentz_transformation`

These are exact canonical copies, not renamed stand-ins.

## High-Value New Nodes

Likely first-pass additions:

- `qft.scattering_amplitude`
- `qft.cross_section`
- `qft.decay_rate`
- `qft.lorentz_invariant_phase_space`
- `qft.two_body_phase_space`
- `qft.mandelstam_variables`
- `qft.flux_factor`
- `qft.breit_wigner_distribution`
- `qft.narrow_width_approximation`
- `qft.partial_wave_expansion`

## Ambiguous Overlap Decisions

- `qft.scattering_amplitude` is `new_distinct`, because LSZ gives the bridge but does not itself play the same query role as the amplitude object.
- `qft.cross_section` is a single canonical observable node for the first pass; defer a total-vs-differential split unless later sources force it.
- `qft.decay_rate` is the canonical decay observable; defer a separate `decay_width` node unless needed by later Schwartz pages.
- `qft.mandelstam_variables` should stay distinct from `relativity.invariant_interval`; the former organizes external-momentum invariants for scattering, not spacetime intervals.
- `qft.breit_wigner_distribution` is preferred over a broader resonance node because the batch is intended to stay formula-driven and process-agnostic.
- `qft.partial_wave_expansion` is the reusable partial-wave branch; keep it tied to amplitudes rather than a specific named process.

## Deferred Items

Keep the following out of this batch unless evidence becomes stronger:

- named process exemplars
- optical theorem / unitarity decomposition
- broader analytic-continuation or pinch-singularity machinery
- a separate width node
- frame-specific kinematics nodes

## Overlap Workflow

When a candidate feels close to an existing batch, classify it explicitly as one of:

- `reuse_existing`
- `new_distinct`
- `part_of_existing`
- `ambiguous`

The current batch should be mostly `new_distinct` additions plus the two reused canonical ids above.
