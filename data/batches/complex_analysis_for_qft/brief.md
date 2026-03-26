# Batch Brief: Complex Analysis for QFT

## Goal

Create a Stage 1 foundation batch for the complex-analysis machinery that shows up in QFT papers, with a narrow topic-centered scope and a source-light, literature-reading orientation.

This batch is a scaffold for future population work, not a derive-first or canonical deep slice of `qft.complex_analysis_for_qft`.

## Proposed Target

- `complex analysis for QFT`

## Why This Slice

This slice is a good Stage 1 foundation batch because it:

- anchors the graph around the paper-facing complex-analysis tools that recur in QFT,
- keeps the topic centered on recognition and practical use rather than derivation,
- gives future agents a defensible place to add prerequisite structure without overexpanding into all of QFT,
- and leaves room for later refinement into deeper subtopics once the surface layer is stable.

## In Scope for Batch 1

- contour deformation
- poles vs branch points
- Feynman `i epsilon` prescription
- propagator singularities
- pinch singularities
- recognition-level references to analytic continuation only when they are directly tied to the above

## Explicitly Out of Scope for Batch 1

- Landau singularity conditions
- loop-momentum stationarity conditions
- full loop-energy derivations
- distributional boundary values as a standalone topic
- broad umbrella nodes such as `QFT` or `complex analysis` unless a sharper decomposition is not available
- derivation-first packaging of the topic before the recognition/use layer is established

## Task Model

- `literature_reading`

For this batch, the goal is to support paper parsing and standard analytic arguments, not to build a full derivation tree.

## Target Mastery Modes

- `recognize`
- `use`

## Initial Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `amplitudes`

## Expected Batch Size

- approximately 4 to 8 nodes
- approximately 4 to 12 dependency edges
- very small or zero overlay count in the first pass

## Review Risks

- drifting into a broader `QFT` umbrella instead of keeping the topic centered,
- overcommitting to derivation-level prerequisites too early,
- confusing paper-facing background with intrinsic dependency structure,
- and letting source-light scaffolding become a proxy for complete coverage.

## Deliverable for This Batch

A small authored foundation slice with a defensible contract, concrete source notes, and placeholder authored files that future agents can populate consistently.
