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
- the analytic duplicate-definition cleanup pass is now complete and the current authored
  union validates without warnings

## 4. Next Followups

After the landed Stage 11 refinement wave, the next good queue shifts to the remaining
coverage decisions and smaller promotion passes such as:

- `dis_and_hadronic_factorization_refinement`
- `scet_mode_and_resummation_refinement`
- `renormalization_toolkit_refinement`
- `Schwinger proper-time` / `Schwinger parameter` should now be treated as already covered
  by `effective_actions_and_background_fields`, not as a separate batch target
- `Schwinger pair production` remains a possible later background-field refinement if the
  remaining Schwartz tail still justifies it after the theorem-level cleanup pass

## 5. Node-Creation Discipline

Do **not** create all `candidate_new_node` entries immediately.

Promote a candidate into a canonical node only if:

- it appears in more than one page/batch context, or
- it is clearly central to a high-yield batch, or
- it changes actual prerequisite answers

Good examples likely to promote soon:

- `qft.t_matrix`
- `qft.unstable_particles`
- `qft.partial_wave_unitarity_bound`
- `qft.feynman_tree_theorem`
- `qcd.twist`
- `qft.bphz_renormalization`
- `qft.schwinger_pair_production`
- `qed.uehling_potential`
- `sm.pmns_matrix`

Examples to delay unless needed:

- highly specialized named bounds
- historical labels
- narrowly contextual process names that can live inside example batches

## 6. Recommended Immediate Action

The best next implementation step is now:

1. launch one or two tightly scoped theorem-level refinements around:
   - DIS / hadronic-factorization residuals such as `Bjorken x`, `Drell-Yan`, `Mellin
     moment`, and `twist`
   - SCET / large-log / mode-structure residuals such as Glauber or eikonal language where
     the current EFT/IR trunk is still too coarse
2. keep `Schwinger proper-time` / `Schwinger parameter` marked as covered by the existing
   effective-actions branch unless query behavior shows a real missing cross-link
3. continue SCET-mode / resummation and renormalization-toolkit expansions, promoting only
   the most repeated residual `candidate_new_node` items into
   similarly small batches

This ordering keeps Schwartz reduction moving while the remaining backlog shifts from broad
topic gaps to a mix of cleanup and narrow theorem-level promotions.
