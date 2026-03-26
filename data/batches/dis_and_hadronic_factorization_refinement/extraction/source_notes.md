# Source Notes: DIS and Hadronic Factorization Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 862 triage, where `Bjorken x` and `Bjorken scaling` were flagged as parton/factorization
  expansion items
- page 864 triage, where `Drell-Yan`, `e- p+ -> e- X`, and `e+e- -> hadrons` were routed into
  the same hadronic-factorization neighborhood
- page 867 triage, where `Mellin moment` was flagged as an expansion of the existing
  parton-model/factorization batch
- page 870 triage, where `twist` was again flagged as a remaining hadronic-factorization item

Observed overlap anchors already in the authored graph:

- `qcd.parton_model_and_factorization`
- `qcd.parton_distribution_function`
- `qcd.factorization_theorem`
- `qcd.collinear_factorization`
- `qcd.hard_scattering_coefficient`
- `qft.cross_section`

Batch-shaping decisions:

- keep the batch centered on reusable hadronic-factorization structure rather than on a long
  list of process exemplars
- use DIS and Drell-Yan as the two concrete process branches that justify the kinematic and
  factorization refinements
- treat Mellin moments and twist as structure-level refinements of the same hadronic branch
  rather than as isolated formal nodes
- leave threshold-region, event-shape, and SCET-mode language for the later SCET/resummation
  queue
