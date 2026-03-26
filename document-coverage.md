# Document Coverage Dashboard

- logical documents tracked: 14
- exhausted: 1
- deferred: 0
- blocked: 0
- active: 13
- max active agents: 8

## Documents

| Priority | Doc ID | Oracle | Status | Domain | Checkpoint | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `schwartz_qft` | `hybrid` | `substantively_exhausted` | `qft` | `stage22_schwartz_refinement_p` | Monitor for future cross-document alias reuse or overlap cleanup only. |
| 2 | `peskin_qft` | `hybrid` | `cross_document_reduced` | `qft` | `batch_promoted` | Cross-document reduce: the 5 candidate_new_nodes are added to global_backlog for multi-doc pressure confirmation before promotion. |
| 3 | `weinberg_qft_vol1` | `hybrid` | `cross_document_reduced` | `qft` | `batch_promoted` | Monitor: qft_axiomatic_foundations batch now in authored graph. Promote complex_analysis_extended also confirmed. |
| 4 | `weinberg_qft_vol2` | `hybrid` | `cross_document_reduced` | `qft` | `batch_promoted` | Monitor: qft_topology_and_solitons batch now in authored graph. |
| 5 | `shankar_qm` | `index` | `cross_document_reduced` | `qm` | `batch_promoted` | Monitor: qm_topology_semiclassical batch now in authored graph. |
| 6 | `jackson_em` | `index` | `cross_document_reduced` | `classical_em` | `triage_complete` | Promote classical_em_foundations batch with Kramers-Kronig and Poynting theorem; defer detailed EM content. |
| 7 | `complex_analysis` | `index` | `cross_document_reduced` | `complex_analysis` | `batch_promoted` | Monitor: complex_analysis_extended batch now in authored graph. |
| 8 | `complex_variables` | `hybrid` | `cross_document_reduced` | `complex_analysis` | `batch_promoted` | Monitor: complex_analysis_extended batch now in authored graph. |
| 9 | `tu_manifolds` | `hybrid` | `cross_document_reduced` | `differential_geometry` | `batch_promoted` | Monitor: differential_geometry_foundations batch now in authored graph. |
| 10 | `lee_smooth_manifolds` | `index` | `cross_document_reduced` | `differential_geometry` | `batch_promoted` | Monitor: differential_geometry_foundations batch now in authored graph. |
| 11 | `axion_lecture_notes` | `toc_fallback` | `cross_document_reduced` | `axion_bsm` | `batch_promoted` | Monitor: qft_topology_and_solitons batch now in authored graph (cross-doc pressure with weinberg_vol2). |
| 12 | `dodelson_modern_cosmology` | `hybrid` | `cross_document_reduced` | `cosmology` | `triage_complete` | Promote cosmology_foundations batch with all cosmology domain nodes. |
| 13 | `weinberg_qft_vol3` | `hybrid` | `cross_document_reduced` | `supersymmetry` | `batch_promoted` | Deferred: SUSY/SUGRA content explicitly out of scope. coleman_mandula_theorem added to qft_axiomatic_foundations batch. |
| 14 | `schwartz_papers` | `hybrid` | `cross_document_reduced` | `qft` | `batch_promoted` | Monitor: 4 frontier batches (landau_analytic_structure, renormalons_and_trans_series, finite_s_matrix, vacuum_decay_and_tunneling) now in authored graph. |

## Notes

- The orchestrator should treat `document-registry.yaml` as the source of truth.
- `document-gap-queue.md` is the operational backlog view generated from the same registry.
- `schwartz_qft` is already substantially exhausted and serves as the seeded calibration document.
