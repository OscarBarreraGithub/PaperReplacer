#!/bin/bash
set -u

ROOT="/Users/emmy/Documents/KnowledgeGraph"
PROMPT_PATH="${PROMPT_PATH:-$ROOT/prompts/handoff-multi-document-autonomous-orchestrator.md}"
MODEL="${MODEL:-gpt-5.4}"
RUN_MODE="${RUN_MODE:-workspace-write}"
SLEEP_SECONDS="${SLEEP_SECONDS:-5}"
LOG_DIR="${LOG_DIR:-$ROOT/data/generated/orchestrator}"

mkdir -p "$LOG_DIR"
cd "$ROOT" || exit 1

failure_streak=0

while true; do
  timestamp="$(date '+%Y%m%d-%H%M%S')"
  python3 "$ROOT/scripts/document_orchestrator.py" --refresh-tracking >/dev/null
  if python3 "$ROOT/scripts/document_orchestrator.py" --check-complete >/dev/null; then
    echo "[$timestamp] document registry is terminal; stopping." | tee -a "$LOG_DIR/runner.log"
    exit 0
  fi

  python3 "$ROOT/scripts/document_orchestrator.py" --queue-json > "$LOG_DIR/queue-current.json"
  cp "$LOG_DIR/queue-current.json" "$LOG_DIR/queue-$timestamp.json"

  if [[ "$RUN_MODE" == "danger" ]]; then
    sandbox_args=(--dangerously-bypass-approvals-and-sandbox)
  else
    sandbox_args=(-s workspace-write)
  fi

  session_log="$LOG_DIR/session-$timestamp.jsonl"
  last_message="$LOG_DIR/last-message.txt"

  codex exec \
    -C "$ROOT" \
    -m "$MODEL" \
    "${sandbox_args[@]}" \
    --json \
    -o "$last_message" \
    < "$PROMPT_PATH" > "$session_log"
  exit_code=$?

  echo "[$timestamp] codex exec exit_code=$exit_code model=$MODEL run_mode=$RUN_MODE" >> "$LOG_DIR/runner.log"

  if [[ $exit_code -eq 0 ]]; then
    failure_streak=0
  else
    failure_streak=$((failure_streak + 1))
    echo "[$timestamp] failure_streak=$failure_streak" >> "$LOG_DIR/runner.log"
  fi

  if [[ $failure_streak -ge 5 ]]; then
    sleep 30
  else
    sleep "$SLEEP_SECONDS"
  fi
done
