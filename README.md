<div align="center">

# Codex Bug Bounty

**Codex-first bug bounty harness for Web2 + Web3: recon, hunting, validation, and reporting.**

<sub>Maintained by <a href="https://github.com/0x1Jar">0x1Jar</a></sub>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Shell](https://img.shields.io/badge/Shell-bash-4EAA25.svg?style=flat-square&logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-0B5FFF.svg?style=flat-square)](https://openai.com)

</div>

## Overview

This repository is structured for **Codex-first execution** with a clean `modules/` runtime layout.

- 7 skill domains in `skills/`
- 8 command cheatsheets in `commands/`
- 5 task-focused agent templates in `agents/`
- Canonical runtime scripts under `modules/*`
- Root-level compatibility wrappers for stable entrypoints

## Quick Start

```bash
git clone https://github.com/0x1Jar/codex-bug.git
cd codex-bug
./install.sh --target codex
```

Then run in Codex:

```bash
codex
# /recon target.com
# /hunt target.com
# /validate
# /report
```

## Direct Runtime Commands

```bash
python3 hunt.py --status
python3 hunt.py --target example.com --quick
./recon_engine.sh example.com
./vuln_scanner.sh recon/example.com
python3 validate.py
python3 report_generator.py findings/example.com
```

## Project Layout

```text
.
├── .codex-plugin/            # Codex local plugin metadata
├── modules/
│   ├── orchestrator/         # hunt, target selection, intel, mindmap
│   ├── recon/                # recon engine + probes
│   ├── scanners/             # scanners/fuzzers/specialized testers
│   ├── reporting/            # validation + report generation
│   └── support/              # shared helper space
├── skills/                   # Codex skill domains
├── commands/                 # command cheatsheets
├── agents/                   # agent templates
├── docs/                     # supporting documentation
├── rules/                    # hunting/reporting rules
└── scripts/                  # smoke and audit scripts
```

Detailed structure reference: `docs/project-structure.md`.

## Canonical Entrypoints

- `modules/orchestrator/hunt.py`
- `modules/recon/recon_engine.sh`
- `modules/scanners/vuln_scanner.sh`
- `modules/reporting/validate.py`
- `modules/reporting/report_generator.py`

## Root Compatibility Wrappers

Primary wrappers kept for day-to-day workflows:

- `hunt.py`
- `recon_engine.sh`
- `vuln_scanner.sh`
- `validate.py`
- `report_generator.py`

Additional wrappers available:

- `target_selector.py`
- `learn.py`
- `mindmap.py`
- `cve_hunter.py`
- `zero_day_fuzzer.py`
- `h1_run.sh`

All wrappers forward execution to canonical scripts in `modules/*`.

## Skills, Commands, Agents

Skills (`skills/*/SKILL.md`):

- `bug-bounty`
- `web2-recon`
- `web2-vuln-classes`
- `security-arsenal`
- `triage-validation`
- `report-writing`
- `web3-audit`

Commands (`commands/*.md`):

- `/recon`
- `/hunt`
- `/validate`
- `/report`
- `/chain`
- `/scope`
- `/triage`
- `/web3-audit`

Agents (`agents/*.md`):

- `recon-agent`
- `report-writer`
- `validator`
- `web3-auditor`
- `chain-builder`

## Quality Checks

```bash
./scripts/smoke_codex_support.sh
./scripts/audit_runtime_paths.sh
```

## Notes

- This repo is optimized for Codex workflows.
- Runtime behavior is designed to be stable from multiple working directories.
- Focus is operational speed: recon to report with validation gates.
