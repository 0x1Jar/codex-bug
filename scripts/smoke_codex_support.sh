#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_DIR"

echo "[1/9] Validate Codex plugin metadata JSON"
python3 -m json.tool .codex-plugin/plugin.json >/dev/null

echo "[2/9] Validate repo skill frontmatter"
python3 scripts/validate_skill_frontmatter.py skills

echo "[3/9] Installer dry-run checks"
./install.sh --dry-run --target codex >/tmp/install_codex_dryrun.log
./install.sh --dry-run --target claude >/tmp/install_claude_dryrun.log
./install.sh --dry-run --target both >/tmp/install_both_dryrun.log
if ! rg -q "Reference docs in .*not built-in Codex slash commands" /tmp/install_codex_dryrun.log; then
  echo "FAIL: installer output is missing the command-docs note"
  cat /tmp/install_codex_dryrun.log
  exit 1
fi

echo "[4/9] Legacy wrapper smoke (--help / --status)"
python3 hunt.py --status >/tmp/hunt_status_wrapper.log
python3 hunt.py --help >/dev/null
python3 report_generator.py --help >/dev/null
python3 validate.py --help >/dev/null
python3 learn.py --help >/dev/null
python3 mindmap.py --help >/dev/null
python3 cve_hunter.py --help >/dev/null
python3 zero_day_fuzzer.py --help >/dev/null
python3 target_selector.py --help >/dev/null

echo "[5/9] Canonical modules smoke (--help / usage checks)"
python3 modules/orchestrator/hunt.py --help >/dev/null
python3 modules/reporting/report_generator.py --help >/dev/null
python3 modules/reporting/validate.py --help >/dev/null
python3 modules/orchestrator/learn.py --help >/dev/null
python3 modules/orchestrator/mindmap.py --help >/dev/null
python3 modules/scanners/cve_hunter.py --help >/dev/null
python3 modules/scanners/zero_day_fuzzer.py --help >/dev/null
python3 modules/orchestrator/target_selector.py --help >/dev/null

set +e
bash modules/recon/recon_engine.sh >/tmp/recon_usage.log 2>&1
recon_status=$?
bash modules/scanners/vuln_scanner.sh >/tmp/vuln_usage.log 2>&1
vuln_status=$?
set -e

if [[ "$recon_status" -eq 0 ]] || [[ "$vuln_status" -eq 0 ]]; then
  echo "FAIL: recon/vuln usage checks unexpectedly exited 0"
  exit 1
fi

if ! rg -q "Usage" /tmp/recon_usage.log; then
  echo "FAIL: recon usage message not found"
  cat /tmp/recon_usage.log
  exit 1
fi

if ! rg -q "Usage" /tmp/vuln_usage.log; then
  echo "FAIL: vuln usage message not found"
  cat /tmp/vuln_usage.log
  exit 1
fi

echo "[6/9] CWD smoke checks"
(cd docs && python3 ../hunt.py --status >/tmp/hunt_status_docs.log)
(cd skills && python3 ../validate.py --help >/dev/null)
(cd commands && python3 ../report_generator.py --help >/dev/null)
(cd docs && python3 ../modules/orchestrator/hunt.py --help >/dev/null)

echo "[7/9] Select-target path regression check"
set +e
python3 hunt.py --select-targets --top 1 >/tmp/hunt_select_targets.log 2>&1
status=$?
set -e
if rg -q "can't open file .*tools/" /tmp/hunt_select_targets.log; then
  echo "FAIL: legacy tools/ path regression detected in hunt --select-targets"
  cat /tmp/hunt_select_targets.log
  exit 1
fi
echo "select-targets exit code: $status (non-zero can happen due network/API issues)"

echo "[8/9] Runtime tools-path and docs audit"
./scripts/audit_runtime_paths.sh

echo "[9/9] Smoke checks complete"
echo "PASS"
