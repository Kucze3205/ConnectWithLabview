#!/usr/bin/env bash
# Machine preparation: what this loop's goal needs on the runner before any session starts (packages, tools, data).
# Every session job runs it, before the agent. The setup map fills it in (topic B); the engine ships it empty.
# Keep it fast and idempotent: it runs once per job. It runs with no secrets in its environment.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
CACHE="${LABVIEW_ENVIRONMENT:-${RUNNER_TEMP:-/tmp}/connectwithlabview-environment}"
python3 "$ROOT/prepare_environment.py" --cache "$CACHE"
if [ -n "${GITHUB_ENV:-}" ]; then
  printf 'LABVIEW_ENVIRONMENT=%s\n' "$CACHE" >> "$GITHUB_ENV"
fi
