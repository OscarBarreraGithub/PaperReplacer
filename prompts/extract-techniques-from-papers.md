# Extract Unlock Techniques from Physics Papers

You are extracting "unlock techniques" from physics papers. These are specific methods that, when you know to apply them, make an otherwise-intractable problem solvable.

There are TWO categories of technique to extract:

## 1. Physical Techniques
Specific physics methods: factorization strategies, power counting schemes, gauge choices, symmetry arguments, effective field theory constructions, matching procedures, etc.

## 2. Mathematical Methods
The underlying mathematical machinery that makes the physical technique work. These are often the hardest part — the reason a physicist gets stuck is typically that they don't know which mathematical tool to reach for. Examples:
- Contour deformation / steepest descent
- Saddle point approximation
- Borel resummation
- Picard-Lefschetz theory
- Sector decomposition for overlapping singularities
- Integration-by-parts (IBP) reduction
- Differential equations for master integrals
- Symbol / coproduct methods for polylogarithms
- Conformal mapping techniques
- Functional determinant computation methods
- Homological algebra (exact sequences, cohomology)
- Group theory techniques (Casimir operators, representation decomposition)
- Analytic continuation techniques
- Distribution theory (plus distributions, delta function identities)

## Output Format

For each technique provide:
- technique_id: short snake_case
- label: human-readable name
- description: 1-2 sentences on what it does and when to use it
- category: "physical" or "mathematical"
- unlocks: what type of problem this makes tractable
- prerequisites: what concepts you need to apply it
- source_paper: the arxiv_id

Focus on KEY methodological moves — not every equation, but the techniques that are the reason you'd cite the paper.

Write results as YAML:
```yaml
papers:
  - arxiv_id: "XXXX.XXXXX"
    title: "..."
    techniques:
      - technique_id: ...
        category: physical
        ...
      - technique_id: ...
        category: mathematical
        ...
```
