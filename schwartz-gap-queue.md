# Schwartz Gap Queue

This document turns the full Schwartz index triage into the next concrete batch queue.

Source inputs:

- [schwartz_index_summary.md](/Users/emmy/Documents/KnowledgeGraph/data/generated/extracted/schwartz_index_summary.md)
- [schwartz_index_summary.json](/Users/emmy/Documents/KnowledgeGraph/data/generated/extracted/schwartz_index_summary.json)
- per-page triage reports under [data/generated/index_triage](/Users/emmy/Documents/KnowledgeGraph/data/generated/index_triage)

## 1. Goal

The next step is not to add 254 isolated terms one by one.

The next step is to reduce the index backlog into a small number of high-yield batch
families that:

- absorb many `candidate_batch_expansion` items at once
- promote only the most reusable `candidate_new_node` items
- keep the graph connected to the existing authored trunk

## 2. Current Backlog Size

From the full 9-page Schwartz index sweep:

- `covered_existing`: 113
- `candidate_batch_expansion`: 153
- `candidate_new_node`: 101
- `skip_non_ontology`: 51

This means the immediate task is primarily **batch expansion**, not blind node creation.

## 3. Highest-Yield Next Wave

These are the best next batches because they absorb many index misses at once and connect
directly to the current graph.

### A. `cross_sections_decay_rates_and_phase_space`

Why next:

- repeated index pressure from cross sections, decay rates, scattering frames, narrow-width
  approximation, Lorentz-invariant phase space, tree-level process formulas
- closes a major hole between LSZ/perturbation and phenomenology-facing calculations

Likely absorbs:

- cross section
- decay rate
- Lorentz-invariant phase space
- Mandelstam variables
- Breit-Wigner distribution
- narrow-width approximation
- partial-wave language
- Bhabha / Moller / Compton / Rutherford / Thomson-style example process hooks

### B. `qed_tree_level_processes`

Why next:

- many index entries are concrete QED scattering exemplars rather than brand-new ontology
- these are important for Schwartz coverage and collider intuition

Likely absorbs:

- Bhabha scattering
- Moller scattering
- Compton scattering
- e+e- -> mu+mu-
- light-by-light scattering
- Klein-Nishina / related formula references where ontologically justified

### C. `gauge_invariance_and_ward_brst`

Why next:

- gauge-fixing families, BRST, Faddeev-Popov, Ward identities, Slavnov-Taylor style
  structure remain too coarse
- this connects free fields, Yang-Mills, path integrals, and anomalies

Likely absorbs:

- BRST invariance
- BRST cohomology
- Faddeev-Popov
- gauge choices and gauge-fixing language
- Ward identities / Ward-Takahashi
- Gauss's law in gauge-theory context

### D. `effective_actions_and_background_fields`

Why next:

- explicit pressure from the index for 1PI effective action, effective action, background
  field method, effective potential
- closes the current gap between path integrals and later-field-theory applications

Likely absorbs:

- 1PI effective action
- effective action
- background field method
- effective potential
- Schwinger proper-time / Schwinger parameter where appropriate

### E. `infrared_divergences_and_jets`

Why next:

- strong index pressure from KLN, Bloch-Nordsieck, soft/collinear structure, inclusive
  observables, jet language, event-shape-related entries
- ties together QCD, EFT/SCET, and cross-section physics

Likely absorbs:

- infrared divergence
- soft divergence
- collinear divergence
- KLN theorem
- Bloch-Nordsieck theorem
- inclusive observable
- jet / heavy-jet-mass-related refinements

### F. `spinor_helicity_and_gluon_scattering`

Why next:

- Schwartz index directly pressures MHV, color-ordered amplitudes, color-stripped
  amplitudes, Schouten identity, and gg -> gg style scattering
- current graph does not yet expose this modern amplitudes branch cleanly

Likely absorbs:

- MHV amplitudes
- color-ordered partial amplitudes
- color-stripped amplitudes
- Schouten identity
- gluon tree scattering

Checkpoint note:

- the Stage 5 follow-on wave now exists at first pass through:
  - `infrared_divergences_and_jets`
  - `spinor_helicity_and_gluon_scattering`
  - `flavor_ckm_pmns_and_precision_observables`
- the Stage 6 follow-on wave is now populated at first pass through:
  - `scalar_qed`
  - `nonperturbative_qcd_and_topology`
  - `critical_phenomena_and_conformal_basics`
  - `heavy_quark_effective_theory_refinement`
- the old Stage 1 blocker has now been integrated as:
  - `distributions_boundary_values`
- the Stage 7 refinement wave now exists at first pass through:
  - `energy_momentum_tensor_and_conformal_currents`
  - `optical_theorem_and_unitarity_cutting_basics`
  - `mandelstam_variables_and_crossing_refinement`
- the Stage 8 refinement wave now exists at first pass through:
  - `soft_photon_theorem_and_low_energy_limits`
  - `subtraction_scheme_and_landau_pole_refinement`
- the Stage 9 refinement wave now exists at first pass through:
  - `goldstone_theorem_and_equivalence_refinement`
- the Stage 10 refinement wave now exists at first pass through:
  - `chiral_symmetry_and_sigma_models`
- the Stage 11 refinement wave now exists at first pass through:
  - `spectral_and_mass_shell_refinement`
- the Stage 12 refinement wave now exists at first pass through:
  - `dis_and_hadronic_factorization_refinement`
- the Stage 13 refinement wave now exists at first pass through:
  - `renormalization_toolkit_refinement`
- the Stage 14 refinement wave now exists at first pass through:
  - `scet_mode_and_resummation_refinement`
- the Stage 15 refinement wave now exists at first pass through:
  - `scattering_spectral_residual_refinement`
- the Stage 16 refinement wave now exists at first pass through:
  - `eft_matching_and_uv_completion_refinement`
- the Stage 17 refinement wave now exists at first pass through:
  - `naturalness_and_hierarchy_refinement`
- the Stage 18 refinement wave now exists at first pass through:
  - `schwinger_pair_production_refinement`
- the Stage 19 refinement wave now exists at first pass through:
  - `qed_loop_precision_refinement`
- the Stage 20 refinement wave now exists at first pass through:
  - `baryogenesis_and_sphaleron_refinement`
- the Stage 21 refinement wave now exists at first pass through:
  - `axion_strong_cp_peccei_quinn_refinement`
- the Stage 22 refinement wave now exists at first pass through:
  - `seesaw_mechanism_refinement`
- the analytic duplicate-definition cleanup pass is now complete and the current authored
  union validates without warnings

## 4. Next Followups

After the landed Stage 22 refinement wave, the substantive residue is now small enough that
the remaining work is best handled as explicit deferral rather than further automatic
canonical promotion.

The remaining residue is:

- `qft.resonance_pole` should stay explicitly deferred for now: a focused query check on
  the landed unstable-particle branch shows `qft.breit_wigner_distribution` and
  `qft.narrow_width_approximation` already sit on a coherent `qft.unstable_particles`
  frontier, so a standalone resonance-pole node is not yet changing prerequisite answers
- `sm.technicolor` and `sm.grand_unification` should stay explicitly deferred unless a
  later overlap-aware batch gives them a cleaner home than the current symmetry-breaking,
  chiral, naturalness, and flavor neighborhoods
- generic `form factor` and `threshold region` should stay deferred until overlap with the
  HQET, hadronic-factorization, and scattering neighborhoods is resolved more explicitly
- isolated formal-QFT tail items such as `qft.stability`, `qft.tachyon`, and
  `qft.seiberg_duality` should stay explicitly deferred unless the advanced-topic residue
  later demands a narrower ontology treatment
- `Schwinger proper-time` / `Schwinger parameter` should now be treated as already covered
  by `effective_actions_and_background_fields`, not as a separate batch target

In other words, after Stage 22 there is no further clearly justified canonical batch
remaining from the substantive Schwartz residue; the rest is now an explicit deferral list.

## 5. Node-Creation Discipline

Do **not** create all `candidate_new_node` entries immediately.

Promote a candidate into a canonical node only if:

- it appears in more than one page/batch context, or
- it is clearly central to a high-yield batch, or
- it changes actual prerequisite answers

There are currently no remaining residual items that clearly clear the promotion bar
without reopening broad overlap-sensitive branches.

Examples to delay unless needed:

- `sm.technicolor`
- `sm.grand_unification`
- generic `form factor`
- `threshold region` until its overlap home is clearer
- `qft.resonance_pole` unless later query behavior proves the current unstable-particle
  branch insufficient
- `qft.stability`
- `qft.tachyon`
- `qft.seiberg_duality`
- highly specialized named bounds
- historical labels
- narrowly contextual process names that can live inside example batches

## 6. Recommended Immediate Action

The best next implementation step is now:

1. treat the canonical-batch side of the substantive Schwartz backlog as exhausted and
   carry the remaining residue only as explicit deferrals
2. keep `sm.technicolor`, `sm.grand_unification`, generic `form factor`,
   `threshold region`, and the isolated formal-QFT tail explicitly deferred unless a later
   overlap-aware query pass shows a real missing branch
3. reopen `qft.resonance_pole` only if future query behavior shows the current
   unstable-particle / Breit-Wigner / narrow-width branch is no longer sufficient

This ordering keeps Schwartz reduction honest: stop canonical promotion once the remaining
tail no longer clears the bar, and preserve the residue as explicit, reviewable deferrals.
