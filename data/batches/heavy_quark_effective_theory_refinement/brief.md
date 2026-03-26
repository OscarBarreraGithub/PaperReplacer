# Batch Brief: Heavy-Quark Effective Theory Refinement

## Goal

Build a Stage 6 refinement batch for the existing HQET branch, centered on the heavy-quark
limit, velocity decomposition, residual momentum, the velocity-labeled field picture, and
the first `1 / m_Q` correction language.

This batch should refine the current EFT/HQET stub without creating a duplicate HQET trunk.

## Target Topic

- `heavy-quark effective theory`

## Batch Purpose

This batch is meant to turn the current two-node HQET stub into a compact recognition/use
branch that makes Schwartz's heavy-quark notation and symmetry claims queryable.

The batch should support:

- recognizing the heavy-quark limit as the organizing asymptotic regime,
- using the `p_Q = m_Q v + k` decomposition and velocity-labeled field vocabulary,
- and reading the `1 / m_Q` expansion as the first controlled refinement of the static
  limit.

## In Scope

Likely high-value topics include:

- heavy-quark limit
- heavy-quark velocity
- residual momentum
- velocity-dependent heavy-quark field
- `1 / m_Q` expansion
- heavy-quark symmetry
- Isgur-Wise function as a single symmetry-facing payoff leaf

## Explicitly Out of Scope

- semileptonic decay catalogs and CKM phenomenology
- inclusive OPE or heavy-hadron spectroscopy programs
- SCET spillover, jet physics, or threshold resummation
- a full form-factor ontology beyond one symmetry-controlled endpoint

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `effective_field_theory`

## Expected Batch Size

- approximately 13 nodes
- approximately 13 to 14 dependency edges
- a compact partonomy under the existing `eft.heavy_quark_effective_theory` root

## Overlap Expectations

This batch should explicitly reuse:

- `eft.heavy_quark_effective_theory`
- `eft.heavy_quark_symmetry`
- `eft.scale_separation`
- `eft.matching`
- `eft.operator_expansion`
- `eft.power_counting`
- `qcd.quark`

The batch-specific nodes here should refine HQET as an existing branch of the EFT trunk,
not create a second EFT or HQET umbrella.

## Review Risks

- duplicating the existing HQET root with a parallel topic node
- drifting into CKM or semileptonic process phenomenology
- letting SCET or jet language leak into the HQET refinement
- turning one symmetry-facing payoff node into a broader form-factor atlas

## Deliverable for This Batch

A compact authored Stage 6 refinement that keeps `eft.heavy_quark_effective_theory` as the
root while adding the heavy-quark limit, velocity decomposition, residual momentum,
velocity-labeled field, and `1 / m_Q` expansion structure used in Schwartz.
