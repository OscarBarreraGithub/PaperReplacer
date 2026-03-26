# Batch Brief: Mandelstam Variables and Crossing Refinement

## Goal

Build a narrow refinement batch around the already-authored Mandelstam-variable node,
adding the smallest reusable crossing and channel vocabulary needed for Schwartz-style
two-to-two scattering discussion.

This batch should refine invariant-kinematics language without becoming a process catalog
or a second general cross-sections batch.

## Target Topic

- `Mandelstam variables`
- `crossing symmetry`

## Batch Purpose

This batch is meant to turn the existing `qft.mandelstam_variables` node into a more
usable local neighborhood for reading channel language and crossing relations.

The batch should support:

- recognizing `s`, `t`, and `u` as the kinematic coordinates of the standard scattering
  channels,
- using crossing symmetry as the relation among amplitudes in different channel
  assignments,
- and reading channel language without collapsing it into specific named processes.

## In Scope

Likely high-value topics include:

- Mandelstam variables
- crossing symmetry
- s channel
- t channel
- u channel

## Explicitly Out of Scope

- named process catalogs
- frame-specific kinematics nodes
- Regge or analytic-continuation technology beyond the immediate crossing use
- a second generic scattering-amplitude or cross-section batch

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 7 nodes
- approximately 7 dependency edges
- a small partonomy rooted in crossing symmetry and channel language

## Overlap Expectations

This batch should explicitly reuse:

- `qft.mandelstam_variables`
- `qft.scattering_amplitude`

The batch-specific nodes here should refine the invariant-kinematics branch without
duplicating the broader cross-sections or named-process neighborhoods.

## Review Risks

- duplicating the existing Mandelstam node instead of refining around it
- letting the batch drift into process exemplars
- overcommitting to analytic-continuation machinery that belongs elsewhere
- flattening channel language into one vague crossing node

## Deliverable for This Batch

A compact authored refinement that reuses `qft.mandelstam_variables` and adds crossing plus
the `s`, `t`, and `u` channel vocabulary used throughout Schwartz.
