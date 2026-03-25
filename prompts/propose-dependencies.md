# Propose Dependencies Prompt

Turn extraction notes into dependency-edge proposals that match the dependency schema.

For each proposed edge, include:

- `from`
- `to`
- relation type
- necessity
- rationale
- evidence
- confidence
- status
- answer to: what concrete failure occurs if the prerequisite is absent?

Do not emit:

- `part_of` relations
- context-free assumed-background claims
- edges justified only by teaching order unless relation type is pedagogical
