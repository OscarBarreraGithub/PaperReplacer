# Agent Playbook

## MVP Roles

The MVP uses four roles:

- `orchestrator`
- `extractor_proposer`
- `validator`
- `reviewer_query_probe`

## Role Boundaries

### Orchestrator

Owns:

- batch setup
- contract creation
- merge gates
- final promotion into canonical authored data
- automatic acceptance of low-risk items under contract

Does not:

- change ontology or contract semantics without escalation

### Extractor-Proposer

Owns:

- evidence gathering
- candidate nodes
- candidate dependency proposals
- candidate partonomy proposals
- overlay suggestions
- initial overlap disposition for each candidate node

Does not:

- edit canonical authored files
- change ontology rules
- silently decide unresolved overlap cases

### Validator

Owns:

- schema validation
- invariant checks
- contract compliance checks

Does not:

- silently repair semantic issues

### Reviewer-Query-Probe

Owns:

- ambiguity reporting
- query execution under the active contract
- semantic warning reports
- exception packet generation

Does not:

- merge content into canonical data

## Later Specialization

Only split the workflow into more specialized agents when one of these becomes true:

- the single extractor-proposer creates too much review noise,
- partonomy and dependency proposals are being confused,
- overlay work becomes meaningfully separate from core dependency work,
- overlap adjudication becomes a repeated bottleneck,
- or batch throughput becomes bottlenecked by one role.
