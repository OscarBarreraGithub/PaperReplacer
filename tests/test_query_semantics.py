import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kg_core import (  # noqa: E402
    expanded_slice,
    intrinsic_vs_profile_adjusted,
    prerequisite_set,
    prerequisites,
)


FIXTURE_PATH = ROOT / "tests" / "fixtures" / "synthetic_query_bundle.json"


class QuerySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = json.loads(FIXTURE_PATH.read_text())

    def test_prerequisites_do_not_cross_partonomy_by_default(self) -> None:
        result = prerequisites(
            self.bundle,
            "qft.pinch_singularities",
            "requires_for_use",
        )
        node_ids = {item["node_id"] for item in result["results"]}
        self.assertNotIn("qft.analytic_structure", node_ids)
        self.assertNotIn("qft.amplitude_analysis", node_ids)

    def test_overlay_adjustment_preserves_intrinsic_structure(self) -> None:
        result = intrinsic_vs_profile_adjusted(
            self.bundle,
            "qft.pinch_singularities",
            "requires_for_use",
            {
                "audience_profile": "hep_th_grad",
                "subfield": "amplitudes",
            },
        )
        self.assertIn(
            "complex_analysis.contour_deformation",
            result["intrinsic_prerequisites"],
        )
        self.assertIn(
            "complex_analysis.contour_deformation",
            result["presumed_by_profile"],
        )
        self.assertNotIn(
            "complex_analysis.contour_deformation",
            result["remaining_unmet_prerequisites"],
        )

    def test_frontier_returns_incomparable_leaves(self) -> None:
        result = prerequisite_set(
            self.bundle,
            "qft.pinch_singularities",
            "requires_for_use",
            "ancestral_frontier",
        )
        self.assertEqual(
            result["sets"][0],
            [
                "math.complex_variables",
                "qft.feynman_i_epsilon",
            ],
        )

    def test_expanded_slice_includes_partonomy_but_keeps_it_separate(self) -> None:
        result = expanded_slice(
            self.bundle,
            "qft.pinch_singularities",
            "requires_for_use",
        )
        self.assertIn("qft.analytic_structure", result["nodes"])
        self.assertTrue(
            any(edge["child"] == "qft.pinch_singularities" for edge in result["partonomy"])
        )
        self.assertTrue(
            any(
                edge["to"] == "qft.pinch_singularities"
                for edge in result["dependencies"]
            )
        )


if __name__ == "__main__":
    unittest.main()
