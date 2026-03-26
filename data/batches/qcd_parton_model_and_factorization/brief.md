# Batch Brief: QCD Parton Model and Factorization

## Goal

Create the first-pass stage 3 neighborhood for the QCD parton model and factorization language that Schwartz develops in Chapter 32.

This batch should stay source-light, recognition/use-first, and narrow enough that parton language does not collapse into a generic hadron-structure umbrella.

## Proposed Target

- `qcd.parton_model_and_factorization`

## Why This Slice

This slice is a good batch because it:

- reuses the QCD color and asymptotic-freedom background from the Yang-Mills batch,
- isolates the parton-model reading before drifting into jets or SCET,
- separates the universal factorization statement from its hadronic ingredients,
- and creates a stable bridge from QCD basics into later collider-facing neighborhoods.

## In Scope

Likely high-value topics include:

- parton-model language for fast hadrons
- quark and gluon partons
- parton distribution functions
- factorization theorems
- collinear factorization
- hard scattering coefficients
- splitting functions
- DGLAP evolution

## Explicitly Out of Scope

- SCET, jets, beam functions, or threshold resummation
- hadronization or other deep nonperturbative modeling
- a broad `QCD` umbrella node that replaces the specific parton/factorization frontier
- electroweak or Standard Model material outside the hadronic/QCD slice

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qcd_factorization`

## Expected Batch Size

- approximately 8 to 12 nodes
- approximately 9 to 13 dependency edges
- a modest partonomy with the parton-model and factorization branches kept distinct

## Overlap Expectations

This batch should explicitly reuse the shared QCD basics from the prior batch:

- `qcd.color_su3`
- `qcd.quark`
- `qcd.gluon`
- `qcd.asymptotic_freedom`

It should not duplicate the Yang-Mills action, gauge-fixing, or ghost machinery.

## Review Risks

- collapsing parton model and factorization into one undifferentiated topic
- overextending into SCET or jet structure before the basic factorization frontier is stable
- treating background QCD color facts as if they were new nodes
- letting the hadronic phenomenology side swallow the reusable factorization statement

## Deliverable for This Batch

A compact authored stage 3 neighborhood that turns QCD color structure into parton language, PDFs, and factorized short-distance scattering formulas.
