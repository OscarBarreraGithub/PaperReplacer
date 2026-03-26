# Batch Brief: Scalar QED

## Goal

Build a first-pass Stage 6 batch for scalar QED, centered on Abelian gauge symmetry for a
charged scalar, minimal coupling, the scalar-QED Lagrangian, the seagull vertex, and the
smallest process-facing leaf that makes the branch structurally useful.

This batch should stay narrow and reusable, sitting between the free-field trunk, the
gauge-invariance branch, and the existing QED process neighborhood.

## Target Topic

- `scalar QED`

## Batch Purpose

This batch is meant to capture the reusable charged-scalar gauge-theory neighborhood that
Schwartz uses as the simplest nontrivial gauge-invariant matter theory before the full
non-Abelian or Standard Model machinery appears.

The batch should support:

- recognizing scalar QED as the Abelian charged-scalar analogue of ordinary QED structure,
- using minimal coupling and the covariant-derivative form of the Lagrangian,
- and reading the seagull vertex as the distinctive structural payoff of the theory.

## In Scope

Likely high-value topics include:

- scalar QED
- Abelian gauge symmetry
- charged scalar field
- minimal coupling
- scalar-QED Lagrangian
- one-photon scalar vertex
- seagull vertex
- scalar Compton scattering as a single grounding process leaf

## Explicitly Out of Scope

- full scalar-QED renormalization and beta-function machinery
- Higgs-sector model building and spontaneous symmetry breaking
- non-Abelian generalizations
- broad process catalogs beyond a single grounding example
- lattice or condensed-matter analogues

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qed_foundations`

## Expected Batch Size

- approximately 12 to 14 nodes
- approximately 14 to 16 dependency edges
- a small partonomy with one process-facing leaf

## Overlap Expectations

This batch should explicitly reuse:

- `qft.free_scalar_field`
- `qft.free_vector_field`
- `qft.gauge_invariance`
- `qft.covariant_derivative`
- `qft.ward_takahashi_identity`
- `qft.feynman_rules`

The batch-specific nodes here should make scalar QED legible without duplicating the existing
fermionic QED example branch.

## Review Risks

- treating scalar QED as a second generic QED umbrella
- duplicating the existing gauge-invariance or covariant-derivative nodes
- letting a single process leaf turn into another process catalog
- collapsing scalar QED into the Higgs sector or generic scalar-field theory

## Deliverable for This Batch

A compact authored Stage 6 neighborhood that connects charged scalar matter to Abelian gauge
symmetry, minimal coupling, the scalar-QED interaction vertices, and one grounding scattering
example.
