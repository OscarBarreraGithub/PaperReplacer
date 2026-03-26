# Batch Brief: Nonperturbative QCD and Topology

## Goal

Build a first-pass Stage 6 batch for the nonperturbative QCD neighborhood centered on
lattice-QCD support, Wilson lines and loops, confinement diagnostics, instantons,
topological charge, and the theta-vacuum branch.

This batch should stay narrow and reusable, sitting between the Yang-Mills/QCD trunk and
later analytic or phenomenology-facing refinements.

## Target Topic

- `nonperturbative QCD`
- `topology in QCD`

## Batch Purpose

This batch is meant to capture the smallest reusable branch that lets Schwartz's
nonperturbative QCD vocabulary read as an organized topic cluster rather than as isolated
index terms.

The batch should support:

- recognizing Wilson-loop language as a confinement probe,
- recognizing instantons and topological charge as nonperturbative Yang-Mills structure,
- and placing theta-vacuum language in a compact QCD-topology neighborhood.

## In Scope

Likely high-value topics include:

- lattice QCD
- link field
- Wilson line
- Wilson loop
- area law for the Wilson loop
- confinement
- instanton
- topological charge
- theta-vacuum
- Witten-Veneziano relation as one topology-facing payoff leaf

## Explicitly Out of Scope

- broad hadron spectroscopy or bound-state catalogs
- axion or strong-CP-problem extensions
- chiral Lagrangians and low-energy pion EFT
- monopoles, dual superconductors, or string-model analogies beyond brief motivation
- detailed lattice algorithms or simulation methodology

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qcd_nonperturbative`

## Expected Batch Size

- approximately 11 to 12 nodes
- approximately 12 to 13 dependency edges
- a modest partonomy connecting the Wilson-loop and instanton/topology branches

## Overlap Expectations

This batch should explicitly reuse:

- `qft.non_abelian_gauge_symmetry`
- `qft.yang_mills_action`

The batch-specific nodes here should make Schwartz's nonperturbative QCD slice legible
without reopening the full Yang-Mills trunk or scattering-oriented QCD branches.

## Review Risks

- turning a local nonperturbative slice into a second generic QCD umbrella
- duplicating the existing Yang-Mills action or gauge-symmetry nodes
- drifting into axions, anomaly phenomenology, or hadron catalogs
- overfitting the batch to lattice-computation details instead of reusable concepts

## Deliverable for This Batch

A compact authored Stage 6 neighborhood that connects Wilson-line and Wilson-loop language
to confinement diagnostics while also exposing the instanton, topological-charge, and
theta-vacuum branch used in Schwartz's later QCD discussion.
