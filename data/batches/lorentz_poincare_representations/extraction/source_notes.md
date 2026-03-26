# Source Notes: Lorentz and Poincare Representations

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `qft.lorentz_poincare_representations` should be understood in the standard particle-physics sense:

- Lorentz transformations and their representations as the symmetry language for boosts and rotations,
- Poincare representations as the spacetime-symmetry action on state spaces,
- and Wigner-style particle classification by mass and little-group labels.

This batch is intended to support paper, lecture-note, and textbook reading in the QFT/HEP-th foundation setting, not a derivation-first reconstruction of induced representations or the Poincare algebra.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize the basic representation-theoretic vocabulary in a source,
- follow ordinary explanations of one-particle states and their symmetry labels,
- and use the standard mass-shell / little-group / spin-label reading of the topic.

The batch is not trying to capture:

- the full theory of group representations,
- proof-heavy classification derivations,
- or a broad dynamical treatment of fields and interactions.

## Likely High-Value Node Candidates

The most likely node candidates are:

- Lorentz group representation
- Poincare group representation
- one-particle state
- mass shell
- little group
- spin label
- Wigner classification

The most likely reuse candidates from the relativistic-kinematics batch are:

- `relativity.lorentz_transformation`
- `relativity.invariant_interval`
- `relativity.rapidity`

## Likely Edge Patterns

High-value dependency patterns probably include:

- Lorentz transformations into representation language
- invariant interval into mass-shell language
- Poincare representation language into one-particle states
- mass-shell and little-group vocabulary into Wigner classification
- little-group labels into spin or helicity labels

## Source Guidance

Prioritize standard QFT and particle-physics passages that explicitly connect symmetry actions to particle labels.

Prefer a small source set with stable terminology over broad representation-theory references or highly formal derivations.

## Anti-Patterns

Avoid:

- broad group-theory umbrellas that flatten the particle-physics reading,
- importing field equations or interaction-specific machinery without direct need,
- treating induced-representation proofs as mandatory for this first pass,
- and losing the connection to one-particle state classification.

## Evidence Guidance

Use evidence that shows:

- how authors name the Lorentz or Poincare action,
- which state-space objects are treated as representation carriers,
- how mass-shell and little-group labels are used in particle classification,
- and when boost parametrizations such as rapidity are treated as standard background.

If a candidate feels like a later derivation batch, flag it instead of forcing it into this first Stage 2 population.
