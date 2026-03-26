# Batch Brief: Scattering Spectral Residual Refinement

## Goal

Build a narrow residual batch for the remaining scattering-side Schwartz items around
T-matrix language, unstable particles, the partial-wave unitarity bound, and the Feynman
tree theorem.

This batch should connect the existing optical-theorem, spectral/LSZ, and
cross-section/decay-rate branches without turning into a broad S-matrix or resonance
program.

## Target Topic

- `scattering-side residual cleanup`
- `unitarity, resonance, and operator notation bridges`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
Schwartz scattering and resonance residue queryable.

The batch should support:

- reading the T-matrix as the operator-level scattering object tied to amplitudes and
  unitarity,
- recognizing unstable-particle language as the conceptual home of the existing
  Breit-Wigner and narrow-width nodes,
- using the partial-wave unitarity bound as the theorem-level refinement of the existing
  partial-wave branch,
- and placing the Feynman tree theorem next to the already-landed cutting-rule and
  on-shell-intermediate-state language.

## In Scope

Likely high-value topics include:

- T-matrix
- unstable particles
- partial-wave unitarity bound
- Feynman tree theorem

## Explicitly Out of Scope

- a full analytic S-matrix program
- a broad resonance-pole or dispersion-relation batch
- process-specific partial-wave examples
- threshold-resummation or form-factor expansion

## Task Model

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 14 to 16 nodes
- approximately 10 to 13 dependency edges
- a compact partonomy rooted in the existing optical-theorem / unitarity topic

## Overlap Expectations

This batch should explicitly reuse:

- `qft.optical_theorem_and_unitarity_cutting_basics`
- `qft.scattering_amplitude`
- `qft.s_matrix_unitarity`
- `qft.optical_theorem`
- `qft.unitarity_cutting_rules`
- `qft.on_shell_intermediate_state`
- `qft.lippmann_schwinger_equation`
- `qft.feynman_propagator`
- `qft.partial_wave_expansion`
- `qft.decay_rate`
- `qft.breit_wigner_distribution`
- `qft.narrow_width_approximation`

The batch-specific nodes here should refine existing scattering and resonance language
without reopening a generic cross-section or spectral-analytic umbrella.

## Review Risks

- treating T-matrix notation as a duplicate of the scattering-amplitude node
- turning unstable-particle language into a broad resonance catalog
- duplicating the already-landed partial-wave expansion rather than refining it with the
  actual unitarity bound
- overgeneralizing the Feynman tree theorem into a full cutting or analytic-structure batch

## Deliverable for This Batch

A compact authored refinement that connects the remaining scattering-operator, resonance,
and theorem-level residue back into the existing unitarity and observable trunks.
