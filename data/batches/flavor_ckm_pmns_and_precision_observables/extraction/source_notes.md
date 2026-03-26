# Source Notes: Flavor, CKM/PMNS, and Precision Observables

Primary coverage pressure for this batch comes from the Schwartz index triage on pages 866,
867, and 870, especially:

- `PMNS matrix`
- `Jarlskog invariant`
- `unitarity triangle`
- `Wolfenstein parametrization`
- neutrino and mass-related subentries
- flavor and precision-observable language tied to weak mixing

Observed overlap anchors already in the authored graph:

- `sm.ewbreak.fermion_mass_generation`
- `sm.ewbreak.electroweak_mixing_angle`
- `sm.precision.electroweak_precision_observable`
- `sm.precision.effective_weak_mixing_angle`

Batch-shaping decisions:

- create a reusable `flavor mixing` node rather than separate disconnected CKM and PMNS
  islands
- keep the precision branch light and explicitly reuse the existing anomalies-and-precision
  nodes
- include neutrino mass and oscillation only as the minimum PMNS-facing branch needed for the
  Schwartz backlog
- defer richer flavor phenomenology and seesaw model-building to later waves
