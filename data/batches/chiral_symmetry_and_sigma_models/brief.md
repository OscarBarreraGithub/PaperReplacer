# Batch Brief: Chiral Symmetry and Sigma Models

## Goal

Build a narrow reusable batch for chiral symmetry, chiral symmetry breaking, sigma-model
methods, and the first chiral-Lagrangian / custodial-symmetry vocabulary.

This batch should stay focused on the symmetry-breaking and low-energy-effective-structure
story, not turn into a hadron catalog or a broad BSM model survey.

## Target Topic

- `chiral symmetry`
- `sigma models`

## Batch Purpose

This batch is meant to capture the smallest defensible neighborhood that makes the
remaining Schwartz chiral-symmetry and sigma-model language queryable.

The batch should support:

- recognizing chiral symmetry as a specific symmetry branch rather than generic chirality,
- using chiral symmetry breaking and its Goldstone-style consequences,
- and reading linear/nonlinear sigma models, chiral Lagrangian language, and the first
  CCWZ / custodial-symmetry references without reopening the whole Standard Model.

## In Scope

Likely high-value topics include:

- chiral symmetry
- chiral symmetry breaking
- linear sigma model
- nonlinear sigma model
- chiral Lagrangian
- CCWZ method
- custodial symmetry

## Explicitly Out of Scope

- technicolor and other BSM model catalogs
- detailed pion phenomenology or hadron process catalogs
- anomaly calculations beyond the existing anomaly batch
- full EFT operator-basis or precision-fit machinery

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `standard_model`

## Expected Batch Size

- approximately 12 to 14 nodes
- approximately 10 to 12 dependency edges
- a compact partonomy rooted in chiral breaking and sigma-model methods

## Overlap Expectations

This batch should explicitly reuse:

- `sm.symmetry_breaking_and_standard_model`
- `sm.ssb.spontaneous_symmetry_breaking`
- `sm.ssb.goldstone_boson`
- `sm.ewbreak.electroweak_symmetry_breaking`
- `classical_fields.lagrangian_density`

The batch-specific nodes here should sharpen the chiral / sigma-model branch without
duplicating the first-pass Higgs core, the anomaly branch, or the EFT/SCET trunk.

## Review Risks

- collapsing the batch back into the whole Standard Model symmetry-breaking umbrella
- confusing chiral symmetry with generic spinor chirality language already handled
  elsewhere
- drifting into hadron-process catalogs or technicolor side branches
- treating CCWZ or custodial symmetry as isolated name drops rather than parts of the
  sigma-model/chiral-Lagrangian branch

## Deliverable for This Batch

A compact authored refinement that connects chiral symmetry breaking to linear and
nonlinear sigma models, chiral-Lagrangian language, and the first custodial / CCWZ
references.
