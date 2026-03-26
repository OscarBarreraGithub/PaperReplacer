# Batch Brief: Regularization, Renormalization, and RG

## Goal

Build a Stage 3 first-pass batch for regularization, renormalization, counterterms, and renormalization-group flow.

This batch should give the graph a reusable perturbative-QFT slice that future batches can lean on for loop divergences, subtraction schemes, running couplings, and flow equations.

## Target Topic

- `regularization, renormalization, and RG`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read and use the standard renormalization vocabulary in perturbative QFT.

The batch should support:

- recognizing ultraviolet divergences and regularization language,
- using counterterms and renormalized perturbation theory,
- and reading the beta-function, anomalous-dimension, and RG-equation machinery.

## In Scope

Likely high-value topics include:

- ultraviolet divergence
- dimensional regularization
- counterterm Lagrangian
- renormalized perturbation theory
- renormalization scale
- beta function
- anomalous dimension
- renormalization-group equation
- Wilsonian RG
- Callan-Symanzik equation

## Explicitly Out of Scope

- EFT matching and power counting as the main branch
- gauge-specific renormalization details unless direct evidence forces them in
- infrared resummation and factorization machinery
- lattice, thermal, or nonperturbative renormalization as primary topics

## Task Model

- `standard_computation`

The batch should stay source-light and topic-centered: enough to support recognition, ordinary use, and derivation-oriented reading of the core flow equations.

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 10 to 14 nodes
- approximately 10 to 16 dependency edges
- a small number of partonomy edges if they clearly help the topic decomposition

## Review Risks

- conflating the regulator with the renormalization scheme
- collapsing renormalized perturbation theory into a generic "everything runs" story
- pulling EFT matching into the batch too early
- making counterterms broader than the divergent-structure problem they solve

## Deliverable for This Batch

A clean Stage 3 population slice for regularization, counterterms, and RG that future agents can extend into perturbation, QCD, and EFT branches while preserving a recognition/use/derive-first interpretation.
