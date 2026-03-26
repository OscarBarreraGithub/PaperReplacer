# Schwartz Coverage Map

This document maps *Quantum Field Theory and the Standard Model* by Matthew D. Schwartz
onto the repository's batch-oriented prerequisite graph.

The graph remains topic-centered. Schwartz chapters are used here as a coverage checklist
and batching guide, not as ontology nodes.

## Coverage Principle

- One canonical topic node per concept.
- Multiple batches may touch the same Schwartz chapter family when they serve different
  prerequisite neighborhoods.
- Broad chapter themes should be decomposed into reusable graph batches, not mirrored
  chapter-for-chapter.

## Chapter Families

### Part I: Field theory

- Chapters 1-3
  - `relativistic_kinematics`
  - `variational_principles_and_classical_fields`
- Chapters 4-7
  - `cross_sections_decay_rates_and_phase_space`
  - `correlators_propagators_lsz`
  - `spectral_and_mass_shell_refinement`
  - `optical_theorem_and_unitarity_cutting_basics`
  - `scattering_spectral_residual_refinement`
  - `perturbation_wick_feynman_rules`

### Part II: Quantum electrodynamics

- Chapters 8-13
  - `free_fields_and_quantization`
  - `gauge_invariance_and_ward_brst`
  - `scalar_qed`
  - `spinor_lorentz_dirac_foundations`
  - `discrete_symmetries_and_cpt`
  - `qed_tree_level_processes`
- Chapter 14
  - `path_integral_and_generating_functionals`

### Part III: Renormalization

- Chapters 15-19
  - `regularization_renormalization_rg`
  - `subtraction_scheme_and_landau_pole_refinement`
  - `renormalization_toolkit_refinement`
- Chapters 20-24
  - `infrared_divergences_and_jets`
  - `effective_field_theory_and_scet`
  - `scet_mode_and_resummation_refinement`
  - `optical_theorem_and_unitarity_cutting_basics`
  - `scattering_spectral_residual_refinement`
  - `soft_photon_theorem_and_low_energy_limits`

### Part IV: The Standard Model

- Chapters 25-27
  - `yang_mills_and_qcd_basics`
  - `qcd_parton_model_and_factorization`
  - `spinor_helicity_and_gluon_scattering`
- Chapters 28-31
  - `symmetry_breaking_and_standard_model`
  - `goldstone_theorem_and_equivalence_refinement`
  - `chiral_symmetry_and_sigma_models`
  - `flavor_ckm_pmns_and_precision_observables`
  - `anomalies_and_precision_sm`

### Part V: Advanced topics

- Chapters 33-34
  - `effective_actions_and_background_fields`
- Chapter 35
  - `heavy_quark_effective_theory_refinement`
- Chapter 36
  - `effective_field_theory_and_scet`
  - `infrared_divergences_and_jets`
  - `scet_mode_and_resummation_refinement`

### Cross-Cutting Schwartz Follow-On Branches

- `nonperturbative_qcd_and_topology`
- `critical_phenomena_and_conformal_basics`
- `distributions_boundary_values`
- `energy_momentum_tensor_and_conformal_currents`
- `optical_theorem_and_unitarity_cutting_basics`
- `mandelstam_variables_and_crossing_refinement`
- `soft_photon_theorem_and_low_energy_limits`
- `subtraction_scheme_and_landau_pole_refinement`
- `goldstone_theorem_and_equivalence_refinement`
- `chiral_symmetry_and_sigma_models`
- `spectral_and_mass_shell_refinement`
- `dis_and_hadronic_factorization_refinement`
- `renormalization_toolkit_refinement`
- `scet_mode_and_resummation_refinement`
- `scattering_spectral_residual_refinement`
- `eft_matching_and_uv_completion_refinement`
- `naturalness_and_hierarchy_refinement`
- `schwinger_pair_production_refinement`
- `qed_loop_precision_refinement`
- `baryogenesis_and_sphaleron_refinement`
- `axion_strong_cp_peccei_quinn_refinement`
- `seesaw_mechanism_refinement`

### Appendices

- Appendix A
  - `spinor_lorentz_dirac_foundations`
- Appendix B
  - `renormalization_toolkit_refinement`

## Population Order

The preferred order is:

1. Finish the core trunk needed for nearly every later chapter.
2. Add the first reusable QED and renormalization branches.
3. Add non-Abelian gauge theory, QCD, and symmetry breaking.
4. Add advanced EFT, SCET, and background-field material.

## Immediate Expansion Trunk

The next broad batches should be:

- `free_fields_and_quantization`
- `correlators_propagators_lsz`
- `perturbation_wick_feynman_rules`
- `path_integral_and_generating_functionals`
- `regularization_renormalization_rg`
- `yang_mills_and_qcd_basics`
- `symmetry_breaking_and_standard_model`
- `effective_field_theory_and_scet`

## Connectivity Rule

The final graph should be globally connected through shared canonical node ids.

Examples:

- `relativity.lorentz_transformation` should connect to spinor and representation batches.
- `classical_fields.lagrangian_density` should connect to free-field, perturbation, and
  path-integral batches.
- `qft.propagator_singularities` should connect the analytic-structure branch back to
  correlator, LSZ, and path-integral neighborhoods.
- renormalization and RG nodes should connect QED, Yang-Mills, EFT, and SCET branches.
