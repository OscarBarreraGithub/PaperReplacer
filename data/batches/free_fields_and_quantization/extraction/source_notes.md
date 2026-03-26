# Source Notes: Free Fields and Quantization

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `free fields and quantization` should be understood as the standard QFT trunk slice covering:

- relativistic free scalar, Dirac, and vector fields,
- their mode expansions in terms of positive- and negative-frequency pieces,
- creation and annihilation operators,
- canonical quantization via equal-time brackets,
- and the locality/spin-statistics constraints that appear in the same reading neighborhood.

This batch is intended to support paper, lecture-note, and textbook reading in the QFT/HEP-th foundation setting, not a derivation-first reconstruction of all quantization formalisms or a move into interactions.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize the free-field species that recur in Schwartz-style QFT writing,
- follow ordinary mode-expansion and operator-language explanations,
- and use the canonical quantization vocabulary in routine reading and calculation tasks.

The batch is not trying to capture:

- propagators or correlators,
- LSZ or scattering theory,
- path-integral machinery,
- renormalization,
- gauge fixing as a separate branch,
- or a complete axiomatization of quantum fields.

## Likely Reuse Candidates

Reuse the canonical ids that already do real work in the earlier foundation batches instead of minting duplicates:

- `classical_fields.field_configuration`
- `classical_fields.action_functional`
- `qft.lorentz_group_representation`
- `qft.poincare_group_representation`
- `qft.one_particle_state`
- `qft.spin_label`
- `qm.commutator`

These should be treated as shared background or prerequisite anchors, not as new topic nodes.

## Likely New Node Candidates

The most likely new node candidates are:

- `qft.free_fields_and_quantization`
- `qft.free_scalar_field`
- `qft.free_dirac_field`
- `qft.free_vector_field`
- `qft.canonical_quantization`
- `qft.mode_expansion`
- `qft.creation_annihilation_operator`
- `qft.equal_time_commutation_relations`
- `qft.microcausality`
- `qft.spin_statistics`

## Likely Edge Patterns

High-value dependency patterns probably include:

- classical field configuration and action language into the free-field starting point
- Lorentz-covariant representation language into the free field species
- free field species into mode expansions
- mode expansions into creation/annihilation operators
- canonical quantization into equal-time brackets
- commutator language into equal-time bracket statements
- equal-time brackets into microcausality
- microcausality and spin labels into spin-statistics statements

## Source Guidance

Prioritize introductory QFT passages that explicitly define free scalar, Dirac, and vector fields; write them in mode-expansion form; and then impose the canonical operator relations.

Prefer a small source set with stable terminology over broad secondary references or highly formal derivations.

## Anti-Patterns

Avoid:

- interacting-field or vertex machinery,
- path-integral or generating-functional branches,
- propagator or LSZ claims,
- gauge-fixing detours that are not needed to understand the free-field slice,
- broad `quantization` umbrella nodes,
- and treating a derivation from first principles as mandatory for every node.

## Evidence Guidance

Use evidence that shows:

- how authors define the free field species,
- which mode-expansion language is treated as standard,
- where the creation/annihilation operators enter the reading,
- which equal-time brackets are imposed,
- and when microcausality or spin-statistics is presented as part of the same operator-reading neighborhood.

If a candidate feels like it belongs to propagators, interactions, or path integrals, flag it for later expansion instead of forcing it into this first-pass trunk slice.
