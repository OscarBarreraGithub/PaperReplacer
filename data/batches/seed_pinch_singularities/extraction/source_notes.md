# Seed Notes: Pinch Singularities

These notes are not canonical graph facts. They are batch-specific extraction context for the autonomous proposer.

## Intended Reading of the Topic

For this batch, `pinch singularities` should be understood in the standard literature-facing sense:

- a contour integral cannot be deformed away from singularities because singularities approach from competing sides and trap the contour,
- with the immediate use-case being paper parsing and following standard analytic arguments,
- not full derivation of Landau equations or a complete theory of singularity surfaces.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize what a pinch singularity is when it appears in a paper,
- and follow a standard argument about why a contour is pinched.

The batch is not trying to capture:

- all of QFT,
- a complete analytic-structure ontology,
- or a derivation-level theory of singularities.

## Domain Hints

The most likely high-value node candidates are:

- contour deformation
- poles versus branch points
- Feynman `i epsilon` prescription
- propagator singularities
- pinch singularities

Likely high-value dependency patterns:

- method-level analytic prerequisites into `pinch singularities`
- propagator-level QFT prerequisites into `pinch singularities`
- literature-facing recognition edges that are weaker than full derivation edges

## Anti-Patterns

Avoid:

- broad prerequisite nodes like `QFT`, `complex analysis`, or `analytic structure` unless the dependency cannot be expressed more sharply,
- importing `Landau singularity conditions` into this first slice,
- importing renormalization, LSZ, or general scattering theory without direct evidence,
- and treating sociological assumptions as intrinsic prerequisites.

## Evidence Guidance

When proposing claims, prefer evidence of these forms:

- standard paper-language dependence such as contour-trapping arguments,
- explicit reliance on pole placement from the Feynman prescription,
- distinctions between pole and branch structure when reading the singularity discussion.

If a claim feels true only at the level of a much broader research program, flag it instead of asserting it for this batch.
