import io
import json
import sys
import tarfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from analyze_paper import analyze_paper  # noqa: E402
from annotate_paper import annotate_paper  # noqa: E402
from condense_paper import condense_paper  # noqa: E402
from paper_pipeline_common import (  # noqa: E402
    ensure_title_and_author_commands,
    extract_arxiv_id,
    extract_source_to_directory,
    find_best_insertion_line,
    load_main_tex,
    safe_extract_tarball,
    strip_comments,
)


def make_source_tarball() -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        files = {
            "paper/main.tex": (
                r"\documentclass{article}" "\n"
                r"\begin{document}" "\n"
                r"\input{sections/background}" "\n"
                r"\section{Main result}" "\n"
                r"We prove the main claim." "\n"
                r"\end{document}" "\n"
            ),
            "paper/sections/background.tex": (
                r"\section{Background}" "\n"
                r"Ward identities appear here." "\n"
                r"\input{details/note}" "\n"
            ),
            "paper/sections/details/note.tex": "Recursive note from include.\n",
            "paper/references.bib": "@article{demo, title={Demo}}\n",
        }
        for name, content in files.items():
            payload = content.encode("utf-8")
            info = tarfile.TarInfo(name=name)
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
    return buffer.getvalue()


class PaperPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.paper_dir = self.root / "paper"
        self.graph_path = self.root / "mini.graph.json"
        self.graph_path.write_text(
            json.dumps(
                {
                    "nodes": [
                        {
                            "id": "qft.ward_identity",
                            "label": "Ward identity",
                            "summary": "Constraint relating amplitudes or correlators to gauge symmetry.",
                        },
                        {
                            "id": "qft.soft_theorem",
                            "label": "Soft theorem",
                            "summary": "Universal low-energy limit governing emission of a soft quantum.",
                        },
                        {
                            "id": "technique.bootstrap_method",
                            "label": "Bootstrap method",
                            "summary": "Infer nontrivial constraints by enforcing consistency conditions.",
                        },
                    ],
                    "dependencies": [],
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_staged_paper(self) -> None:
        self.paper_dir.mkdir(parents=True, exist_ok=True)
        (self.paper_dir / "main.tex").write_text(
            "\n".join(
                [
                    r"\documentclass{article}",
                    r"\title{Demo paper}",
                    r"\author{A. Author}",
                    r"\begin{document}",
                    r"\maketitle",
                    r"\section{Ward identities and soft factors}",
                    r"The Ward identity organizes the gauge-theory constraints in our setup.",
                    r"\section{Stokes sectors}",
                    r"We use Stokes sectors without reviewing them in detail.",
                    r"\section{New resonance bootstrap construction}",
                    r"In this paper we introduce a resonance bootstrap construction for the model.",
                    r"\bibliography{references}",
                    r"\end{document}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (self.paper_dir / "metadata.yaml").write_text(
            yaml.safe_dump(
                {
                    "arxiv_id": "2401.12345",
                    "title": "Demo paper",
                    "authors": ["A. Author", "B. Author"],
                    "abstract": "A short abstract.",
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def test_extract_arxiv_id_handles_bare_and_url_forms(self) -> None:
        self.assertEqual(extract_arxiv_id("2401.12345"), "2401.12345")
        self.assertEqual(extract_arxiv_id("https://arxiv.org/abs/2401.12345"), "2401.12345")
        self.assertEqual(extract_arxiv_id("https://arxiv.org/pdf/2401.12345.pdf"), "2401.12345")
        self.assertEqual(extract_arxiv_id("hep-th/9802150"), "hep-th/9802150")
        self.assertEqual(extract_arxiv_id("https://arxiv.org/abs/hep-th/9802150"), "hep-th/9802150")
        self.assertEqual(extract_arxiv_id("https://arxiv.org/pdf/hep-th/9802150.pdf"), "hep-th/9802150")

    def test_extract_source_to_directory_writes_main_tex_and_metadata(self) -> None:
        metadata = {
            "arxiv_id": "2401.12345",
            "title": "Demo title",
            "authors": ["A. Author"],
            "abstract": "Demo abstract",
        }
        with patch("paper_pipeline_common.download_bytes", return_value=make_source_tarball()), patch(
            "paper_pipeline_common.fetch_arxiv_metadata",
            return_value=metadata,
        ), patch("paper_pipeline_common.http_last_modified", return_value="2026-03-27T00:00:00+00:00"):
            extract_source_to_directory("2401.12345", self.paper_dir)

        self.assertTrue((self.paper_dir / "main.tex").exists())
        self.assertTrue((self.paper_dir / "metadata.yaml").exists())
        self.assertTrue((self.paper_dir / "source" / "paper" / "sections" / "background.tex").exists())
        manifest = json.loads((self.paper_dir / "source_manifest.json").read_text(encoding="utf-8"))
        self.assertIn("paper/main.tex", manifest["tex_files"])
        rendered = load_main_tex(self.paper_dir)
        self.assertIn("Ward identities appear here.", rendered)
        self.assertIn("Recursive note from include.", rendered)
        self.assertNotIn(r"\input{sections/background}", rendered)

    def test_safe_extract_tarball_skips_link_members(self) -> None:
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
            payload = b"safe payload"
            regular = tarfile.TarInfo(name="safe.txt")
            regular.size = len(payload)
            archive.addfile(regular, io.BytesIO(payload))

            link = tarfile.TarInfo(name="unsafe-link")
            link.type = tarfile.SYMTYPE
            link.linkname = "../outside.txt"
            archive.addfile(link)

        buffer.seek(0)
        destination = self.root / "extract"
        destination.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=buffer, mode="r:gz") as archive:
            safe_extract_tarball(archive, destination)

        self.assertTrue((destination / "safe.txt").exists())
        self.assertFalse((destination / "unsafe-link").exists())

    def test_strip_comments_treats_double_backslash_percent_as_comment(self) -> None:
        tex = "line\\\\%comment\nnext line"
        self.assertEqual(strip_comments(tex), "line\\\\\nnext line")

    def test_ensure_title_and_author_commands_replaces_nested_brace_commands(self) -> None:
        preamble = "\n".join(
            [
                r"\documentclass{article}",
                r"\title{Old \texorpdfstring{Nested {brace} title}{Nested brace title}}",
                r"\author{Old Author \thanks{Supported by \emph{grants}}}",
                "",
            ]
        )

        updated = ensure_title_and_author_commands(preamble, "New Title", ["A. Author"])

        self.assertIn(r"\title{New Title}", updated)
        self.assertIn(r"\author{A. Author}", updated)
        self.assertIn(r"\date{}", updated)
        self.assertNotIn("texorpdfstring", updated)
        self.assertNotIn(r"\thanks{", updated)

    def test_find_best_insertion_line_skips_math_environments(self) -> None:
        lines = [
            r"\begin{document}",
            r"\begin{equation}",
            r"\text{Ward identity}",
            r"\end{equation}",
            r"The Ward identity appears in prose here.",
            r"\end{document}",
        ]

        self.assertEqual(find_best_insertion_line(lines, "Ward identity", start_index=2), 4)

    def test_analyze_paper_produces_in_graph_gap_and_novel_outputs(self) -> None:
        self.write_staged_paper()
        payload = analyze_paper(self.paper_dir, self.graph_path)

        classifications = {entry["classification"] for entry in payload["paper_concepts"]}
        self.assertIn("in_graph", classifications)
        self.assertIn("gap", classifications)
        self.assertIn("novel", classifications)

        matched_ids = {entry.get("matched_node_id") for entry in payload["paper_concepts"]}
        self.assertIn("qft.ward_identity", matched_ids)
        self.assertTrue(any(gap["concept"].lower() == "stokes sectors" for gap in payload["gaps"]))
        self.assertTrue(any("bootstrap" in item["concept"].lower() for item in payload["novel_contributions"]))
        self.assertEqual(len(payload["quiz_questions"]), 30)
        self.assertTrue((self.paper_dir / "prompts" / "analysis_review.yaml").exists())
        self.assertTrue((self.paper_dir / "prompts" / "quiz_generation.yaml").exists())

    def test_annotate_paper_inserts_blue_background_note(self) -> None:
        self.write_staged_paper()
        (self.paper_dir / "analysis.yaml").write_text(
            yaml.safe_dump(
                {
                    "gaps": [
                        {
                            "concept": "Stokes sectors",
                            "why_needed": "Used without review.",
                            "suggested_explanation": "Explain how Stokes sectors organize asymptotic behavior.",
                            "related_graph_nodes": [],
                        }
                    ]
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        output = annotate_paper(self.paper_dir, self.paper_dir / "annotated.tex")
        rendered = output.read_text(encoding="utf-8")
        self.assertIn(r"\usepackage{xcolor}", rendered)
        self.assertIn(r"\textcolor{blue}{\small [Background:", rendered)
        self.assertIn("Stokes sectors", rendered)
        self.assertTrue((self.paper_dir / "prompts" / "annotation_review.yaml").exists())

    def test_condense_paper_keeps_novel_section_and_condenses_background(self) -> None:
        self.write_staged_paper()
        (self.paper_dir / "analysis.yaml").write_text(
            yaml.safe_dump(
                {
                    "paper_concepts": [
                        {
                            "concept": "Ward identity",
                            "classification": "in_graph",
                            "matched_node_id": "qft.ward_identity",
                            "context_snippet": "Ward identity organizes the gauge-theory constraints.",
                        }
                    ],
                    "gaps": [
                        {
                            "concept": "Stokes sectors",
                            "why_needed": "Used without review.",
                            "suggested_explanation": "Explain how Stokes sectors govern asymptotic branches.",
                            "related_graph_nodes": [
                                {
                                    "id": "qft.soft_theorem",
                                    "label": "Soft theorem",
                                    "summary": "Universal low-energy limit governing emission of a soft quantum.",
                                }
                            ],
                        }
                    ],
                    "novel_contributions": [
                        {
                            "concept": "New resonance bootstrap construction",
                            "description": "The paper introduces a resonance bootstrap construction.",
                        }
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        output = condense_paper(self.paper_dir, self.paper_dir / "condensed.tex", self.graph_path)
        rendered = output.read_text(encoding="utf-8")
        self.assertIn(r"\section*{Reading guide}", rendered)
        self.assertIn(r"\section{New resonance bootstrap construction}", rendered)
        self.assertIn(r"\textit{Condensed background.}", rendered)
        self.assertIn(r"\section*{Prerequisites from knowledge graph}", rendered)
        self.assertIn("Stokes sectors", rendered)
        self.assertTrue((self.paper_dir / "prompts" / "condense_review.yaml").exists())


if __name__ == "__main__":
    unittest.main()
