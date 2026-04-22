# Project Structure (Codex-First)

Dokumen ini menjelaskan struktur final yang disederhanakan.

## Prinsip

- Domain-based: kode dikelompokkan per domain kerja.
- Root clean: root dipakai untuk metadata, docs, installer, dan wrapper kompatibilitas.
- Strict compatibility: command lama tetap hidup via wrapper.

## Folder Utama

- `modules/orchestrator`: orchestrator pipeline, target selection, learning, mindmap.
- `modules/recon`: pipeline recon dan probe.
- `modules/scanners`: scanner, fuzzer, dan script uji.
- `modules/reporting`: validasi dan generasi report.
- `modules/support`: helper non-domain (reservasi untuk util bersama).

## Wrapper Kompatibilitas

Root wrapper dipertahankan untuk entrypoint publik lama, misalnya:
- `hunt.py` -> `modules/orchestrator/hunt.py`
- `recon_engine.sh` -> `modules/recon/recon_engine.sh`
- `vuln_scanner.sh` -> `modules/scanners/vuln_scanner.sh`
- `validate.py` -> `modules/reporting/validate.py`
- `report_generator.py` -> `modules/reporting/report_generator.py`

Wrapper hanya forward argumen + exit code, tanpa logic bisnis.

## Runtime Path Policy

- Script canonical di `modules/*` wajib bisa dijalankan dari cwd mana pun.
- Resolver path memprioritaskan layout baru (`modules/*`).
- Layout legacy `tools/` tetap didukung sebagai fallback.

## Operasional

- Installer resmi: `install.sh`
- Smoke test: `scripts/smoke_codex_support.sh`
- Audit hardcoded path: `scripts/audit_runtime_paths.sh`
