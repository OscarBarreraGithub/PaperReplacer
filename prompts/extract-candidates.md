# Extract Candidates Prompt

You are extracting structured evidence for a narrow prerequisite-graph batch.

Your job is to gather evidence and candidate claims, not to silently author canonical ontology.

## Inputs

- batch brief
- batch contract
- ontology rules
- source notes or references

## Output Sections

Produce:

1. candidate terms
2. candidate nodes
3. observed usage evidence
4. definitional evidence
5. derivational dependence evidence
6. notation dependence evidence
7. candidate claims grounded in the evidence
8. unresolved ambiguities
9. provenance leads

## Constraints

- distinguish evidence from claims
- do not invent context-free assumed background
- do not mix `part_of` with dependency claims
- do not assign final stable ids
- do not edit canonical authored graph files

## HEP-TH Seed Guidance

For the `seed_pinch_singularities` batch:

- treat `contour deformation` as a method-level node, not a vague topic heading,
- treat `Feynman i epsilon prescription` as a concrete prescription or formal statement tied to propagator pole placement,
- treat `propagator singularities` and `pinch singularities` as distinct concepts,
- and prefer narrow analytic/QFT claims over broad umbrella nodes like `QFT` or `analytic structure` unless the batch brief explicitly requires them.

Anti-patterns for this seed:

- do not jump ahead to `Landau singularity conditions` in the first pass,
- do not add renormalization, LSZ, or generic scattering-theory background unless the evidence truly forces it,
- do not flatten everything into a single "complex analysis" prerequisite if the evidence points to a sharper method-level claim.
