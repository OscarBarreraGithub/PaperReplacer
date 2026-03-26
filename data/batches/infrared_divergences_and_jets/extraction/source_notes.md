# Source Notes: Infrared Divergences and Jets

Primary coverage pressure for this batch comes from the Schwartz index triage on pages 866,
869, and 870, especially:

- `inclusive observable`
- `soft interaction`
- `Sudakov` subentries
- `thrust`
- `Kinoshita-Lee-Nauenberg theorem`
- `Bloch-Nordsieck theorem`
- `threshold region`

Observed overlap anchors already in the authored graph:

- `qft.cross_section`
- `qcd.factorization_theorem`
- `qcd.collinear_factorization`
- `eft.soft_collinear_effective_theory`
- `eft.large_logarithm_resummation`
- `eft.jet_function`
- `eft.soft_function`

Batch-shaping decisions:

- keep the theorem branch reusable across gauge-theory scattering rather than QED-only
- let `jet` and `thrust` be the first reusable event-shape foothold without adding a full
  taxonomy
- reuse existing factorization and SCET nodes rather than recreating them under an infrared
  namespace
- keep threshold and soft-photon refinements for later followup slices unless they are needed
  to connect the current graph
