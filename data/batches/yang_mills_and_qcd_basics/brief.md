# Batch Brief: Yang-Mills and QCD Basics

## Goal

Create the first-pass stage 3 neighborhood for non-Abelian gauge theory and the QCD basics that Schwartz develops in Chapters 25 and 26.

This batch should stay source-light, recognition/use-first, and reusable across later QCD, Standard Model, and factorization work.

## Proposed Target

- `qft.yang_mills_and_qcd_basics`

## Why This Slice

This slice is a good batch because it:

- reuses the classical-field action vocabulary instead of rebuilding it,
- isolates the non-Abelian gauge structure that distinguishes Yang-Mills theory from Abelian gauge theory,
- keeps color, quarks, gluons, and gauge fixing visible without collapsing into a generic gauge-theory umbrella,
- and gives later QCD/factorization batches a stable background frontier.

## In Scope

Likely high-value topics include:

- non-Abelian gauge symmetry
- gauge fields and covariant derivatives
- field-strength tensors
- Yang-Mills action language
- color SU(3)
- quarks and gluons as QCD color carriers
- gauge fixing and ghost fields
- asymptotic freedom

## Explicitly Out of Scope

- parton distributions and factorization theorems
- DGLAP evolution or PDFs as standalone topics
- SCET, jets, or threshold resummation
- electroweak symmetry breaking or the Standard Model gauge sector beyond the QCD slice
- broad `QFT` or `gauge theory` umbrella nodes that erase the non-Abelian/QCD distinction

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qcd_theory`

## Expected Batch Size

- approximately 10 to 15 nodes
- approximately 10 to 14 dependency edges
- a small partonomy that keeps the gauge and color branches legible

## Overlap Expectations

This batch should explicitly reuse:

- `classical_fields.action_functional`
- `classical_fields.continuous_symmetry_of_action`
- `classical_fields.field_configuration`

The QCD-specific nodes here should also become the shared background for the later factorization batch.

## Review Risks

- collapsing Yang-Mills into a generic gauge-theory summary node
- overcommitting to running-coupling details before the renormalization branch is ready
- hiding gauge-fixing and ghost structure behind a clean-looking but misleading action story
- drifting into parton/factorization machinery too early

## Deliverable for This Batch

A compact authored stage 3 neighborhood that connects classical-field language to non-Abelian gauge theory, QCD color, and the first QCD-specific asymptotic-freedom frontier.
