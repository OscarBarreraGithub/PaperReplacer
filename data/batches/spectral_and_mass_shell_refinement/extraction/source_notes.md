# Source Notes: Spectral and Mass-Shell Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 862 triage, where `advanced propagator` was flagged as a correlator/progagator
  expansion item
- page 866 triage, where `Kallen-Lehmann representation` and `Lippmann-Schwinger
  equation` were flagged as candidate-batch-expansion items
- page 867 and the residual-queue review, which still point to off-shell / on-shell and
  related spectral/mass-shell language as undercovered in the current correlator trunk

Observed overlap anchors already in the authored graph:

- `qft.correlators_propagators_lsz`
- `qft.feynman_i_epsilon_prescription`
- `qft.propagator_singularities`
- `qft.feynman_propagator`
- `qft.asymptotic_one_particle_state`
- `qft.lsz_reduction_formula`

Batch-shaping decisions:

- keep the batch attached to the existing correlator/propagator/LSZ branch rather than
  broadening into a full S-matrix formalism
- use on-shell/off-shell language as the local bridge from propagator singularities into
  spectral and scattering-adjacent vocabulary
- include the advanced propagator and Kallen-Lehmann representation as propagator-facing
  refinements, not as separate analytic-structure umbrellas
- leave unstable particles, resonance line shapes, and full T-matrix formalism for later
  overlap-aware follow-on work
