# Batch Brief: Seesaw Mechanism Refinement

## Goal

Build a narrow Stage 22 refinement batch for the remaining Schwartz neutrino-mass residue
around the seesaw mechanism, the right-handed-neutrino ingredient, and the Majorana-mass
structure that makes the mechanism intelligible.

This batch should live under the existing flavor / PMNS / neutrino-mass branch rather than
reopening the full Standard-Model symmetry-breaking trunk or drifting into grand
unification and leptogenesis.

## Target Topic

- `see-saw mechanism`
- `neutrino mass`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that explains how the
existing neutrino-mass and PMNS branch can be refined by the standard seesaw explanation.

The batch should support:

- recognizing seesaw language as a neutrino-mass mechanism rather than an isolated BSM
  slogan,
- using right-handed-neutrino and Majorana-mass vocabulary in the minimal way needed to
  read the branch,
- and preserving the existing PMNS / neutrino-mass structure instead of duplicating it.

## In Scope

Likely high-value topics include:

- seesaw mechanism
- right-handed neutrino
- Majorana mass
- reuse of the existing neutrino-mass, PMNS, fermion-mass-generation, and lepton-number
  anchors

## Explicitly Out of Scope

- leptogenesis and baryogenesis extensions
- grand unification model building
- sterile-neutrino phenomenology or one-node-per-model catalogs
- full neutrino-data phenomenology beyond the existing PMNS / oscillation branch
- supersymmetry or broader BSM unification programs

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `standard_model_flavor`

## Expected Batch Size

- approximately 7 to 9 nodes
- approximately 5 to 7 dependency edges
- a compact partonomy centered on neutrino mass and the seesaw explanation

## Overlap Expectations

This batch should explicitly reuse:

- `sm.flavor_ckm_pmns_and_precision_observables`
- `sm.neutrino_mass`
- `sm.pmns_matrix`
- `sm.ewbreak.fermion_mass_generation`
- `sm.lepton_number`

The batch-specific nodes here should make Schwartz's seesaw residue queryable without
opening leptogenesis, GUT, or sterile-neutrino side branches.

## Review Risks

- treating seesaw as a generic BSM umbrella rather than a neutrino-mass refinement
- duplicating the existing PMNS / oscillation branch instead of refining it
- introducing Majorana mass without tying it to lepton-number language
- drifting into grand unification, leptogenesis, or sterile-neutrino cataloging

## Deliverable for This Batch

A compact authored Stage 22 neighborhood that connects neutrino mass to seesaw language via
the right-handed-neutrino and Majorana-mass ingredients.
