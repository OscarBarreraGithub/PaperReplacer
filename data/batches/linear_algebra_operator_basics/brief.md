# Batch Brief: Linear Algebra and Operator Basics

## Goal

Create the first-wave foundation slice for the topic-centered neighborhood around linear algebra and operator basics.

This batch is Stage 1 foundation: source-light, recognition-oriented, and deliberately not derive-first. It should define the smallest defensible graph neighborhood needed for reading, naming, and using the basic objects and operations that later QM and QFT batches will reuse.

## Proposed Target

- `linear algebra and operator basics`

## Why This Slice

This slice is a good first batch because it:

- centers on a compact topic family rather than a theorem stack,
- exercises recognition and everyday use of the core vocabulary,
- distinguishes objects, maps, and representations without pulling the graph into advanced proof territory,
- and stays small enough for future agents to populate from a limited source set.

## In Scope for Batch 1

- vectors and vector spaces
- subspaces, spans, and bases
- linear maps and linear operators
- matrix representations of linear maps
- composition and identity maps
- invertibility, kernels, and images at the recognition/use level
- eigenvalues and eigenvectors as basic operator vocabulary
- transpose or adjoint in the minimal sense needed to read operator language, if evidence supports it

## Explicitly Out of Scope for Batch 1

- proof-heavy derivations such as rank-nullity or spectral theorem unless a source explicitly requires them
- advanced functional analysis or unbounded operator theory
- canonical forms, diagonalization, and Jordan theory unless needed for a future distinct slice
- numerical linear algebra, optimization, or category-theoretic generalizations
- broad umbrella topics that flatten the distinction between linear algebra and operator language

## Task Model

- `literature_reading`

For this batch, the goal is to support recognition and ordinary use in reading or following QM/QFT-facing explanations, not derivation-first reconstruction.

## Target Mastery Modes

- `recognize`
- `use`

## Initial Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 6 to 12 nodes
- approximately 4 to 12 dependency edges
- small or zero overlay count in the first pass

## Review Risks

- drifting into theorem-proving content too early
- using a giant umbrella node like `linear algebra` when sharper nodes are available
- conflating matrices with operators without stating the representation step
- promoting advanced operator theory before the basic vocabulary is established

## Deliverable for This Batch

A small authored foundation slice with a defensible contract, concise extraction guidance, and placeholder authored files ready for the next population pass.
