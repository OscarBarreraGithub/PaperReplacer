# Source Notes: Baryogenesis and Sphaleron Refinement

Primary Schwartz coverage pressure for this batch comes from:

- page 862 triage, where `baryogenesis` remained a direct candidate-new-node item and
  `B - L` was still routed only to coarse Standard-Model expansion
- page 866 triage, where `lepton number` remained a Standard-Model expansion item
- page 869 triage, where `Sakharov conditions` and `Sphaleron` remained direct
  candidate-new-node items

Observed overlap anchors already in the authored graph:

- `sm.symmetry_breaking_and_standard_model`
- `classical_fields.noether_theorem`
- `sm.ewbreak.electroweak_symmetry_breaking`

Batch-shaping decisions:

- refine the existing `sm.symmetry_breaking_and_standard_model` root instead of opening a
  new cosmology namespace for a single late-SM tail cluster
- treat baryon/lepton-number and `B - L` language as the charge-symmetry side of the batch
- keep `sm.baryogenesis_sakharov_conditions` under the `sm.baryogenesis` branch so the
  criteria are attached to the phenomenon they motivate
- keep `sm.sphaleron` attached to electroweak symmetry breaking rather than treating it as
  an isolated nonperturbative curiosity
- leave `axion` and `technicolor` for a later BSM-tail decision because they do not fit as
  cleanly into the same charge-symmetry and sphaleron cluster
