#!/usr/bin/env python3
"""Shared helpers for the paper-reading pipeline."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
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


def derive_gap_explanation(gap: dict[str, Any]) -> str:
    """Build a concise background explanation for a gap concept."""

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
        for _, _, start, end in iter_command_arguments(search_text, {command}):
            return text[:start] + replacement + text[end:]
        return text.rstrip() + "\n" + replacement + "\n"

    updated = _replace_or_append(preamble, "title", title_command)
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


def load_analysis(paper_dir: Path) -> dict[str, Any]:
    """Load `analysis.yaml` from a paper directory."""

    path = paper_dir / "analysis.yaml"
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
