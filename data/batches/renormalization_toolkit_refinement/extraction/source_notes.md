# Source Notes: Renormalization Toolkit Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 862 triage, where `BPHZ theorem` was flagged as a remaining renormalization item
- page 865 triage, where `Pauli-Villars` and `Wilson-Fisher` pressure was routed to the
  regularization/RG branch
- page 867 triage, where `Pauli-Villars regularization` and `non-renormalizable theory`
  were still assigned to the existing RG batch
- page 869 triage, where `super-renormalizable theory` and `superficial degree of divergence`
  were again flagged as residual RG expansions

Observed overlap anchors already in the authored graph:

- `qft.regularization_renormalization_rg`
- `qft.ultraviolet_divergence`
- `qft.dimensional_regularization`
- `qft.renormalized_perturbation_theory`
- `qft.renormalization_scale`
- `qft.beta_function`

Batch-shaping decisions:

- keep the batch centered on reusable regulator, subtraction-toolkit, and divergence-
  classification language rather than on a broad EFT or critical-phenomena branch
- distinguish regulator methods from subtraction-scheme language already covered in the
  Stage 8 subtraction refinement
- use superficial degree of divergence as the local bridge into super- and
  nonrenormalizable-theory vocabulary
- keep effective charge and dimensional transmutation as compact RG payoffs rather than
  expanding into a larger phenomenology branch
