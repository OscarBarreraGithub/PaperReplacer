# Population Plan: Broad QFT Coverage

## 1. Goal

This document describes the best way to systematically populate the graph so that it covers essentially all of perturbative quantum field theory, with enough breadth and depth to follow Matthew Schwartz's QFT book and the main QFT/collider/EFT directions visible in his research program.

This is a population plan, not an ontology redesign.

The ontology remains:

- topic-centered
- mastery-relative
- dependency/partonomy separated
- context overlays kept separate from intrinsic prerequisites

## 2. Practical Coverage Target

The operational target is:

- all major reusable QFT topic families represented as canonical graph neighborhoods
- strong coverage of the material spanned by *Quantum Field Theory and the Standard Model*
- enough advanced coverage for Schwartz-adjacent theory papers in:
  - scattering and S-matrix structure
  - renormalization and RG
  - EFT
  - gauge theory and the Standard Model
  - QCD infrared structure
  - factorization, jets, and SCET
  - analytic structure and amplitudes

This plan does **not** treat textbooks or papers as ontology nodes.

Textbooks and papers should be used as:

- seeding guides
- evidence/provenance support
- coverage checks

not as the center of the graph itself.

## 3. Core Decision

The graph should be populated by **topic families and batches**, not by chapter order.

Why:

- textbook order mostly encodes pedagogy, not prerequisite semantics
- paper-local assumptions are contextual and should not define ontology
- broad umbrella nodes like `QFT` are too coarse to be useful as the real work surface
- the graph becomes trustworthy only if reusable concepts, methods, representations, and formal statements are the canonical units

So the right systematic strategy is:

1. define broad topic families
2. expand them through narrow, contract-driven batches
3. merge repeated frontiers into reusable foundational neighborhoods
4. use textbooks and papers only to support those graph claims

## 4. Population Principle

Broaden with two coupled programs:

- **vertical research slices**
  - narrow advanced batches such as `pinch_singularities`, `landau_singularity_conditions`, `spinor_helicity`, `scet_thrust`
- **horizontal frontier closure**
  - when the same prerequisite frontier recurs across multiple slices, promote it into a foundational batch

A topic should enter the graph because:

- it recurs across batches
- it has a stable meaning
- it has a distinct failure mode if absent
- and it changes real query answers

It should **not** enter the graph just because a textbook teaches it early.

## 5. Coverage Map

These are the major batch families for broad QFT population.

### Foundational families

1. `mathematical_methods_for_qft`
   - linear algebra
   - multivariable calculus
   - Fourier analysis
   - distributions and boundary-value language
   - complex analysis for contour arguments
   - tensor and index manipulation

2. `relativistic_symmetry_and_kinematics`
   - Minkowski space
   - Lorentz invariance
   - Poincare symmetry
   - four-vectors and invariants
   - spin, helicity, and one-particle representations
   - discrete symmetries

3. `variational_and_classical_field_theory`
   - action principle
   - Euler-Lagrange equations
   - canonical momenta
   - Hamiltonian density
   - Noether theorem
   - Green functions in classical field theory

4. `qm_operator_and_scattering_foundations`
   - Hilbert-space/operator language
   - commutators
   - time evolution
   - perturbation theory
   - Lippmann-Schwinger
   - scattering states
   - cross sections and decay rates

### Core QFT trunk

5. `free_fields_and_quantization`
   - scalar, fermion, and vector free fields
   - mode expansions
   - creation/annihilation operators
   - equal-time quantization
   - spin-statistics
   - microcausality

6. `propagators_green_functions_and_lsz`
   - time ordering
   - propagators
   - correlation functions
   - LSZ reduction
   - spectral decomposition
   - optical theorem

7. `perturbation_theory_and_diagrammatics`
   - Dyson series
   - Wick theorem
   - Feynman rules
   - symmetry factors
   - connected vs 1PI objects
   - loop expansion

8. `path_integral_and_generating_functionals`
   - functional measure
   - Gaussian functional integrals
   - source functionals
   - Schwinger-Dyson equations
   - Ward-Takahashi identities
   - fermionic path integrals

9. `regularization_renormalization_and_rg`
   - dimensional regularization
   - counterterms
   - renormalized perturbation theory
   - scheme dependence
   - beta functions
   - anomalous dimensions
   - Wilsonian RG

### Major reusable branches

10. `gauge_theory_and_ward_brst_structure`
    - covariant derivative
    - field strength
    - Abelian and non-Abelian gauge theory
    - gauge fixing
    - ghosts
    - Ward identities
    - Slavnov-Taylor/BRST structure
    - Wilson lines

11. `symmetry_breaking_eft_and_anomalies`
    - spontaneous symmetry breaking
    - Goldstone theorem
    - Higgs mechanism
    - EFT matching and power counting
    - operator expansions
    - chiral and gauge anomalies
    - anomaly matching

12. `analytic_structure_and_amplitudes`
    - contour deformation
    - poles vs branch cuts
    - analytic continuation in invariants
    - Cutkosky discontinuities
    - dispersion relations
    - Landau singularity conditions
    - pinch singularities
    - spinor-helicity and on-shell recursion

13. `qcd_ir_structure`
    - color algebra
    - Yang-Mills perturbation theory
    - asymptotic freedom
    - soft and collinear singularities
    - splitting functions
    - DGLAP
    - PDFs
    - parton model and factorization basics

14. `factorization_scet_and_jets`
    - factorization theorems
    - hard/jet/soft/beam functions
    - mode scaling
    - SCET operators
    - matching QCD to SCET
    - Sudakov logarithms
    - event shapes
    - jet algorithms
    - threshold/TMD-style branches as needed

### Deferred branches

These should stay outside the first broad pass unless they become necessary:

- lattice QFT
- thermal and nonequilibrium QFT
- deep nonperturbative strong-coupling topics
- SUSY/SUGRA
- string theory / AdS/CFT
- curved-spacetime QFT
- condensed-matter many-body QFT
- machine-learning-specific branches

## 6. How Broad Expansion Should Actually Work

Each population step should happen through a narrow batch, not a mega-batch.

For every batch:

1. choose a fixed target neighborhood
2. choose mastery modes
3. fix a node budget and dependency-depth budget
4. define likely overlap targets
5. freeze the batch contract
6. extract proposals in parallel
7. reduce and overlap-check them
8. validate and query-probe them
9. merge through one canonical writer

The batch should be narrow enough that:

- every node has a clear reason to exist
- every edge has a real failure mode
- overlap can still be adjudicated honestly

## 7. Minimal Source Policy

Do **not** build a heavyweight source system before broad population starts.

For now, every asserted edge or overlay should keep:

- `rationale`
- `failure_mode_if_absent`
- `evidence`
- `confidence`
- `status`

The source side can stay lightweight:

- one or more canonical textbooks/notes per batch
- a few representative papers when needed
- simple references in evidence/provenance fields

This is enough to populate the graph without over-engineering a second source ontology.

## 8. Rollout Order

### Stage 0: Lock the current analytic anchor

- keep `seed_pinch_singularities` as calibration
- keep `pinch_singularities_deep` as the first serious anchor neighborhood
- reconcile analytic-structure overlaps before broader rollout

### Stage 1: Nearest reusable prerequisites

Run in parallel:

- `complex_analysis_for_qft`
- `relativistic_kinematics`
- `linear_algebra_operator_basics`

Run after a small decomposition check:

- `distributions_boundary_values`

### Stage 2: Physics trunk under QFT

Run in parallel once Stage 1 is stable:

- `qm_operator_foundations`
- `variational_principles_and_classical_fields`
- `lorentz_poincare_representations`

### Stage 3: Core QFT backbone

Run first:

- `free_fields_and_quantization`

Then partially overlap:

- `correlators_propagators_lsz`
- `perturbation_wick_feynman_rules`

### Stage 4: Universal advanced trunk

Run after Stage 3 stabilizes:

- `path_integral_and_generating_functionals`
- `regularization_renormalization`
- `renormalization_group`

### Stage 5: Major reusable branches

Run in parallel once Stage 4 is stable:

- `gauge_theory_foundations`
- `s_matrix_and_analytic_structure`
- `eft_symmetry_breaking_anomalies`
- `qcd_ir_structure`

### Stage 6: Schwartz perimeter

Run in parallel once Stage 5 is stable:

- `factorization_scet_and_jets`
- `spinor_helicity_and_on_shell_methods`
- `standard_model_precision_and_electroweak`
- `hqet_and_heavy_quark_tools`

### Stage 7: Paper-driven perimeter cleanup

Use vertical research slices to close remaining gaps:

- soft-collinear factorization papers
- jet substructure papers
- finite S-matrix / massless scattering papers
- EFT/gravity-adjacent papers when needed

## 9. Parallelization Strategy

Broad population should use many subagents, but only in staging.

### Safe operating model

- `1` global orchestrator / canonical writer
- `3` active topic batches by default
- up to `4` active batches if they are clearly disjoint
- `4-6` extraction shards per batch
- `1` node proposer per batch
- `1` dependency proposer per batch
- `1` partonomy proposer per batch
- optional `1` overlay proposer per batch
- `1` reducer / validator / query-probe chain per batch

### Hard rule

There should be only **one canonical merge lane**.

That means:

- many subagents can read and propose in parallel
- only the orchestrator promotes to `data/authored/**`

## 10. Overlap Control

Broad expansion will fail if overlap is not controlled.

So every active batch should carry:

- reserved root namespace
- likely overlap targets
- expected shared frontier
- node budget
- dependency-depth budget

And every proposed node should carry:

- `overlap_disposition`
- `possible_existing_matches`
- rationale for reuse / alias / new node / part-of

Special care is required for reusable canonical nodes such as:

- `LSZ reduction`
- `dimensional regularization`
- `Feynman i epsilon prescription`
- `Wilson lines`
- `spinor-helicity`
- `Landau singularity conditions`

These should not be cloned into multiple batch-local variants.

## 11. Definition of Done

The graph is “broad enough for Schwartz-level QFT coverage” when all of the following are true:

1. Every major family in Sections 5 and 8 has at least one stable authored batch.
2. The trunk supports `recognize` and `use` queries end-to-end across core QFT.
3. `derive` exists for the most central backbone areas:
   - free fields
   - propagators/LSZ
   - perturbation theory
   - renormalization/RG
   - gauge-theory essentials
4. Schwartz-style advanced topics in analytic structure, EFT, QCD IR structure, factorization, and SCET can be expressed without giant missing frontiers.
5. A paper-facing query for representative Schwartz topics returns a credible assumed-background manifest without collapsing into `QFT`.

## 12. Immediate Next Moves

The next concrete steps should be:

1. create a batch queue for Stage 1 and Stage 2
2. lock decomposition decisions for:
   - distributions vs boundary values vs principal value vs `i epsilon`
   - Lorentz vs Poincare vs representation-theory nodes
   - correlators vs Green functions vs propagators vs generating functionals
3. launch three parallel foundation batches:
   - `complex_analysis_for_qft`
   - `relativistic_kinematics`
   - `linear_algebra_operator_basics`
4. keep the orchestrator as the only canonical writer
5. harvest repeated frontiers from every advanced batch and promote them into reusable foundation neighborhoods

## 13. Seed References for Population Guidance

These should guide extraction and coverage checks, without becoming ontology nodes themselves:

- Matthew D. Schwartz, *Quantum Field Theory and the Standard Model* table of contents:
  [Cambridge TOC PDF](https://assets.cambridge.org/97811070/34730/toc/9781107034730_toc.pdf)
- Matthew D. Schwartz research overview:
  [Harvard research page](https://schwartz.scholars.harvard.edu/research)
- Matthew D. Schwartz jet-physics overview:
  [Jet Physics page](https://schwartz.scholars.harvard.edu/jet-physics)
