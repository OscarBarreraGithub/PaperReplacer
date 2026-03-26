# Batch Brief: Flavor, CKM/PMNS, and Precision Observables

## Goal

Build a first-pass Stage 5 batch for flavor mixing, the CKM and PMNS matrices, the
Wolfenstein and unitarity-triangle vocabulary, the Jarlskog invariant, neutrino-oscillation
language, and the precision-observable bridge that shows up across the later Schwartz
Standard Model chapters.

This batch should keep the graph topic-centered and avoid exploding into one node per
measurement or experimental anomaly.

## Target Topic

- `flavor, CKM/PMNS, and precision observables`

## Batch Purpose

This batch is meant to capture the reusable Standard Model neighborhood that explains how
fermion mass generation turns into flavor mixing, how CKM and PMNS language is organized,
and how the resulting vocabulary meets the existing precision-observable branch.

The batch should support:

- recognizing flavor mixing as a reusable Standard Model topic rather than as a list of
  process names,
- using CKM, PMNS, Wolfenstein, unitarity-triangle, and Jarlskog language in papers,
- and reading the precision-observable bridge without duplicating the existing anomalies and
  precision batch.

## In Scope

Likely high-value topics include:

- flavor mixing
- CKM matrix
- PMNS matrix
- Wolfenstein parametrization
- unitarity triangle
- Jarlskog invariant
- neutrino mass
- neutrino oscillation
- electroweak precision-observable bridge reuse

## Explicitly Out of Scope

- full flavor-changing-neutral-current phenomenology
- detailed neutrino-oscillation data fits and matter effects
- seesaw-model building and leptogenesis branches
- baryogenesis, technicolor, or grand-unification detours
- one node per flavor experiment or decay mode

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `standard_model_flavor`

## Expected Batch Size

- approximately 11 to 14 nodes
- approximately 10 to 14 dependency edges
- a compact partonomy centered on flavor mixing with a light precision-observable bridge

## Overlap Expectations

This batch should explicitly reuse:

- `sm.ewbreak.fermion_mass_generation`
- `sm.ewbreak.electroweak_mixing_angle`
- `sm.precision.electroweak_precision_observable`
- `sm.precision.effective_weak_mixing_angle`

The new nodes here should become the reusable flavor-mixing branch that later Standard Model
coverage can attach to without rebuilding the existing precision neighborhood.

## Review Risks

- duplicating the electroweak precision branch that already exists
- flattening CKM, PMNS, Wolfenstein, and unitarity-triangle language into unrelated one-off
  labels
- treating every neutrino topic as if it belonged in the first-pass flavor batch
- overcommitting the ontology to phenomenology-specific observables

## Deliverable for This Batch

A compact authored Stage 5 neighborhood that connects flavor mixing to CKM and PMNS
language, the first CP-violation invariant branch, and the shared precision-observable
bridge.
