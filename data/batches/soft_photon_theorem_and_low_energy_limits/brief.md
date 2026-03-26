# Batch Brief: Soft Photon Theorem and Low-Energy Limits

## Goal

Build a narrow refinement batch for the soft-photon theorem branch, centered on the soft
limit of amplitudes, universal factorization of soft emission, and the first low-energy
photon-emission vocabulary.

This batch should stay theorem-centered and reusable, not collapse into a process catalog or
duplicate the broader infrared-cancellation batch.

## Target Topic

- `soft photon theorem`
- `low-energy photon limits`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes Schwartz-style
soft-photon and low-energy-emission language queryable.

The batch should support:

- recognizing the soft limit as the low-energy limit of an emitted photon inside a
  scattering amplitude,
- using universal soft-emission factorization and the eikonal soft factor,
- and reading the soft-photon theorem as the theorem-level payoff of the same branch.

## In Scope

Likely high-value topics include:

- soft limit
- soft-radiation factorization
- eikonal soft factor
- soft photon theorem

## Explicitly Out of Scope

- broad infrared-cancellation theorems already handled by Bloch-Nordsieck and KLN
- process-specific low-energy photon examples
- full soft-collinear EFT or resummation machinery
- non-Abelian soft theorems or graviton soft theorems

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 7 nodes
- approximately 8 dependency edges
- a small partonomy rooted in the theorem and its factorization branch

## Overlap Expectations

This batch should explicitly reuse:

- `qft.scattering_amplitude`
- `qft.soft_divergence`

The batch-specific nodes here should sharpen the QED soft-emission theorem without
reopening the wider infrared or process-facing branches.

## Review Risks

- duplicating the broader infrared-divergence and cancellation-theorem branch
- turning the theorem into a process catalog
- overgeneralizing into non-Abelian or gravitational soft theorems
- flattening factorization and theorem language into a single vague node

## Deliverable for This Batch

A compact authored refinement that connects the soft limit of amplitudes to universal
soft-radiation factorization and the soft-photon theorem.
