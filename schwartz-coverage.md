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
  - `old_fashioned_perturbation_and_scattering`
  - `cross_sections_decay_rates_and_phase_space`
  - `correlators_propagators_lsz`
  - `spectral_and_mass_shell_refinement`
  - `perturbation_wick_feynman_rules`

### Part II: Quantum electrodynamics

- Chapters 8-13
  - `free_fields_and_quantization`
  - `gauge_invariance_and_ward_identities`
  - `scalar_qed`
  - `spinor_lorentz_dirac_foundations`
  - `discrete_symmetries_and_cpt`
  - `spin_statistics_microcausality`
  - `qed_tree_level_processes`
- Chapter 14
  - `path_integral_and_generating_functionals`

### Part III: Renormalization

- Chapters 15-19
  - `regularization_and_one_loop_renormalization`
  - `renormalized_perturbation_theory`
  - `subtraction_scheme_and_landau_pole_refinement`
- Chapters 20-24
  - `infrared_divergences_and_jets`
  - `renormalizability_and_effective_operators`
  - `renormalization_group`
  - `unitarity_optical_theorem_spectral_polology`
  - `soft_photon_theorem_and_low_energy_limits`

### Part IV: The Standard Model

- Chapters 25-27
  - `yang_mills_and_nonabelian_gauge_theory`
  - `quantum_yang_mills_and_running_coupling`
  - `spinor_helicity_and_gluon_scattering`
- Chapters 28-31
  - `spontaneous_symmetry_breaking_and_higgs`
  - `goldstone_theorem_and_equivalence_refinement`
  - `chiral_symmetry_and_sigma_models`
  - `electroweak_interactions`
  - `anomalies`
  - `flavor_ckm_pmns_and_precision_observables`
  - `precision_standard_model_constraints`
  - `qcd_parton_model_and_factorization`

### Part V: Advanced topics

- Chapters 33-34
  - `effective_actions_and_background_fields`
- Chapter 35
  - `heavy_quark_effective_theory_refinement`
- Chapter 36
  - `jets_and_scet`

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

### Appendices

- Appendix A
  - `conventions_and_dirac_algebra`
- Appendix B
  - `regularization_toolkit`

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
