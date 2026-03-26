# Batch Brief: Lorentz and Poincare Representations

## Goal

Build the first real Stage 2 neighborhood for the topic-centered representation story around Lorentz and Poincare symmetry.

This batch should be source-light, recognition/use-first, and useful for later QFT field-content work. It is not a derivation-first reconstruction of the Lorentz or Poincare groups.

## Proposed Target

- `qft.lorentz_poincare_representations`

## Why This Slice

This slice is a good Stage 2 batch because it:

- connects standard kinematics to the representation vocabulary used in particle classification,
- keeps the particle-physics reading of the topic front and center,
- reuses existing relativistic-kinematics ids where they sharpen the graph,
- and stays small enough to be reviewed by hand while still being materially useful.

## In Scope

Likely high-value topics include:

- Lorentz group representation language
- Poincare group representations on state spaces
- one-particle states as representation carriers
- mass shell language for particle labels
- little-group vocabulary
- spin or helicity labels as representation data
- Wigner classification at the recognize/use level
- rapidity when it is used as a practical boost parameter

## Explicitly Out of Scope

- full induced-representation derivations
- proof-heavy Poincare algebra or Casimir machinery
- broad representation-theory umbrellas that erase the particle-physics reading
- field equations, interactions, or dynamics-specific machinery
- a second generic "group theory" node that does not stay topic-centered

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 7 to 10 nodes
- approximately 8 to 14 dependency edges
- a small but real partonomy only where it helps the topic structure

## Overlap Expectations

This batch should explicitly reuse the relativistic-kinematics neighborhood where appropriate, especially:

- `relativity.lorentz_transformation`
- `relativity.invariant_interval`
- `relativity.rapidity`

## Review Risks

- splitting Lorentz and Poincare representations into unrelated topics
- collapsing the classification story into a broad group-theory umbrella
- drifting into induced-representation proofs too early
- losing the connection to mass-shell and little-group labels that later field-content batches will need

## Deliverable for This Batch

A compact authored Stage 2 representation-theory neighborhood that connects spacetime symmetry to one-particle state labels and provides a stable base for later QFT field-content batches.
