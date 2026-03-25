# Review: Autonomous Proposal Pass for `seed_pinch_singularities`

## Outcome

The autonomous proposal pass is structurally successful.

- all proposal files are schema-valid,
- the node set stayed narrow,
- no forbidden broad umbrella nodes were introduced,
- and the pass respected the batch's literature-facing scope.

## Comparison to the Calibration Slice

The proposed node set exactly matches the current hand-authored calibration slice:

- `complex_analysis.contour_deformation`
- `complex_analysis.poles_vs_branch_points`
- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.pinch_singularities`

The dependency set is close, but not identical.

### Matching proposals

The autonomous pass reproduced these dependencies:

- `contour_deformation -> pinch_singularities` for `requires_for_use`
- `feynman_i_epsilon_prescription -> propagator_singularities` for `requires_for_use`
- `propagator_singularities -> pinch_singularities` for both `requires_for_recognize` and `requires_for_use`

### Meaningful divergence

The main divergence is the treatment of `poles_vs_branch_points`.

Current calibration slice:

- `poles_vs_branch_points -> propagator_singularities` for `requires_for_recognize`
- `poles_vs_branch_points -> pinch_singularities` for `requires_for_use`

Autonomous proposal:

- `poles_vs_branch_points -> pinch_singularities` for `requires_for_recognize`
- `poles_vs_branch_points -> pinch_singularities` for `requires_for_use`

This is not obviously wrong. It reflects a slightly more direct literature-reading interpretation of the target topic.

## Overlay Proposal

The autonomous pass also proposed one overlay:

- `assumed_background(pinch_singularities, contour_deformation)` in the `hep_th_grad / amplitudes / paper` context

This is consistent with the batch brief and source notes. It was not present in the hand-authored calibration slice, so it is a genuine addition rather than a copy.

## Recommendation

Recommendation: treat this autonomous pass as a successful workflow rehearsal, but do not automatically replace the calibration slice with it yet.

Suggested disposition:

- keep the current hand-authored authored slice as the calibration fixture,
- keep the autonomous proposal pack as the first staged agent-generated comparison point,
- and decide explicitly whether the `poles_vs_branch_points` recognize edge should terminate at `propagator_singularities` or directly at `pinch_singularities`.

## What This Demonstrates

This pass shows that the prompts and contract are good enough to generate a narrow, plausible proposal pack without broad ontology drift.

The remaining question is no longer "can the agent stay on topic?" but "how should subtle epistemic choices be adjudicated when more than one sharp representation is plausible?"
