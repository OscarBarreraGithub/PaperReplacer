# Batch Brief: Path Integral and Generating Functionals

## Goal

Build a Stage 3 first-pass batch for the path-integral / generating-functional neighborhood.

This batch should give the graph a reusable source-coupled functional-integral slice that future batches can lean on for correlators, Schwinger-Dyson identities, and Ward-Takahashi identities.

## Target Topic

- `path integral and generating functionals`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read and use the path-integral formalism in QFT literature.

The batch should support:

- recognizing the functional-integral setup,
- using source-dependent generating functionals to organize correlators,
- and reading the standard functional identities that follow from shifts or symmetries of the integral.

## In Scope

Likely high-value topics include:

- classical action functional reuse
- functional measure
- source-coupled path integral
- generating functional
- connected generating functional
- Gaussian functional integral
- fermionic path integrals
- Schwinger-Dyson equations
- Ward-Takahashi identities
- `i epsilon` background where Minkowski-signature path integrals need it

## Explicitly Out of Scope

- full renormalization or RG machinery
- gauge-fixing structure as a separate branch unless direct evidence forces it
- effective-action and 1PI formalism as a primary branch
- broad perturbation-theory or scattering umbrellas unless a sharper decomposition is not available

## Task Model

- `literature_reading`

The batch should stay source-light and topic-centered: enough to support recognition, ordinary use, and a small amount of derivation-oriented reading.

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 10 to 14 nodes
- approximately 10 to 16 dependency edges
- a small number of partonomy edges if they clearly help the topic decomposition

## Review Risks

- collapsing generating functionals into effective action language too early
- treating the source-coupled formalism as if it were just notation for ordinary perturbation theory
- dragging renormalization or gauge structure into the slice before it is needed
- forgetting that the `i epsilon` background is a reuse choice, not a new ontology decision

## Deliverable for This Batch

A clean Stage 3 population slice for path integrals and generating functionals that future agents can extend into correlator, identity, and functional-method batches while preserving a recognition/use/derive-first interpretation.
