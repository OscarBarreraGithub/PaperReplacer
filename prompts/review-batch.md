# Review Batch Prompt

Review a batch proposal for semantic correctness and ontology drift.

Focus on:

- edge inversions
- over-broad or redundant nodes
- unresolved overlap between new and existing nodes
- unsupported dependency claims
- missing evidence or provenance
- accidental mixing of dependency, partonomy, and overlays
- query outputs that sound more canonical than the data supports

Return:

- findings
- disputed items
- items needing revision
- warnings about query semantics
