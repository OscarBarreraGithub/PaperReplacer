# Batch Brief: Pinch Singularities Deep

## Goal

Build a deeper, production-oriented graph neighborhood around the existing canonical node:

- `qft.pinch_singularities`

This batch should not create a second "deep" topic node for pinch singularities. It should enrich the surrounding graph while keeping the same canonical target node.

## Relationship to the Seed Batch

- `seed_pinch_singularities` remains the calibration fixture and regression slice.
- `pinch_singularities_deep` is the serious topic-development batch.

The deep batch should reuse existing nodes when appropriate and only add new nodes where there is a meaningful semantic distinction.

## Target Topic

- `qft.pinch_singularities`

## Batch Purpose

This batch is meant to push beyond the literature-facing minimum and capture a more realistic analytic neighborhood for the topic.

The goal is to support:

- literature reading,
- standard contour or singularity reasoning,
- and a first pass at derivation-oriented structure where it is genuinely needed.

## In Scope

Likely high-value topics include:

- contour deformation
- poles vs branch points
- Feynman `i epsilon` prescription
- propagator singularities
- loop-energy or loop-momentum integration structure
- boundary values and distributions
- analytic continuation in invariants
- pinch singularities
- Landau singularity conditions

## Explicitly Out of Scope

- the full analytic structure of all amplitudes
- broad umbrella nodes unless decomposition genuinely requires them
- unrelated QFT topics such as renormalization or LSZ unless direct evidence forces them into the slice

## Task Models

- `literature_reading`
- `standard_computation`

Potential later extension:

- `derivation_reproduction`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Overlap Expectations

This batch should strongly overlap the seed slice and should explicitly reuse:

- `complex_analysis.contour_deformation`
- `complex_analysis.poles_vs_branch_points`
- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.pinch_singularities`

New nodes should be added only when they represent genuinely new structure around the same target.

## Review Risks

- accidentally creating a second pinch-singularities node under a new name
- importing broad QFT umbrella nodes instead of sharp local structure
- overcommitting to derivation-level edges without strong evidence
- blurring overlap with `Landau singularity conditions` instead of modeling it explicitly

## Deliverable

A deeper batch proposal and eventual authored graph expansion around the same canonical `qft.pinch_singularities` node, suitable for replacing the seed slice as the main topic-facing representation while preserving the seed as calibration.
