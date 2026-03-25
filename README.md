# KnowledgeGraph

This repository is building a trustworthy prerequisite graph for HEP-TH topics.

Key docs:

- [idea.md](/Users/emmy/Documents/KnowledgeGraph/idea.md): ontology and semantic design
- [plan.md](/Users/emmy/Documents/KnowledgeGraph/plan.md): implementation workflow
- [CONTRIBUTING.md](/Users/emmy/Documents/KnowledgeGraph/CONTRIBUTING.md): branch and merge discipline

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

Agent-generated proposal packs live under [data/batches/](/Users/emmy/Documents/KnowledgeGraph/data/batches) locally, but should normally stay off `main`.
