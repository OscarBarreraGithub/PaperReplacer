# Multi-Document Autonomous Orchestrator Handoff

You are working in:

- `/Users/emmy/Documents/KnowledgeGraph`

Your job is to act as the orchestrator for the long-running autonomous population of this repository across every logical source in `Ref material`.

Do not treat this as a one-batch task. Treat it as a continuing program of work with durable checkpoints. Continue until every document in `document-registry.yaml` is either:

- substantively exhausted,
- explicitly deferred with reasons, or
- blocked with a narrow recorded blocker.

## Read First

Read these files before making decisions:

- `/Users/emmy/Documents/KnowledgeGraph/README.md`
- `/Users/emmy/Documents/KnowledgeGraph/idea.md`
- `/Users/emmy/Documents/KnowledgeGraph/plan.md`
- `/Users/emmy/Documents/KnowledgeGraph/population-plan.md`
- `/Users/emmy/Documents/KnowledgeGraph/document-registry.yaml`
- `/Users/emmy/Documents/KnowledgeGraph/document-coverage.md`
- `/Users/emmy/Documents/KnowledgeGraph/document-gap-queue.md`
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

## Control Plane

`document-registry.yaml` is the source of truth. Read it first on every run and update it after every stable action.

Supporting tracked views:

- `document-coverage.md`: human-readable dashboard
- `document-gap-queue.md`: live queue and lane plan

Generated per-document workspaces:

- `data/generated/extracted/<doc_id>/`
- `data/generated/oracles/<doc_id>/`

Do not treat `data/generated/**` as canonical graph state.

## Canonical Tools

Use these scripts:

- `.venv/bin/python scripts/extract_document_oracle.py --doc-id <doc_id>`
- `python3 scripts/summarize_source_triage.py --doc-id <doc_id>`
- `python3 scripts/document_orchestrator.py --queue-json`
- `python3 scripts/render_document_tracking.py`
- `python3 scripts/validate_graph.py --batch <batch_id>`
- `python3 scripts/compile_graph.py --batch <batch_id>`
- `python3 scripts/validate_graph.py --all-authored`
- `python3 scripts/compile_graph.py --all-authored`
- `python3 scripts/query_graph.py ...`

Keep `scripts/extract_schwartz_index.py` and `scripts/summarize_index_triage.py` as compatibility wrappers only.

## Operating Model

You are the only canonical writer. Use subagents aggressively, but keep one central merge lane.

Target concurrency budget:

- `3` ingestion agents
- `3` content agents
- `2` overlap/review agents

Never exceed `8` active spawned agents at once.

Never let concurrent content workers write in overlapping namespaces.

While subagents run:

- integrate disjoint completed work locally
- update `document-registry.yaml`
- refresh `document-coverage.md` and `document-gap-queue.md`
- validate and compile stable checkpoints

## Per-Document Workflow

For each active document:

1. inspect structure and confirm `index`, `toc_fallback`, or `hybrid`
2. extract oracle artifacts into `data/generated/extracted/<doc_id>/` and `data/generated/oracles/<doc_id>/`
3. generate document-local triage reports under `data/generated/oracles/<doc_id>/triage/`
4. summarize them with `scripts/summarize_source_triage.py`
5. reduce repeated pressure into shared reusable backlog clusters instead of document-private nodes
6. promote disjoint, topic-centered graph batches only when justified
7. validate, compile, checkpoint, and update the registry

## Scheduling Priority

On each loop:

1. unblock active population work
2. merge any validated disjoint batch that is ready
3. ingest the next unstarted document
4. promote the best cross-document reusable backlog cluster
5. record explicit deferrals for residual material that should not become graph structure

Do not stop after a summary or a single wave unless you hit a genuine blocker.

## Invariants

- textbooks and papers are not ontology nodes
- do not create one node per index entry
- reuse existing canonical ids whenever the meaning is the same
- keep partonomy separate from dependency edges
- prefer reusable shared refinements over book-local duplications
- author index PDFs are never a coverage oracle
- split works such as the Weinberg volumes are one logical document each
- keep generated extraction artifacts out of tracked canonical graph files

## Checkpoint Discipline

A stable checkpoint requires:

1. registry state updated truthfully
2. coverage and gap docs refreshed
3. any merged batch files written to disk
4. batch validation and compile passing
5. `all_authored` validation and compile passing after stable integration
6. targeted query probes for new branches when needed

Do not stage or commit `data/generated/**`.

## Hard Stop Conditions

Only stop if:

- every registry document is terminal
- a validation or compile failure cannot be resolved safely
- there are conflicting local edits that would make automated merges unsafe
- a destructive decision is required

If blocked, record the blocker narrowly in `document-registry.yaml` before stopping.
