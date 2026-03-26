# Batch Brief: QED Loop Precision Refinement

## Goal

Build a compact refinement batch for `electron self-energy`, `anomalous magnetic moment`,
and `Uehling potential`.

This batch should close the remaining coherent QED loop-precision residue without turning
into a broad radiative-corrections or precision-electroweak umbrella.

## Target Topic

- `QED loop precision tail`
- `electron-sector and vacuum-polarization payoffs`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
QED loop-precision vocabulary in Schwartz queryable.

The batch should support:

- reading electron self-energy as the canonical electron-sector loop correction,
- recognizing anomalous magnetic moment as the standard precision payoff of loop-corrected
  QED vertex structure,
- and placing the Uehling potential as the vacuum-polarization correction to the Coulomb
  potential.

## In Scope

Likely high-value topics include:

- electron self-energy
- anomalous magnetic moment
- Uehling potential

## Explicitly Out of Scope

- a full QED radiative-correction catalog
- electroweak precision observables beyond the reused vacuum-polarization bridge
- muon-specific precision phenomenology
- generic form-factor or threshold cleanup

## Task Model

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qed`

## Expected Batch Size

- approximately 7 to 8 nodes
- approximately 7 to 8 dependency edges
- a compact partonomy rooted in a dedicated QED loop-precision slice

## Overlap Expectations

This batch should explicitly reuse:

- `qft.renormalized_perturbation_theory`
- `qft.spinor_lorentz_dirac_foundations`
- `qft.free_dirac_field`
- `sm.precision.gauge_boson_self_energy`

The batch-specific nodes here should capture the remaining QED loop payoffs without
duplicating the earlier renormalization trunk or the electroweak precision branch.

## Review Risks

- duplicating generic renormalization nodes with QED-local names
- treating `anomalous magnetic moment` as a detached precision number instead of a loop-level
  QED payoff
- recreating a second vacuum-polarization node rather than reusing the existing self-energy
  bridge
- allowing the batch to drift into process-specific or muon-specific precision catalogs

## Deliverable for This Batch

A compact authored refinement that closes the remaining QED loop-precision tail around the
electron self-energy, anomalous magnetic moment, and Uehling potential.
