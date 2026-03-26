# Batch Brief: Cross Sections, Decay Rates, and Phase Space

## Goal

Build a reusable first-pass neighborhood around the canonical topic

- `qft.cross_sections_decay_rates_and_phase_space`

The batch should support Schwartz-style scattering formulas without exploding into a process catalog or a separate analytic-structure batch.

## In Scope

High-value topics include:

- scattering amplitudes as the bridge from LSZ to observables
- cross sections and decay rates
- Lorentz-invariant phase space
- the two-body phase-space specialization
- Mandelstam variables
- flux factors
- the narrow-width approximation
- Breit-Wigner distribution language
- partial-wave language

## Explicitly Out of Scope

- a full named-process inventory
- a second decay-width node unless later extraction forces it
- generic contour/pinch machinery
- broad unitarity or optical-theorem decomposition
- frame-specific nodes like Breit frame or center-of-mass frame

## Reuse Expectations

Reuse existing canonical ids where they already carry the right prerequisite behavior:

- `relativity.lorentz_transformation`
- `qft.lsz_reduction_formula`

Treat these as shared trunk nodes, not as new topic splits.

## Overlap Decisions

- `qft.scattering_amplitude` is introduced as a distinct bridge node, not as an alias for LSZ.
- `qft.cross_section` and `qft.decay_rate` are kept as the first-pass observable nodes; no separate width split yet.
- `qft.breit_wigner_distribution` is preferred over a generic resonance node because the Schwartz usage is physics-first but still formula-driven.
- Specific exemplars like Bhabha, Moller, Compton, Rutherford, or Thomson scattering are deferred to the process batch.

## Deliverable

A compact authored batch that can be reused in later amplitudes and phenomenology work without introducing duplicate canonical ids or premature topic fragmentation.
