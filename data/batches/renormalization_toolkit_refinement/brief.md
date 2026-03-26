# Batch Brief: Renormalization Toolkit Refinement

## Goal

Build a narrow refinement batch for regulator and subtraction-toolkit language around
Pauli-Villars, BPHZ, superficial degree of divergence, super/nonrenormalizable theories,
effective charge, and dimensional transmutation.

This batch should stay attached to the existing regularization/RG trunk and avoid turning
into a broad EFT or nonperturbative renormalization umbrella.

## Target Topic

- `renormalization toolkit`
- `regulator and subtraction methods`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
Schwartz renormalization-toolkit vocabulary queryable.

The batch should support:

- recognizing alternative regulator and subtraction language beyond the first-pass dim-reg
  trunk,
- using superficial degree of divergence to orient renormalizability classifications,
- and reading effective charge and dimensional transmutation as downstream RG consequences.

## In Scope

Likely high-value topics include:

- Pauli-Villars regularization
- BPHZ renormalization
- superficial degree of divergence
- super-renormalizable theory
- nonrenormalizable theory
- effective charge
- dimensional transmutation

## Explicitly Out of Scope

- EFT matching and operator-basis construction as the main branch
- infrared resummation, factorization, or SCET mode structure
- lattice or nonperturbative renormalization programs
- a full operator-product-expansion batch

## Task Model

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 13 to 15 nodes
- approximately 10 to 14 dependency edges
- a compact partonomy rooted in toolkit methods, divergence classification, and RG payoffs

## Overlap Expectations

This batch should explicitly reuse:

- `qft.regularization_renormalization_rg`
- `qft.ultraviolet_divergence`
- `qft.dimensional_regularization`
- `qft.renormalized_perturbation_theory`
- `qft.renormalization_scale`
- `qft.beta_function`

The batch-specific nodes here should refine the existing RG trunk without collapsing into
the subtraction-scheme batch or the EFT trunk.

## Review Risks

- conflating regularization method, subtraction prescription, and EFT logic
- duplicating the already-landed subtraction-scheme / Landau-pole refinement
- turning divergence classification into a generic power-counting umbrella
- treating effective charge or dimensional transmutation as disconnected name-only nodes

## Deliverable for This Batch

A compact authored refinement that connects the existing renormalization trunk to regulator
alternatives, divergence-classification language, and a few high-yield RG payoffs.
