import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from query_techniques import format_markdown_results, query_techniques  # noqa: E402


class QueryTechniquesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.graph_path = Path(self.temp_dir.name) / "mini.graph.json"
        graph = {
            "nodes": [
                {
                    "id": "concept.multiscale_loop_integral",
                    "label": "Multiscale loop integral",
                    "summary": "Two-scale one-loop integral with a small mass hierarchy.",
                },
                {
                    "id": "eft.scale_separation",
                    "label": "Scale separation",
                    "summary": "Separate distinct momentum and mass scales before expanding.",
                },
                {
                    "id": "concept.parameter_hierarchy",
                    "label": "Parameter hierarchy",
                    "summary": "A small parameter organizes an asymptotic expansion.",
                },
                {
                    "id": "technique.method_of_regions",
                    "label": "Method of regions",
                    "summary": "Expand a loop integral in hard and soft momentum regions for multiscale problems.",
                },
                {
                    "id": "technique.mellin_barnes_representation",
                    "label": "Mellin-Barnes (MB) representation",
                    "summary": "Rewrite denominators with contour integrals to support analytic continuation.",
                },
                {
                    "id": "technique.asymptotic_expansion_toolkit",
                    "label": "Asymptotic expansion toolkit",
                    "summary": "Organize calculations in a small parameter or mass hierarchy.",
                },
            ],
            "dependencies": [
                {
                    "from": "technique.method_of_regions",
                    "to": "concept.multiscale_loop_integral",
                    "relation_type": "requires_for_use",
                    "confidence": 0.95,
                },
                {
                    "from": "technique.method_of_regions",
                    "to": "eft.scale_separation",
                    "relation_type": "requires_for_use",
                    "confidence": 0.9,
                },
                {
                    "from": "technique.mellin_barnes_representation",
                    "to": "concept.multiscale_loop_integral",
                    "relation_type": "requires_for_use",
                    "confidence": 0.7,
                },
            ],
        }
        self.graph_path.write_text(json.dumps(graph))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_query_ranks_method_of_regions_first(self) -> None:
        results = query_techniques(
            "I need to evaluate a two-scale one-loop integral where one mass is much smaller than the external momentum",
            self.graph_path,
            top_n=5,
        )
        self.assertEqual(results[0]["id"], "technique.method_of_regions")
        self.assertGreaterEqual(results[0]["unlock_edge_count"], 2)
        unlocked_ids = {concept["id"] for concept in results[0]["unlocked_concepts"]}
        self.assertIn("concept.multiscale_loop_integral", unlocked_ids)
        self.assertIn("eft.scale_separation", unlocked_ids)

    def test_direct_text_match_can_surface_without_unlock_edge(self) -> None:
        results = query_techniques(
            "Need an asymptotic expansion with a small mass hierarchy",
            self.graph_path,
            top_n=5,
        )
        ids = [result["id"] for result in results]
        self.assertIn("technique.asymptotic_expansion_toolkit", ids)

    def test_markdown_formatter_mentions_unlocked_concepts(self) -> None:
        results = query_techniques(
            "two-scale one-loop integral with external momentum",
            self.graph_path,
            top_n=2,
        )
        rendered = format_markdown_results("two-scale one-loop integral with external momentum", results)
        self.assertIn("Method of regions", rendered)
        self.assertIn("Unlocks matched concepts", rendered)


if __name__ == "__main__":
    unittest.main()
