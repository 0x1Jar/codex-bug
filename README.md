# Codex Bug Bounty Toolkit (Codex-First)

Toolkit ini sekarang memakai struktur **modules-first** supaya lebih mudah dibaca, dirawat, dan di-scale.
Kompatibilitas command lama tetap hidup lewat wrapper di root (strict compatibility).

## Quick Start

```bash
./install.sh --target codex
python3 hunt.py --status
python3 hunt.py --target example.com --quick
python3 validate.py --help
python3 report_generator.py --help
```

## Instalasi

```bash
./install.sh --target codex
./install.sh --target claude
./install.sh --target both
./install.sh --dry-run --target both
```

Flag utama:
- `--target codex|claude|both`
- `--dry-run`
- `--force`

## Struktur Proyek (Sederhana)

```text
.
├── modules/
│   ├── orchestrator/   # alur utama (hunt, selector, learning)
│   ├── recon/          # recon engine + probe
│   ├── scanners/       # scanner/fuzzer/testing
│   ├── reporting/      # validator + report generator
│   └── support/        # helper non-domain
├── commands/           # cheatsheet prompt/command
├── skills/             # skill definitions
├── docs/               # dokumentasi
├── install.sh          # installer resmi lintas platform
└── <root wrappers>     # kompatibilitas command lama
```

Detail struktur: `docs/project-structure.md`

## Entry Point Canonical

- `modules/orchestrator/hunt.py`
- `modules/recon/recon_engine.sh`
- `modules/scanners/vuln_scanner.sh`
- `modules/reporting/validate.py`
- `modules/reporting/report_generator.py`

## Kompatibilitas Lama (No Breaking)

Command lama tetap valid:
- `python3 hunt.py`
- `./recon_engine.sh`
- `./vuln_scanner.sh`
- `python3 validate.py`
- `python3 report_generator.py`

Root file di atas sekarang berperan sebagai wrapper tipis ke `modules/*`.

## Smoke Check

```bash
./scripts/smoke_codex_support.sh
./scripts/audit_runtime_paths.sh
```

## Catatan

- Fokus v1 migrasi: keterbacaan + stabilitas path/runtime.
- Fitur inti tidak diubah secara fungsional.
