# Document Gap Queue

This file is the cross-document source of truth for what the overnight orchestrator should do next.

## Operating Rules

- Read `document-registry.yaml` first on every run.
- Keep one canonical merge lane.
- Use at most `8` spawned agents at once.
- Keep ingestion one or two documents ahead of active merge work.
- Prefer reusable shared batches over document-local one-off nodes.

## Agent Plan

- max active agents: `8`
- canonical merge lanes: `1`
- currently assigned agents: `5`

### Ingestion Lane

- none scheduled

### Content Lane

- `peskin_qft`: `cross_document_reduced` / `hybrid` / Cross-document reduce: the 5 candidate_new_nodes are added to global_backlog for multi-doc pressure confirmation before promotion.
- `weinberg_qft_vol1`: `cross_document_reduced` / `hybrid` / Monitor: qft_axiomatic_foundations batch now in authored graph. Promote complex_analysis_extended also confirmed.
- `weinberg_qft_vol2`: `cross_document_reduced` / `hybrid` / Monitor: qft_topology_and_solitons batch now in authored graph.

### Review Lane

- `jackson_em`: `cross_document_reduced` / `index` / Promote classical_em_foundations batch with Kramers-Kronig and Poynting theorem; defer detailed EM content.
- `weinberg_qft_vol3`: `cross_document_reduced` / `hybrid` / Deferred: SUSY/SUGRA content explicitly out of scope. coleman_mandula_theorem added to qft_axiomatic_foundations batch.

## Active Queue

### Suggested Wave 1

- `peskin_qft`: `cross_document_reduced` / `hybrid` / `qft`
  next: Cross-document reduce: the 5 candidate_new_nodes are added to global_backlog for multi-doc pressure confirmation before promotion.
- `weinberg_qft_vol1`: `cross_document_reduced` / `hybrid` / `qft`
  next: Monitor: qft_axiomatic_foundations batch now in authored graph. Promote complex_analysis_extended also confirmed.
- `weinberg_qft_vol2`: `cross_document_reduced` / `hybrid` / `qft`
  next: Monitor: qft_topology_and_solitons batch now in authored graph.

### Suggested Wave 2

- `shankar_qm`: `cross_document_reduced` / `index` / `qm`
  next: Monitor: qm_topology_semiclassical batch now in authored graph.
- `jackson_em`: `cross_document_reduced` / `index` / `classical_em`
  next: Promote classical_em_foundations batch with Kramers-Kronig and Poynting theorem; defer detailed EM content.
- `complex_analysis`: `cross_document_reduced` / `index` / `complex_analysis`
  next: Monitor: complex_analysis_extended batch now in authored graph.

### Suggested Wave 3

- `complex_variables`: `cross_document_reduced` / `hybrid` / `complex_analysis`
  next: Monitor: complex_analysis_extended batch now in authored graph.
- `tu_manifolds`: `cross_document_reduced` / `hybrid` / `differential_geometry`
  next: Monitor: differential_geometry_foundations batch now in authored graph.
- `lee_smooth_manifolds`: `cross_document_reduced` / `index` / `differential_geometry`
  next: Monitor: differential_geometry_foundations batch now in authored graph.

### Suggested Wave 4

- `axion_lecture_notes`: `cross_document_reduced` / `toc_fallback` / `axion_bsm`
  next: Monitor: qft_topology_and_solitons batch now in authored graph (cross-doc pressure with weinberg_vol2).
- `dodelson_modern_cosmology`: `cross_document_reduced` / `hybrid` / `cosmology`
  next: Promote cosmology_foundations batch with all cosmology domain nodes.
- `weinberg_qft_vol3`: `cross_document_reduced` / `hybrid` / `supersymmetry`
  next: Deferred: SUSY/SUGRA content explicitly out of scope. coleman_mandula_theorem added to qft_axiomatic_foundations batch.

### Suggested Wave 5

- `schwartz_papers`: `cross_document_reduced` / `hybrid` / `qft`
  next: Monitor: 4 frontier batches (landau_analytic_structure, renormalons_and_trans_series, finite_s_matrix, vacuum_decay_and_tunneling) now in authored graph.

## Reusable Backlog Clusters

- `complex_analysis_extended`: `promoted`
  summary: 
- `differential_geometry_foundations`: `promoted`
  summary: 
- `qft_topology_and_solitons`: `promoted`
  summary: 
- `qft_axiomatic_foundations`: `promoted`
  summary: 
- `qm_topology_semiclassical`: `promoted`
  summary: 
- `qft_radiative_corrections_extensions`: `awaiting_cross_doc_pressure`
  summary: 
- `cosmology_foundations`: `promoted`
  summary: 
- `classical_em_foundations`: `promoted`
  summary: 
- `landau_analytic_structure`: `promoted`
  summary: 
- `renormalons_and_trans_series`: `promoted`
  summary: 
- `finite_s_matrix`: `promoted`
  summary: 
- `vacuum_decay_and_tunneling`: `promoted`
  summary: 

## Cross-Document Cautions

- Do not let textbook titles or chapter names become ontology nodes.
- Do not duplicate existing canonical topics because a second book uses different language.
- Split works such as the Weinberg volumes must be processed as one logical document each.
- `author index` PDFs are never a coverage oracle.
- `weinberg_qft_vol3` is expected to hit the current SUSY/SUGRA perimeter early and may end partially deferred.
- `axion_lecture_notes` and `dodelson_modern_cosmology` can open same-graph expansion, but only when repeated pressure justifies reusable new branches.

## Completion Rule

- A document is done only when its substantive oracle residue is either promoted, covered by existing graph structure, or explicitly deferred.
