# Batch Brief: Distributions and Boundary Values

## Goal

Build a small authored bridge batch for reading plus-or-minus `i0` notation as
distributional boundary-value language, centered on upper/lower boundary values, principal
value, and Dirac-delta pieces.

This batch should stay minimal and should not become a general distributions course or a
second pinch-singularities branch.

## Target Topic

- `distributional boundary values`
- `principal value / delta decomposition`

## Batch Purpose

This batch is meant to resolve the old decomposition blocker by landing only the smallest
local cluster that makes Schwartz-style `x +/- i0` notation queryable.

The batch should support:

- recognizing plus-or-minus `i0` language as upper/lower boundary-value notation,
- reading principal-value and delta-function pieces as the local decomposition of singular
  denominators,
- and connecting that vocabulary back to the existing `qft.distributional_boundary_values`
  hub without reopening the whole analytic-structure branch.

## In Scope

Likely high-value topics include:

- `qft.distributional_boundary_values` as the existing hub
- plus-or-minus `i0` limits
- Cauchy principal value
- Dirac delta distribution
- local `i epsilon` reading support only where it helps interpret the notation

## Explicitly Out of Scope

- a broad `distributions` umbrella node
- a broad discontinuity or absorptive-part branch
- a second generic `i epsilon` node
- Hilbert transforms or full distribution-theory derivations
- further pinch-singularity or Landau-analysis expansion

## Task Model

- `literature_reading`

For this batch, the goal is recognition and routine use in paper-facing reading, not a
derive-heavy proof program.

## Target Mastery Modes

- `recognize`
- `use`

## Initial Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 7 nodes
- approximately 9 dependency edges
- a very small partonomy around the existing boundary-value hub

## Review Risks

- duplicating `qft.feynman_i_epsilon_prescription`
- minting a broad discontinuity node too early
- letting the batch drift into a general analysis umbrella
- overfitting the batch to the pinch-singularities anchor instead of keeping it local

## Deliverable for This Batch

A narrow authored bridge that translates `x +/- i0` notation into a compact
distributional-boundary-value neighborhood with principal-value and delta-distribution
components.
