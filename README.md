# KnowledgeGraph

This repository is building a trustworthy prerequisite graph for HEP-TH topics.

Key docs:

- [idea.md](/Users/emmy/Documents/KnowledgeGraph/idea.md): ontology and semantic design
- [plan.md](/Users/emmy/Documents/KnowledgeGraph/plan.md): implementation workflow

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

The current canonical authored slice is the `seed_pinch_singularities` batch in [data/authored/](/Users/emmy/Documents/KnowledgeGraph/data/authored).

Important note:

- `seed_pinch_singularities` should now be treated as a calibration fixture and regression slice, not as the final deep graph for the topic.
- the deeper production-oriented follow-up batch is [pinch_singularities_deep](/Users/emmy/Documents/KnowledgeGraph/data/batches/pinch_singularities_deep).

Agent-generated proposal packs live under [data/batches/](/Users/emmy/Documents/KnowledgeGraph/data/batches).
