# Schwartz Autonomous Orchestrator Handoff

You are working in:

- `/Users/emmy/Documents/KnowledgeGraph`

Your job is to act as the **orchestrator** for the long-running autonomous population of this repository until the graph has exhausted the substantive coverage of *Quantum Field Theory and the Standard Model* by Matthew D. Schwartz.

Do not treat this as a one-batch task. Treat it as a continuing program of work with durable checkpoints.

## Read First

Read these files before making decisions:

- `/Users/emmy/Documents/KnowledgeGraph/README.md`
- `/Users/emmy/Documents/KnowledgeGraph/idea.md`
- `/Users/emmy/Documents/KnowledgeGraph/plan.md`
- `/Users/emmy/Documents/KnowledgeGraph/population-plan.md`
- `/Users/emmy/Documents/KnowledgeGraph/schwartz-coverage.md`
- `/Users/emmy/Documents/KnowledgeGraph/schwartz-gap-queue.md`
- `/Users/emmy/Documents/KnowledgeGraph/batch-registry.yaml`
- `/Users/emmy/Documents/KnowledgeGraph/CONTRIBUTING.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/query-semantics.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/ontology-rules.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/review-policy.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/overlap-resolution.md`

Also inspect:

- `/Users/emmy/Documents/KnowledgeGraph/data/authored/`
- `/Users/emmy/Documents/KnowledgeGraph/data/batches/`
- `/Users/emmy/Documents/KnowledgeGraph/scripts/`
- `/Users/emmy/Documents/KnowledgeGraph/tests/`

## Current State You Are Inheriting

The repo already has:

- a topic-centered ontology
- mastery-relative dependency semantics
- partonomy separated from prerequisite edges
- an `all_authored` synthetic global bundle
- a local UI at `http://127.0.0.1:8766`

Current validated authored union:

- `228` nodes
- `318` dependencies
- `200` partonomy edges
- `46` overlays

`all_authored` currently validates cleanly. The remaining warnings are old duplicate-definition merge warnings in reused nodes such as:

- `complex_analysis.contour_deformation`
- `complex_analysis.poles_vs_branch_points`
- `qft.analytic_continuation_in_kinematic_invariants`
- `qft.feynman_i_epsilon_prescription`
- `qft.pinch_singularities`
- `qft.propagator_singularities`
- `qm.unitary_evolution`

These warnings are real cleanup targets, but they are not blockers for continued population.

## What Has Already Been Mapped

Foundation and trunk waves already exist at first pass, including:

- `complex_analysis_for_qft`
- `relativistic_kinematics`
- `linear_algebra_operator_basics`
- `qm_operator_foundations`
- `variational_principles_and_classical_fields`
- `lorentz_poincare_representations`
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
- `cross_sections_decay_rates_and_phase_space`
- `qed_tree_level_processes`
- `gauge_invariance_and_ward_brst`
- `effective_actions_and_background_fields`

The pinch-singularities anchor and calibration slices also exist:

- `seed_pinch_singularities`
- `pinch_singularities_deep`

## Schwartz Coverage Oracle

The back-of-book Schwartz index has already been extracted and triaged.

Use these as the coverage oracle:

- `/Users/emmy/Documents/KnowledgeGraph/data/generated/extracted/schwartz_index.txt`
- `/Users/emmy/Documents/KnowledgeGraph/data/generated/extracted/schwartz_index.json`
- `/Users/emmy/Documents/KnowledgeGraph/data/generated/extracted/schwartz_index_summary.md`
- `/Users/emmy/Documents/KnowledgeGraph/data/generated/extracted/schwartz_index_summary.json`
- `/Users/emmy/Documents/KnowledgeGraph/data/generated/index_triage/page_*.md`

Current triage totals:

- `covered_existing`: 113
- `candidate_batch_expansion`: 153
- `candidate_new_node`: 101
- `skip_non_ontology`: 51

Important principle:

- Do **not** force every index entry to become a node.
- The end goal is that every substantive index entry is accounted for as one of:
  - `canonical_node`
  - `alias_to_node`
  - `covered_by_existing_node_or_batch`
  - `out_of_scope_or_non_ontology`

## Core Mission

Continue autonomously until the substantive Schwartz backlog is exhausted.

That means:

1. keep launching population waves
2. use the Schwartz index triage as the backlog driver
3. reduce backlog via high-yield batches first
4. only create standalone nodes when they are reusable and structurally justified
5. keep the graph coherent, connected, and queryable

Do not stop after one wave unless you hit a genuine blocker.

## How To Operate

Act as an orchestrator, not just a single worker.

Use subagents aggressively, with the maximum safe parallelism the environment supports.
If there is a live thread cap, saturate it with the most valuable mix of:

- content workers for disjoint batches
- explorers for overlap/risk questions

Recommended pattern:

- 4 content workers + 2 explorers when doing a major wave
- if more capacity is available, scale up carefully
- do not send all workers into overlapping namespaces at once

While workers run:

- do central integration work locally
- update the registry
- resolve overlap
- validate partial results
- maintain durable checkpoints

Do not wait idly if there is non-overlapping integration work to do.

## Checkpoint Discipline

Checkpoint so work is not lost.

A checkpoint means:

1. batch files and authored YAMLs are actually written to disk
2. batch validation passes
3. batch compile passes
4. `batch-registry.yaml` reflects true status and counts
5. `README.md` is updated when the repo’s high-level state materially changes
6. `all_authored` is revalidated after stable integration points
7. if git use is appropriate and available, make small durable commits on a `codex/*` branch

If git operations are unavailable or blocked, the authoritative checkpoint is the tracked repo state:

- `data/authored/**`
- `data/batches/**`
- `batch-registry.yaml`
- `README.md`
- `schwartz-gap-queue.md`
- other tracked design docs

Do not commit:

- `data/generated/**`
- `data/batches/*/proposals/**`
- local scratch outputs

Follow `/Users/emmy/Documents/KnowledgeGraph/CONTRIBUTING.md`.

## Always Keep These Invariants

- Reuse existing canonical node ids whenever the meaning is genuinely the same.
- Do not create duplicate topic nodes because a topic appears again in a different chapter.
- Keep textbooks and papers out of the ontology layer.
- Keep partonomy separate from dependency edges.
- Keep assumed background contextual.
- Prefer smaller trustworthy batches over vague umbrella batches.
- Do not let broad chapter labels become ontology nodes.

## Current Best Next Waves

The next high-yield queue after the completed Stage 4 wave is:

### Immediate next wave

- `infrared_divergences_and_jets`
- `spinor_helicity_and_gluon_scattering`
- `flavor_ckm_pmns_and_precision_observables`

### Next after that

- `scalar_qed`
- `nonperturbative_qcd_and_topology`
- `critical_phenomena_and_conformal_basics`
- `heavy_quark_effective_theory_refinement`
- unblock and integrate `distributions_boundary_values`

### Continue until Schwartz is exhausted

Keep reducing the remaining index backlog in waves until:

- major `candidate_batch_expansion` clusters are absorbed
- the residual `candidate_new_node` items are either promoted or explicitly classified
- Schwartz coverage is no longer materially missing reusable QFT neighborhoods

## Specific Local Tools You Should Use

Validation:

```bash
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/validate_graph.py --batch <batch_id>
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/validate_graph.py --all-authored
```

Compilation:

```bash
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/compile_graph.py --batch <batch_id>
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/compile_graph.py --all-authored
```

Tests:

```bash
python3 -m unittest /Users/emmy/Documents/KnowledgeGraph/tests/test_graph_pipeline.py /Users/emmy/Documents/KnowledgeGraph/tests/test_query_semantics.py
```

UI:

```bash
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/serve_ui.py --port 8766
```

Schwartz index tools:

```bash
/Users/emmy/Documents/KnowledgeGraph/.venv/bin/python /Users/emmy/Documents/KnowledgeGraph/scripts/extract_schwartz_index.py
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/summarize_index_triage.py
```

## What To Do At The Start Of Your Run

1. Read the files listed above.
2. Inspect `batch-registry.yaml` and `schwartz-gap-queue.md`.
3. Revalidate `all_authored`.
4. Determine the next best wave from the remaining Schwartz backlog.
5. Launch the wave with parallel subagents.
6. Integrate continuously and checkpoint after each stable batch.

## What To Do At The End Of Any Given Session

Before stopping, always leave the repo in a durable state:

- batch registry updated
- completed batches validated and compiled
- `all_authored` validated if integration changed
- README updated if high-level coverage changed
- no in-progress ambiguity hidden silently

Summarize:

- what waves ran
- what batches landed
- current authored-union counts
- what remains in the Schwartz backlog
- any unresolved overlap or ontology decisions

## Tone / Decision Style

Be proactive, not passive.

- Make reasonable decisions without asking unless the ontology is genuinely at risk.
- Use overlap reduction and shared-node reuse aggressively.
- Use the index to drive coverage, not to flatten the ontology into a glossary.
- Keep going wave after wave until Schwartz is substantially exhausted.

## Stop Condition

Do **not** stop merely because one wave is complete.

Stop only when one of these is true:

1. the substantive Schwartz backlog is exhausted
2. the remaining items are mostly explicit non-ontology skips or minor aliases
3. you hit a genuine blocker that requires human judgment

If blocked, surface the blocker clearly and narrowly.
