# Batch Brief: Infrared Divergences and Jets

## Goal

Build a first-pass Stage 5 batch for infrared divergences, the soft/collinear split,
cancellation theorems, inclusive observables, and the jet/event-shape language that ties
factorization to SCET in the Schwartz QFT backlog.

This batch should stay topic-centered, reusable across QCD and EFT work, and avoid turning
named observables into one-off ontology debris.

## Target Topic

- `infrared divergences and jets`

## Batch Purpose

This batch is meant to capture the reusable neighborhood that explains why unresolved
radiation produces infrared singularities, why inclusive observables matter, and how jet
language becomes the bridge into factorization and SCET.

The batch should support:

- recognizing infrared divergences as observable-level singular structures in scattering,
- using the soft/collinear split and the Bloch-Nordsieck / KLN theorems in literature-facing
  arguments,
- and reading jet and thrust language as the event-shape side of the same factorized
  neighborhood.

## In Scope

Likely high-value topics include:

- infrared divergence
- soft divergence
- collinear divergence
- inclusive observable
- Bloch-Nordsieck theorem
- Kinoshita-Lee-Nauenberg theorem
- factorization and collinear factorization reuse
- SCET reuse where it organizes the same infrared structure
- jet and thrust as the first reusable event-shape branch

## Explicitly Out of Scope

- full jet-algorithm taxonomies
- non-global logarithms, grooming, and modern collider-substructure refinements
- detailed hadronization modeling
- process-specific soft-photon examples
- threshold-resummation subbranches beyond a first event-shape foothold

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qcd_ir`

## Expected Batch Size

- approximately 12 to 16 nodes
- approximately 12 to 16 dependency edges
- a compact partonomy that keeps the cancellation-theorem and jet branches legible

## Overlap Expectations

This batch should explicitly reuse:

- `qft.cross_section`
- `qcd.factorization_theorem`
- `qcd.collinear_factorization`
- `eft.soft_collinear_effective_theory`
- `eft.large_logarithm_resummation`
- `eft.jet_function`
- `eft.soft_function`

The new nodes here should become the reusable bridge from the existing factorization and SCET
trunk into the remaining Schwartz infrared backlog.

## Review Risks

- treating all infrared structure as if it were only a QED soft-photon story
- duplicating the existing factorization and SCET nodes instead of reusing them
- creating one node per named event shape
- confusing cancellation theorems with structural `part_of` decomposition
- letting a broad `jets` umbrella erase the actual soft/collinear structure

## Deliverable for This Batch

A compact authored Stage 5 neighborhood that connects infrared divergences to cancellation
theorems, inclusive observables, and the first reusable jet/event-shape branch.
