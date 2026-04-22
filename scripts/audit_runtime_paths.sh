#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_DIR"

FILES=(
  install.sh
  README.md
  docs/project-structure.md
  scripts/smoke_codex_support.sh
  hunt.py
  recon_engine.sh
  vuln_scanner.sh
  report_generator.py
  validate.py
  learn.py
  mindmap.py
  cve_hunter.py
  zero_day_fuzzer.py
  target_selector.py
  modules/orchestrator/hunt.py
  modules/orchestrator/learn.py
  modules/orchestrator/mindmap.py
  modules/orchestrator/target_selector.py
  modules/recon/recon_engine.sh
  modules/scanners/vuln_scanner.sh
  modules/reporting/report_generator.py
  modules/reporting/validate.py
)

echo "Auditing runtime/docs for stale hardcoded tools/ execution references..."

matches="$(rg -n "python3 tools/|bash tools/|\./tools/|tools/install_tools\.sh|tools/report_generator\.py|tools/validate\.py|tools/learn\.py|tools/mindmap\.py|tools/recon_engine\.sh|tools/vuln_scanner\.sh" "${FILES[@]}" || true)"

if [[ -n "$matches" ]]; then
  echo "FAIL: stale tools/ execution references found"
  echo "$matches"
  exit 1
fi

echo "PASS: no stale hardcoded tools/ execution references"
