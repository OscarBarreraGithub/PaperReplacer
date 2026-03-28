#!/usr/bin/env python3
"""Shared helpers for the paper-reading pipeline."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from functools import lru_cache
import gzip
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import tarfile
import tempfile
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml

from query_techniques import (  # type: ignore[attr-defined]
    DEFAULT_GRAPH_PATH,
    _build_query_terms,
    _load_graph_index,
    _match_entry,
    _normalize_text,
    _should_keep_keyword,
    _sorted_matches,
    _tokenize,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "data" / "papers"
ARXIV_API_URL = "https://export.arxiv.org/api/query?id_list={arxiv_id}"
ARXIV_EPRINT_URL = "https://arxiv.org/e-print/{arxiv_id}"
DEFAULT_TIMEOUT_SECONDS = 30
USER_AGENT = "KnowledgeGraphPaperPipeline/1.0 (+https://github.com/openai/codex)"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
EQUATION_ENVIRONMENTS = (
    "equation",
    "equation*",
    "align",
    "align*",
    "gather",
    "gather*",
    "multline",
    "multline*",
    "eqnarray",
    "eqnarray*",
    "displaymath",
)
NOVELTY_MARKERS = (
    "we propose",
    "we present",
    "we introduce",
    "we derive",
    "we prove",
    "we show",
    "our result",
    "our results",
    "our contribution",
    "in this paper",
    "new method",
    "new theorem",
    "new construction",
)
BACKGROUND_TITLE_MARKERS = (
    "introduction",
    "background",
    "preliminaries",
    "notation",
    "review",
    "setup",
    "conventions",
    "motivation",
)
NOVEL_TITLE_MARKERS = (
    "result",
    "results",
    "theorem",
    "theorems",
    "method",
    "methods",
    "construction",
    "proof",
    "analysis",
    "application",
    "applications",
    "discussion",
    "conclusion",
    "algorithm",
)
LATEX_TEXT_COMMANDS = {
    "textbf",
    "textit",
    "textrm",
    "textsf",
    "texttt",
    "textsc",
    "textsl",
    "textup",
    "emph",
    "underline",
    "mbox",
    "mathrm",
    "mathbf",
    "mathit",
    "mathsf",
    "mathtt",
    "operatorname",
    "texorpdfstring",
}
ARXIV_ID_RE = re.compile(
    r"(?P<id>(?:\d{4}\.\d{4,5}|[A-Za-z\-]+(?:\.[A-Za-z\-]+)?/\d{7})(?:v\d+)?)"
)
PERSONALIZATION_EDGE_RELATIONS = {"requires_for_use", "requires_for_derive"}
PERSONALIZATION_BRIDGE_RELATIONS = PERSONALIZATION_EDGE_RELATIONS | {"requires_for_recognize"}
PERSONALIZATION_CONCEPT_NODE_ALIASES = {
    "Sector decomposition": "technique.generic_sector_decomposition",
    "Feynman-parameter and Baikov representations": "technique.feynman_parametrization",
    "Integration-by-parts reduction and master integrals": "technique.integration_by_parts_reduction",
    "Differential equations for master integrals": "technique.differential_equations_for_master_integrals",
    "Auxiliary-mass flow / AMFlow-style evaluation": "technique.differential_equations_for_master_integrals",
    "AMFlow evaluation": "technique.differential_equations_for_master_integrals",
    "Generalized polylogarithms and iterated integrals": "qft.iterated_integral",
    "GPLs and iterated integrals": "qft.iterated_integral",
    "Classical polylogarithms and logarithms": "qft.iterated_integral",
    "Classical polylogarithms": "qft.iterated_integral",
    "Symbol formalism": "qft.symbol_calculus",
    "Integrability constraints and transcendental weight": "technique.integrability_product_constraints",
    "Integrability constraints": "technique.integrability_product_constraints",
    "Leading singularities, maximal cuts, and algebraic prefactors": "technique.landau_bootstrap",
    "Leading singularities and maximal cuts": "technique.landau_bootstrap",
    "Kinematic variable rationalization": "complex_analysis.conformal_map",
    "Feynman integrals": "qft.loop_momentum_integration_structure",
    "Dimensional regularization and epsilon expansion": "qft.dimensional_regularization",
    "Landau singularities and symbol alphabets": "qft.landau_singularity_conditions",
    "Analytic continuation, branch cuts, and Euclidean kinematics": "qft.analytic_continuation_in_kinematic_invariants",
    "Linear algebra over the rationals and basis decompositions": "math.linear_algebra.basis_and_coordinates",
    "Lattice-reduction basics: LLL, L^2, shortest vector, Lovasz condition": "technique.lattice_reduction_analytic_regression",
}
PERSONALIZATION_EXPLANATION_HINTS = {
    "Sector decomposition": {
        "bridge_preferences": [
            "Dimensional regularization and epsilon expansion",
            "High-precision numerical evaluation",
        ],
        "mention_terms": ["sector decomposition"],
        "rating_2_sentence": (
            "In this paper, sector decomposition is the older strategy for isolating epsilon-singular integration regions before numerical integration, so it mainly serves as the benchmark that the AMFlow differential-equation pipeline is meant to beat."
        ),
    },
    "Feynman-parameter and Baikov representations": {
        "bridge_preferences": ["Feynman integrals", "Linear algebra over the rationals and basis decompositions"],
        "mention_terms": ["Feynman parameters", "Feynman parameter", "Baikov", "Baikov variables"],
        "rating_1_paragraph_1": (
            "A loop integral starts as an integral over loop momenta with many propagator denominators. "
            "Feynman parametrization combines those denominators into one denominator and trades the loop-momentum integrals for auxiliary parameters, while the Baikov representation uses inverse propagators and scalar products themselves as integration variables. "
            "Both rewritings expose where the singular regions and algebraic polynomials live, which is why they are standard starting points for direct numerical integration. "
            "In this paper the authors mention them to explain the naive route to numerical evaluation. "
            "After either rewrite, one still faces a genuinely multidimensional integral, so reaching the precision needed for exact reconstruction is usually expensive."
        ),
        "rating_1_bridge": (
            "These representations do not change the observable; they are alternate coordinate systems for the same regulated Feynman integral. "
            "If you think of the integral you already know as the fixed object, then parametrization is just a change of variables that makes some structures more visible and some computations easier. "
            "That perspective is why the paper can compare direct multidimensional integration with DE-based methods without changing the physics problem itself."
        ),
    },
    "Integration-by-parts reduction and master integrals": {
        "bridge_preferences": ["Feynman integrals", "Linear algebra over the rationals and basis decompositions"],
        "mention_terms": ["Integration-by-Parts", "IBP", "IBPs", "master integrals"],
        "rating_2_sentence": (
            "In this paper, IBP reduction is the step that collapses a large family of integrals to a finite master basis, so only the masters need to be computed numerically before the whole topology is reconstructed."
        ),
    },
    "Differential equations for master integrals": {
        "bridge_preferences": ["High-precision numerical evaluation", "Feynman integrals"],
        "mention_terms": ["differential equation", "differential equations", "DE", "master integrals"],
        "rating_2_sentence": (
            "In this paper, differential equations for master integrals are the mechanism that turns evaluation into solving a controlled flow from boundary data instead of directly attacking a high-dimensional integral."
        ),
    },
    "Auxiliary-mass flow / AMFlow-style evaluation": {
        "bridge_preferences": [
            "High-precision numerical evaluation",
            "Dimensional regularization and epsilon expansion",
        ],
        "manual_implicit_prerequisites": [
            "Differential equations for master integrals",
            "Integration-by-parts reduction and master integrals",
        ],
        "mention_terms": ["AMFlow", "auxiliary mass", "eta", "auxiliary-mass flow"],
        "rating_1_paragraph_1": (
            "AMFlow is a modern numerical pipeline for Feynman integrals that avoids direct high-dimensional integration. "
            "It introduces an auxiliary mass parameter, uses IBP identities to derive differential equations in that parameter, and starts from a boundary point where the integral becomes simpler, typically the large-mass limit. "
            "Solving that flow back to the physical point produces coefficients of the epsilon expansion to very high precision. "
            "In this paper those high-precision values are not the final answer; they are the data that analytic regression will later fit exactly. "
            "Without this picture, the source of the paper's trusted numerical samples stays opaque."
        ),
        "rating_1_bridge": (
            "You already know why hundreds of reliable digits matter when one wants exact rational reconstruction rather than a floating-point approximation. "
            "AMFlow is the machine that manufactures those digits for a regulated Feynman integral while respecting its singular structure. "
            "Conceptually, it plays the role of a precision-preserving oracle: lattice reduction is the recovery step, but AMFlow is what makes the sampled numbers good enough for that recovery to succeed."
        ),
    },
    "Generalized polylogarithms and iterated integrals": {
        "bridge_preferences": [
            "Lattice-reduction basics: LLL, L^2, shortest vector, Lovasz condition",
            "Feynman integrals",
        ],
        "mention_terms": ["Generalized Polylogarithms", "GPLs", "GPL", "iterated integrals"],
        "rating_2_sentence": (
            "In this paper, generalized polylogarithms are the basis functions whose rational coefficients are reconstructed from samples, so they play the same role on the function side that a lattice basis plays on the arithmetic side of the final fit."
        ),
    },
    "Classical polylogarithms and logarithms": {
        "bridge_preferences": [
            "Lattice-reduction basics: LLL, L^2, shortest vector, Lovasz condition",
            "PSLQ algorithm",
        ],
        "mention_terms": ["classical polylogarithms", "logarithms", "Li", "polylogarithms"],
        "rating_2_sentence": (
            "In this paper, logarithms and classical polylogarithms are the simplest explicit basis functions, giving toy examples where the regression problem is a cleaner version of the exact-reconstruction tasks you already know from lattice reduction and PSLQ."
        ),
    },
    "Symbol formalism": {
        "bridge_preferences": [
            "Landau singularities and symbol alphabets",
            "Analytic continuation, branch cuts, and Euclidean kinematics",
        ],
        "mention_terms": ["symbol formalism", "symbol", "symbols", "integrable symbols"],
        "rating_1_paragraph_1": (
            "The symbol of a polylogarithmic function is a tensor-like record of the ordered logarithmic letters that appear under repeated differentiation. "
            "It throws away additive constants such as zeta values and powers of pi, but it keeps the combinatorial structure that controls functional identities, branch cuts, and integrability. "
            "Because of that, symbols are much easier to enumerate and constrain than full GPL formulas. "
            "In this paper the authors first build spaces of allowed symbols, prune them with integrability and singularity information, and only later integrate the survivors back into actual functions. "
            "So the symbol is not just notation here; it is the working representation in which the candidate basis is constructed."
        ),
        "rating_1_bridge": (
            "You already know how Landau analysis supplies the alphabet of allowed letters. "
            "The symbol is the next layer up: it records ordered strings of those letters and therefore tracks how the function can branch as one moves across singular loci. "
            "If the alphabet tells you which letters are allowed, the symbol tells you which words the paper is allowed to spell with them. "
            "That is why Appendix B sits so close to the Landau-bootstrap logic you already recognize."
        ),
    },
    "Integrability constraints and transcendental weight": {
        "bridge_preferences": [
            "Landau singularities and symbol alphabets",
            "Linear algebra over the rationals and basis decompositions",
        ],
        "mention_terms": ["integrability", "integrable symbols", "transcendental weight", "weight"],
        "rating_2_sentence": (
            "In this paper, integrability constraints and weight grading are the filters that discard formal symbol combinations which cannot come from honest functions, sharply shrinking the basis before any coefficient fit is attempted."
        ),
    },
    "Leading singularities, maximal cuts, and algebraic prefactors": {
        "bridge_preferences": ["Landau singularities and symbol alphabets", "Feynman integrals"],
        "mention_terms": ["leading singularity", "leading singularities", "maximal cut", "prefactor"],
        "rating_2_sentence": (
            "In this paper, leading singularities and maximal cuts fix the algebraic prefactor multiplying the pure polylogarithmic part, so the regression only has to solve for rational coefficients of the remaining transcendental basis."
        ),
    },
    "Kinematic variable rationalization": {
        "bridge_preferences": [
            "Analytic continuation, branch cuts, and Euclidean kinematics",
            "Landau singularities and symbol alphabets",
        ],
        "mention_terms": ["rationalize", "rationalized", "change of variables", "w, z", "x, z", "zbar"],
        "rating_2_sentence": (
            "In this paper, rationalizing variables such as x, z, zbar, w, and z are chosen so that square roots in the alphabet become rational functions, which makes symbols and GPLs easier to integrate and evaluate."
        ),
    },
}


@dataclass(frozen=True)
class SectionBlock:
    """A parsed top-level section in a LaTeX document body."""

    level: str
    title_tex: str
    title_text: str
    heading_tex: str
    full_tex: str
    content_tex: str
    start: int
    end: int


@dataclass(frozen=True)
class CandidateConcept:
    """A candidate concept extracted from the paper."""

    concept: str
    context_snippet: str
    source: str
    weight: float
    novelty_score: float = 0.0


def utc_timestamp() -> str:
    """Return the current UTC time in ISO-8601 format."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_directory(path: Path) -> Path:
    """Create a directory if it does not already exist."""

    path.mkdir(parents=True, exist_ok=True)
    return path


def write_yaml_file(path: Path, payload: Any) -> None:
    """Write YAML with stable formatting."""

    ensure_directory(path.parent)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def read_yaml_file(path: Path) -> Any:
    """Read YAML content from disk."""

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sanitize_arxiv_id_for_path(arxiv_id: str) -> str:
    """Return a filesystem-safe directory name for an arXiv identifier."""

    return arxiv_id.replace("/", "_")


def default_paper_dir(arxiv_id: str) -> Path:
    """Return the default paper directory for an arXiv identifier."""

    return PAPERS_DIR / sanitize_arxiv_id_for_path(arxiv_id)


def extract_arxiv_id(value: str) -> str:
    """Extract a normalized arXiv identifier from a URL or raw identifier."""

    raw = value.strip()
    if not raw:
        raise ValueError("arXiv identifier must not be empty.")
    raw = raw.removeprefix("arXiv:")
    parsed = urlparse(raw)
    candidates: list[str] = []
    if parsed.scheme and parsed.netloc:
        for part in parsed.path.split("/"):
            if part:
                candidates.append(part.removesuffix(".pdf"))
    else:
        candidates.append(raw)
    for candidate in candidates:
        match = ARXIV_ID_RE.fullmatch(candidate.strip())
        if match:
            return match.group("id")
    match = ARXIV_ID_RE.search(raw)
    if match:
        return match.group("id")
    raise ValueError(f"Could not extract an arXiv identifier from: {value}")


def download_bytes(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> bytes:
    """Fetch raw bytes from a URL with basic error normalization."""

    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    except HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace").strip()
        detail = f" ({message})" if message else ""
        raise RuntimeError(f"HTTP {exc.code} while fetching {url}{detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error while fetching {url}: {exc.reason}") from exc


def http_last_modified(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> str | None:
    """Fetch the Last-Modified header for a URL if available."""

    request = Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.headers.get("Last-Modified")
    except Exception:
        return None
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).astimezone(timezone.utc).replace(microsecond=0).isoformat()
    except Exception:
        return raw


def read_text_file(path: Path) -> str:
    """Read text using a small set of fallback encodings."""

    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _count_preceding_backslashes(text: str, index: int) -> int:
    """Count consecutive backslashes immediately before an index."""

    count = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        count += 1
        cursor -= 1
    return count


def mask_comments(tex: str) -> str:
    """Mask LaTeX comments with spaces while preserving text offsets."""

    masked: list[str] = []
    index = 0
    while index < len(tex):
        if tex[index] == "%" and _count_preceding_backslashes(tex, index) % 2 == 0:
            while index < len(tex) and tex[index] not in "\r\n":
                masked.append(" ")
                index += 1
            continue
        masked.append(tex[index])
        index += 1
    return "".join(masked)


def strip_comments(tex: str) -> str:
    """Remove LaTeX comments while preserving escaped percent signs."""

    cleaned_lines: list[str] = []
    for line in tex.splitlines():
        pieces: list[str] = []
        index = 0
        while index < len(line):
            if line[index] == "%" and _count_preceding_backslashes(line, index) % 2 == 0:
                break
            pieces.append(line[index])
            index += 1
        cleaned_lines.append("".join(pieces))
    return "\n".join(cleaned_lines)


def _skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _read_group(text: str, start: int, open_char: str, close_char: str) -> tuple[str, int]:
    if start >= len(text) or text[start] != open_char:
        raise ValueError(f"Expected {open_char!r} at index {start}")
    depth = 0
    index = start
    buffer: list[str] = []
    while index < len(text):
        char = text[index]
        if char == "\\":
            if depth >= 1 and index + 1 < len(text):
                buffer.append(char)
                index += 1
                buffer.append(text[index])
                index += 1
                continue
        if char == open_char:
            depth += 1
            if depth > 1:
                buffer.append(char)
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return "".join(buffer), index + 1
            buffer.append(char)
        else:
            buffer.append(char)
        index += 1
    raise ValueError(f"Unterminated {open_char}{close_char} group starting at index {start}")


def iter_command_arguments(text: str, command_names: Iterable[str]) -> Iterable[tuple[str, str, int, int]]:
    """Yield LaTeX command arguments for the requested command names."""

    wanted = set(command_names)
    pattern = re.compile(r"\\([A-Za-z@]+)\*?")
    index = 0
    while True:
        match = pattern.search(text, index)
        if match is None:
            return
        command = match.group(1)
        if command not in wanted:
            index = match.end()
            continue
        cursor = _skip_whitespace(text, match.end())
        while cursor < len(text) and text[cursor] == "[":
            _, cursor = _read_group(text, cursor, "[", "]")
            cursor = _skip_whitespace(text, cursor)
        if cursor >= len(text) or text[cursor] != "{":
            index = match.end()
            continue
        argument, end = _read_group(text, cursor, "{", "}")
        yield command, argument, match.start(), end
        index = end


def unwrap_latex_text_commands(tex: str) -> str:
    """Replace simple formatting commands with their textual content."""

    updated = tex
    for _ in range(8):
        changed = False
        for command in LATEX_TEXT_COMMANDS:
            pattern = re.compile(rf"\\{command}\*?(?:\[[^\]]*\])?\{{([^{{}}]*)\}}")
            next_value, count = pattern.subn(r" \1 ", updated)
            if count:
                updated = next_value
                changed = True
        if not changed:
            break
    return updated


def tex_to_plain_text(tex: str) -> str:
    """Convert a LaTeX fragment into rough plain text."""

    text = strip_comments(tex)
    text = unwrap_latex_text_commands(text)
    text = re.sub(r"\\(?:cite|citet|citep|citealp|citeauthor|ref|eqref|autoref|cref|Cref|label)\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"\\url\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"\\href\{[^{}]*\}\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"\\[A-Za-z@]+", lambda match: f" {match.group(0)[1:]} ", text)
    text = text.replace("~", " ")
    text = text.replace("\\\\", " ")
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\\[(.*?)\\\]", r" \1 ", text, flags=re.DOTALL)
    text = text.replace("{", " ").replace("}", " ")
    text = text.replace("&", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def condense_whitespace(text: str) -> str:
    """Collapse whitespace into single spaces."""

    return re.sub(r"\s+", " ", text).strip()


def reference_key_to_phrase(value: str) -> str:
    """Turn a citation or label key into a readable phrase."""

    token = value.strip()
    if not token:
        return ""
    parts = token.split(":", 1)
    if len(parts) == 2 and len(parts[0]) <= 5:
        token = parts[1]
    token = re.sub(r"[_./-]+", " ", token)
    token = re.sub(r"([a-z])([A-Z])", r"\1 \2", token)
    token = re.sub(r"\d+", " ", token)
    return condense_whitespace(token)


def normalize_candidate_text(text: str) -> str:
    """Normalize candidate text for deduplication."""

    return _normalize_text(text)


@lru_cache(maxsize=1)
def personalization_hint_index() -> dict[str, dict[str, Any]]:
    """Return explanation hints keyed by normalized concept text."""

    return {
        normalize_candidate_text(concept): deepcopy(payload)
        for concept, payload in PERSONALIZATION_EXPLANATION_HINTS.items()
    }


@lru_cache(maxsize=1)
def personalization_alias_index() -> dict[str, str]:
    """Return graph-node aliases keyed by normalized concept text."""

    return {
        normalize_candidate_text(concept): node_id
        for concept, node_id in PERSONALIZATION_CONCEPT_NODE_ALIASES.items()
    }


def personalization_hint_for_concept(concept: str) -> dict[str, Any]:
    """Return pedagogical metadata for a concept when available."""

    return deepcopy(personalization_hint_index().get(normalize_candidate_text(concept), {}))


def significant_tokens(text: str) -> list[str]:
    """Return searchable tokens for a phrase."""

    return [token for token in _tokenize(text) if _should_keep_keyword(token)]


def snippet_from_text(text: str, limit: int = 220) -> str:
    """Build a compact human-readable context snippet."""

    compact = condense_whitespace(tex_to_plain_text(text))
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def safe_extract_tarball(tar: tarfile.TarFile, destination: Path) -> None:
    """Extract a tarball while rejecting path traversal and link entries."""

    destination = destination.resolve()
    safe_members: list[tarfile.TarInfo] = []
    for member in tar.getmembers():
        if member.issym() or member.islnk():
            continue
        target = (destination / member.name).resolve()
        if target != destination and destination not in target.parents:
            raise RuntimeError(f"Refusing to extract unsafe archive member: {member.name}")
        safe_members.append(member)
    tar.extractall(destination, members=safe_members)


def unpack_source_payload(payload: bytes, destination: Path) -> list[Path]:
    """Unpack an arXiv source payload into a destination directory."""

    ensure_directory(destination)
    extracted_files: list[Path] = []

    def _collect_files(root: Path) -> list[Path]:
        return [path for path in root.rglob("*") if path.is_file()]

    def _extract_bytes(data: bytes, root: Path, default_name: str) -> list[Path]:
        with BytesIO(data) as buffer:
            try:
                with tarfile.open(fileobj=buffer, mode="r:*") as archive:
                    safe_extract_tarball(archive, root)
                    return _collect_files(root)
            except tarfile.TarError:
                pass
        try:
            decompressed = gzip.decompress(data)
        except OSError:
            decompressed = None
        if decompressed is not None:
            nested_root = root / "content"
            ensure_directory(nested_root)
            nested = _extract_bytes(decompressed, nested_root, default_name)
            if nested:
                return nested
            output_path = nested_root / default_name
            output_path.write_bytes(decompressed)
            return [output_path]
        output_path = root / default_name
        output_path.write_bytes(data)
        return [output_path]

    extracted_files.extend(_extract_bytes(payload, destination, "source.tex"))
    return extracted_files


def find_tex_files(root: Path) -> list[Path]:
    """Return all LaTeX source files under a root directory."""

    return sorted(path for path in root.rglob("*.tex") if path.is_file())


def find_main_tex_file(paths: Iterable[Path]) -> Path:
    """Pick the most likely main LaTeX file from extracted sources."""

    scored: list[tuple[int, int, str, Path]] = []
    for path in paths:
        text = read_text_file(path)
        if r"\begin{document}" not in text:
            continue
        score = 0
        normalized_name = path.name.lower()
        if normalized_name in {"main.tex", "paper.tex", "ms.tex"}:
            score += 10
        if r"\title" in text:
            score += 4
        if r"\author" in text:
            score += 4
        if r"\maketitle" in text:
            score += 2
        score += max(0, 5 - len(path.parts))
        scored.append((score, len(text), str(path), path))
    if not scored:
        raise RuntimeError("Could not find a LaTeX source file containing \\begin{document}.")
    scored.sort(key=lambda item: (-item[0], -item[1], item[2]))
    return scored[0][3]


def copy_source_tree(source_root: Path, destination_root: Path) -> None:
    """Copy a source tree into the paper directory."""

    if destination_root.exists():
        shutil.rmtree(destination_root)
    shutil.copytree(source_root, destination_root)


def resolve_input_path(reference: str, source_dir: Path) -> Path | None:
    """Resolve a LaTeX input/include path relative to a source directory."""

    relative = reference.strip()
    if not relative:
        return None
    candidates = [source_dir / relative]
    if not Path(relative).suffix:
        candidates.append(source_dir / f"{relative}.tex")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def expand_inputs(
    tex_content: str,
    source_dir: Path,
    _stack: tuple[Path, ...] = (),
) -> str:
    """Recursively inline `\\input` and `\\include` directives."""

    search_text = mask_comments(tex_content)
    replacements: list[tuple[int, int, str]] = []
    for _, argument, start, end in iter_command_arguments(search_text, {"input", "include"}):
        include_path = resolve_input_path(argument, source_dir)
        if include_path is None:
            continue
        resolved_path = include_path.resolve()
        if resolved_path in _stack:
            continue
        expanded = expand_inputs(
            read_text_file(include_path),
            include_path.parent,
            _stack + (resolved_path,),
        )
        replacements.append((start, end, expanded))
    if not replacements:
        return tex_content

    pieces: list[str] = []
    cursor = 0
    for start, end, replacement in replacements:
        pieces.append(tex_content[cursor:start])
        pieces.append(replacement)
        cursor = end
    pieces.append(tex_content[cursor:])
    return "".join(pieces)


def fetch_arxiv_metadata(arxiv_id: str) -> dict[str, Any]:
    """Fetch title, authors, and abstract from the arXiv Atom API."""

    api_url = ARXIV_API_URL.format(arxiv_id=quote(arxiv_id))
    payload = download_bytes(api_url)
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise RuntimeError("Could not parse arXiv API response.") from exc

    entry = root.find("atom:entry", ATOM_NS)
    if entry is None:
        raise RuntimeError(f"No arXiv API entry found for {arxiv_id}.")

    def _entry_text(tag: str) -> str:
        node = entry.find(f"atom:{tag}", ATOM_NS)
        return condense_whitespace(node.text or "") if node is not None else ""

    authors = [
        condense_whitespace(author.findtext("atom:name", default="", namespaces=ATOM_NS))
        for author in entry.findall("atom:author", ATOM_NS)
    ]
    authors = [author for author in authors if author]

    metadata = {
        "arxiv_id": arxiv_id,
        "title": _entry_text("title"),
        "authors": authors,
        "abstract": _entry_text("summary"),
        "published": _entry_text("published"),
        "updated": _entry_text("updated"),
        "entry_id": _entry_text("id"),
        "api_url": api_url,
        "source_url": ARXIV_EPRINT_URL.format(arxiv_id=arxiv_id),
        "fetched_at": utc_timestamp(),
    }
    return metadata


def split_document(tex: str) -> tuple[str, str]:
    """Split a LaTeX document into preamble and body."""

    marker = r"\begin{document}"
    if marker not in tex:
        raise ValueError("Expected \\begin{document} in LaTeX source.")
    preamble, body = tex.split(marker, 1)
    return preamble, body


def split_body_and_bibliography(body: str) -> tuple[str, str]:
    """Separate the document body from bibliography commands if present."""

    patterns = [
        re.compile(r"\\begin\{thebibliography\}", re.MULTILINE),
        re.compile(r"\\printbibliography\b", re.MULTILINE),
        re.compile(r"\\bibliography\{", re.MULTILINE),
    ]
    earliest: re.Match[str] | None = None
    for pattern in patterns:
        match = pattern.search(body)
        if match is None:
            continue
        if earliest is None or match.start() < earliest.start():
            earliest = match
    if earliest is None:
        return body, ""
    return body[: earliest.start()], body[earliest.start() :]


def extract_abstract(body: str) -> str:
    """Extract the abstract environment if present."""

    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, flags=re.DOTALL)
    if match is None:
        return ""
    return match.group(0).strip()


def strip_abstract(body: str) -> str:
    """Remove the abstract environment from the body."""

    return re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", "", body, flags=re.DOTALL)


def parse_top_level_sections(body: str) -> list[SectionBlock]:
    """Parse top-level `\\section{...}` blocks from a LaTeX document body."""

    command_matches: list[tuple[int, int, str, str]] = []
    for command, argument, start, end in iter_command_arguments(body, {"section"}):
        heading_tex = body[start:end]
        title_tex = argument
        title_text = condense_whitespace(tex_to_plain_text(argument))
        command_matches.append((start, end, title_tex, title_text))

    if not command_matches:
        content = body.strip()
        if not content:
            return []
        return [
            SectionBlock(
                level="section",
                title_tex="Document Body",
                title_text="Document Body",
                heading_tex="",
                full_tex=content,
                content_tex=content,
                start=0,
                end=len(body),
            )
        ]

    sections: list[SectionBlock] = []
    for index, (start, end, title_tex, title_text) in enumerate(command_matches):
        section_end = command_matches[index + 1][0] if index + 1 < len(command_matches) else len(body)
        full_tex = body[start:section_end].strip()
        content_tex = body[end:section_end].strip()
        sections.append(
            SectionBlock(
                level="section",
                title_tex=title_tex,
                title_text=title_text,
                heading_tex=body[start:end],
                full_tex=full_tex,
                content_tex=content_tex,
                start=start,
                end=section_end,
            )
        )
    return sections


def extract_command_phrases(tex: str, commands: Iterable[str], source: str, weight: float) -> list[CandidateConcept]:
    """Extract concept candidates from command arguments."""

    candidates: list[CandidateConcept] = []
    for _, argument, start, end in iter_command_arguments(tex, commands):
        for raw_piece in argument.split(","):
            phrase = reference_key_to_phrase(raw_piece)
            if len(significant_tokens(phrase)) < 2:
                continue
            snippet_start = max(0, start - 120)
            snippet_end = min(len(tex), end + 120)
            candidates.append(
                CandidateConcept(
                    concept=phrase,
                    context_snippet=snippet_from_text(tex[snippet_start:snippet_end]),
                    source=source,
                    weight=weight,
                )
            )
    return candidates


def extract_equation_candidates(tex: str) -> list[CandidateConcept]:
    """Extract candidate concepts from equation environments."""

    candidates: list[CandidateConcept] = []
    patterns = [
        re.compile(rf"\\begin\{{{re.escape(name)}\}}(.*?)\\end\{{{re.escape(name)}\}}", re.DOTALL)
        for name in EQUATION_ENVIRONMENTS
    ]
    patterns.append(re.compile(r"\\\[(.*?)\\\]", re.DOTALL))
    for pattern in patterns:
        for match in pattern.finditer(tex):
            equation_tex = match.group(0)
            labels = extract_command_phrases(equation_tex, {"label"}, "equation_label", 5.0)
            candidates.extend(labels)
            text = condense_whitespace(tex_to_plain_text(equation_tex))
            if len(significant_tokens(text)) >= 3:
                candidates.append(
                    CandidateConcept(
                        concept=text,
                        context_snippet=snippet_from_text(equation_tex),
                        source="equation",
                        weight=3.0,
                    )
                )
    return candidates


def split_sentences(text: str) -> list[str]:
    """Split text into rough sentences."""

    replaced = text.replace("\n", " ")
    pieces = re.split(r"(?<=[.!?])\s+", replaced)
    return [piece.strip() for piece in pieces if piece.strip()]


def extract_frequent_phrases(text: str, limit: int = 24) -> list[CandidateConcept]:
    """Extract repeated content phrases from plain text."""

    counter: Counter[str] = Counter()
    snippets: dict[str, str] = {}
    for sentence in split_sentences(text):
        tokens = significant_tokens(sentence)
        if len(tokens) < 4:
            continue
        seen_in_sentence: set[str] = set()
        for size in (2, 3, 4):
            for index in range(len(tokens) - size + 1):
                phrase = " ".join(tokens[index : index + size])
                if phrase in seen_in_sentence:
                    continue
                seen_in_sentence.add(phrase)
                counter[phrase] += 1
                snippets.setdefault(phrase, snippet_from_text(sentence))
    candidates: list[CandidateConcept] = []
    for phrase, count in counter.most_common():
        if count < 2:
            continue
        candidates.append(
            CandidateConcept(
                concept=phrase,
                context_snippet=snippets[phrase],
                source="prose_ngram",
                weight=float(count),
            )
        )
        if len(candidates) >= limit:
            break
    return candidates


def extract_candidate_concepts(tex: str) -> list[CandidateConcept]:
    """Extract candidate concepts from section titles, refs, cites, equations, and prose."""

    body = strip_abstract(split_document(tex)[1])
    sections = parse_top_level_sections(body)
    candidates: list[CandidateConcept] = []
    for section in sections:
        if len(significant_tokens(section.title_text)) >= 2:
            novelty_bonus = 1.5 if is_probably_novel_section(section) else 0.0
            candidates.append(
                CandidateConcept(
                    concept=section.title_text,
                    context_snippet=snippet_from_text(section.full_tex),
                    source="section_title",
                    weight=7.0,
                    novelty_score=novelty_bonus,
                )
            )
            for fragment in re.split(r"[:;,()-]| and | with ", section.title_text):
                phrase = condense_whitespace(fragment)
                if phrase != section.title_text and len(significant_tokens(phrase)) >= 2:
                    candidates.append(
                        CandidateConcept(
                            concept=phrase,
                            context_snippet=snippet_from_text(section.full_tex),
                            source="section_fragment",
                            weight=5.0,
                            novelty_score=novelty_bonus,
                        )
                    )
    candidates.extend(extract_command_phrases(tex, {"subsection", "subsubsection"}, "subsection_title", 6.0))
    candidates.extend(extract_command_phrases(tex, {"ref", "eqref", "autoref", "cref", "Cref", "label"}, "reference", 4.0))
    candidates.extend(extract_command_phrases(tex, {"cite", "citet", "citep", "citealp", "citeauthor"}, "citation", 3.0))
    candidates.extend(extract_equation_candidates(tex))
    candidates.extend(extract_frequent_phrases(tex_to_plain_text(body)))
    return deduplicate_candidates(candidates)


def deduplicate_candidates(candidates: Iterable[CandidateConcept]) -> list[CandidateConcept]:
    """Merge duplicate concept candidates while keeping the strongest evidence."""

    best: dict[str, CandidateConcept] = {}
    for candidate in candidates:
        normalized = normalize_candidate_text(candidate.concept)
        if len(significant_tokens(normalized)) < 2:
            continue
        existing = best.get(normalized)
        if existing is None or (candidate.weight, candidate.novelty_score, len(candidate.context_snippet)) > (
            existing.weight,
            existing.novelty_score,
            len(existing.context_snippet),
        ):
            best[normalized] = candidate
    return sorted(
        best.values(),
        key=lambda item: (-item.weight, -item.novelty_score, item.concept.lower()),
    )


def graph_index(graph_path: str | Path = DEFAULT_GRAPH_PATH):
    """Load the compiled graph index."""

    return _load_graph_index(str(Path(graph_path).resolve()))


def match_text_against_graph(
    text: str,
    graph_path: str | Path = DEFAULT_GRAPH_PATH,
    top_n: int = 5,
    include_techniques: bool = True,
) -> list[Any]:
    """Return ranked graph matches for free text using query_techniques scoring."""

    terms = _build_query_terms(text)
    if not terms.tokens and not terms.phrases:
        return []
    index = graph_index(graph_path)
    node_ids: list[str] = list(index.concept_ids)
    if include_techniques:
        node_ids.extend(index.technique_ids)
    matches = []
    for node_id in node_ids:
        match = _match_entry(index.entries[node_id], terms, index.token_idf)
        if match is not None:
            matches.append(match)
    return _sorted_matches(matches)[:top_n]


def match_overlap(candidate_text: str, node_label: str, node_id: str) -> float:
    """Compute a rough overlap score between candidate text and a graph node."""

    candidate_tokens = set(significant_tokens(candidate_text))
    node_tokens = set(significant_tokens(f"{node_label} {node_id}"))
    if not candidate_tokens or not node_tokens:
        return 0.0
    shared = candidate_tokens & node_tokens
    return len(shared) / max(1, min(len(candidate_tokens), len(node_tokens)))


def is_strong_graph_match(candidate_text: str, match: Any, graph_path: str | Path = DEFAULT_GRAPH_PATH) -> bool:
    """Decide whether a match is strong enough to count as in-graph coverage."""

    index = graph_index(graph_path)
    entry = index.entries[match.node_id]
    candidate_normalized = normalize_candidate_text(candidate_text)
    overlap = match_overlap(candidate_text, match.label, match.node_id)
    if candidate_normalized and f" {candidate_normalized} " in f" {entry.search_text} ":
        return True
    if overlap >= 0.66:
        return True
    if match.keyword_hits >= 3 and match.keyword_score >= 4.5:
        return True
    return False


def node_match_payload(match: Any, graph_path: str | Path = DEFAULT_GRAPH_PATH) -> dict[str, Any]:
    """Serialize a node match for YAML output."""

    index = graph_index(graph_path)
    node = index.nodes[match.node_id]
    return {
        "id": match.node_id,
        "label": match.label or match.node_id,
        "summary": str(node.get("summary", "")),
        "keyword_hits": int(match.keyword_hits),
        "keyword_score": float(match.keyword_score),
        "matched_keywords": list(match.token_hits + match.phrase_hits),
    }


def related_graph_nodes(candidate_text: str, graph_path: str | Path = DEFAULT_GRAPH_PATH, limit: int = 3) -> list[dict[str, Any]]:
    """Return the closest graph nodes for a candidate concept."""

    matches = match_text_against_graph(candidate_text, graph_path=graph_path, top_n=limit)
    return [node_match_payload(match, graph_path=graph_path) for match in matches]


@lru_cache(maxsize=4)
def compiled_graph_payload(graph_path: str) -> dict[str, Any]:
    """Load the compiled graph JSON."""

    return json.loads(Path(graph_path).read_text(encoding="utf-8"))


@lru_cache(maxsize=4)
def compiled_graph_dependency_maps(
    graph_path: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, tuple[dict[str, Any], ...]], dict[str, tuple[dict[str, Any], ...]]]:
    """Return node and dependency lookup tables for the compiled graph."""

    graph = compiled_graph_payload(graph_path)
    nodes_by_id = {
        str(node["id"]): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph.get("dependencies", []):
        if not isinstance(edge, dict):
            continue
        from_id = str(edge.get("from", "")).strip()
        to_id = str(edge.get("to", "")).strip()
        if not from_id or not to_id:
            continue
        outgoing[from_id].append(edge)
        incoming[to_id].append(edge)
    return (
        nodes_by_id,
        {node_id: tuple(edges) for node_id, edges in incoming.items()},
        {node_id: tuple(edges) for node_id, edges in outgoing.items()},
    )


def _resolved_graph_path(graph_path: str | Path) -> str:
    return str(Path(graph_path).resolve())


def _topic_text(entry: dict[str, Any]) -> str:
    return str(entry.get("concept") or entry.get("topic") or "").strip()


def _topic_key(entry: dict[str, Any] | str) -> str:
    if isinstance(entry, dict):
        return normalize_candidate_text(_topic_text(entry))
    return normalize_candidate_text(str(entry))


def _profile_topics(user_profile: dict[str, Any]) -> list[dict[str, Any]]:
    ratings = user_profile.get("ratings")
    if isinstance(ratings, list):
        return [item for item in ratings if isinstance(item, dict)]
    combined = []
    for key in ("known_topics", "gap_topics", "strengths", "gaps"):
        values = user_profile.get(key)
        if isinstance(values, list):
            combined.extend(item for item in values if isinstance(item, dict))
    return combined


def resolve_graph_node_for_topic(topic: dict[str, Any], graph_path: str | Path = DEFAULT_GRAPH_PATH) -> str | None:
    """Resolve the best graph node for a topic or gap entry."""

    resolved_graph_path = _resolved_graph_path(graph_path)
    nodes_by_id, _, _ = compiled_graph_dependency_maps(resolved_graph_path)
    for field in ("resolved_graph_node", "graph_node", "matched_node_id"):
        node_id = str(topic.get(field) or "").strip()
        if node_id and node_id in nodes_by_id:
            return node_id
    for related in topic.get("related_graph_nodes") or []:
        if not isinstance(related, dict):
            continue
        node_id = str(related.get("id") or "").strip()
        if node_id and node_id in nodes_by_id:
            return node_id
    alias = personalization_alias_index().get(_topic_key(topic))
    if alias and alias in nodes_by_id:
        return alias
    for text in filter(None, [_topic_text(topic), str(topic.get("description") or "").strip()]):
        matches = match_text_against_graph(text, graph_path=resolved_graph_path, top_n=5)
        for match in matches:
            if is_strong_graph_match(text, match, graph_path=resolved_graph_path):
                return match.node_id
    return None


def _node_payload(node_id: str, graph_path: str | Path = DEFAULT_GRAPH_PATH) -> dict[str, Any]:
    """Serialize a graph node for personalization metadata."""

    resolved_graph_path = _resolved_graph_path(graph_path)
    nodes_by_id, _, _ = compiled_graph_dependency_maps(resolved_graph_path)
    node = nodes_by_id.get(node_id, {})
    label = str(node.get("label") or node_id)
    summary = condense_whitespace(str(node.get("summary") or ""))
    return {
        "id": node_id,
        "label": label,
        "summary": summary,
    }


def _resolved_profile_topics(
    user_profile: dict[str, Any],
    graph_path: str | Path = DEFAULT_GRAPH_PATH,
) -> list[dict[str, Any]]:
    """Attach resolved graph nodes to profile topics."""

    resolved: list[dict[str, Any]] = []
    for topic in _profile_topics(user_profile):
        entry = deepcopy(topic)
        entry["resolved_graph_node"] = resolve_graph_node_for_topic(entry, graph_path=graph_path)
        resolved.append(entry)
    return resolved


def _best_profile_entry(entries: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    bucket = [entry for entry in entries if isinstance(entry, dict)]
    if not bucket:
        return None
    return sorted(
        bucket,
        key=lambda item: (
            -int(item.get("rating", 0)),
            int(item.get("importance_rank", 99)),
            _topic_text(item).lower(),
        ),
    )[0]


def _profile_lookup_maps(
    resolved_topics: Iterable[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    by_key: dict[str, dict[str, Any]] = {}
    by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    known_topics: list[dict[str, Any]] = []
    for topic in resolved_topics:
        key = _topic_key(topic)
        if key:
            previous = by_key.get(key)
            by_key[key] = _best_profile_entry([entry for entry in (previous, topic) if entry is not None]) or topic
        node_id = str(topic.get("resolved_graph_node") or "").strip()
        if node_id:
            by_node[node_id].append(topic)
        if int(topic.get("rating", 0)) >= 3:
            known_topics.append(topic)
    return by_key, by_node, known_topics


def _build_implicit_gap_payload(
    node_id: str,
    node_payload: dict[str, Any],
    profile_entry: dict[str, Any] | None,
    depth: int,
    edge: dict[str, Any],
) -> dict[str, Any]:
    topic = _topic_text(profile_entry) if profile_entry is not None else str(node_payload.get("label") or node_id)
    profile_description = ""
    if profile_entry is not None:
        profile_description = str(profile_entry.get("description") or profile_entry.get("why_important") or "").strip()
    return {
        "topic": topic,
        "label": str(node_payload.get("label") or topic),
        "summary": profile_description or str(node_payload.get("summary") or "").strip(),
        "graph_node": node_id,
        "rating": int(profile_entry.get("rating", 0)) if profile_entry is not None else None,
        "depth": depth,
        "relation_type": str(edge.get("relation_type") or ""),
        "necessity": str(edge.get("necessity") or ""),
    }


def _build_bridge_anchor_payload(
    profile_entry: dict[str, Any],
    graph_node: str | None,
    graph_label: str,
    graph_summary: str,
    distance: int | None,
    reason: str,
) -> dict[str, Any]:
    return {
        "topic": _topic_text(profile_entry) or graph_label,
        "label": graph_label or _topic_text(profile_entry),
        "summary": str(profile_entry.get("why_important") or profile_entry.get("description") or graph_summary).strip(),
        "graph_node": graph_node,
        "rating": int(profile_entry.get("rating", 0)),
        "distance": distance,
        "reason": reason,
    }


def _unique_topic_payloads(items: Iterable[dict[str, Any]], key_fields: tuple[str, ...]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for item in items:
        key = tuple(normalize_candidate_text(str(item.get(field) or "")) for field in key_fields)
        if not any(key):
            continue
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _walk_upstream_prerequisites(
    start_node_id: str,
    profile_by_node: dict[str, list[dict[str, Any]]],
    graph_path: str | Path = DEFAULT_GRAPH_PATH,
    max_depth: int = 2,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Walk necessary upstream edges and collect implicit gaps plus known stop nodes."""

    resolved_graph_path = _resolved_graph_path(graph_path)
    nodes_by_id, incoming_edges, _ = compiled_graph_dependency_maps(resolved_graph_path)
    implicit: dict[str, dict[str, Any]] = {}
    anchors: dict[str, dict[str, Any]] = {}
    queue: deque[tuple[str, int]] = deque([(start_node_id, 0)])
    visited: set[str] = {start_node_id}

    while queue:
        node_id, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for edge in incoming_edges.get(node_id, ()):
            if str(edge.get("relation_type") or "") not in PERSONALIZATION_EDGE_RELATIONS:
                continue
            if str(edge.get("necessity") or "") != "necessary":
                continue
            parent_id = str(edge.get("from") or "").strip()
            if not parent_id or parent_id in visited:
                continue
            visited.add(parent_id)
            node_payload = _node_payload(parent_id, resolved_graph_path)
            profile_entry = _best_profile_entry(profile_by_node.get(parent_id, []))
            next_depth = depth + 1
            if profile_entry is not None and int(profile_entry.get("rating", 0)) >= 3:
                anchors[parent_id] = _build_bridge_anchor_payload(
                    profile_entry,
                    parent_id,
                    str(node_payload.get("label") or _topic_text(profile_entry)),
                    str(node_payload.get("summary") or ""),
                    next_depth,
                    "upstream_stop",
                )
                continue
            existing = implicit.get(parent_id)
            payload = _build_implicit_gap_payload(parent_id, node_payload, profile_entry, next_depth, edge)
            if existing is None or int(existing.get("depth", 99)) > next_depth:
                implicit[parent_id] = payload
            queue.append((parent_id, next_depth))

    implicit_items = sorted(
        implicit.values(),
        key=lambda item: (int(item.get("depth", 99)), str(item.get("topic") or item.get("label") or "").lower()),
    )
    anchor_items = sorted(
        anchors.values(),
        key=lambda item: (
            int(item.get("distance", 99) or 99),
            -int(item.get("rating", 0)),
            str(item.get("topic") or item.get("label") or "").lower(),
        ),
    )
    return implicit_items, anchor_items


def _find_closest_bridge_anchors(
    start_node_id: str,
    profile_by_node: dict[str, list[dict[str, Any]]],
    graph_path: str | Path = DEFAULT_GRAPH_PATH,
    max_depth: int = 2,
) -> list[dict[str, Any]]:
    """Find nearby known topics to use as bridge anchors."""

    resolved_graph_path = _resolved_graph_path(graph_path)
    nodes_by_id, incoming_edges, outgoing_edges = compiled_graph_dependency_maps(resolved_graph_path)
    anchors: dict[str, dict[str, Any]] = {}
    queue: deque[tuple[str, int]] = deque([(start_node_id, 0)])
    visited: set[str] = {start_node_id}

    while queue:
        node_id, depth = queue.popleft()
        if depth >= max_depth:
            continue
        neighbors: list[tuple[str, dict[str, Any]]] = []
        for edge in outgoing_edges.get(node_id, ()):
            relation_type = str(edge.get("relation_type") or "")
            necessity = str(edge.get("necessity") or "")
            if relation_type not in PERSONALIZATION_BRIDGE_RELATIONS:
                continue
            if necessity not in {"necessary", "typical"}:
                continue
            neighbor_id = str(edge.get("to") or "").strip()
            if neighbor_id:
                neighbors.append((neighbor_id, edge))
        for edge in incoming_edges.get(node_id, ()):
            relation_type = str(edge.get("relation_type") or "")
            necessity = str(edge.get("necessity") or "")
            if relation_type not in PERSONALIZATION_BRIDGE_RELATIONS:
                continue
            if necessity not in {"necessary", "typical"}:
                continue
            neighbor_id = str(edge.get("from") or "").strip()
            if neighbor_id:
                neighbors.append((neighbor_id, edge))
        for neighbor_id, _edge in neighbors:
            if neighbor_id in visited:
                continue
            visited.add(neighbor_id)
            next_depth = depth + 1
            profile_entry = _best_profile_entry(profile_by_node.get(neighbor_id, []))
            if profile_entry is not None and int(profile_entry.get("rating", 0)) >= 3:
                node_payload = _node_payload(neighbor_id, resolved_graph_path)
                current = anchors.get(neighbor_id)
                candidate = _build_bridge_anchor_payload(
                    profile_entry,
                    neighbor_id,
                    str(node_payload.get("label") or _topic_text(profile_entry)),
                    str(node_payload.get("summary") or ""),
                    next_depth,
                    "graph_neighbor",
                )
                if current is None or (
                    int(candidate.get("distance", 99) or 99),
                    -int(candidate.get("rating", 0)),
                ) < (
                    int(current.get("distance", 99) or 99),
                    -int(current.get("rating", 0)),
                ):
                    anchors[neighbor_id] = candidate
            queue.append((neighbor_id, next_depth))

    return sorted(
        anchors.values(),
        key=lambda item: (
            int(item.get("distance", 99) or 99),
            -int(item.get("rating", 0)),
            str(item.get("topic") or item.get("label") or "").lower(),
        ),
    )


def _find_preferred_bridge(
    concept: str,
    profile_by_key: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """Pick a hand-curated bridge anchor from the reader's known topics."""

    hints = personalization_hint_for_concept(concept)
    for preferred_topic in hints.get("bridge_preferences") or []:
        profile_entry = profile_by_key.get(normalize_candidate_text(preferred_topic))
        if profile_entry is None:
            continue
        if int(profile_entry.get("rating", 0)) < 3:
            continue
        resolved_node = str(profile_entry.get("resolved_graph_node") or "").strip() or None
        label = _topic_text(profile_entry)
        summary = str(profile_entry.get("why_important") or profile_entry.get("description") or "").strip()
        return _build_bridge_anchor_payload(
            profile_entry,
            resolved_node,
            label,
            summary,
            None,
            "preferred_bridge",
        )
    return None


def _manual_implicit_prerequisites(
    concept: str,
    profile_by_key: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return curated implicit prerequisites when the graph lacks a direct node."""

    hints = personalization_hint_for_concept(concept)
    payloads: list[dict[str, Any]] = []
    for prerequisite in hints.get("manual_implicit_prerequisites") or []:
        profile_entry = profile_by_key.get(normalize_candidate_text(prerequisite))
        if profile_entry is None or int(profile_entry.get("rating", 0)) >= 3:
            continue
        resolved_node = str(profile_entry.get("resolved_graph_node") or "").strip() or None
        payloads.append(
            {
                "topic": _topic_text(profile_entry),
                "label": _topic_text(profile_entry),
                "summary": str(profile_entry.get("description") or profile_entry.get("why_important") or "").strip(),
                "graph_node": resolved_node,
                "rating": int(profile_entry.get("rating", 0)),
                "depth": 1,
                "relation_type": "manual",
                "necessity": "necessary",
            }
        )
    return payloads


def expand_upstream_gaps(
    gap_topics: list[dict[str, Any]],
    user_profile: dict[str, Any],
    graph_path: str | Path,
) -> list[dict[str, Any]]:
    """
    Enrich gap topics with implicit prerequisites and bridge anchors.

    Rating-1 gaps expand upstream along necessary `requires_for_use` and
    `requires_for_derive` edges up to depth 2. Rating-2 gaps skip expansion but
    still receive the nearest bridge anchor.
    """

    resolved_graph_path = _resolved_graph_path(graph_path)
    resolved_topics = _resolved_profile_topics(user_profile, graph_path=resolved_graph_path)
    profile_by_key, profile_by_node, _known_topics = _profile_lookup_maps(resolved_topics)
    enriched_gaps: list[dict[str, Any]] = []

    for raw_gap in gap_topics:
        gap = deepcopy(raw_gap)
        profile_entry = profile_by_key.get(_topic_key(gap))
        if profile_entry is not None:
            for field in (
                "prerequisite_id",
                "description",
                "importance",
                "importance_label",
                "importance_rank",
                "rating",
                "rating_label",
                "rating_short_label",
                "why_important",
            ):
                if profile_entry.get(field) is not None and not gap.get(field):
                    gap[field] = profile_entry.get(field)
            gap.setdefault("profile_topic", _topic_text(profile_entry))
        concept = _topic_text(gap)
        if profile_entry is not None and not concept:
            concept = _topic_text(profile_entry)
            gap["concept"] = concept
        if not concept:
            continue
        rating = int(gap.get("rating", profile_entry.get("rating", 0) if profile_entry else 0) or 0)
        gap["rating"] = rating
        resolved_node = resolve_graph_node_for_topic(gap, graph_path=resolved_graph_path)
        if resolved_node is None and profile_entry is not None:
            resolved_node = str(profile_entry.get("resolved_graph_node") or "").strip() or None
        if resolved_node:
            gap["resolved_graph_node"] = resolved_node
        related_nodes = list(gap.get("related_graph_nodes") or [])
        if resolved_node and not any(str(item.get("id") or "").strip() == resolved_node for item in related_nodes if isinstance(item, dict)):
            related_nodes.insert(0, _node_payload(resolved_node, resolved_graph_path))
        gap["related_graph_nodes"] = related_nodes[:5]

        hints = personalization_hint_for_concept(concept)
        mention_terms = [concept]
        mention_terms.extend(str(term).strip() for term in gap.get("mention_terms") or [] if str(term).strip())
        mention_terms.extend(str(term).strip() for term in hints.get("mention_terms") or [] if str(term).strip())
        source_concept = str(gap.get("source_analysis_concept") or "").strip()
        if source_concept:
            mention_terms.append(source_concept)
        gap["mention_terms"] = list(dict.fromkeys(mention_terms))

        implicit_prerequisites: list[dict[str, Any]] = []
        bridge_anchors: list[dict[str, Any]] = []
        if rating <= 1 and resolved_node:
            implicit_prerequisites, bridge_anchors = _walk_upstream_prerequisites(
                resolved_node,
                profile_by_node,
                graph_path=resolved_graph_path,
            )
        elif rating == 2 and resolved_node:
            bridge_anchors = _find_closest_bridge_anchors(
                resolved_node,
                profile_by_node,
                graph_path=resolved_graph_path,
            )

        implicit_prerequisites.extend(_manual_implicit_prerequisites(concept, profile_by_key))
        implicit_prerequisites = _unique_topic_payloads(
            sorted(
                implicit_prerequisites,
                key=lambda item: (int(item.get("depth", 99)), str(item.get("topic") or "").lower()),
            ),
            ("topic", "graph_node"),
        )

        if rating <= 1 and resolved_node and not bridge_anchors:
            bridge_anchors = _find_closest_bridge_anchors(
                resolved_node,
                profile_by_node,
                graph_path=resolved_graph_path,
                max_depth=3,
            )
        preferred_bridge = _find_preferred_bridge(concept, profile_by_key)
        if preferred_bridge is not None:
            bridge_anchors = [preferred_bridge, *bridge_anchors]
        bridge_anchors = _unique_topic_payloads(bridge_anchors, ("topic", "graph_node"))
        if rating == 2 and bridge_anchors:
            bridge_anchors = bridge_anchors[:1]

        gap["implicit_prerequisites"] = implicit_prerequisites
        gap["bridge_anchors"] = bridge_anchors
        if bridge_anchors:
            gap["bridge_anchor"] = bridge_anchors[0]
        enriched_gaps.append(gap)

    return enriched_gaps


def extract_novel_contributions(tex: str, graph_path: str | Path = DEFAULT_GRAPH_PATH) -> list[dict[str, str]]:
    """Extract likely novel contributions from novelty-heavy sections."""

    body = strip_abstract(split_document(tex)[1])
    sections = parse_top_level_sections(body)
    contributions: list[dict[str, str]] = []
    seen: set[str] = set()
    for section in sections:
        if not is_probably_novel_section(section):
            continue
        title = section.title_text
        normalized_title = normalize_candidate_text(title)
        if normalized_title and normalized_title not in seen and len(significant_tokens(title)) >= 2:
            seen.add(normalized_title)
            contributions.append(
                {
                    "concept": title,
                    "description": build_novel_description(section, graph_path=graph_path),
                }
            )
        for sentence in split_sentences(tex_to_plain_text(section.content_tex)):
            lowered = sentence.lower()
            if not any(marker in lowered for marker in NOVELTY_MARKERS):
                continue
            phrase = sentence
            if len(significant_tokens(phrase)) < 4:
                continue
            normalized_phrase = normalize_candidate_text(phrase)
            if normalized_phrase in seen:
                continue
            seen.add(normalized_phrase)
            contributions.append(
                {
                    "concept": condense_whitespace(phrase[:160]),
                    "description": condense_whitespace(sentence),
                }
            )
            if len(contributions) >= 12:
                return contributions
    return contributions


def build_novel_description(section: SectionBlock, graph_path: str | Path = DEFAULT_GRAPH_PATH) -> str:
    """Build a concise description for a novel section."""

    first_sentences = split_sentences(tex_to_plain_text(section.content_tex))[:2]
    base = condense_whitespace(" ".join(first_sentences))
    if not base:
        base = f"This section develops {section.title_text.lower()}."
    matches = related_graph_nodes(section.title_text, graph_path=graph_path, limit=2)
    if not matches:
        return base
    related_labels = ", ".join(match["label"] for match in matches)
    return f"{base} It appears to extend or recombine background from {related_labels}."


def is_probably_novel_section(section: SectionBlock) -> bool:
    """Heuristically classify whether a section likely contains novel work."""

    title_lower = section.title_text.lower()
    body_lower = tex_to_plain_text(section.content_tex[:2500]).lower()
    title_hits = sum(marker in title_lower for marker in NOVEL_TITLE_MARKERS)
    novelty_hits = sum(marker in body_lower for marker in NOVELTY_MARKERS)
    background_hits = sum(marker in title_lower for marker in BACKGROUND_TITLE_MARKERS)
    if title_hits >= 1 and background_hits == 0:
        return True
    return novelty_hits >= 2 and background_hits == 0


def is_background_section(section: SectionBlock) -> bool:
    """Heuristically classify whether a section is mostly background."""

    title_lower = section.title_text.lower()
    if any(marker in title_lower for marker in BACKGROUND_TITLE_MARKERS):
        return True
    if is_probably_novel_section(section):
        return False
    body_lower = tex_to_plain_text(section.content_tex[:1800]).lower()
    novelty_hits = sum(marker in body_lower for marker in NOVELTY_MARKERS)
    return novelty_hits == 0


def _bridge_anchor_name(gap: dict[str, Any]) -> str | None:
    anchor = gap.get("bridge_anchor")
    if isinstance(anchor, dict):
        topic = str(anchor.get("topic") or anchor.get("label") or "").strip()
        if topic:
            return topic
    anchors = gap.get("bridge_anchors") or []
    if isinstance(anchors, list):
        for item in anchors:
            if not isinstance(item, dict):
                continue
            topic = str(item.get("topic") or item.get("label") or "").strip()
            if topic:
                return topic
    return None


def _gap_reason(gap: dict[str, Any]) -> str:
    return condense_whitespace(
        str(
            gap.get("why_important")
            or gap.get("why_needed")
            or gap.get("role_in_paper")
            or gap.get("description")
            or gap.get("context_snippet")
            or ""
        )
    )


def _gap_prerequisite_names(gap: dict[str, Any], limit: int = 3) -> list[str]:
    names: list[str] = []
    for prerequisite in gap.get("implicit_prerequisites") or []:
        if not isinstance(prerequisite, dict):
            continue
        label = str(prerequisite.get("topic") or prerequisite.get("label") or "").strip()
        if label:
            names.append(label)
        if len(names) >= limit:
            break
    return names


def _fallback_rating_1_explanation(gap: dict[str, Any]) -> str:
    concept = str(gap.get("concept") or gap.get("topic") or "This topic").strip()
    reason = _gap_reason(gap)
    bridge_name = _bridge_anchor_name(gap) or "material you already know"
    prerequisites = _gap_prerequisite_names(gap)
    prerequisite_clause = ""
    if prerequisites:
        prerequisite_clause = (
            " To use it comfortably in this paper, it helps to already have "
            + ", ".join(prerequisites)
            + " in view."
        )
    paragraph_1 = (
        f"{concept} is part of the background machinery the paper assumes rather than rederives. "
        f"It matters here because {reason or f'the authors rely on {concept.lower()} when they set up the analytic-regression pipeline.'} "
        f"The key reading move is to treat it as a tool that reshapes the computation so later numerical or symbolic steps become manageable."
        f"{prerequisite_clause} "
        f"Once that role is clear, the later formulas read as applications of the tool rather than as isolated tricks."
    )
    paragraph_2 = (
        f"Connection to {bridge_name}. "
        f"The paper is not introducing {concept.lower()} as a disconnected new object; it plugs directly into the parts of the workflow you already know better. "
        f"Use {bridge_name} as the anchor, then read {concept.lower()} as the extra structure that makes that familiar part of the pipeline possible or more efficient in this specific problem."
    )
    return f"{condense_whitespace(paragraph_1)}\n\n{condense_whitespace(paragraph_2)}"


def _fallback_rating_2_explanation(gap: dict[str, Any]) -> str:
    concept = str(gap.get("concept") or gap.get("topic") or "this topic").strip()
    reason = _gap_reason(gap)
    if reason:
        return f"In this paper, {concept} is used to {reason[0].lower() + reason[1:] if len(reason) > 1 else reason.lower()}."
    return f"In this paper, {concept} is used as local background for the analytic-regression workflow rather than being derived from scratch."


def derive_rating_aware_gap_explanation(gap: dict[str, Any]) -> str:
    """Build a pedagogical explanation that respects the reader's rating."""

    concept = str(gap.get("concept") or gap.get("topic") or "").strip()
    hints = personalization_hint_for_concept(concept)
    rating = int(gap.get("rating", 0) or 0)
    bridge_name = _bridge_anchor_name(gap)
    if rating <= 1:
        paragraph_1 = condense_whitespace(str(hints.get("rating_1_paragraph_1") or ""))
        if not paragraph_1:
            return _fallback_rating_1_explanation(gap)
        bridge_body = condense_whitespace(str(hints.get("rating_1_bridge") or ""))
        if bridge_name:
            paragraph_2 = f"Connection to {bridge_name}. {bridge_body or ''}".strip()
        else:
            paragraph_2 = bridge_body or "Connection to the paper's better-known ingredients makes this topic easier to place."
        return f"{paragraph_1}\n\n{condense_whitespace(paragraph_2)}"
    if rating == 2:
        sentence = condense_whitespace(str(hints.get("rating_2_sentence") or ""))
        return sentence or _fallback_rating_2_explanation(gap)
    return condense_whitespace(str(gap.get("suggested_explanation") or "")) or _fallback_rating_2_explanation(gap)


def derive_gap_explanation(gap: dict[str, Any]) -> str:
    """Build a background explanation for a gap concept."""

    explanation = str(gap.get("pedagogical_explanation") or "").strip()
    if explanation:
        return explanation
    rating = int(gap.get("rating", 0) or 0)
    if rating in {1, 2}:
        return derive_rating_aware_gap_explanation(gap)
    explanation = condense_whitespace(str(gap.get("suggested_explanation", "")))
    if explanation:
        return explanation
    concept = str(gap.get("concept", "")).strip()
    related = gap.get("related_graph_nodes") or []
    if related:
        first = related[0]
        label = str(first.get("label", first.get("id", "")))
        summary = condense_whitespace(str(first.get("summary", "")))
        if summary:
            return f"{concept} is used here without review; connect it to {label}: {summary}"
        return f"{concept} is used here without review; relate it to {label} from the knowledge graph."
    return f"{concept} is used here without review; add a brief prerequisite explanation before continuing."


def escape_latex_text(text: str) -> str:
    """Escape text for safe insertion into LaTeX prose."""

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def escape_latex_paragraphs(text: str) -> str:
    """Escape prose while preserving paragraph breaks with `\\par`."""

    paragraphs = [
        escape_latex_text(condense_whitespace(paragraph))
        for paragraph in re.split(r"\n\s*\n", text)
        if condense_whitespace(paragraph)
    ]
    return r"\par ".join(paragraphs)


def find_document_body_start_line(lines: list[str]) -> int:
    """Return the line index immediately after `\\begin{document}` if present."""

    for index, line in enumerate(lines):
        if r"\begin{document}" in line:
            return index + 1
    return 0


def find_best_insertion_line(lines: list[str], concept: str, start_index: int = 0) -> int | None:
    """Return the first line that best matches a concept mention."""

    normalized_phrase = normalize_candidate_text(concept)
    tokens = set(significant_tokens(concept))
    best_index: int | None = None
    best_score = -1.0
    math_environment_pattern = re.compile(
        rf"\\(?:begin|end)\{{(?:{'|'.join(re.escape(name) for name in EQUATION_ENVIRONMENTS)})\}}|\\\[|\\\]"
    )
    math_depth = 0
    display_math_depth = 0
    for index, line in enumerate(lines):
        line = lines[index]
        scan_line = strip_comments(line)
        line_in_math = math_depth > 0 or display_math_depth > 0
        for match in math_environment_pattern.finditer(scan_line):
            token = match.group(0)
            line_in_math = True
            if token == r"\[":
                display_math_depth += 1
            elif token == r"\]":
                display_math_depth = max(0, display_math_depth - 1)
            elif token.startswith(r"\begin"):
                math_depth += 1
            else:
                math_depth = max(0, math_depth - 1)
        if index < start_index:
            continue
        stripped = line.strip()
        if line_in_math or not stripped or stripped.startswith("%"):
            continue
        normalized_line = normalize_candidate_text(line)
        if normalized_phrase and normalized_phrase in normalized_line:
            return index
        line_tokens = set(significant_tokens(line))
        overlap = len(tokens & line_tokens)
        if not overlap:
            continue
        score = float(overlap)
        if stripped.startswith("\\section") or stripped.startswith("\\subsection"):
            score += 0.5
        if score > best_score:
            best_score = score
            best_index = index
    if best_score >= 2.0:
        return best_index
    return None


def ensure_usepackage(tex: str, package_name: str) -> str:
    """Ensure a LaTeX preamble contains a package import."""

    package_pattern = re.compile(rf"\\usepackage(?:\[[^\]]*\])?\{{[^}}]*\b{re.escape(package_name)}\b[^}}]*\}}")
    if package_pattern.search(tex):
        return tex
    preamble, body = split_document(tex)
    insertion = f"\\usepackage{{{package_name}}}\n"
    return f"{preamble.rstrip()}\n{insertion}\n\\begin{{document}}{body}"


def ensure_title_and_author_commands(preamble: str, title: str, authors: list[str]) -> str:
    """Replace or inject `\\title`, `\\author`, and `\\date` commands."""

    title_command = f"\\title{{{escape_latex_text(title)}}}"
    author_text = " \\\\ ".join(escape_latex_text(author) for author in authors) if authors else "Unknown authors"
    author_command = f"\\author{{{author_text}}}"
    date_command = "\\date{}"

    def _replace_or_append(text: str, command: str, replacement: str) -> str:
        search_text = mask_comments(text)
        matches = list(iter_command_arguments(search_text, {command}))
        if matches:
            first_start = matches[0][2]
            first_end = matches[0][3]
            updated = text[:first_start] + replacement + text[first_end:]
            offset = len(replacement) - (first_end - first_start)
            for _, _, start, end in matches[1:]:
                adjusted_start = start + offset
                adjusted_end = end + offset
                updated = updated[:adjusted_start] + updated[adjusted_end:]
                offset -= adjusted_end - adjusted_start
            return updated
        return text.rstrip() + "\n" + replacement + "\n"

    updated = _replace_or_append(preamble, "title", title_command)
    if "\\affiliation" not in updated and "\\emailAdd" not in updated:
        updated = _replace_or_append(updated, "author", author_command)
    updated = _replace_or_append(updated, "date", date_command)
    return updated


def paper_prompts_dir(paper_dir: Path) -> Path:
    """Return the prompts directory for a paper."""

    return ensure_directory(paper_dir / "prompts")


def write_structured_prompt(paper_dir: Path, name: str, payload: dict[str, Any]) -> Path:
    """Write a structured YAML prompt to the paper prompt directory."""

    path = paper_prompts_dir(paper_dir) / f"{name}.yaml"
    write_yaml_file(path, payload)
    return path


def load_metadata(paper_dir: Path) -> dict[str, Any]:
    """Load `metadata.yaml` from a paper directory."""

    path = paper_dir / "metadata.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Missing metadata file: {path}")
    payload = read_yaml_file(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


def load_analysis(paper_dir: Path, analysis_path: str | Path | None = None) -> dict[str, Any]:
    """Load an analysis YAML payload for a paper directory."""

    path = Path(analysis_path) if analysis_path is not None else paper_dir / "analysis.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Missing analysis file: {path}")
    payload = read_yaml_file(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


def load_main_tex(paper_dir: Path) -> str:
    """Load `main.tex` from a paper directory."""

    path = paper_dir / "main.tex"
    if not path.exists():
        raise FileNotFoundError(f"Missing main.tex file: {path}")
    tex = read_text_file(path)

    source_dir = paper_dir
    metadata_path = paper_dir / "metadata.yaml"
    if metadata_path.exists():
        try:
            metadata = read_yaml_file(metadata_path)
        except Exception:
            metadata = None
        if isinstance(metadata, dict):
            relative_main = str(metadata.get("main_source_file", "")).strip()
            if relative_main:
                candidate = paper_dir / "source" / relative_main
                if candidate.exists():
                    source_dir = candidate.parent
            elif (paper_dir / "source").exists():
                source_dir = paper_dir / "source"
    elif (paper_dir / "source").exists():
        source_dir = paper_dir / "source"

    return expand_inputs(tex, source_dir)


def top_unique_graph_concepts(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Return unique in-graph concepts from an analysis payload."""

    concepts = analysis.get("paper_concepts") or []
    buckets: dict[str, dict[str, Any]] = {}
    for concept in concepts:
        if not isinstance(concept, dict):
            continue
        if concept.get("classification") != "in_graph":
            continue
        node_id = concept.get("matched_node_id")
        if not node_id:
            continue
        buckets.setdefault(
            str(node_id),
            {
                "id": str(node_id),
                "concept": str(concept.get("concept", "")),
                "context_snippet": str(concept.get("context_snippet", "")),
            },
        )
    return sorted(buckets.values(), key=lambda item: item["concept"].lower())


def summarize_section_with_graph(section: SectionBlock, graph_path: str | Path = DEFAULT_GRAPH_PATH, limit: int = 3) -> str:
    """Summarize a background section and attach graph node references."""

    matches = match_text_against_graph(f"{section.title_text}\n{tex_to_plain_text(section.content_tex[:1800])}", graph_path=graph_path, top_n=limit)
    if matches:
        labels = ", ".join(f"{match.label} ({match.node_id})" for match in matches)
        return f"This section is condensed to background on {labels}. Consult the knowledge graph nodes for the fuller prerequisite story."
    return "This section is condensed because it is mostly background relative to the paper's main contributions."


def build_prerequisite_appendix_items(analysis: dict[str, Any]) -> list[str]:
    """Build appendix lines listing graph-backed prerequisites."""

    items: list[str] = []
    seen: set[str] = set()
    for concept in analysis.get("paper_concepts") or []:
        if not isinstance(concept, dict):
            continue
        if concept.get("classification") != "in_graph":
            continue
        node_id = str(concept.get("matched_node_id", "")).strip()
        if not node_id or node_id in seen:
            continue
        seen.add(node_id)
        label = str(concept.get("concept", "")).strip() or node_id
        items.append(f"{label} ({node_id})")
    for gap in analysis.get("gaps") or []:
        if not isinstance(gap, dict):
            continue
        for related in gap.get("related_graph_nodes") or []:
            node_id = str(related.get("id", "")).strip()
            if not node_id or node_id in seen:
                continue
            seen.add(node_id)
            label = str(related.get("label", node_id))
            items.append(f"{label} ({node_id})")
    return sorted(items, key=str.lower)


def write_json_file(path: Path, payload: Any) -> None:
    """Write indented JSON to disk."""

    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def extract_source_to_directory(arxiv_id: str, out_dir: Path) -> dict[str, Any]:
    """Download and unpack an arXiv source bundle into a paper directory."""

    source_url = ARXIV_EPRINT_URL.format(arxiv_id=arxiv_id)
    metadata = fetch_arxiv_metadata(arxiv_id)
    payload = download_bytes(source_url)
    metadata["source_last_modified"] = http_last_modified(source_url)
    with tempfile.TemporaryDirectory(prefix="paper-source-") as temp_dir:
        temp_root = Path(temp_dir)
        extracted_root = temp_root / "source"
        unpack_source_payload(payload, extracted_root)
        tex_files = find_tex_files(extracted_root)
        if not tex_files:
            raise RuntimeError("Downloaded source did not contain any .tex files.")
        main_tex_path = find_main_tex_file(tex_files)

        ensure_directory(out_dir)
        copy_source_tree(extracted_root, out_dir / "source")
        relative_main = main_tex_path.relative_to(extracted_root)
        main_tex_text = expand_inputs(read_text_file(main_tex_path), main_tex_path.parent)
        (out_dir / "main.tex").write_text(main_tex_text, encoding="utf-8")
        metadata["main_source_file"] = str(relative_main)
        metadata["paper_dir"] = str(out_dir)
        metadata["downloaded_at"] = utc_timestamp()
        write_yaml_file(out_dir / "metadata.yaml", metadata)
        write_json_file(
            out_dir / "source_manifest.json",
            {
                "arxiv_id": arxiv_id,
                "downloaded_at": metadata["downloaded_at"],
                "source_url": source_url,
                "main_source_file": str(relative_main),
                "tex_files": [str(path.relative_to(extracted_root)) for path in tex_files],
            },
        )
    return metadata
