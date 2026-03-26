# Batch Brief: EFT Matching and UV Completion Refinement

## Goal

Build a narrow EFT-tail refinement batch for `integrating out`, `ultraviolet completion`,
and `4-Fermi theory`.

This batch should sharpen the generic EFT trunk without turning into a broad naturalness,
operator-taxonomy, or weak-interaction phenomenology branch.

## Target Topic

- `generic EFT tail cleanup`
- `matching-side EFT vocabulary`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
generic EFT residue in Schwartz queryable.

The batch should support:

- reading `integrating out` as the conceptual step that produces a low-energy EFT,
- recognizing `ultraviolet completion` as the full-theory side of the EFT/UV split,
- and using `4-Fermi theory` as the canonical higher-dimensional low-energy EFT example.

## In Scope

Likely high-value topics include:

- integrating out
- ultraviolet completion
- 4-Fermi theory

## Explicitly Out of Scope

- naturalness / hierarchy arguments
- SCET mode structure or resummation
- a full relevant / marginal / irrelevant operator taxonomy
- process-specific weak-decay phenomenology

## Task Model

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `effective_field_theory`

## Expected Batch Size

- approximately 8 to 10 nodes
- approximately 8 to 10 dependency edges
- a compact partonomy rooted in the existing generic EFT branch

## Overlap Expectations

This batch should explicitly reuse:

- `eft.effective_field_theory`
- `eft.scale_separation`
- `eft.higher_dimensional_operator`
- `eft.matching`
- `eft.wilson_coefficient`
- `eft.ultraviolet_sensitivity`

The batch-specific nodes here should refine the generic EFT trunk and reuse the already
landed Wilson-coefficient language, rather than duplicating the SCET or renormalization
branches.

## Review Risks

- splitting `four_fermi_theory` vs `four_fermion_theory` into parallel namespaces
- treating `ultraviolet completion` as identical to `ultraviolet sensitivity`
- letting `integrating out` collapse into a synonym for `matching`
- allowing the canonical `4-Fermi theory` example to sprawl into a weak-process catalog

## Deliverable for This Batch

A compact authored refinement that closes the remaining generic EFT vocabulary gap around
matching-side intuition and the canonical low-energy four-Fermi example.
