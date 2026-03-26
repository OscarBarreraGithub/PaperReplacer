# Batch Brief: Perturbation, Wick, and Feynman-Rule Structure

## Goal

Build a reusable Stage 3 trunk for the perturbative operator-expansion machinery that turns
interaction-picture evolution into Dyson expansions, Wick contractions, and diagrammatic rules.

## Target Topic

- `perturbation, Wick, and Feynman-rule structure`

## What This Batch Is For

This batch should stabilize the core reusable slice needed to:

- recognize the interaction-picture setup in perturbation theory,
- use the time-ordered exponential and Dyson expansion,
- apply Wick theorem and contractions to time-ordered products,
- and read off Feynman rules with the right combinatorial factors.

## In Scope

- interaction picture
- time-ordered exponential
- Dyson series
- time-ordered products
- normal ordering
- contractions
- Wick theorem
- Feynman rules
- symmetry factors
- propagator lines as diagrammatic ingredients

## Explicitly Out of Scope

- free-field quantization as a standalone topic
- renormalization or loop regularization
- gauge theory
- path-integral generating-function machinery
- chapter-by-chapter textbook mirroring

## Task Models

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_backbone`

## Expected Batch Size

- approximately 8 to 12 nodes
- approximately 8 to 14 dependency edges
- one small overlay layer

## Overlap Expectations

This batch should reuse the shared frontiers that already stabilize the correlator/LSZ slice:

- `qft.time_ordering`
- `qft.time_ordered_product`
- `qft.feynman_propagator`

It should also reuse `qm.unitary_evolution` as the background for the interaction-picture setup.
The batch should not mint duplicate Dyson or Wick nodes under new labels.

## Review Risks

- drifting into free-field quantization before the perturbation trunk is stable
- turning Wick theorem into multiple near-synonymous nodes
- losing the link from contractions to propagator lines
- letting the batch become a lecture-note chapter mirror

## Deliverable

A first-pass perturbative backbone that later diagrammatic, scattering, and path-integral batches can
reuse without rebuilding the Dyson/Wick/Feynman-rule frontier.
