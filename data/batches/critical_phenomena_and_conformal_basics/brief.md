# Batch Brief: Critical Phenomena and Conformal Basics

## Goal

Build a first-pass Stage 6 batch for the reusable bridge from Wilsonian critical phenomena
to the reading-level scale, conformal, and Weyl-invariance vocabulary that Schwartz
touches without needing a full statistical-mechanics or CFT ontology.

This batch should stay narrow and connected to the existing RG trunk.

## Target Topic

- `critical phenomena`
- `conformal basics`

## Batch Purpose

This batch is meant to capture the smallest reusable cluster that makes phase-transition,
fixed-point, universality, and scale/conformal language queryable as one neighborhood.

The batch should support:

- recognizing continuous phase transitions through order parameters and correlation length,
- using RG fixed points and anomalous dimensions to orient critical exponents and
  universality,
- and reading scale, conformal, and Weyl invariance as the symmetry-facing end of the
  critical-point branch.

## In Scope

Likely high-value topics include:

- phase transition
- continuous phase transition
- order parameter
- correlation length
- RG fixed point
- universality class
- critical exponent
- scale invariance
- conformal invariance
- Weyl invariance

## Explicitly Out of Scope

- model-specific condensed-matter catalogs such as the Ising model
- full conformal-field-theory machinery
- operator-state correspondence, bootstrap, or Virasoro-style extensions
- detailed thermal-field-theory or cosmology applications
- broad symmetry-breaking cleanup outside the local critical-point branch

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_rg`

## Expected Batch Size

- approximately 12 to 13 nodes
- approximately 11 to 12 dependency edges
- a medium partonomy anchored by the continuous-transition and fixed-point branches

## Overlap Expectations

This batch should explicitly reuse:

- `qft.wilsonian_renormalization_group`
- `qft.anomalous_dimension`

The batch-specific nodes here should make critical-point and conformal-basics language
legible without turning the graph into a chapter-by-chapter statistical-mechanics mirror.

## Review Risks

- drifting into model-specific condensed-matter ontology
- overstating logical equivalence between scale and conformal invariance
- duplicating the existing RG trunk instead of refining it
- expanding into a full CFT branch before the basics are stabilized

## Deliverable for This Batch

A compact authored Stage 6 neighborhood that connects continuous phase transitions and
universality to RG fixed points, anomalous dimensions, and the first scale/conformal/Weyl
symmetry vocabulary.
