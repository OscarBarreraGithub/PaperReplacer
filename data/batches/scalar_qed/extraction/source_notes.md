# Source Notes: Scalar QED

Primary coverage pressure for this batch comes from the Schwartz index triage on page 869,
especially:

- `scalar QED`
- `seagull vertex`

Observed overlap anchors already in the authored graph:

- `qft.free_scalar_field`
- `qft.free_vector_field`
- `qft.gauge_invariance`
- `qft.covariant_derivative`
- `qft.ward_takahashi_identity`
- `qft.feynman_rules`
- `qed.compton_scattering`

Batch-shaping decisions:

- keep scalar QED as a charged-scalar gauge-theory branch, not a duplicate generic QED batch
- keep only one process-facing leaf so the seagull vertex has a visible failure mode
- reuse the generic gauge and covariant-derivative nodes instead of rebuilding Abelian gauge
  basics from scratch
- keep renormalization and Higgs-sector spillover for later waves
