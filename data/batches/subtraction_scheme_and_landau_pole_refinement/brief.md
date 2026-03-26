# Batch Brief: Subtraction Scheme and Landau Pole Refinement

## Goal

Build a narrow refinement batch for renormalization-scheme language, subtraction points,
running couplings, and the Landau-pole branch.

This batch should stay inside the perturbative RG neighborhood and avoid turning into a
general regularization survey.

## Target Topic

- `subtraction scheme`
- `Landau pole`

## Batch Purpose

This batch is meant to capture the small but reusable renormalization slice that Schwartz
uses when scheme choice, subtraction points, and pathological running behavior come into
view.

The batch should support:

- recognizing a subtraction scheme as the rule set that fixes finite renormalized
  parameters,
- using subtraction points and minimal-subtraction language,
- and reading the Landau pole as the divergence of a running coupling obtained from RG
  evolution.

## In Scope

Likely high-value topics include:

- subtraction point
- subtraction scheme
- minimal subtraction scheme
- running coupling
- Landau pole

## Explicitly Out of Scope

- a full regularization catalog
- gauge-specific renormalization subtleties
- nonperturbative RG fixed points
- EFT matching and threshold decoupling details

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 9 nodes
- approximately 9 dependency edges
- a compact partonomy rooted in subtraction-scheme and running-coupling language

## Overlap Expectations

This batch should explicitly reuse:

- `qft.renormalized_perturbation_theory`
- `qft.renormalization_scale`
- `qft.beta_function`
- `qft.renormalization_group_equation`

The batch-specific nodes here should refine the existing RG trunk without duplicating the
full regularization batch.

## Review Risks

- conflating regulator choice with renormalization-scheme choice
- letting the batch drift into a full regularization toolkit
- introducing running-coupling language too vaguely to support the Landau-pole branch
- treating the Landau pole as a generic UV pathology node instead of a specific RG outcome

## Deliverable for This Batch

A compact authored refinement that connects subtraction-scheme language to running coupling
and the Landau-pole branch of perturbative RG reasoning.
