# Source Notes: Distributions and Boundary Values

Primary Schwartz and authored-graph pressure for this batch comes from:

- page 866 triage, where `i epsilon prescription` is already covered but not decomposed into
  local boundary-value language
- the existing `qft.distributional_boundary_values` node in the pinch-singularities anchor,
  which currently has no small standalone support batch
- the old decomposition blocker recorded in the batch brief and registry

Observed overlap anchors already in the authored graph:

- `qft.distributional_boundary_values`
- `qft.feynman_i_epsilon_prescription`
- `complex_analysis.poles_vs_branch_points`
- `qft.analytic_continuation_in_kinematic_invariants`

Batch-shaping decisions:

- reuse `qft.distributional_boundary_values` as the hub instead of creating a second
  boundary-values anchor
- add only one local notation shim, `qft.boundary_values.plus_minus_i0_limits`
- keep the decomposition minimal: plus-or-minus `i0`, principal value, and delta-function
  pieces
- avoid broad discontinuity, absorptive-part, or second `i epsilon` nodes
