# KnowledgeGraph

This repository is building a trustworthy prerequisite graph for HEP-TH topics.

Key docs:

- [idea.md](/Users/emmy/Documents/KnowledgeGraph/idea.md): ontology and semantic design
- [plan.md](/Users/emmy/Documents/KnowledgeGraph/plan.md): implementation workflow
- [population-plan.md](/Users/emmy/Documents/KnowledgeGraph/population-plan.md): broad QFT population roadmap
- [schwartz-coverage.md](/Users/emmy/Documents/KnowledgeGraph/schwartz-coverage.md): chapter-family coverage map for Schwartz QFT
- [batch-registry.yaml](/Users/emmy/Documents/KnowledgeGraph/batch-registry.yaml): active wave and namespace reservation tracker
- [CONTRIBUTING.md](/Users/emmy/Documents/KnowledgeGraph/CONTRIBUTING.md): branch and merge discipline

Reference PDFs and notes may live under [Ref material/](/Users/emmy/Documents/KnowledgeGraph/Ref%20material), but that folder is intentionally git-ignored and should be treated as local extraction support rather than canonical repository content.

## Local UI

There is a lightweight local interactive graph UI in [ui/](/Users/emmy/Documents/KnowledgeGraph/ui).

Run it with:

```bash
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/serve_ui.py --port 8766 --open
```

Then open [http://127.0.0.1:8766](http://127.0.0.1:8766).

The UI reads compiled batch data and lets you:

- rotate, pan, and zoom the graph
- click nodes for details
- switch batch and relation type
- view full-batch or focused neighborhood graphs

## Current State

The authored graph currently contains two pinch-singularities-oriented batches in [data/authored/](/Users/emmy/Documents/KnowledgeGraph/data/authored):

- `seed_pinch_singularities`: calibration fixture and regression slice
- `pinch_singularities_deep`: the richer production-oriented batch around the same canonical `qft.pinch_singularities` node

Important note:

- `seed_pinch_singularities` should be kept for calibration and tests, not treated as the main topic-facing graph.
- `pinch_singularities_deep` is the branch-ready local graph expansion that adds the deeper analytic neighborhood for the topic.

The first broad-population wave has also started:

- populated first-pass foundation batches:
  - `complex_analysis_for_qft`
  - `relativistic_kinematics`
  - `linear_algebra_operator_basics`
  - `distributions_boundary_values`

The second trunk-building wave is now also populated at first pass:

- `qm_operator_foundations`
- `variational_principles_and_classical_fields`
- `lorentz_poincare_representations`

The third broad-expansion wave is now active in parallel, centered on Schwartz QFT coverage:

- `free_fields_and_quantization`
- `correlators_propagators_lsz`
- `perturbation_wick_feynman_rules`
- `spinor_lorentz_dirac_foundations`
- `discrete_symmetries_and_cpt`
- `path_integral_and_generating_functionals`
- `regularization_renormalization_rg`
- `yang_mills_and_qcd_basics`
- `qcd_parton_model_and_factorization`
- `symmetry_breaking_and_standard_model`
- `anomalies_and_precision_sm`
- `effective_field_theory_and_scet`

Most of the Stage 3 Schwartz trunk now exists at first pass. The current authored union is available as the synthetic `all_authored` batch in the localhost UI and query tools.

The first Stage 4 Schwartz gap-closing wave is also now populated at first pass:

- `cross_sections_decay_rates_and_phase_space`
- `qed_tree_level_processes`
- `gauge_invariance_and_ward_brst`
- `effective_actions_and_background_fields`

The second Stage 5 Schwartz gap-closing wave is now also populated at first pass:

- `infrared_divergences_and_jets`
- `spinor_helicity_and_gluon_scattering`
- `flavor_ckm_pmns_and_precision_observables`

The Stage 6 follow-on wave is now also populated at first pass through:

- `scalar_qed`
- `nonperturbative_qcd_and_topology`
- `critical_phenomena_and_conformal_basics`
- `heavy_quark_effective_theory_refinement`

The Stage 7 refinement wave is now also populated at first pass through:

- `energy_momentum_tensor_and_conformal_currents`
- `optical_theorem_and_unitarity_cutting_basics`
- `mandelstam_variables_and_crossing_refinement`

The Stage 8 refinement wave is now also populated at first pass through:

- `soft_photon_theorem_and_low_energy_limits`
- `subtraction_scheme_and_landau_pole_refinement`

The Stage 9 refinement wave is now also populated at first pass through:

- `goldstone_theorem_and_equivalence_refinement`

The Stage 10 refinement wave is now also populated at first pass through:

- `chiral_symmetry_and_sigma_models`

The Stage 11 refinement wave is now also populated at first pass through:

- `spectral_and_mass_shell_refinement`

Current integration model:

- batches connect by reusing shared canonical node ids across neighborhoods
- the repo now has a synthetic global compiled view at `all_authored`
- the current UI and query tools are still batch-oriented
- the current validated authored union stands at `341` nodes, `500` dependencies, `319` partonomy edges, and `78` overlays
- the authored union currently validates cleanly with no warnings

Agent-generated proposal packs live under [data/batches/](/Users/emmy/Documents/KnowledgeGraph/data/batches) locally, but should normally stay off `main`.
