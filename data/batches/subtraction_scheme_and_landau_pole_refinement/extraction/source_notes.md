# Source Notes: Subtraction Scheme and Landau Pole Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 869 triage, where `subtraction point` / `subtraction scheme` were flagged as
  candidate-new-node items
- page 866 triage, where `Landau pole` was flagged as a candidate-new-node item

Observed overlap anchors already in the authored graph:

- `qft.renormalized_perturbation_theory`
- `qft.renormalization_scale`
- `qft.beta_function`
- `qft.renormalization_group_equation`

Batch-shaping decisions:

- keep subtraction-scheme language in the renormalization branch, not in the regulator
  branch
- add one running-coupling bridge node so the Landau pole has a local RG object to diverge
- keep minimal subtraction as the single concrete scheme leaf rather than opening a broad
  scheme catalog
