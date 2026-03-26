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
