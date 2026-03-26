#!/usr/bin/env python3
"""Extract the Schwartz QFT back-of-book index into machine-readable files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "Ref material" / "Schwartz QFT.pdf"
DEFAULT_JSON = ROOT / "data" / "generated" / "extracted" / "schwartz_index.json"
DEFAULT_TXT = ROOT / "data" / "generated" / "extracted" / "schwartz_index.txt"


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default=str(DEFAULT_PDF))
    parser.add_argument("--start-page", type=int, default=862)
    parser.add_argument("--end-page", type=int, default=870)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--txt-out", default=str(DEFAULT_TXT))
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    json_out = Path(args.json_out)
    txt_out = Path(args.txt_out)

    reader = PdfReader(str(pdf_path))
    pages = []
    text_blocks = []

    for page_number in range(args.start_page, args.end_page + 1):
        page = reader.pages[page_number - 1]
        raw_text = page.extract_text() or ""
        normalized_text = normalize_whitespace(raw_text)
        pages.append(
            {
                "page_number": page_number,
                "raw_text": raw_text,
                "normalized_text": normalized_text,
            }
        )
        text_blocks.append(f"=== PAGE {page_number} ===\n{raw_text.strip()}\n")

    payload = {
        "source_pdf": str(pdf_path),
        "pdf_page_count": len(reader.pages),
        "index_start_page": args.start_page,
        "index_end_page": args.end_page,
        "pages": pages,
    }

    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2))
    txt_out.parent.mkdir(parents=True, exist_ok=True)
    txt_out.write_text("\n".join(text_blocks))

    print(
        json.dumps(
            {
                "source_pdf": str(pdf_path),
                "pages_extracted": len(pages),
                "json_out": str(json_out),
                "txt_out": str(txt_out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
