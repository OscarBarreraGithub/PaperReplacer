# Batch Brief: Spectral and Mass-Shell Refinement

## Goal

Build a narrow refinement batch for on-shell/off-shell language, spectral representation,
advanced propagators, and the first Lippmann-Schwinger bridge.

This batch should stay attached to the existing correlator/propagator/LSZ trunk and avoid
turning into a full scattering-formalism or resonance catalog.

## Target Topic

- `spectral representation`
- `mass-shell language`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
Schwartz spectral and mass-shell vocabulary queryable.

The batch should support:

- recognizing on-shell and off-shell language in propagator and LSZ discussions,
- reading the Kallen-Lehmann representation and advanced-propagator terminology,
- and following the first Lippmann-Schwinger references without reopening the entire
  S-matrix branch.

## In Scope

Likely high-value topics include:

- on shell
- off shell
- Kallen-Lehmann representation
- advanced propagator
- Lippmann-Schwinger equation

## Explicitly Out of Scope

- full optical-theorem or cutting-rule expansions
- unstable-particle / resonance line-shape catalogs
- full T-matrix formalism
- broad nonrelativistic scattering theory outside the QFT bridge points

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_backbone`

## Expected Batch Size

- approximately 10 to 12 nodes
- approximately 8 to 10 dependency edges
- a compact partonomy rooted in the spectral and shell-language refinements

## Overlap Expectations

This batch should explicitly reuse:

- `qft.correlators_propagators_lsz`
- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.feynman_propagator`
- `qft.asymptotic_one_particle_state`
- `qft.lsz_reduction_formula`

The batch-specific nodes here should refine the correlator/propagator trunk without
duplicating the optical-theorem or cross-section branches.

## Review Risks

- splitting the correlator trunk into near-duplicate propagator batches
- drifting into full scattering-formalism machinery before the graph needs it
- conflating on-shell/off-shell vocabulary with resonance or decay phenomenology
- using textbook sequencing instead of the reusable dependency structure

## Deliverable for This Batch

A compact authored refinement that connects propagator and LSZ vocabulary to on-shell /
off-shell language, spectral representation, advanced propagators, and the
Lippmann-Schwinger bridge.
