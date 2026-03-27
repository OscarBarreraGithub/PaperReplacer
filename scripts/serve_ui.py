#!/usr/bin/env python3
"""Serve the local interactive graph UI and JSON APIs."""

from __future__ import annotations

import argparse
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import webbrowser

from kg_core import (
    ALL_AUTHORED_BATCH_ID,
    BATCHES_DIR,
    expanded_slice,
    extended_neighborhood_slice,
    intrinsic_vs_profile_adjusted,
    load_batch_contract,
    load_or_compile_bundle,
    prerequisites,
)


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "ui"


class GraphUIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api(parsed)
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def handle_api(self, parsed) -> None:
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/health":
                self.send_json({"ok": True})
                return
            if path == "/api/batches":
                self.send_json(list_batches())
                return
            if path.startswith("/api/batch/"):
                batch_id = path.removeprefix("/api/batch/")
                self.send_json(load_or_compile_bundle(batch_id))
                return
            if path == "/api/neighborhood":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(expanded_slice(bundle, target, relation_type))
                return
            if path == "/api/extended-neighborhood":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(
                    extended_neighborhood_slice(bundle, target, relation_type)
                )
                return
            if path == "/api/prereqs":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(prerequisites(bundle, target, relation_type))
                return
            if path == "/api/intrinsic-vs-profile":
                batch_id = _required(query, "batch")
                target = _required(query, "target")
                relation_type = _required(query, "relation_type")
                audience_profile = _required(query, "audience_profile")
                subfield = _required(query, "subfield")
                task_type = query.get("task_type", [None])[0]
                profile = {
                    "audience_profile": audience_profile,
                    "subfield": subfield,
                }
                if task_type:
                    profile["task_type"] = task_type
                bundle = load_or_compile_bundle(batch_id)
                self.send_json(
                    intrinsic_vs_profile_adjusted(bundle, target, relation_type, profile)
                )
                return
        except Exception as exc:  # noqa: BLE001
            self.send_json(
                {
                    "ok": False,
                    "error": type(exc).__name__,
                    "message": str(exc),
                },
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        self.send_json(
            {"ok": False, "message": f"Unknown API route: {path}"},
            status=HTTPStatus.NOT_FOUND,
        )

    def send_json(self, payload, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _required(query: dict[str, list[str]], key: str) -> str:
    value = query.get(key, [None])[0]
    if value is None or value == "":
        raise ValueError(f"Missing required query parameter: {key}")
    return value


def list_batches() -> list[dict[str, str]]:
    batches = [
        {
            "batch_id": ALL_AUTHORED_BATCH_ID,
            "description": "Synthetic connected view combining all authored batches.",
        }
    ]
    for batch_dir in sorted(path for path in BATCHES_DIR.iterdir() if path.is_dir()):
        contract_path = batch_dir / "batch_contract.yaml"
        description = ""
        if contract_path.exists():
            contract = load_batch_contract(batch_dir.name)
            description = contract.get("description", "")
        batches.append(
            {
                "batch_id": batch_dir.name,
                "description": description,
            }
        )
    return batches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="Open the UI in a browser")
    args = parser.parse_args()

    handler = partial(GraphUIHandler)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Serving graph UI at {url}")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
