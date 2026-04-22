#!/usr/bin/env bash
# Compatibility wrapper. Canonical implementation: modules/recon/recon_engine.sh
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$ROOT_DIR/modules/recon/recon_engine.sh"

if [ ! -f "$TARGET" ]; then
  echo "Missing canonical script: $TARGET" >&2
  exit 1
fi

exec bash "$TARGET" "$@"
