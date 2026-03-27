# KnowledgeGraph — Claude Code Instructions

## Agent Orchestration

**You (Claude main) are a thin orchestrator.** Delegate heavy or bulk work to subagents.

### Golden Rule: Protect Your Context
- **NEVER** read many large files directly — delegate to Codex or a Claude subagent
- **NEVER** do bulk file analysis inline — spawn a subagent that writes results to `/tmp/`
- **ALWAYS** receive results as short summaries, then synthesize for the user

### Codex CLI (gpt-5.4)
- **Wrapper:** `scripts/codex_worker.sh` (handles nvm sourcing + non-interactive bypass flag)
- **Invocation:** `bash scripts/codex_worker.sh [--out /tmp/file.md] "prompt"`
- **Background:** append `&` and `wait` for parallel tasks
- **Config:** `~/.codex/config.toml` — model=gpt-5.4, effort=xhigh, approval=never

### Delegation Table
| Task | Delegate to |
|---|---|
| Read/summarize many files | Codex |
| Mechanical edits, bulk YAML work | Codex |
| Deep reasoning, planning, ontology | Claude subagent |
| Code review (high confidence) | Both → cross-review pattern |
| Quick search (Grep/Glob) | Inline (no subagent overhead) |

### Invocation Patterns

**Codex foreground:**
```bash
bash scripts/codex_worker.sh "Read data/authored/nodes/ and count how many nodes exist"
```

**Codex with file output:**
```bash
bash scripts/codex_worker.sh --out /tmp/result.md "Summarize all batch briefs in data/batches/"
```

**Parallel Codex tasks:**
```bash
bash scripts/codex_worker.sh --out /tmp/a.md "Task A" &
bash scripts/codex_worker.sh --out /tmp/b.md "Task B" &
wait
```

**Claude subagent + Codex in parallel:**
- Launch Claude subagent via Agent tool (`run_in_background=true`)
- Launch Codex via Bash tool (background `&`)
- Read both `/tmp/` outputs, synthesize

**Cross-Review pattern:**
1. Both agents analyze independently → `/tmp/claude_r1.md`, `/tmp/codex_r1.md`
2. Each reviews the other → APPROVE or REQUEST_CHANGES
3. Iterate (max 3 rounds; main Claude breaks ties)
4. Main Claude synthesizes final answer

## Project Overview

This repo builds a HEP-TH prerequisite knowledge graph based on Schwartz *Quantum Field Theory and the Standard Model*.

- **Ontology & semantics:** `spec/`, `idea.md`
- **Batch workflow:** `plan.md`, `spec/agent-playbook.md`
- **Authored graph data:** `data/authored/` (nodes, dependencies, partonomy, overlays)
- **Batch staging:** `data/batches/<batch-id>/` (brief, contract, extraction, proposals)
- **Scripts:** `scripts/validate_graph.py`, `compile_graph.py`, `query_graph.py`
- **Prompts:** `prompts/` (extract-candidates, propose-nodes, propose-dependencies, etc.)

## Key Constraints
- Only Codex/orchestrator writes to `data/authored/` (canonical graph files)
- Subagents write to staging areas only (`data/batches/<id>/extraction/`, `proposals/`)
- Human review is exception-driven, not per-item
- Ontology and contract changes always require human approval


----

You are working in /Users/emmy/Documents/KnowledgeGraph.

Your job is to implement and execute the multi-document population plan until it is actually done, not just partially set up.

Read these files first:

- /Users/emmy/Documents/KnowledgeGraph/prompts/handoff-multi-document-autonomous-orchestrator.md
- /Users/emmy/Documents/KnowledgeGraph/document-registry.yaml
- /Users/emmy/Documents/KnowledgeGraph/document-coverage.md
- /Users/emmy/Documents/KnowledgeGraph/document-gap-queue.md
- /Users/emmy/Documents/KnowledgeGraph/README.md
- /Users/emmy/Documents/KnowledgeGraph/batch-registry.yaml
- /Users/emmy/Documents/KnowledgeGraph/spec/ontology-rules.md
- /Users/emmy/Documents/KnowledgeGraph/spec/overlap-resolution.md
- /Users/emmy/Documents/KnowledgeGraph/spec/query-semantics.md

Implement the plan described in /Users/emmy/Documents/KnowledgeGraph/prompts/handoff-multi-document-autonomous-orchestrator.md.

Operational requirements:

- Act as the orchestrator, not a single worker.
- Spawn Codex agents aggressively when useful, with up to 8 active agents at once.
- Keep one canonical merge lane. Do not let parallel workers edit overlapping namespaces.
- Treat /Users/emmy/Documents/KnowledgeGraph/document-registry.yaml as the source of truth.
- Keep your work tracked continuously by updating:
  - /Users/emmy/Documents/KnowledgeGraph/document-registry.yaml
  - /Users/emmy/Documents/KnowledgeGraph/document-coverage.md
  - /Users/emmy/Documents/KnowledgeGraph/document-gap-queue.md
- Update /Users/emmy/Documents/KnowledgeGraph/README.md when the repo’s high-level state materially changes.
- Continue until every document is either substantively exhausted, explicitly deferred with reasons, or blocked with a narrow recorded blocker.
- Do not stop at summaries, checkpoints, or runtime boundaries. If one pass ends, resume from the registry and continue.
- Only ask for user input if there is a real blocker, conflicting local edits, or a destructive decision that should not be taken automatically.

Execution rules:

- Use .venv/bin/python for extraction/oracle work.
- Use the existing repo scripts rather than inventing parallel workflows:
  - /Users/emmy/Documents/KnowledgeGraph/scripts/extract_document_oracle.py
  - /Users/emmy/Documents/KnowledgeGraph/scripts/summarize_source_triage.py
  - /Users/emmy/Documents/KnowledgeGraph/scripts/render_document_tracking.py
  - /Users/emmy/Documents/KnowledgeGraph/scripts/document_orchestrator.py
  - /Users/emmy/Documents/KnowledgeGraph/scripts/validate_graph.py
  - /Users/emmy/Documents/KnowledgeGraph/scripts/compile_graph.py
  - /Users/emmy/Documents/KnowledgeGraph/scripts/query_graph.py
- Validate each stable batch/checkpoint.
- Keep generated extraction artifacts under data/generated/** and do not treat them as canonical graph state.
- Reuse existing canonical node ids whenever the meaning is the same.
- Do not create textbook-title nodes.
- Do not create one node per index entry.
- Prefer shared reusable batches over document-private duplications.
- Keep the graph topic-centered.

Definition of done:

- Every logical document in /Users/emmy/Documents/KnowledgeGraph/document-registry.yaml is terminal.
- The registry and rendered tracking docs match the actual repo state.
- Stable graph checkpoints validate and compile cleanly.
- Any remaining residue is explicitly deferred or blocked, not silently dropped.

Start by reading the control-plane files, determining the highest-value next wave from the registry, spawning the appropriate agents, and executing the work.
