import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from document_pipeline import (  # noqa: E402
    DocumentSpec,
    build_agent_lane_plan,
    detect_oracle_mode,
    extract_document_oracle,
    load_document_registry,
    parse_triage_report,
    registry_is_complete,
    render_document_coverage,
    render_document_gap_queue,
    resolve_logical_documents,
    summarize_triage_reports,
    transition_document_status,
)


FIXTURE_REGISTRY = ROOT / "tests" / "fixtures" / "synthetic_document_registry.yaml"


class DocumentPipelineTests(unittest.TestCase):
    def test_load_document_registry_sorts_by_priority(self) -> None:
        registry = load_document_registry(FIXTURE_REGISTRY)
        self.assertEqual(
            [doc["doc_id"] for doc in registry["documents"]],
            ["alpha_doc", "beta_doc", "gamma_doc"],
        )
        self.assertEqual(registry["orchestrator"]["lane_budget"]["review"], 2)
        self.assertEqual(registry["global_backlog"][0]["cluster_id"], "shared_cluster")

    def test_load_document_registry_rejects_duplicate_doc_ids(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "document-registry.yaml"
            path.write_text(
                json.dumps(
                    {
                        "documents": [
                            {
                                "doc_id": "dup_doc",
                                "title": "A",
                                "source_paths": ["Ref material/a.pdf"],
                                "domain_family": "qft",
                                "priority": 1,
                                "oracle_mode": "index",
                                "status": "unstarted",
                                "assigned_wave": None,
                                "last_checkpoint": None,
                                "coverage_state": "todo",
                                "blocking_issues": [],
                                "next_actions": ["scan"],
                            },
                            {
                                "doc_id": "dup_doc",
                                "title": "B",
                                "source_paths": ["Ref material/b.pdf"],
                                "domain_family": "qft",
                                "priority": 2,
                                "oracle_mode": "index",
                                "status": "unstarted",
                                "assigned_wave": None,
                                "last_checkpoint": None,
                                "coverage_state": "todo",
                                "blocking_issues": [],
                                "next_actions": ["scan"],
                            },
                        ]
                    }
                )
            )
            with self.assertRaisesRegex(ValueError, "Duplicate document id"):
                load_document_registry(path)

    def test_load_document_registry_rejects_duplicate_source_paths(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "document-registry.yaml"
            path.write_text(
                json.dumps(
                    {
                        "documents": [
                            {
                                "doc_id": "alpha",
                                "title": "A",
                                "source_paths": ["Ref material/shared.pdf"],
                                "domain_family": "qft",
                                "priority": 1,
                                "oracle_mode": "index",
                                "status": "unstarted",
                                "assigned_wave": None,
                                "last_checkpoint": None,
                                "coverage_state": "todo",
                                "blocking_issues": [],
                                "next_actions": ["scan"],
                            },
                            {
                                "doc_id": "beta",
                                "title": "B",
                                "source_paths": ["Ref material/shared.pdf"],
                                "domain_family": "qft",
                                "priority": 2,
                                "oracle_mode": "index",
                                "status": "unstarted",
                                "assigned_wave": None,
                                "last_checkpoint": None,
                                "coverage_state": "todo",
                                "blocking_issues": [],
                                "next_actions": ["scan"],
                            },
                        ]
                    }
                )
            )
            with self.assertRaisesRegex(ValueError, "Duplicate source path"):
                load_document_registry(path)

    def test_resolve_logical_documents_groups_split_sources(self) -> None:
        with TemporaryDirectory() as temp_dir:
            ref_root = Path(temp_dir)
            (ref_root / "Ref One.pdf").write_text("")
            (ref_root / "Nested").mkdir()
            (ref_root / "Nested" / "Part A.pdf").write_text("")
            (ref_root / "Nested" / "Part B.pdf").write_text("")
            specs = (
                DocumentSpec(
                    doc_id="doc_one",
                    title="Doc One",
                    source_patterns=("Ref One.pdf",),
                    domain_family="qft",
                    priority=2,
                    default_oracle_mode="index",
                ),
                DocumentSpec(
                    doc_id="doc_two",
                    title="Doc Two",
                    source_patterns=("Nested/*.pdf",),
                    domain_family="qft",
                    priority=1,
                    default_oracle_mode="hybrid",
                ),
            )
            documents = resolve_logical_documents(ref_root=ref_root, specs=specs)
            self.assertEqual([doc["doc_id"] for doc in documents], ["doc_two", "doc_one"])
            self.assertEqual(
                documents[0]["source_paths"],
                ["Nested/Part A.pdf", "Nested/Part B.pdf"],
            )

    def test_detect_oracle_mode_handles_index_toc_and_fallback(self) -> None:
        self.assertEqual(
            detect_oracle_mode([Path("doc_subject_index.pdf")]),
            "index",
        )
        self.assertEqual(
            detect_oracle_mode([Path("doc_subject_index.pdf"), Path("doc_contents.pdf")]),
            "hybrid",
        )
        self.assertEqual(
            detect_oracle_mode(
                [Path("doc.pdf")],
                scans=[{"front_has_contents": True, "tail_has_index": False}],
            ),
            "toc_fallback",
        )

    def test_transition_document_status_validates_progression(self) -> None:
        entry = {
            "status": "oracle_extracted",
        }
        self.assertEqual(
            transition_document_status(entry, "triaged")["status"],
            "triaged",
        )
        with self.assertRaisesRegex(ValueError, "Invalid document status transition"):
            transition_document_status(entry, "substantively_exhausted")

    def test_parse_triage_report_supports_bullets_and_classification_table(self) -> None:
        with TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "triage.md"
            report.write_text(
                "\n".join(
                    [
                        "## covered_existing",
                        "- LSZ reduction",
                        "## candidate_batch_expansion",
                        "| term | note |",
                        "| --- | --- |",
                        "| Jet function | SCET cluster |",
                        "| term | classification | match |",
                        "| --- | --- | --- |",
                        "| PMNS matrix | alias_candidate | sm.pmns_matrix |",
                    ]
                )
            )
            parsed = parse_triage_report(report)
            self.assertEqual(parsed["covered_existing"], ["LSZ reduction"])
            self.assertEqual(parsed["candidate_batch_expansion"], ["Jet function | SCET cluster"])
            self.assertEqual(parsed["alias_candidate"], ["PMNS matrix | sm.pmns_matrix"])

    def test_summarize_triage_reports_uses_filename_fallback(self) -> None:
        with TemporaryDirectory() as temp_dir:
            triage_dir = Path(temp_dir)
            (triage_dir / "chapter-alpha.md").write_text("## covered_existing\n- LSZ reduction\n")
            payload = summarize_triage_reports(triage_dir)
            self.assertEqual(payload["report_count"], 1)
            self.assertIn("chapter-alpha", payload["reports"])
            self.assertEqual(payload["totals"]["covered_existing"], 1)

    def test_extract_document_oracle_respects_declared_oracle_mode(self) -> None:
        document = {
            "doc_id": "alpha_doc",
            "title": "Alpha",
            "source_paths": ["Ref material/alpha.pdf"],
            "domain_family": "qft",
            "priority": 1,
            "oracle_mode": "index",
        }

        class DummyReader:
            pages = [object(), object(), object()]

        with TemporaryDirectory() as temp_dir:
            extracted_root = Path(temp_dir) / "extracted"
            oracle_root = Path(temp_dir) / "oracles"
            with patch("document_pipeline.scan_pdf_structure", return_value={"front_has_contents": True, "tail_has_index": False}), patch(
                "document_pipeline.detect_oracle_mode",
                return_value="toc_fallback",
            ), patch("document_pipeline._load_pdf_reader", return_value=DummyReader()), patch(
                "document_pipeline._find_marker_page",
                return_value=None,
            ):
                manifest = extract_document_oracle(
                    document,
                    extracted_root=extracted_root,
                    oracle_root=oracle_root,
                )
            self.assertEqual(manifest["oracle_mode"], "index")
            source_manifest = json.loads((extracted_root / "alpha_doc" / "source_manifest.json").read_text())
            self.assertEqual(source_manifest["declared_oracle_mode"], "index")
            self.assertEqual(source_manifest["detected_oracle_mode"], "toc_fallback")

    def test_lane_plan_and_completion_follow_registry_state(self) -> None:
        registry = load_document_registry(FIXTURE_REGISTRY)
        plan = build_agent_lane_plan(registry)
        self.assertFalse(registry_is_complete(registry))
        self.assertEqual(plan["lanes"]["content"][0]["doc_id"], "alpha_doc")
        self.assertEqual(plan["lanes"]["ingestion"][0]["doc_id"], "beta_doc")
        self.assertEqual(plan["lanes"]["review"][0]["doc_id"], "gamma_doc")
        self.assertEqual(plan["active_agents"], 3)

    def test_render_tracking_outputs_dashboard_and_gap_queue(self) -> None:
        registry = load_document_registry(FIXTURE_REGISTRY)
        coverage = render_document_coverage(registry)
        gap_queue = render_document_gap_queue(registry)
        self.assertIn("# Document Coverage Dashboard", coverage)
        self.assertIn("`alpha_doc`", coverage)
        self.assertIn("## Agent Plan", gap_queue)
        self.assertIn("## Reusable Backlog Clusters", gap_queue)
        self.assertIn("shared_cluster", gap_queue)


if __name__ == "__main__":
    unittest.main()
