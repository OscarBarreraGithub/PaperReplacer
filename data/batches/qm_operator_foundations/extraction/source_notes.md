# Source Notes: QM Operator Foundations

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `quantum mechanics operator foundations` should be understood as the shared vocabulary needed to recognize and use the state-and-operator language that appears in ordinary QM writing and in later QFT-facing operator discussions.

High-value candidates are likely to include:

- Hilbert spaces
- state vectors and kets
- bra-ket notation
- inner products at the reading level
- observables as operator-valued quantities
- unitary evolution
- commutators
- eigenstates and eigenvalues
- projection operators if the source uses measurement or decomposition language

This batch is not trying to capture the whole formal edifice of quantum mechanics.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize the basic objects named in a QM source,
- follow ordinary explanations of how operators act on states,
- and use that vocabulary in simple reading or recall tasks.

The batch is not trying to capture:

- measurement-postulate derivations,
- spectral theorem or completeness proofs,
- unbounded operator theory,
- path-integral machinery,
- second quantization,
- or broad umbrella nodes that flatten the distinction between a state space and an operator on that space.

## Relationship to the Stage 1 Linear-Algebra Slice

This batch should reuse the Stage 1 canonical ids whenever they do real work:

- `math.linear_algebra.vector_space`
- `math.linear_algebra.basis_and_coordinates`
- `math.linear_algebra.linear_map`
- `math.operator_basics.linear_operator`
- `math.operator_basics.matrix_representation_of_linear_map`
- `math.operator_basics.composition_identity_inverse`
- `math.operator_basics.eigenvalues_and_eigenvectors`

The QM slice should build on those nodes rather than restating them in a new way.

## Domain Hints

Likely high-value node candidates are:

- `qm.hilbert_space`
- `qm.state_vector`
- `qm.bra_ket_notation`
- `qm.inner_product`
- `qm.observable_operator`
- `qm.unitary_evolution`
- `qm.commutator`
- `qm.eigenstate_and_eigenvalue`
- `qm.projection_operator`

Likely high-value dependency patterns:

- vector-space and operator-language prerequisites flowing into QM state/operator vocabulary
- basis-sensitive notation for kets and coordinate-like reading
- unitary and observable language built from linear-operator background
- eigenvalue language shared with the Stage 1 operator slice

## Anti-Patterns

Avoid:

- broad `quantum mechanics` umbrella nodes,
- treating bra-ket notation as a substitute for the underlying state/operator distinctions,
- importing advanced functional analysis too early,
- and collapsing observables, unitary maps, and general linear maps into one undifferentiated operator node.

## Evidence Guidance

When proposing claims, prefer evidence of these forms:

- source language that names states, operators, and Hilbert spaces directly,
- explanations that move from vectors to operators to physical interpretation,
- and operator-facing QM references that use commutator, unitary, observable, or eigenstate language without requiring derivation-first setup.

If a claim feels like it belongs to a later, deeper batch, flag it instead of asserting it here.
