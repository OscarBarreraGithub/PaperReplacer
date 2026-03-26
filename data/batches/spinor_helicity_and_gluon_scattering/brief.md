# Batch Brief: Spinor-Helicity and Gluon Scattering

## Goal

Build a first-pass Stage 5 batch for spinor-helicity notation, Schouten identity,
color-ordered amplitudes, MHV structure, the Parke-Taylor formula, and the canonical gluon
tree-scattering neighborhood under pressure from the Schwartz index.

This batch should keep the modern amplitudes branch readable without flattening it into a
glossary of every named formula or historical subprogram.

## Target Topic

- `spinor-helicity and gluon scattering`

## Batch Purpose

This batch is meant to capture the reusable neighborhood that lets a reader parse on-shell
spinor-helicity formulas and the standard tree-level gluon-amplitude simplifications.

The batch should support:

- recognizing spinor-helicity notation as an on-shell amplitude language,
- using Schouten and color ordering as the basic simplification tools,
- and reading MHV / Parke-Taylor formulas as compact statements about tree-level gluon
  amplitudes.

## In Scope

Likely high-value topics include:

- spinor-helicity notation
- angle and square spinor products
- Schouten identity
- color-ordered amplitudes
- MHV amplitudes
- Parke-Taylor formula
- gluon tree scattering

## Explicitly Out of Scope

- loop-level unitarity and generalized cuts
- BCFW recursion and broader on-shell bootstrap machinery
- supersymmetric amplitudes or twistor-string branches
- every helicity configuration as a separate node
- historical or named-formula branches that do not change prerequisite answers

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_amplitudes`

## Expected Batch Size

- approximately 12 to 15 nodes
- approximately 12 to 16 dependency edges
- a compact partonomy centered on notation, color ordering, and MHV structure

## Overlap Expectations

This batch should explicitly reuse:

- `qft.mass_shell`
- `qft.spin_label`
- `qft.scattering_amplitude`
- `qcd.color_su3`
- `qcd.gluon`
- `qft.non_abelian_gauge_symmetry`

The new nodes here should become the reusable amplitudes-facing bridge back into the existing
Lorentz/spinor and Yang-Mills trunk.

## Review Risks

- duplicating generic spinor foundations that already live in the trunk
- making `color-ordered` and `color-stripped` separate nodes when one canonical node will do
- proliferating named formulas without a reusable branch structure
- treating the whole amplitudes program as if it were required for ordinary tree-level QFT
  reading

## Deliverable for This Batch

A compact authored Stage 5 neighborhood that connects on-shell spinor-helicity notation to
color ordering, MHV structure, and the Parke-Taylor gluon-tree formula.
