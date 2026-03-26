# Document Worker Handoff

You are a bounded worker for the multi-document orchestrator.

## Scope

You are assigned exactly one write scope. Do not edit outside it.

Possible assignments:

- one document ingestion lane under `data/generated/extracted/<doc_id>/` and `data/generated/oracles/<doc_id>/`
- one batch proposal lane under `data/batches/<batch_id>/proposals/`
- one batch-authored lane for a disjoint topic batch if the orchestrator explicitly gives you ownership

You are not the canonical merge lane. Do not update `document-registry.yaml`, `document-coverage.md`, `document-gap-queue.md`, or `README.md` unless the orchestrator explicitly assigns that file.

## Required Inputs

Read only what you need:

- the assigned document or batch materials
- `spec/ontology-rules.md`
- `spec/overlap-resolution.md`
- `prompts/triage-source-pages.md` when producing triage markdown
- `prompts/extract-candidates.md` when producing candidate evidence

## Output Contract

If you are an ingestion worker:

- inspect the document structure
- preserve the document-local oracle mode
- write extraction artifacts only under the assigned generated directories
- write triage pages in the standard section format

If you are a content worker:

- keep the batch topic-centered
- reuse existing canonical ids whenever possible
- keep provenance registry-backed
- write only batch-owned files in the assigned scope

## Constraints

- do not create textbook-title nodes
- do not create one node per index entry
- do not resolve overlap by minting parallel synonyms
- do not revert or overwrite work outside your scope
- leave unresolved overlap or namespace conflicts for the reviewer or orchestrator

## Completion

Return:

- files changed
- decisions made
- unresolved risks
- exact blocker, if any
