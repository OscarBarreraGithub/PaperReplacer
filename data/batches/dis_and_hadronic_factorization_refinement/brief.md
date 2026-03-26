# Batch Brief: DIS and Hadronic Factorization Refinement

## Goal

Build a narrow refinement batch for deep-inelastic scattering, Bjorken variables and
scaling, Drell-Yan, Mellin moments, and twist.

This batch should stay centered on reusable hadronic-factorization language rather than
turn into a broad collider-process catalog or a SCET/resummation branch.

## Target Topic

- `deep-inelastic scattering`
- `hadronic factorization`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
Schwartz DIS and hadronic-factorization vocabulary queryable.

The batch should support:

- recognizing DIS and Drell-Yan as the central hadronic process contexts for factorization,
- using Bjorken x and Bjorken scaling in the DIS branch,
- and reading Mellin moments and twist as the first structure-level refinements of the
  same hadronic factorization story.

## In Scope

Likely high-value topics include:

- deep-inelastic scattering
- Bjorken x
- Bjorken scaling
- Drell-Yan process
- Mellin moment
- twist

## Explicitly Out of Scope

- event shapes, thrust, or jet-mass observables
- threshold resummation and SCET mode structure
- a broad hadronization or nonperturbative QCD survey
- full resonance or electroweak process catalogs

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qcd_factorization`

## Expected Batch Size

- approximately 12 to 14 nodes
- approximately 10 to 14 dependency edges
- a compact partonomy rooted in the DIS, Drell-Yan, and structure-level branches

## Overlap Expectations

This batch should explicitly reuse:

- `qcd.parton_model_and_factorization`
- `qcd.parton_distribution_function`
- `qcd.factorization_theorem`
- `qcd.collinear_factorization`
- `qcd.hard_scattering_coefficient`
- `qft.cross_section`

The batch-specific nodes here should sharpen the hadronic-factorization branch without
reopening SCET, jet physics, or a broad collider-process neighborhood.

## Review Risks

- turning the refinement into a generic scattering-process catalog
- duplicating the existing parton/PDF/factorization trunk instead of refining it
- pulling threshold or event-shape language in too early and colliding with the SCET queue
- treating Mellin moments or twist as isolated formulas rather than hadronic-structure
  refinements

## Deliverable for This Batch

A compact authored refinement that connects the existing parton/factorization trunk to DIS,
Bjorken variables, Drell-Yan, Mellin moments, and twist.
