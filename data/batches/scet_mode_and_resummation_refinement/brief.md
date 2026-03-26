# Batch Brief: SCET Mode and Resummation Refinement

## Goal

Build a narrow refinement batch for the remaining SCET-facing Schwartz residue around
Wilson-coefficient language, ultraviolet sensitivity, Glauber mode, collinear interaction,
and heavy-jet-mass event-shape usage.

This batch should sharpen the existing SCET trunk without reopening generic factorization,
jet basics, or a broad event-shape catalog.

## Target Topic

- `soft-collinear effective theory`
- `SCET mode structure and resummation payoffs`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
SCET and large-log vocabulary in Schwartz queryable.

The batch should support:

- reading Wilson coefficients as the short-distance EFT payload produced by matching,
- recognizing ultraviolet sensitivity as the EFT-side reason short-distance coefficients
  matter,
- identifying Glauber mode and collinear-interaction language as missing mode-structure
  refinements,
- and connecting heavy jet mass to the existing jet, soft-function, and resummation trunk.

## In Scope

Likely high-value topics include:

- Wilson coefficient
- ultraviolet sensitivity
- Glauber mode
- collinear interaction
- heavy jet mass

## Explicitly Out of Scope

- a generic `form factor` ontology branch
- threshold-region or threshold-resummation expansion as a separate hadronic batch
- a full event-shape catalog beyond the existing thrust node plus the single heavy-jet-mass
  payoff leaf
- rebuilding Sudakov language as a duplicate subtree when the existing
  `eft.large_logarithm_resummation` node already covers the central resummation branch

## Task Model

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `effective_field_theory`

## Expected Batch Size

- approximately 15 to 17 nodes
- approximately 12 to 14 dependency edges
- a compact partonomy rooted in the existing SCET topic plus one event-shape payoff leaf

## Overlap Expectations

This batch should explicitly reuse:

- `eft.soft_collinear_effective_theory`
- `eft.matching`
- `eft.large_logarithm_resummation`
- `eft.mode_scaling`
- `eft.collinear_mode`
- `eft.soft_mode`
- `eft.hard_function`
- `eft.jet_function`
- `eft.soft_function`
- `qft.eikonal_soft_factor`
- `qft.jet`
- `qft.thrust`

The batch-specific nodes here should refine the existing EFT/SCET and infrared trunks
without collapsing into hadronic factorization, threshold resummation, or a generic
observable catalog.

## Review Risks

- treating `Wilson coefficient` as a duplicate of `hard function` or `hard scattering
  coefficient`
- letting the batch drift into a broad event-shape namespace
- overpromoting Sudakov or threshold language that is already adequately covered by the
  current resummation trunk
- turning `Glauber mode` into a generic nonperturbative QCD umbrella instead of a narrow
  SCET mode refinement

## Deliverable for This Batch

A compact authored refinement that attaches the remaining SCET mode and coefficient language
to the existing EFT, infrared, and event-shape neighborhoods without broadening the ontology
unnecessarily.
