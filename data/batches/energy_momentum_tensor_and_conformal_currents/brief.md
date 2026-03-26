# Batch Brief: Energy-Momentum Tensor and Conformal Currents

## Goal

Build a narrow refinement batch for the energy-momentum-tensor branch that bridges the
existing Noether/classical-fields trunk to scale, conformal, and Weyl-current language.

This batch should stay structural and reusable, not become a full conformal-field-theory
atlas or a generic symmetry survey.

## Target Topic

- `energy-momentum tensor`
- `conformal currents`

## Batch Purpose

This batch is meant to make Schwartz-style stress-tensor and conformal-current language
queryable without reopening the whole critical-phenomena or variational-principles trunks.

The batch should support:

- recognizing the energy-momentum tensor as the translation-current branch of Noether
  reasoning,
- distinguishing the canonical and improved tensor vocabulary,
- and reading dilatation and conformal currents as the current-side payoff of scale and
  conformal invariance.

## In Scope

Likely high-value topics include:

- Noether current
- energy-momentum tensor
- canonical energy-momentum tensor
- improved energy-momentum tensor
- dilatation current
- conformal current
- scale invariance
- conformal invariance
- Weyl invariance

## Explicitly Out of Scope

- full CFT/OPE/bootstrap machinery
- trace-anomaly detail beyond the local current vocabulary
- gravitational stress-tensor or curved-background technology
- broad symmetry-classification cleanup outside the current branch

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 10 to 11 nodes
- approximately 10 to 11 dependency edges
- a compact partonomy rooted in the energy-momentum-tensor and current branches

## Overlap Expectations

This batch should explicitly reuse:

- `classical_fields.noether_theorem`
- `qft.scale_invariance`
- `qft.conformal_invariance`
- `qft.weyl_invariance`

The batch-specific nodes here should refine the current/stress-tensor branch without
duplicating the critical-phenomena batch or the classical variational trunk.

## Review Risks

- minting a duplicate energy-momentum-tensor node in the wrong namespace
- drifting into full conformal-field-theory machinery
- turning Weyl invariance into a full anomaly branch
- flattening canonical and improved stress-tensor language into a single vague node

## Deliverable for This Batch

A compact authored refinement that connects Noether currents to the canonical and improved
energy-momentum tensor, then uses that branch to orient dilatation and conformal-current
language.
