# Source Notes: EFT Matching and UV Completion Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 862 triage, where `4-Fermi theory` was already routed into the EFT neighborhood but
  still under a spelling variant
- page 865 triage, where `4-Fermi theory` again reappeared as an EFT-tail item
- page 866 triage, where `integrating out` was still only attached to the coarse EFT batch
- page 870 triage, where `4-Fermi theory` and `ultraviolet completion` remained unresolved
  generic EFT expansion items

Observed overlap anchors already in the authored graph:

- `eft.effective_field_theory`
- `eft.scale_separation`
- `eft.higher_dimensional_operator`
- `eft.matching`
- `eft.wilson_coefficient`
- `eft.ultraviolet_sensitivity`

Batch-shaping decisions:

- refine the existing `eft.effective_field_theory` root instead of creating a second generic
  EFT topic anchor
- canonicalize the spelling as `eft.four_fermi_theory` because that is the queue wording in
  the later triage pages and the current checkpoint docs
- keep `integrating out` distinct from, but adjacent to, `matching`: integrating out is the
  conceptual low-energy construction step, while matching is the coefficient-fixing step
- use `ultraviolet completion` as the full-theory-side concept that explains what the EFT is
  an approximation to, without reopening a broader UV-model catalog
- keep naturalness, hierarchy, and technical-naturalness language for a later dedicated pass
