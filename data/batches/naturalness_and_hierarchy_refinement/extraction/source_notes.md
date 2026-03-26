# Source Notes: Naturalness and Hierarchy Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 867 triage, where `naturalness`, `technical naturalness`, and `Planck scale` were
  still only routed into the coarse Standard-Model symmetry-breaking batch
- page 864 triage, where `fine-tuning` remained a direct candidate-new-node item
- page 866 triage, where `mass naturalness` and `Lee-Quigg-Thacker bound` were still
  unresolved expansion items
- page 862 triage, where `Lee-Quigg-Thacker bound` also appeared as a direct candidate-new-node
  item

Observed overlap anchors already in the authored graph:

- `sm.symmetry_breaking_and_standard_model`
- `sm.higgs.higgs_mechanism`
- `sm.ewbreak.goldstone_boson_equivalence_theorem`
- `eft.ultraviolet_sensitivity`
- `eft.ultraviolet_completion`
- `qft.partial_wave_unitarity_bound`

Batch-shaping decisions:

- refine the existing `sm.symmetry_breaking_and_standard_model` root instead of creating a
  second hierarchy-problem umbrella
- use `sm.mass_naturalness` as the Standard-Model-facing node that absorbs the generic
  `naturalness` and `technical naturalness` pressure from Schwartz
- keep `qft.fine_tuning` and `qft.planck_scale` as support nodes under the naturalness branch
  rather than building a separate cosmology or gravity subtree
- attach `sm.lee_quigg_thacker_bound` directly to the newly landed
  `qft.partial_wave_unitarity_bound` and the existing Goldstone-boson equivalence theorem so
  it lands as a genuine electroweak unitarity leaf
- leave technicolor, axion, baryogenesis, and other broader BSM directions for later
  tail cleanup
