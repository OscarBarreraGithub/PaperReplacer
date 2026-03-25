You are working in the repository `/Users/emmy/Documents/KnowledgeGraph`.

Your task is to populate the deep production-oriented batch for pinch singularities.

Read these files first:

- `/Users/emmy/Documents/KnowledgeGraph/README.md`
- `/Users/emmy/Documents/KnowledgeGraph/idea.md`
- `/Users/emmy/Documents/KnowledgeGraph/plan.md`
- `/Users/emmy/Documents/KnowledgeGraph/CONTRIBUTING.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/query-semantics.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/ontology-rules.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/review-policy.md`
- `/Users/emmy/Documents/KnowledgeGraph/spec/overlap-resolution.md`
- `/Users/emmy/Documents/KnowledgeGraph/data/batches/pinch_singularities_deep/brief.md`
- `/Users/emmy/Documents/KnowledgeGraph/data/batches/pinch_singularities_deep/batch_contract.yaml`
- `/Users/emmy/Documents/KnowledgeGraph/data/batches/pinch_singularities_deep/extraction/source_notes.md`

Important context:

- `seed_pinch_singularities` is a calibration fixture and regression slice only.
- Do not create a second canonical node for the same topic. Keep `qft.pinch_singularities` as the single canonical topic node.
- Depth should come from the surrounding graph, mastery modes, and task/audience context, not from duplicating the topic node.
- `main` should not accumulate generated artifacts or proposal-pack junk. Follow `/Users/emmy/Documents/KnowledgeGraph/CONTRIBUTING.md`.

Branching:

- Create and use a topic branch named `codex/pinch_singularities_deep` unless it already exists.
- Do not do active development on `main`.

What to build:

- A substantially richer local prerequisite neighborhood around `qft.pinch_singularities`.
- Reuse existing nodes when they are genuinely the same.
- Add distinct new nodes only when they carry new dependency structure.
- Use `part_of` only for structural decomposition, not as a substitute for prerequisite edges.

Target outcome:

- The graph around `qft.pinch_singularities` should move beyond the 5-node calibration slice and become a credible research-facing batch.
- It should still stay local and disciplined rather than trying to encode all of QFT.

Suggested scope, subject to the ontology rules and evidence quality:

- contour deformation
- poles vs branch points
- Feynman `i epsilon` prescription
- propagator singularities
- loop-energy or loop-momentum contour structure where justified
- analytic continuation in kinematic invariants where justified
- distributions or boundary values if they are genuinely needed for the chosen mastery/task scope
- Landau singularity conditions if the batch evidence supports including them
- related formal statements only if they create real new structure

Anti-goals:

- do not introduce broad umbrella nodes like `QFT analytic structure` unless you can justify them under the admissibility rules
- do not duplicate the existing pinch singularities topic under names like `pinch_singularities_deep`
- do not mix partonomy and prerequisite semantics
- do not silently change the ontology or query contract

Workflow:

1. Inspect the existing canonical authored files under `/Users/emmy/Documents/KnowledgeGraph/data/authored/`.
2. Build the deep batch around the existing node `qft.pinch_singularities`.
3. Use overlap resolution against the current graph for every substantial new node.
4. Populate:
   - `/Users/emmy/Documents/KnowledgeGraph/data/authored/nodes/pinch_singularities_deep.yaml`
   - `/Users/emmy/Documents/KnowledgeGraph/data/authored/dependencies/pinch_singularities_deep.yaml`
   - `/Users/emmy/Documents/KnowledgeGraph/data/authored/partonomy/pinch_singularities_deep.yaml`
   - `/Users/emmy/Documents/KnowledgeGraph/data/authored/overlays/pinch_singularities_deep.yaml`
5. Add or update tests if the deeper batch exposes missing query/validation coverage.
6. Run validation and tests.
7. Summarize:
   - what nodes and edges were added
   - what overlap/reuse decisions were made
   - any items that remain semantically ambiguous

Validation commands:

```bash
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/validate_graph.py --batch seed_pinch_singularities
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/compile_graph.py --batch seed_pinch_singularities
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/validate_graph.py --batch pinch_singularities_deep
python3 /Users/emmy/Documents/KnowledgeGraph/scripts/compile_graph.py --batch pinch_singularities_deep
python3 -m unittest /Users/emmy/Documents/KnowledgeGraph/tests/test_graph_pipeline.py /Users/emmy/Documents/KnowledgeGraph/tests/test_query_semantics.py
```

Output expectations:

- Make the authored deep-batch files real and nontrivial.
- Keep provenance and rationale fields meaningful.
- Call out any controversial edge choices explicitly instead of hiding them.
- Prefer a smaller trustworthy graph over a larger mushy one.
