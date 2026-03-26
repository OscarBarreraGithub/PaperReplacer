# Source Notes: Mandelstam Variables and Crossing Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 867 triage, where `Mandelstam variables` appeared as a candidate-new-node item
- the already landed cross-sections batch, which promoted `qft.mandelstam_variables` but
  intentionally deferred the crossing and channel refinement

Observed overlap anchors already in the authored graph:

- `qft.mandelstam_variables`
- `qft.scattering_amplitude`

Batch-shaping decisions:

- reuse the existing `qft.mandelstam_variables` node exactly rather than restating it
- keep the batch centered on crossing and channel language, not on process examples
- avoid Regge, dispersive, or broad analytic-continuation branches for now
