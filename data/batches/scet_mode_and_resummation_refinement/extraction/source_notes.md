# Source Notes: SCET Mode and Resummation Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 863 triage, where `collinear interaction` was still routed only to the coarse EFT/SCET
  batch
- page 864 triage, where `eikonal` factor / identity / limit language remained attached only
  at the coarse SCET level
- page 865 triage, where `Glauber mode` and `heavy jet mass` were still unresolved SCET-side
  expansion items
- page 869 triage, where `Sudakov` / `double logarithm` / `factor` / `peak` were treated as
  residual large-log language already covered only coarsely by the existing resummation node
- page 870 triage, where `Wilson coefficient` and `ultraviolet sensitivity` remained queued
  as missing EFT/SCET refinements

Observed overlap anchors already in the authored graph:

- `eft.soft_collinear_effective_theory`
- `eft.matching`
- `eft.large_logarithm_resummation`
- `eft.mode_scaling`
- `eft.collinear_mode`
- `eft.soft_mode`
- `eft.hard_function`
- `eft.jet_function`
- `eft.soft_function`
- `qft.eikonal_soft_factor`
- `qft.jet`
- `qft.thrust`

Batch-shaping decisions:

- refine the existing `eft.soft_collinear_effective_theory` root instead of creating a second
  SCET topic anchor
- treat `Wilson coefficient` as generic EFT short-distance coefficient language rather than
  as a duplicate of the more process-facing `hard function` or `hard scattering coefficient`
- use `ultraviolet sensitivity` as the narrow EFT-side motivation node that explains why
  those coefficients encode short-distance information
- promote `Glauber mode` and `collinear interaction` as the smallest reusable missing mode
  refinements from the SCET chapter
- use `heavy jet mass` as the single new event-shape payoff leaf because it is repeated in
  the Schwartz SCET chapter and sits cleanly next to the existing `qft.thrust` node
- leave generic `form factor` and `threshold region` for later overlap-aware follow-on work
  so this batch stays centered on SCET mode structure and resummation
