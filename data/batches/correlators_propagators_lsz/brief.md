# Batch Brief: Correlators, Propagators, and LSZ Reduction

## Goal

Build a reusable core QFT trunk for time-ordered correlators, propagators, and LSZ reduction.
The target is a clean prerequisite neighborhood that later scattering, path-integral, and
perturbation batches can reuse.

## Target Topic

- `correlators, propagators, and LSZ reduction`

## What This Batch Is For

This batch should stabilize the smallest defensible slice needed to:

- recognize the standard correlator and propagator language used in QFT papers,
- use the causal propagator and time-ordering vocabulary in standard arguments,
- and connect time-ordered Green functions to scattering amplitudes through LSZ reduction.

## In Scope

- time ordering
- time-ordered products
- time-ordered Green functions
- Feynman propagator
- propagator singularities as they affect the propagator node
- amputation
- asymptotic one-particle states
- LSZ reduction formula

## Explicitly Out of Scope

- free-field quantization as a standalone batch
- perturbative diagram rules
- renormalization
- path-integral generating-function machinery
- broad umbrella nodes such as `QFT` or `S-matrix`

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

- approximately 7 to 10 nodes
- approximately 8 to 12 dependency edges
- one small overlay layer

## Overlap Expectations

This batch should explicitly reuse the existing analytic-structure frontier where it matters:

- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.time_ordering`
- `qft.time_ordered_product`
- `qft.feynman_propagator`

The batch should not create separate LSZ or propagator variants just because different books phrase
them differently.

## Review Risks

- drifting into free-field quantization too early
- duplicating propagator or LSZ nodes under near-synonymous names
- letting the batch turn into a textbook chapter mirror
- losing the distinction between correlators, amputated objects, and scattering amplitudes

## Deliverable

A first-pass reusable trunk that later Stage 3 and Stage 4 QFT batches can connect to without
recreating the correlator/propagator/LSZ frontier.
