# Triage Source Pages

You are triaging extracted source pages for one logical document.

Your goal is to classify document-local pressure, not to author final ontology directly.

## Inputs

- document id
- oracle artifact pages
- seed candidates
- current graph context if needed

## Required Output Format

Produce Markdown with zero or more of these exact `##` section headers:

- `covered_existing`
- `candidate_batch_expansion`
- `candidate_new_node`
- `alias_candidate`
- `out_of_scope_or_non_ontology`
- `skip_non_ontology`

Each section may use either:

- bullet items beginning with `- `
- a two-column table
- a three-column table with `term | classification | match`

If you use the three-column table, the `classification` cell must be one of the exact section names above.

## Classification Rules

- `covered_existing`: already substantively covered by current canonical nodes or batches
- `candidate_batch_expansion`: best handled by expanding an existing or planned batch
- `candidate_new_node`: reusable new concept that is not already present
- `alias_candidate`: alternate wording that should probably map to an existing node
- `out_of_scope_or_non_ontology`: real term, but not one that should become graph structure in this program
- `skip_non_ontology`: pagination noise, chapter furniture, person names, or other extraction junk

## Constraints

- do not create one row per page number variant
- do not let chapter titles become ontology nodes by default
- prefer reusable shared concepts over document-private wording
- note ambiguity explicitly instead of forcing a new node
