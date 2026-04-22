# Project Structure (Codex-First)

This document explains the simplified final structure.

## Principles

- Domain-based: code is grouped by operational domain.
- Clean root: root is reserved for metadata, docs, installer, and compatibility wrappers.
- Strict compatibility: legacy commands remain available through wrappers.

## Main Folders

- `modules/orchestrator`: orchestrator pipeline, target selection, learning, mindmap.
- `modules/recon`: recon pipeline and probing scripts.
- `modules/scanners`: scanner, fuzzer, and testing scripts.
- `modules/reporting`: validation and report generation.
- `modules/support`: shared non-domain helpers.

## Compatibility Wrappers

Root wrappers are kept for legacy public entrypoints, for example:
- `hunt.py` -> `modules/orchestrator/hunt.py`
- `recon_engine.sh` -> `modules/recon/recon_engine.sh`
- `vuln_scanner.sh` -> `modules/scanners/vuln_scanner.sh`
- `validate.py` -> `modules/reporting/validate.py`
- `report_generator.py` -> `modules/reporting/report_generator.py`

Wrappers only forward arguments and exit codes, without business logic.

## Runtime Path Policy

- Canonical scripts in `modules/*` must run from any cwd.
- Path resolution prioritizes the new layout (`modules/*`).
- Legacy `tools/` layout remains supported as fallback.

## Operations

- Official installer: `install.sh`
- Smoke test: `scripts/smoke_codex_support.sh`
- Audit hardcoded path: `scripts/audit_runtime_paths.sh`
