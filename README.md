# Codex Bug Bounty Toolkit (Codex-First)

This toolkit now uses a **modules-first** structure to improve readability, maintainability, and scalability.
Legacy command compatibility is preserved through root-level wrappers (strict compatibility).

## Quick Start

```bash
./install.sh --target codex
python3 hunt.py --status
python3 hunt.py --target example.com --quick
python3 validate.py --help
python3 report_generator.py --help
```

## Installation

```bash
./install.sh --target codex
./install.sh --dry-run --target codex
```

Primary flags:
- `--target codex`
- `--dry-run`
- `--force`

## Project Structure (Simple)

```text
.
├── modules/
│   ├── orchestrator/   # main workflow (hunt, selector, learning)
│   ├── recon/          # recon engine + probe
│   ├── scanners/       # scanner/fuzzer/testing
│   ├── reporting/      # validator + report generator
│   └── support/        # shared non-domain helpers
├── commands/           # cheatsheet prompt/command
├── skills/             # skill definitions
├── docs/               # documentation
├── install.sh          # cross-platform installer
└── <root wrappers>     # legacy command compatibility
```

Structure details: `docs/project-structure.md`

## Entry Point Canonical

- `modules/orchestrator/hunt.py`
- `modules/recon/recon_engine.sh`
- `modules/scanners/vuln_scanner.sh`
- `modules/reporting/validate.py`
- `modules/reporting/report_generator.py`

## Legacy Compatibility (No Breaking Changes)

Legacy commands remain valid:
- `python3 hunt.py`
- `./recon_engine.sh`
- `./vuln_scanner.sh`
- `python3 validate.py`
- `python3 report_generator.py`

The root files above now act as thin wrappers that forward to `modules/*`.

## Smoke Check

```bash
./scripts/smoke_codex_support.sh
./scripts/audit_runtime_paths.sh
```

## Notes

- v1 migration focus: readability and path/runtime stability.
- Core functionality is unchanged.
