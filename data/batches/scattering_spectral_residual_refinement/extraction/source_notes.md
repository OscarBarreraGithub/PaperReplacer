# Source Notes: Scattering Spectral Residual Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 864 triage, where `Feynman tree theorem` remained a direct candidate-new-node item
- page 867 triage, where `partial wave` and `narrow-width approximation` continued to put
  pressure on the scattering-observable branch
- page 870 triage, where `unstable particles`, `T-matrix`, and `partial-wave unitarity
  bound` remained unresolved residual items
- the extracted Schwartz index entries around pages 452-477 and 461-466, where unitarity,
  optical-theorem, unstable-particle, and partial-wave language cluster tightly together

Observed overlap anchors already in the authored graph:

- `qft.optical_theorem_and_unitarity_cutting_basics`
- `qft.scattering_amplitude`
- `qft.s_matrix_unitarity`
- `qft.optical_theorem`
- `qft.unitarity_cutting_rules`
- `qft.on_shell_intermediate_state`
- `qft.lippmann_schwinger_equation`
- `qft.feynman_propagator`
- `qft.partial_wave_expansion`
- `qft.decay_rate`
- `qft.breit_wigner_distribution`
- `qft.narrow_width_approximation`

Batch-shaping decisions:

- refine the existing `qft.optical_theorem_and_unitarity_cutting_basics` root instead of
  creating a second scattering-unitarity topic anchor
- use `qft.t_matrix` as the operator-notation bridge connecting amplitudes, LSZ-adjacent
  scattering-state language, and unitarity formulas
- use `qft.unstable_particles` as the conceptual parent that makes the existing
  Breit-Wigner and narrow-width nodes answerable as a coherent neighborhood
- promote `qft.partial_wave_unitarity_bound` as the theorem-level refinement of the already
  existing `qft.partial_wave_expansion` node
- keep `qft.feynman_tree_theorem` narrowly attached to the existing cutting-rule and
  on-shell-intermediate-state branch instead of reopening a larger loop-tree duality or
  analytic-structure program
