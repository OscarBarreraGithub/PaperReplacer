# Batch Brief: Optical Theorem and Unitarity Cutting Basics

## Goal

Build a narrow refinement batch for the optical-theorem branch that connects S-matrix
unitarity, forward scattering, and the first cutting-rule language without reopening the
entire analytic-structure or loop-amplitudes program.

This batch should stay reusable and paper-facing, not become a generalized-cuts or
multi-loop amplitudes catalog.

## Target Topic

- `optical theorem`
- `unitarity cutting basics`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes Schwartz-style
optical-theorem and unitarity-cutting language queryable.

The batch should support:

- recognizing the optical theorem as a direct consequence of S-matrix unitarity,
- reading forward-scattering language as the theorem's local kinematic specialization,
- and placing simple cutting rules as the next structural extension of the same unitarity
  branch.

## In Scope

Likely high-value topics include:

- S-matrix unitarity
- forward scattering amplitude
- optical theorem
- on-shell intermediate state
- unitarity cutting rules

## Explicitly Out of Scope

- generalized cuts and modern loop-amplitudes technology
- broad branch-cut or discontinuity ontology
- full spectral representations
- detailed detector or phenomenology applications
- Cutkosky-rule variants beyond a single reusable cutting-rule node

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 8 nodes
- approximately 8 to 9 dependency edges
- a small partonomy rooted in the unitarity and optical-theorem branch

## Overlap Expectations

This batch should explicitly reuse:

- `qft.scattering_amplitude`
- `qft.asymptotic_one_particle_state`

The batch-specific nodes here should refine the observable-scattering branch without
pulling in the full analytic-continuation or pinch-singularities neighborhoods.

## Review Risks

- duplicating branch-cut or discontinuity nodes that belong to later analytic work
- turning the batch into a generalized-cuts amplitudes branch
- drifting into process-specific cross-section examples
- separating optical theorem from unitarity so far that the theorem loses its structural
  meaning

## Deliverable for This Batch

A compact authored refinement that connects S-matrix unitarity to the optical theorem,
forward scattering, and a first reusable cutting-rule node.
