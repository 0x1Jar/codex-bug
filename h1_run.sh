#!/usr/bin/env bash
# Compatibility wrapper. Canonical implementation: modules/orchestrator/h1_run.sh
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$ROOT_DIR/modules/orchestrator/h1_run.sh"

if [ ! -f "$TARGET" ]; then
  echo "Missing canonical script: $TARGET" >&2
  exit 1
fi

exec bash "$TARGET" "$@"
