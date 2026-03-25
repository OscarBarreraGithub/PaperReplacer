# Extraction Report: Seed Pinch Singularities

## Summary

This pass stayed narrow and literature-facing. The proposal set focuses on the smallest defensible slice needed to recognize and use `pinch singularities` in amplitudes papers.

## Main Proposal Choices

- Proposed 5 nodes only.
- Kept the node set to contour deformation, poles versus branch points, Feynman `i epsilon` prescription, propagator singularities, and pinch singularities.
- Split recognition and use where it sharpened the dependency story, especially for `poles vs branch points` and `propagator singularities`.
- Added one assumed-background overlay for contour deformation in the amplitudes reading context.
- Left `partonomy` empty because this seed slice did not force a defensible decomposition claim.

## Evidence Style

All dependency proposals are grounded in the batch extraction notes rather than imported broad background. Each dependency includes:

- a rationale,
- a concrete failure mode if the prerequisite is absent,
- evidence,
- and a confidence score.

## Ambiguities

- The batch notes suggest that `poles vs branch points` is useful for both recognition and use. I proposed both edges, but the use edge is weaker than the contour and propagator edges.
- I did not promote `Landau singularity conditions`, `LSZ`, renormalization, or generic `QFT` because the batch notes explicitly warned against broadening the first slice.
- I did not propose any `part_of` edges because no decomposition claim was strong enough to survive this first pass.

## Follow-Up

If this proposal is accepted, the next useful step is to run the same extraction workflow on a second, slightly deeper seed slice or to ask for a synthetic query fixture that exercises more overlay and partonomy behavior.
