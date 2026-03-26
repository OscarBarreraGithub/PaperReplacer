# Batch Brief: QED Tree-Level Processes

## Goal

Build a first-pass Stage 3 batch for the canonical tree-level QED scattering neighborhood that Schwartz reuses for intuition and worked examples.

This batch should stay reusable and process-centered: enough structure to recognize the standard QED exemplar processes and process-sensitive results, but not a second QED foundation universe.

## Target Topic

- `qed tree-level processes`

## Batch Purpose

This batch is meant to capture the smallest defensible structure needed to read and use the standard QED process examples that recur in Schwartz-style QFT writing.

The batch should support:

- recognizing the named QED exemplar processes and result-like nodes,
- using the process-sensitive language that changes with the external particles or channels,
- and keeping the process neighborhood distinct from generic cross-section, decay, phase-space, and gauge-fixing machinery.

## In Scope

Likely high-value topics include:

- Bhabha scattering
- Moller scattering
- Compton scattering
- electron-positron to muon-antimuon scattering
- light-by-light scattering
- equivalent photon approximation
- Mott formula

## Explicitly Out of Scope

- cross sections, decay rates, and phase-space formulas
- renormalization, loops, and self-energy corrections
- scalar QED as a separate branch
- gauge-fixing, BRST, or Ward-identity machinery
- broad umbrella nodes such as `QED` or `scattering` unless a concrete decomposition need appears
- generic process-agnostic machinery such as `Mandelstam variables`, `Lorentz-invariant phase space`, `Breit-Wigner distribution`, `narrow-width approximation`, or `partial-wave` language

## Task Model

- `standard_computation`

## Target Mastery Modes

- `recognize`
- `use`
- `derive`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_backbone`

## Expected Batch Size

- approximately 8 to 10 nodes
- approximately 16 to 20 dependency edges
- a small overlay layer

## Review Risks

- turning each named process into a separate ontology universe instead of a compact reusable neighborhood
- drifting into cross sections, phase space, or generic utility machinery before the exemplar-process slice is stable
- adding a duplicate QED scattering root instead of reusing the shared process nodes

## Deliverable for This Batch

A compact authored Stage 3 tree-level QED process scaffold that later cross-section, gauge-invariance, and loop-level batches can reuse without rebuilding the process neighborhood from scratch.
