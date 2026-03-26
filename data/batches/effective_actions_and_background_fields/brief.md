# Batch Brief: Effective Actions and Background Fields

## Goal

Build a first-pass reusable batch for the effective-action neighborhood, centered on the 1PI effective action, background-field methods, effective potentials, and the closest Schwartz-style one-loop functional machinery.

## Target Topic

- `effective actions and background fields`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read and use the effective-action language that shows up in advanced QFT notes and Schwartz chapters 33-34.

The batch should support:

- recognizing the 1PI effective-action formalism,
- using the background-field method as a computational branch,
- reading effective-potential discussions,
- and keeping the one-loop functional tools that commonly support those derivations.

## In Scope

Likely high-value topics include:

- effective action and 1PI effective action
- connected generating functional reuse from the path-integral batch
- background field and background-field method
- effective potential
- one-loop effective action
- functional determinant language
- Schwinger proper-time / Schwinger parameter machinery where the source uses it
- renormalized perturbation theory as supporting background for the effective-potential branch

## Explicitly Out of Scope

- full gauge-fixing or BRST structure unless the source passage forces it in
- a full renormalization batch or RG derivation
- EFT matching or operator-basis construction
- SM-specific Higgs effective potentials unless a source passage explicitly narrows the topic there
- broad path-integral or scattering umbrellas that do not sharpen the effective-action slice

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 12 to 16 nodes
- approximately 10 to 16 dependency edges
- a small branch structure with reused path-integral and renormalization support nodes

## Review Risks

- collapsing the slice back into generic path-integral formalism
- pulling in full renormalization or gauge-fixing machinery too early
- splitting effective action, 1PI action, and effective potential into disconnected near-duplicates
- turning Schwinger proper-time into a separate detour instead of a reusable helper branch

## Deliverable for This Batch

A clean first-pass effective-action and background-field neighborhood that future agents can extend into one-loop, effective-potential, and later Standard Model branches without losing the reusable 1PI core.
