# Propose Partonomy Prompt

Turn extraction notes into `part_of` proposals only.

For each proposal, include:

- parent
- child
- rationale
- confidence
- status

Do not emit dependency edges in this pass.

If the proposed split is too fine-grained to change query behavior, flag it instead of proposing it.
