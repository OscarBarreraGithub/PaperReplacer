# Batch Brief: Discrete Symmetries and CPT

## Goal

Create a Stage 2 population batch for the discrete-symmetry and CPT neighborhood that Schwartz uses alongside the spinor/Dirac material.

This batch should be source-light, recognition/use-first, and reusable as the canonical bridge from spinor/Dirac notation into parity, charge conjugation, time reversal, and CPT language.

## Target Topic

- `discrete symmetries and cpt`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read and use the standard discrete-symmetry vocabulary in QFT texts.

The batch should support:

- recognizing parity, charge conjugation, and time reversal as distinct operations,
- using the standard CPT statement in relativistic fermion contexts,
- and keeping the discrete-symmetry neighborhood distinct from the underlying spinor/Dirac foundation and from later interaction-specific work.

## In Scope

Likely high-value topics include:

- parity, charge conjugation, and time reversal as separate transformations
- their action on Dirac spinors and spinor bilinears
- CPT as the combined symmetry statement
- the discrete-symmetry reading of gamma-matrix and chirality notation when it appears

## Explicitly Out of Scope

- full proof-level CPT-theorem derivations
- interaction-specific symmetry breaking
- gauge-theory anomaly machinery beyond the local batch needs
- broad umbrella nodes such as `symmetry` or `CPT` without the discrete-fermion context
- field-quantization details that belong to later batches

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 8 to 11 nodes
- approximately 9 to 15 dependency edges
- a small amount of partonomy where it clarifies the P, C, T, and CPT split

## Overlap Expectations

This batch should explicitly reuse the spinor/Dirac neighborhood where appropriate, especially:

- `qft.spinor_lorentz_dirac_foundations`
- `qft.dirac_spinor`
- `qft.gamma_matrices`

## Review Risks

- collapsing parity, charge conjugation, and time reversal into one generic symmetry node
- trying to state CPT without the spinor/Dirac context that makes it readable
- drifting into anomaly or gauge-theory territory before the discrete-symmetry core is stable
- making CPT the only symmetry and losing the distinct P/C/T pieces

## Deliverable for This Batch

A compact authored Stage 2 discrete-symmetry neighborhood that can be reused by later fermion, anomaly, and symmetry-breaking batches without re-deciding the CPT scaffolding.
