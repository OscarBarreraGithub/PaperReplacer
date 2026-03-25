# Implementation Plan: Building the Tooling and Review Loop with Codex

## 1. Goal

This document is the implementation plan for how Codex should help build and maintain the HEP-TH prerequisite graph described in [idea.md](/Users/emmy/Documents/KnowledgeGraph/idea.md).

The central idea is:

- the ontology and query semantics live in the idea document,
- while this plan describes the operational workflow, repo structure, and review loop for producing graph data with Codex.

The implementation should be staged so that we can trust the graph before we scale it.

## 1.5. Autonomy Stance

This project should use Codex in a high-responsibility mode.

That means:

- Codex should do most routine graph construction work,
- Codex should be allowed to write canonical graph records under an approved batch contract,
- and human intervention should be exception-driven rather than item-by-item.

The human should still retain authority over:

- ontology changes,
- contract changes,
- disputed or low-confidence claims,
- decomposition changes that affect existing graph structure,
- and query outputs that appear semantically dishonest or unstable.

## 2. What Codex Is Responsible For

Codex should not be treated as an oracle that automatically decides the ontology. Its role is to build and run the tooling, extraction workflow, validation pipeline, and review loop around human-governed graph construction.

Codex should help with:

- decomposing candidate topics into nodes,
- proposing dependency and partonomy relations,
- attaching rationales and provenance,
- validating schemas and graph invariants,
- compiling source YAML into queryable graph artifacts,
- generating review reports for ambiguous or disputed annotations.

Codex should not silently decide:

- ontology changes,
- edge semantics,
- context overlays,
- or controversial prerequisite claims

without surfacing them for human review.

So the right mental model is:

- Codex builds the graph infrastructure and performs most graph-authoring work under contract,
- while humans govern ontology, contracts, and exceptions.

## 3. High-Level Architecture

The implementation should revolve around one main Codex orchestrator and a small number of bounded helper roles.

### Main orchestrator

The main Codex agent owns:

- the current batch definition,
- subagent delegation,
- schema and invariant enforcement,
- merge decisions into canonical graph files,
- and communication with the human collaborator.

The orchestrator should be the only agent that edits canonical graph artifacts directly. It may author, promote, or reject graph facts when the batch contract allows autonomous merge behavior.

### MVP roles

For the MVP, the workflow should stay simple. We do not need a large cast of specialized subagents before we know the semantics are stable.

Recommended MVP roles:

- `orchestrator`: owns workflow state, batch definition, validation gates, automatic merge decisions, and canonical artifacts.
- `extractor_proposer`: reads sources or notes and produces staged evidence plus candidate nodes and edges.
- `validator`: enforces schemas, invariants, and contract-level rules.
- `reviewer_query_probe`: runs the query suite, reports semantic failures, and prepares exception packets for human review when needed.

This is enough for the first serious slice.

### Later specialization

After the first batch works end to end, we can split the workflow further. Specialized agents should work on narrow, disjoint responsibilities and write only to staging areas or files explicitly assigned to them.

Possible later roles:

- `semantics agent`: owns query semantics, closure rules, traversal policy, and contract templates.
- `source extractor`: reads source material or notes for a topic batch and produces structured extraction notes.
- `node agent`: proposes admissible nodes from the extraction notes.
- `structure agent`: proposes `part_of` relations only.
- `dependency agent`: proposes dependency edges only.
- `overlay agent`: proposes contextual assumed-background overlays only.
- `normalizer`: checks IDs, naming conventions, and YAML shape before merge.
- `reviewer`: flags ambiguities, possible inversions, over-broad nodes, missing provenance, and ontology drift.
- `query probe`: runs canned queries against the compiled graph and reports semantic failures.
- `adjudicator`: resolves disputed or contradictory proposals before merge.

These roles should be introduced only when they reduce review burden instead of creating coordination overhead.

## 4. Orchestrator Workflow

Each batch should follow the same pipeline.

### Step 1: Define the batch

The human and orchestrator agree on:

- the topic slice,
- the target mastery modes,
- the audience profile if needed,
- the source material or seed references,
- and the scope boundary for this batch.

Output:

- `data/batches/<batch-id>/brief.md`

### Step 2: Freeze the semantic contract

Before graph-writing agents run, the orchestrator should lock the active semantic contract for the batch in a machine-readable file:

- `data/batches/<batch-id>/batch_contract.yaml`

The contract should include:

- allowed relation types,
- active mastery modes,
- closure policy,
- relation-composition rules,
- composite expansion policy,
- overlay rules,
- tie-breaking policy for non-unique outputs,
- the active task model,
- the fixed query suite for the batch,
- the autonomy policy for the batch,
- and forbidden heuristics,
- and any batch-specific context assumptions.

This contract should be versioned and referenced by downstream artifacts. A human-readable explanation can live beside it, but the contract itself should drive validators and tests.

### Step 3: Run extraction work

The orchestrator sends independent extraction tasks to the active extractor role or, later, to specialized extraction helpers in parallel.

Each extractor should receive:

- the batch brief,
- the current ontology constraints,
- admissibility rules,
- and a narrow source slice or question.

Extractor outputs should be staging notes only, not canonical graph files.

Output examples:

- candidate node list
- observed usage evidence
- definitional evidence
- derivational dependence evidence
- notation dependence evidence
- candidate claims
- possible overlap with existing nodes
- unresolved terms
- notation bottlenecks
- provenance leads

### Step 4: Consolidate into structured proposals

The orchestrator or dedicated worker turns extraction notes into structured proposals:

- node proposals,
- dependency edge proposals,
- partonomy proposals,
- contextual overlay suggestions when relevant.

These proposals should already conform to the schema shape, but they should remain unmerged.

In the MVP, these proposals may all come from one `extractor_proposer` role. Later, each proposal layer can be split into separate agents if that reduces ambiguity rather than increasing it.

Each proposal layer should remain separate. A dependency proposal should not also write `part_of` relations, and an overlay proposal should not write core prerequisite edges.

### Step 4.5: Resolve overlap against the existing graph

Before merge, every proposed node should be classified relative to existing graph content as one of:

- `reuse_existing`
- `alias_existing`
- `new_distinct`
- `part_of_existing`
- `ambiguous`

This overlap pass should combine semantic judgment with cheap validator heuristics such as exact-label or normalized-label matches.

Unresolved overlap should block automatic merge.

### Step 5: Validate and normalize

Before anything enters the canonical graph, the normalizer and validator should check:

- schema validity,
- stable ID rules,
- admissibility rules,
- graph invariants,
- duplicate or near-duplicate nodes,
- overlap risk against existing authored nodes,
- edge orientation,
- missing rationale, provenance, or evidence type.

### Step 6: Autonomous merge gate and exception review

The orchestrator should first decide whether proposals are safe to merge automatically under the active contract.

Automatic merge should be allowed only when all of the following are true:

- schemas and invariants pass,
- no duplicate or near-duplicate warning remains unresolved,
- no unresolved overlap disposition remains,
- confidence meets the contract threshold,
- no ontology drift warning is present,
- no disputed item is involved,
- no forbidden heuristic is triggered,
- and the query probe reports no semantic warning above the contract threshold.

When those conditions hold, the orchestrator may merge directly.

When they do not hold, the orchestrator presents an exception packet covering:

- new nodes,
- new edges,
- overlap disposition and possible existing matches,
- low-confidence or disputed items,
- ontology changes implied by the batch,
- and any suggested suppressions or merges.

High-impact or ambiguous changes should be escalated, but routine low-risk graph construction should not require per-item human approval.

### Step 7: Merge into canonical graph

After automatic acceptance or human exception review, the orchestrator merges accepted changes into the canonical graph files and regenerates compiled artifacts.

### Step 8: Query test the batch

The query probe runs a fixed suite of semantic checks, for example:

- all prerequisites of the target node at `recognize`
- all prerequisites at `use`
- all prerequisites at `derive`
- the contract-defined prerequisite-set query
- expanded slice query with composites

Each query run should emit a reviewable report including:

- output set,
- derivation provenance,
- relation-composition trace,
- suppressed alternatives when tie-breaking occurs,
- confidence bottlenecks,
- and semantic warnings such as context mixing or disputed-edge adjacency.

The orchestrator records any surprising outputs before the next batch begins and escalates only those that exceed the contract's warning threshold.

## 5. Recommended Agent Boundaries

To reduce merge conflicts and accidental drift, each agent should have a clear write scope.

### Orchestrator-owned files

- canonical node files
- canonical dependency files
- canonical partonomy files
- compiled graph artifacts
- review summaries

### Subagent-owned staging files

- extraction notes
- proposal drafts
- ambiguity reports
- validation reports

Practical rule:

- subagents do not edit canonical graph files directly in the MVP,
- the orchestrator performs merges after validation,
- and human review is reserved for contract exceptions rather than ordinary items.

This preserves a single canonical writer while still giving Codex substantial responsibility.

## 6. Repository Layout

A simple layout should be enough for the MVP.

```text
/Users/emmy/Documents/KnowledgeGraph/
  README.md
  idea.md
  plan.md
  spec/
    query-semantics.md
    ontology-rules.md
    overlap-resolution.md
    review-policy.md
    agent-playbook.md
  schemas/
    node.schema.json
    dependency.schema.json
    partonomy.schema.json
    overlay.schema.json
  prompts/
    extract-candidates.md
    propose-nodes.md
    propose-dependencies.md
    propose-partonomy.md
    review-batch.md
  data/
    authored/
      nodes/
      dependencies/
      partonomy/
      overlays/
    batches/
      <batch-id>/
        brief.md
        batch_contract.yaml
        extraction/
        proposals/
        review.md
    generated/
      normalized/
      compiled/
      reports/
      artifacts/
  scripts/
    validate_graph.py
    compile_graph.py
    query_graph.py
    render_graph.py
    serve_ui.py
  ui/
    index.html
    app.js
    styles.css
  tests/
    test_schemas.py
    test_queries.py
    test_relation_composition.py
    fixtures/
```

## 7. Human-Authored vs Machine-Generated Artifacts

This split should be explicit.

### Human-authored or human-approved

- ontology and semantics docs
- prompt templates
- batch briefs
- final canonical graph entries in `data/authored/` when an exception review is required
- review decisions
- topic selection decisions

### Machine-generated

- extraction notes
- proposal drafts
- normalized JSON or JSONL
- compiled bundles and indexes
- validation reports
- query test outputs
- rendered views or diagrams

The graph should remain auditable by keeping generated artifacts separate from accepted source data.

## 8. Data Flow

The data pipeline should look like this:

1. human selects a topic batch
2. orchestrator creates the batch brief
3. orchestrator writes and freezes `batch_contract.yaml`
4. extractor or extractor-proposer work produces staging notes
5. layer-specific proposals are created from those notes
6. overlap resolution is performed against the existing graph
7. validator checks schemas and invariants
8. reviewer and query probe generate warnings and exception packets
9. orchestrator auto-merges safe items and escalates exceptions
10. human reviews only the escalated exceptions
11. compile scripts regenerate queryable artifacts
12. query probe confirms behavior

This should be the default loop for every batch.

## 9. First Implementation Phases

The implementation should be staged in a way that proves the semantics and review loop before scaling agent complexity.

### Phase 0: Bootstrap the repo

Create:

- repo structure
- spec placeholders
- empty schema files
- empty authored and generated data directories
- basic validation and compile script stubs

Goal:

- make the workspace ready for structured graph work.

### Phase 1: Formalize the contract and tests

Create:

- `spec/query-semantics.md`
- `spec/ontology-rules.md`
- `batch_contract.yaml` template
- initial JSON schemas or Pydantic models
- synthetic relation-composition tests

Goal:

- make the semantics executable enough to validate data before real graph population.

### Phase 2: Hand-author one tiny slice

Create a very small slice by hand, with no extraction agents yet.

Goal:

- confirm that the schema, compilation, and query behavior are usable on real content.

### Phase 3: Build validation, compilation, and reporting

Implement:

- compile step from YAML to normalized JSON
- query CLI or script
- derivation and provenance reporting
- positive and negative query behavior tests

Goal:

- make the graph inspectable and testable, not just editable.

### Phase 4: Use Codex for workflow support

Use Codex for:

- repo scaffolding
- schema generation
- validator and test implementation
- report rendering
- proposal formatting

Goal:

- make the workflow efficient without handing over ontology authority.

### Phase 5: Introduce one proposal agent

Only after the earlier phases are stable should we introduce one `extractor_proposer` agent for candidate extraction from source notes, with automatic merge for low-risk items enabled by contract.

### Phase 6: Add more specialization only if needed

Only after the proposal workflow proves useful should we split into more specialized agents such as separate dependency, partonomy, or overlay proposers.

## 10. Subagent Prompt Design

Each subagent should be given a narrow objective and a strict output contract.

### Extractor prompt

Should ask for:

- candidate terms,
- candidate nodes,
- notation issues,
- methods vs concepts,
- observed usage evidence,
- derivational dependence evidence,
- definitional evidence,
- notation dependence evidence,
- candidate claims grounded in that evidence,
- possible overlap with existing nodes,
- and provenance leads.

Should not ask for:

- final IDs,
- ontology changes,
- or direct edits to canonical graph data.

### Proposal prompt

Should ask for:

- schema-shaped YAML proposals,
- explicit rationale,
- a short answer to the question "what concrete failure occurs if this prerequisite is absent?",
- evidence type,
- confidence,
- overlap disposition for each node proposal,
- and notes on ambiguity.

### Reviewer prompt

Should ask for:

- potential edge inversions,
- over-broad or under-specified nodes,
- duplicate concepts under different labels,
- unsupported assumptions,
- and violations of the ontology rules.

This separation will make it easier to compare outputs and spot drift.

## 11. Validation Rules

Validation should happen in layers.

### Schema validation

Check:

- required fields
- enum values
- field types
- reference existence

### Graph validation

Check:

- `part_of` acyclicity
- no self-loops in dependencies
- no orphan references
- no duplicate IDs
- no dependency edges missing mastery semantics
- no unresolved overlap warning marked as auto-mergeable

### Policy validation

Check:

- every asserted dependency edge has rationale, evidence type, and provenance
- assumed-background overlays include context
- composite expansion rules are respected
- no canonical prerequisite edges rely only on pedagogical ordering language

### Query behavior tests

Check positive behavior:

- prerequisite queries do not cross `part_of` by default
- profile-adjusted views are distinguishable from intrinsic dependency views
- derived results are labeled as derived rather than asserted

Check negative behavior:

- shortest-path output is not shown unless explicitly requested
- pedagogical edges do not enter minimal-prerequisite style queries by default
- overlays do not rewrite intrinsic dependency edges
- disputed edges do not silently participate in default closure

## 12. Review and Dispute Handling

The workflow should assume disagreement will happen.

For each proposed item, we should be able to mark:

- accepted
- needs revision
- disputed
- deferred

The orchestrator should keep disputed items out of the main compiled graph by default unless we later decide to support multiple parallel views.

Human review should be exception-triggered, not universal.

Escalate when:

- confidence falls below the contract threshold,
- ontology drift is detected,
- an existing decomposition is being changed,
- a duplicate-risk warning is unresolved,
- an overlap-disposition warning is unresolved,
- a query report contains semantic warnings above threshold,
- or a proposal touches forbidden heuristics from the active contract.

## 13. How Topic Selection Fits In

We should discuss the actual starting topics after this plan is in place, but the implementation needs a slot for that choice.

For each seed batch, we should specify:

- target topic or topic cluster
- why it is a good semantic stress test
- expected node count
- expected dependency depth
- source material to consult
- likely ambiguity hotspots
- the active task model for the batch, for example `literature_reading` or `standard_computation`
- likely overlap candidates with existing graph material

The first topic batch should be:

- narrow,
- rich in real dependency structure,
- small enough to review by hand,
- and strong enough to expose ontology problems early.

We do not need to decide the exact batch in this document, but the workflow assumes one will be chosen next.

## 14. Success Criteria for the MVP

The MVP is successful if:

- Codex can run a full batch from brief to validated proposals,
- Codex can merge routine low-risk items without waiting for per-item approval,
- the human can review only exception packets without drowning in noise,
- the graph answers a few nontrivial prerequisite queries sensibly,
- the compiled artifacts preserve provenance and auditability,
- and adding a second batch does not require rethinking the whole structure.

## 15. Immediate Next Steps

The next work should proceed in this order:

1. finalize this implementation plan,
2. choose the initial repository layout,
3. write `spec/query-semantics.md`,
4. define the `batch_contract.yaml` template,
5. write the first schemas and synthetic relation-composition tests,
6. create the review policy, prompt templates, and agent playbook,
7. choose the first topic batch,
8. hand-author one tiny seed batch before introducing extraction agents.

Once we agree on the first topic batch, we can turn this plan into actual repo scaffolding and scripts.
