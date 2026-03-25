import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kg_core import (  # noqa: E402
    BatchRecords,
    compile_batch,
    load_batch_records,
    prerequisite_set,
    prerequisites,
    validate_batch_records,
)


class GraphPipelineTests(unittest.TestCase):
    def test_seed_batch_validates(self) -> None:
        records = load_batch_records("seed_pinch_singularities")
        report = validate_batch_records(records)
        self.assertTrue(report["valid"], report)

    def test_deep_batch_validates(self) -> None:
        records = load_batch_records("pinch_singularities_deep")
        report = validate_batch_records(records)
        self.assertTrue(report["valid"], report)

    def test_use_prerequisites_close_over_chain(self) -> None:
        records = load_batch_records("seed_pinch_singularities")
        bundle = compile_batch(records)
        result = prerequisites(bundle, "qft.pinch_singularities", "requires_for_use")
        node_ids = {item["node_id"] for item in result["results"]}
        self.assertEqual(
            node_ids,
            {
                "complex_analysis.contour_deformation",
                "complex_analysis.poles_vs_branch_points",
                "qft.feynman_i_epsilon_prescription",
                "qft.propagator_singularities",
            },
        )
        derived = {
            item["node_id"]: item["derived"]
            for item in result["results"]
        }
        self.assertTrue(derived["qft.feynman_i_epsilon_prescription"])
        self.assertFalse(derived["qft.propagator_singularities"])

    def test_deep_batch_use_prerequisites_capture_richer_local_structure(self) -> None:
        records = load_batch_records("pinch_singularities_deep")
        bundle = compile_batch(records)
        result = prerequisites(bundle, "qft.pinch_singularities", "requires_for_use")
        node_ids = {item["node_id"] for item in result["results"]}
        self.assertEqual(
            node_ids,
            {
                "complex_analysis.contour_deformation",
                "complex_analysis.poles_vs_branch_points",
                "qft.analytic_continuation_in_kinematic_invariants",
                "qft.feynman_i_epsilon_prescription",
                "qft.landau_singularity_conditions",
                "qft.loop_energy_contour_analysis",
                "qft.loop_momentum_integration_structure",
                "qft.opposite_side_pole_placement",
                "qft.propagator_singularities",
            },
        )
        derived = {item["node_id"]: item["derived"] for item in result["results"]}
        self.assertTrue(derived["qft.feynman_i_epsilon_prescription"])
        self.assertTrue(derived["qft.loop_momentum_integration_structure"])
        self.assertTrue(derived["qft.opposite_side_pole_placement"])
        self.assertFalse(derived["qft.loop_energy_contour_analysis"])

    def test_frontier_semantics_returns_leaves(self) -> None:
        records = load_batch_records("seed_pinch_singularities")
        bundle = compile_batch(records)
        result = prerequisite_set(
            bundle,
            "qft.pinch_singularities",
            "requires_for_use",
            "ancestral_frontier",
        )
        self.assertEqual(
            result["sets"][0],
            [
                "complex_analysis.contour_deformation",
                "complex_analysis.poles_vs_branch_points",
                "qft.feynman_i_epsilon_prescription",
            ],
        )

    def test_partonomy_cycle_is_rejected(self) -> None:
        records = load_batch_records("seed_pinch_singularities")
        cycle_records = BatchRecords(
            batch_id=records.batch_id,
            contract=records.contract,
            nodes=records.nodes,
            dependencies=records.dependencies,
            partonomy=[
                {
                    "parent": "qft.pinch_singularities",
                    "child": "qft.propagator_singularities",
                    "rationale": "test",
                    "status": "asserted",
                    "confidence": 0.9,
                },
                {
                    "parent": "qft.propagator_singularities",
                    "child": "qft.pinch_singularities",
                    "rationale": "test",
                    "status": "asserted",
                    "confidence": 0.9,
                },
            ],
            overlays=records.overlays,
        )
        report = validate_batch_records(cycle_records)
        self.assertFalse(report["valid"])
        self.assertTrue(
            any("part_of cycle detected" in error for error in report["errors"]),
            report,
        )

    def test_overlap_warning_is_emitted_for_matching_labels(self) -> None:
        temp_path = (
            ROOT
            / "data"
            / "authored"
            / "nodes"
            / "temporary_overlap_fixture.yaml"
        )
        temp_path.write_text(
            "- id: temporary.other_contour_deformation\n"
            "  label: Contour deformation\n"
            "  knowledge_kind: method\n"
            "  granularity_level: atomic\n"
            "  composite: false\n"
            "  mastery_modes_supported:\n"
            "    - recognize\n"
            "  summary: Temporary overlap fixture.\n"
            "  status: asserted\n"
        )
        try:
            records = load_batch_records("seed_pinch_singularities")
            report = validate_batch_records(records)
            self.assertTrue(
                any("overlap risk: label match" in warning for warning in report["warnings"]),
                report,
            )
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
