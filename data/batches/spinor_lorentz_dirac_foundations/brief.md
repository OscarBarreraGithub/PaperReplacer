# Batch Brief: Spinor, Lorentz, and Dirac Foundations

## Goal

Create a Stage 2 population batch for the spinor and Dirac neighborhood that Schwartz uses before the discrete-symmetry chapter family.

This batch should be source-light, recognition/use-first, and reusable as the canonical bridge from Lorentz representation language into Dirac spinors, gamma matrices, and chirality notation.

## Target Topic

- `spinor lorentz dirac foundations`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read and use the standard spinor/Dirac vocabulary in QFT texts.

The batch should support:

- recognizing how spinors sit inside the Lorentz-representation story,
- using gamma-matrix and Dirac-equation notation in ordinary reading,
- and keeping the spinor/Dirac neighborhood distinct from discrete symmetries and from later free-field quantization.

## In Scope

Likely high-value topics include:

- Lorentz-group spinor representations
- Dirac spinors and Weyl spinors
- gamma matrices and Dirac algebra
- gamma five and chirality projectors
- the Dirac equation at the recognize/use level
- Dirac adjoints when bilinears are in view

## Explicitly Out of Scope

- full Clifford-algebra derivations
- unbounded-operator subtleties
- interaction-specific fermion dynamics
- discrete symmetries as a separate branch
- broad umbrella nodes such as `QFT` or `spinor theory` unless a sharper decomposition is not available

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 9 to 12 nodes
- approximately 10 to 16 dependency edges
- a small amount of partonomy where it clarifies the spinor/Dirac split

## Overlap Expectations

This batch should explicitly reuse the Lorentz-representation neighborhood where appropriate, especially:

- `relativity.lorentz_transformation`
- `qft.lorentz_group_representation`

## Review Risks

- splitting spinor objects away from the Lorentz-representation story that motivates them
- collapsing Dirac and Weyl spinors into one undifferentiated fermion node
- drifting into discrete symmetries before the spinor/Dirac notation is stable
- creating a second gamma-matrix or Dirac-algebra vocabulary with no clear reuse path

## Deliverable for This Batch

A compact authored Stage 2 spinor/Dirac neighborhood that can be reused by later discrete-symmetry and fermion-field batches without re-deciding the representation scaffolding.
