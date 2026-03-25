# Propose Nodes Prompt

Turn candidate extraction notes into node proposals that match the node schema.

For each node, provide:

- label
- proposed id slug
- knowledge kind
- granularity level
- composite flag
- supported mastery modes
- short summary
- overlap disposition
- possible existing matches
- notes on ambiguity

Reject or flag candidates that fail the node admissibility rules.

Allowed overlap dispositions:

- `reuse_existing`
- `alias_existing`
- `new_distinct`
- `part_of_existing`
- `ambiguous`

Do not create a new node when `reuse_existing` or `alias_existing` is the better fit.
