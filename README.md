# KnowledgeGraph

This repository is building a trustworthy prerequisite graph for HEP-TH topics.

Key docs:

- [idea.md](/Users/emmy/Documents/KnowledgeGraph/idea.md): ontology and semantic design
- [plan.md](/Users/emmy/Documents/KnowledgeGraph/plan.md): implementation workflow
- [population-plan.md](/Users/emmy/Documents/KnowledgeGraph/population-plan.md): broad QFT population roadmap
- [schwartz-coverage.md](/Users/emmy/Documents/KnowledgeGraph/schwartz-coverage.md): chapter-family coverage map for Schwartz QFT
- [batch-registry.yaml](/Users/emmy/Documents/KnowledgeGraph/batch-registry.yaml): active wave and namespace reservation tracker
- [document-registry.yaml](/Users/emmy/Documents/KnowledgeGraph/document-registry.yaml): multi-document control plane for overnight orchestration
- [document-coverage.md](/Users/emmy/Documents/KnowledgeGraph/document-coverage.md): registry-backed dashboard of logical document progress
- [document-gap-queue.md](/Users/emmy/Documents/KnowledgeGraph/document-gap-queue.md): registry-backed overnight backlog and lane plan
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

The Stage 12 refinement wave is now also populated at first pass through:

- `dis_and_hadronic_factorization_refinement`

The Stage 13 refinement wave is now also populated at first pass through:

- `renormalization_toolkit_refinement`

The Stage 14 refinement wave is now also populated at first pass through:

- `scet_mode_and_resummation_refinement`

The Stage 15 refinement wave is now also populated at first pass through:

- `scattering_spectral_residual_refinement`

The Stage 16 refinement wave is now also populated at first pass through:

- `eft_matching_and_uv_completion_refinement`

The Stage 17 refinement wave is now also populated at first pass through:

- `naturalness_and_hierarchy_refinement`

The Stage 18 refinement wave is now also populated at first pass through:

- `schwinger_pair_production_refinement`

The Stage 19 refinement wave is now also populated at first pass through:

- `qed_loop_precision_refinement`

The Stage 20 refinement wave is now also populated at first pass through:

- `baryogenesis_and_sphaleron_refinement`

The Stage 21 refinement wave is now also populated at first pass through:

- `axion_strong_cp_peccei_quinn_refinement`

The Stage 22 refinement wave is now also populated at first pass through:

- `seesaw_mechanism_refinement`

Current integration model:

- batches connect by reusing shared canonical node ids across neighborhoods
- the repo now has a synthetic global compiled view at `all_authored`
- the current UI and query tools are still batch-oriented
- the current validated authored union stands at `454` nodes, `730` dependencies, `415` partonomy edges, and `158` overlays
- the authored union currently validates cleanly with no warnings
- the remaining substantive Schwartz residue is now tracked as explicit deferrals in [schwartz-gap-queue.md](/Users/emmy/Documents/KnowledgeGraph/schwartz-gap-queue.md) unless later query behavior reveals a real missing branch
- multi-document cross-doc reduction has promoted 7 new batches (see below)

Agent-generated proposal packs live under [data/batches/](/Users/emmy/Documents/KnowledgeGraph/data/batches) locally, but should normally stay off `main`.

## Multi-Document Cross-Document Reduction

The following new ontology batches were promoted from multi-document cross-confirmation:

- `complex_analysis_extended` — 11 nodes (analytic_function, Cauchy theorems, Laurent series, residue theorem, analytic continuation, branch cuts, etc.) confirmed across `complex_analysis` + `complex_variables`
- `differential_geometry_foundations` — 10 nodes (smooth manifold, tangent space, differential forms, Lie groups, fiber bundle, de Rham cohomology, etc.) confirmed across `tu_manifolds` + `lee_smooth_manifolds`
- `qft_topology_and_solitons` — 10 nodes (homotopy groups, magnetic monopoles, vortices, Skyrmions, Chern-Simons, anomaly inflow, etc.) confirmed across `weinberg_qft_vol2` + `axion_lecture_notes`
- `qft_axiomatic_foundations` — 8 nodes (cluster decomposition, Wigner's theorem, Haag's theorem, Furry's theorem, Coleman-Mandula, superselection, connected amplitudes) confirmed across `weinberg_qft_vol1` + `weinberg_qft_vol3`
- `qm_topology_semiclassical` — 8 nodes (Berry phase, Berry connection, Aharonov-Bohm, WKB, angular momentum addition, Landau levels, Dirac monopole) confirmed from `shankar_qm`
- `classical_em_foundations` — 4 nodes (Poynting theorem, Maxwell stress tensor, Kramers-Kronig, Thomas precession) from `jackson_em`
- `cosmology_foundations` — 13 nodes (FRW metric, scale factor, Friedmann equations, Hubble parameter, inflation, inflaton, CMB, CMB power spectrum, BAO, matter power spectrum, dark matter, dark energy, Lambda-CDM) from `dodelson_modern_cosmology`

All 13 logical documents are now at `cross_document_reduced` or `substantively_exhausted` status. The `qft_radiative_corrections_extensions` backlog cluster (5 Peskin-unique nodes) awaits cross-doc pressure from additional QFT sources before promotion.

## Multi-Document Orchestration

The repo now includes a document-centric control plane for running the same population workflow across every logical source in [Ref material/](/Users/emmy/Documents/KnowledgeGraph/Ref%20material), not just Schwartz.

Core files:

- [document-registry.yaml](/Users/emmy/Documents/KnowledgeGraph/document-registry.yaml): source of truth for document state, blockers, next actions, and priority
- [document-coverage.md](/Users/emmy/Documents/KnowledgeGraph/document-coverage.md): rendered dashboard from the registry
- [document-gap-queue.md](/Users/emmy/Documents/KnowledgeGraph/document-gap-queue.md): rendered queue, lane allocation, and backlog cluster view
- [prompts/handoff-multi-document-autonomous-orchestrator.md](/Users/emmy/Documents/KnowledgeGraph/prompts/handoff-multi-document-autonomous-orchestrator.md): orchestrator prompt
- [prompts/handoff-document-worker.md](/Users/emmy/Documents/KnowledgeGraph/prompts/handoff-document-worker.md): worker prompt
- [prompts/handoff-overlap-reviewer.md](/Users/emmy/Documents/KnowledgeGraph/prompts/handoff-overlap-reviewer.md): overlap-review prompt

Core scripts:

- [scripts/extract_document_oracle.py](/Users/emmy/Documents/KnowledgeGraph/scripts/extract_document_oracle.py): extract structure, contents/index payloads, and seed candidates for a logical document
- [scripts/summarize_source_triage.py](/Users/emmy/Documents/KnowledgeGraph/scripts/summarize_source_triage.py): summarize per-document triage pages into stable JSON and Markdown
- [scripts/document_orchestrator.py](/Users/emmy/Documents/KnowledgeGraph/scripts/document_orchestrator.py): registry-backed queue and completion helper for the overnight runner
- [scripts/render_document_tracking.py](/Users/emmy/Documents/KnowledgeGraph/scripts/render_document_tracking.py): refresh the tracked coverage and queue docs from the registry
- [scripts/run_multi_document_orchestrator.sh](/Users/emmy/Documents/KnowledgeGraph/scripts/run_multi_document_orchestrator.sh): restartable overnight loop for `codex exec`

Typical local commands:

```bash
.venv/bin/python /Users/emmy/Documents/KnowledgeGraph/scripts/extract_document_oracle.py --doc-id peskin_qft
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/summarize_source_triage.py --doc-id peskin_qft
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/render_document_tracking.py
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/document_orchestrator.py --queue-json
```

Overnight loop:

```bash
bash /Users/emmy/Documents/KnowledgeGraph/scripts/run_multi_document_orchestrator.sh
```

The default lane budget is one canonical merge lane plus up to `8` active spawned agents, split as `3` ingestion, `3` content, and `2` overlap/review lanes. Generated extraction artifacts stay under `data/generated/**` and should not be committed.
