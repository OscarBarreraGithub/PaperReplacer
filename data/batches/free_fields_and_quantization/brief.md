# Batch Brief: Free Fields and Quantization

## Goal

Build the first-pass Stage 3 trunk batch for free fields and quantization as a topic-centered, source-light slice that supports recognition and ordinary use before any derive-heavy expansion.

This batch should give future agents a compact canonical neighborhood for the free relativistic field species, their mode expansions, and the quantization machinery that Schwartz-style QFT writing routinely assumes.

## Target Topic

- `free fields and quantization`

## Batch Purpose

This batch is meant to capture the smallest defensible structure needed to read and use the free-field/quantization layer that sits between classical fields and later propagator/perturbation batches.

The batch should support:

- recognizing the standard free scalar, Dirac, and vector field vocabulary,
- using mode expansions and creation/annihilation operator language in ordinary calculations,
- and keeping the topic distinct from interactions, propagators, path integrals, and renormalization.

## In Scope

Likely high-value topics include:

- free scalar fields
- free Dirac fields
- free vector fields
- Lorentz-covariant field species and spin labels
- mode expansions
- creation and annihilation operators
- canonical quantization
- equal-time commutation or anticommutation relations
- microcausality
- spin-statistics as the locality/quantization constraint that ties the branch together

## Explicitly Out of Scope

- interacting fields and vertices
- propagators, correlators, LSZ, and scattering machinery
- path integrals and generating functionals
- gauge fixing as a standalone topic
- renormalization and perturbative loop technology
- broad umbrella nodes such as `QFT` or `quantization` unless a concrete decomposition need appears

## Task Model

- `literature_reading`

The batch should stay source-light and topic-centered: enough to support recognition and standard use, but not a derivation-first reconstruction of the full operator formalism.

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 10 to 14 nodes
- approximately 12 to 18 dependency edges
- a small number of overlays if a source explicitly treats operator or spacetime-symmetry machinery as background

## Review Risks

- drifting from free fields into interacting QFT or propagator/LSZ machinery
- making the quantization branch more derivation-heavy than the first-pass contract allows
- introducing duplicate background nodes instead of reusing canonical ids from the earlier foundation batches
- overfitting the batch to a single textbook presentation instead of a stable topic core

## Deliverable for This Batch

A clean Stage 3 trunk scaffold for free fields and quantization that future agents can extend into the propagator, perturbation, and path-integral neighborhoods while preserving a recognition/use-first interpretation.
