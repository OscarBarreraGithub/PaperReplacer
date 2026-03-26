# Batch Brief: QM Operator Foundations

## Goal

Create the first-pass foundation slice for the topic-centered neighborhood around quantum-mechanics operator language.

This batch is Stage 2 foundation work: source-light, recognition-oriented, and deliberately not derive-first. It should establish the smallest defensible graph neighborhood needed for reading and using the basic state, operator, and notation vocabulary that later QM and QFT batches will reuse.

## Proposed Target

- `quantum mechanics operator foundations`

## Why This Slice

This slice is a good Stage 2 batch because it:

- reuses the Stage 1 linear-algebra/operator backbone instead of rebuilding it,
- adds the QM-specific vocabulary that makes operator language usable in physics text,
- keeps states, operators, and notation distinct enough to read papers without overcommitting to derivations,
- and stays compact enough to serve as a stable bridge into later QFT-facing batches.

## In Scope for Batch 2

- Hilbert spaces as the ambient state space
- state vectors and kets
- bra-ket notation and basis-dependent reading of states
- inner products at the recognition/use level
- observables as operator-valued quantities
- unitary evolution as the standard state-evolution language
- commutators as basic operator algebra
- eigenstates and eigenvalues in the QM operator setting
- projection operators if they help read measurement or decomposition language

## Explicitly Out of Scope for Batch 2

- the full measurement postulate stack
- spectral theorem or resolution-of-identity derivations
- unbounded operator theory and domain subtleties
- path-integral or second-quantized machinery
- broad umbrella nodes such as `quantum mechanics` or `operator theory` unless a sharper decomposition is not available

## Task Model

- `literature_reading`

For this batch, the goal is to support recognition and ordinary use in QM/QFT-facing explanations, not derivation-first reconstruction.

## Target Mastery Modes

- `recognize`
- `use`

## Initial Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `qft_foundations`

## Expected Batch Size

- approximately 8 to 10 nodes
- approximately 8 to 14 dependency edges
- small overlay count in the first pass

## Review Risks

- drifting into full quantum foundations instead of the operator-facing slice,
- importing unbounded operator theory before the basic vocabulary is in place,
- conflating basis-dependent notation with intrinsic operator structure,
- and losing the connection back to the Stage 1 linear-algebra/operator baseline.

## Deliverable for This Batch

A small authored Stage 2 foundation slice with a defensible contract, concise extraction guidance, and a first-pass operator-facing QM neighborhood ready for later QFT use.
