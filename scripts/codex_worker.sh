#!/usr/bin/env bash
# scripts/codex_worker.sh
# Wrapper for invoking Codex CLI (gpt-5.4) as a subagent from Claude.
#
# Usage:
#   bash scripts/codex_worker.sh "your prompt here"
#   bash scripts/codex_worker.sh --out /tmp/result.md "your prompt here"
#
# The --out flag writes output to a file instead of stdout.
# Use this for background invocations where stdout isn't captured.

set -euo pipefail

OUT_FILE=""
PROMPT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      OUT_FILE="$2"
      shift 2
      ;;
    *)
      PROMPT="$1"
      shift
      ;;
  esac
done

if [[ -z "$PROMPT" ]]; then
  echo "Usage: $0 [--out /path/to/output.md] \"prompt\"" >&2
  exit 1
fi

# Ensure nvm/node are in PATH if needed
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
  . "$NVM_DIR/nvm.sh"
fi

CODEX_BIN="$(which codex 2>/dev/null || echo '')"
if [[ -z "$CODEX_BIN" ]]; then
  echo "ERROR: codex binary not found in PATH" >&2
  exit 1
fi

# --dangerously-bypass-approvals-and-sandbox is required for non-interactive
# scripted invocation. Config sets approval_policy=never but the flag is
# still needed for subprocess calls from Claude.
if [[ -n "$OUT_FILE" ]]; then
  "$CODEX_BIN" exec --dangerously-bypass-approvals-and-sandbox "$PROMPT" > "$OUT_FILE" 2>&1
else
  "$CODEX_BIN" exec --dangerously-bypass-approvals-and-sandbox "$PROMPT"
fi
