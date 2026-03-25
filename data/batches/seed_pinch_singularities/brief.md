# Batch Brief: Seed Pinch Singularities

## Goal

Create the first hand-authored seed slice for the graph using a narrow, research-facing topic that stresses the ontology without exploding scope.

This batch is a calibration fixture, not the final deep representation of `qft.pinch_singularities`.

## Proposed Target

- `pinch singularities`

## Why This Slice

This slice is a good first batch because it:

- forces a distinction between concept, method, and formal statement,
- naturally exercises mastery-relative prerequisites,
- depends on analytic and QFT-adjacent structure without requiring all of QFT as a monolith,
- and is narrow enough to review by hand.

## In Scope for Batch 1

- contour deformation
- poles vs branch points
- Feynman `i epsilon` prescription
- propagator singularities
- pinch singularities

## Explicitly Out of Scope for Batch 1

- Landau singularity conditions
- loop-momentum integration structure beyond what is needed to interpret the target slice
- boundary values and distributions
- analytic continuation in kinematic invariants
- broad umbrella nodes such as `QFT analytic structure` unless a concrete decomposition need appears

## Task Model

- `literature_reading`

For this batch, the goal is to support recognition and paper-level use in reading or following standard arguments, not full research derivation.

## Target Mastery Modes

- `recognize`
- `use`

## Initial Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 5 to 10 nodes
- approximately 6 to 15 dependency edges
- very small or zero overlay count in the first pass

## Review Risks

- overusing umbrella QFT nodes
- conflating contour-method prerequisites with broader QFT background
- treating sociological background as intrinsic dependency
- overcommitting on derivation-level claims before the ontology is proven

## Deliverable for This Batch

A small authored calibration slice with a defensible contract, auditable evidence, and queries that behave sensibly under `recognize` and `use`.
