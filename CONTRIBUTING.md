# Contributing Workflow

This repository separates canonical graph content from staging and generated artifacts.

## What Belongs on `main`

`main` should contain:

- ontology and workflow docs
- schemas
- scripts
- tests
- UI files
- canonical graph data in `data/authored/**`
- batch briefs and contracts in `data/batches/*/brief.md` and `data/batches/*/batch_contract.yaml`
- extraction context notes that define a batch's intent
- calibration fixtures that are intentionally part of the repository

## What Should Not Live on `main`

These are local or branch-only working artifacts and should not be committed to `main`:

- `data/generated/**`
- `data/batches/*/proposals/**`
- temporary exports
- ad hoc scratch files

## Branch Discipline

Use topic branches for active work.

Recommended branch format:

- `codex/<batch-id>`
- `codex/<batch-id>-<purpose>`

Examples:

- `codex/pinch_singularities_deep`
- `codex/landau_conditions-overlap-pass`

Do not do active batch development directly on `main`.

## Promotion Flow

1. Create or switch to a `codex/*` branch.
2. Work locally with proposal files under `data/batches/*/proposals/`.
3. Generate local artifacts under `data/generated/`.
4. Review and validate the batch.
5. Promote only accepted canonical changes into `data/authored/**`.
6. Open a PR or merge request from the topic branch into `main`.

## PR Checklist

Before merge:

- no proposal files are staged for commit
- no generated artifacts are staged for commit
- validation passes for affected batches
- tests pass
- overlap decisions are documented when relevant
- canonical authored changes are intentional and minimal

## Current Conventions

- `seed_pinch_singularities` is a calibration fixture
- `pinch_singularities_deep` is the next production-oriented batch scaffold
