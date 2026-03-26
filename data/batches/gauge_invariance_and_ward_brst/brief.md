# Batch Brief: Gauge Invariance and Ward/BRST Structure

## Goal

Build a first-pass reusable Stage 3 batch for gauge invariance, Ward/Ward-Takahashi identities,
Faddeev-Popov gauge fixing, BRST structure, and the gauge-fixing families Schwartz uses in the
QED and gauge-theory chapters.

This batch should stay source-light, recognition/use-first, and reusable across later Yang-Mills,
anomaly, and effective-field-theory work.

## Target Topic

- `gauge invariance, Ward identities, and BRST structure`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read and use the
gauge-redundancy vocabulary in QFT literature.

The batch should support:

- recognizing gauge invariance as the reason gauge fixing is needed,
- using Ward-Takahashi identities as the functional constraint family tied to symmetry,
- and reading the BRST/Faddeev-Popov apparatus that appears once the gauge-fixed theory is
  written down.

## In Scope

Likely high-value topics include:

- local gauge invariance
- Ward identities and Ward-Takahashi identities
- gauge fixing and gauge-orbit language
- Faddeev-Popov determinants and ghosts
- BRST symmetry and BRST cohomology
- Slavnov-Taylor identities
- common gauge-fixing families such as Lorenz, Coulomb, and `R_xi`

## Explicitly Out of Scope

- full anomaly cancellation or anomaly-matching programs
- detailed renormalization-group machinery
- lattice gauge fixing or nonperturbative gauge-copy issues
- broad `gauge theory` umbrella nodes that erase the gauge-fixing and BRST split
- full proof-level BRST derivations beyond the first-pass reusable slice

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

- approximately 13 to 16 nodes
- approximately 13 to 18 dependency edges
- a small partonomy that keeps the gauge, Ward, and BRST branches legible

## Overlap Expectations

This batch should explicitly reuse:

- `qft.yang_mills_action`
- `qft.non_abelian_gauge_symmetry`
- `qft.gauge_fixing`
- `qft.ghost_field`
- `qft.path_integral_and_generating_functionals`
- `qft.ward_takahashi_identity`

The batch-specific nodes here should also become the reusable bridge to the later anomaly and
gauge-theory refinement batches.

## Review Risks

- collapsing Ward identities into a generic symmetry slogan
- splitting Ward identity and Ward-Takahashi identity into duplicate nodes
- treating Faddeev-Popov ghosts as a separate ontology from the existing ghost field node
- hiding BRST behind a generic gauge-theory umbrella
- over-proliferating gauge-fixing families before the reusable branch is stable

## Deliverable for This Batch

A compact authored Stage 3 neighborhood that connects gauge invariance to Ward identities,
gauge fixing, Faddeev-Popov ghosts, and BRST structure while preserving reuse across the
Schwartz chapter family.
