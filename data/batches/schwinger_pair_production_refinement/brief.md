# Batch Brief: Schwinger Pair Production Refinement

## Goal

Build a minimal payoff refinement for `Schwinger pair production` under the existing
effective-action and background-field branch.

This batch should add the physical background-field payoff without reopening the already
landed Schwinger proper-time formalism or expanding into a broader strong-field QED catalog.

## Target Topic

- `background-field payoff cleanup`
- `Schwinger pair production`

## Batch Purpose

This batch is meant to capture the smallest reusable neighborhood that makes the remaining
Schwartz background-field payoff queryable.

The batch should support:

- recognizing Schwinger pair production as the physical instability of the vacuum in a
  strong background electric field,
- reading it as a payoff of the already-landed one-loop effective-action and proper-time
  tools.

## In Scope

Likely high-value topics include:

- Schwinger pair production

## Explicitly Out of Scope

- a broad strong-field QED branch
- detailed worldline formalism
- QED loop precision observables such as g-2 or the Uehling potential

## Task Model

- `standard_computation`
- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 6 to 7 nodes
- approximately 4 to 5 dependency edges
- a minimal partonomy rooted in the existing effective-action / background-field branch

## Overlap Expectations

This batch should explicitly reuse:

- `qft.effective_actions_and_background_fields`
- `qft.background_field`
- `qft.background_field_method`
- `qft.one_loop_effective_action`
- `qft.schwinger_proper_time`

The new node here should act as a payoff leaf of the existing background-field branch rather
than as the start of a new strong-field program.

## Review Risks

- duplicating the already-landed Schwinger proper-time node with a second formalism node
- letting the batch expand into a generic external-field QED catalog
- treating pair production as a free-floating historical label instead of a background-field
  payoff

## Deliverable for This Batch

A compact authored refinement that adds the remaining Schwinger pair-production payoff leaf
to the current effective-action and background-field neighborhood.
