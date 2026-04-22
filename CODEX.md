# Codex Bug Bounty — Compatibility Guide

This repo is now **Codex-first** for professional bug bounty hunting across HackerOne, Bugcrowd, Intigriti, and Immunefi.

## Primary Mode (Codex)

Use skills-first flow in Codex with natural-language prompts:

```bash
codex
# "Use the web2-recon skill to map example.com and summarize the best attack surface."
# "Use the bug-bounty skill to plan the next hunting step for example.com."
# "Use the report-writing skill to turn this validated finding into a submission-ready report."
```

Skills are selected by relevance. This repo does not register repo-specific slash commands in Codex CLI.

Install to Codex paths:

```bash
./install.sh --target codex
```

## Optional Multi-Target Install

```bash
./install.sh --target both
```

## What's Here

### Skills (7 domains)

| Skill | Domain |
|---|---|
| `skills/bug-bounty/` | Master workflow — recon to report, all vuln classes, LLM testing, chains |
| `skills/web2-recon/` | Subdomain enum, live host discovery, URL crawling, nuclei |
| `skills/web2-vuln-classes/` | 18 bug classes with bypass tables (SSRF, open redirect, file upload, Agentic AI) |
| `skills/security-arsenal/` | Payloads, bypass tables, gf patterns, always-rejected list |
| `skills/web3-audit/` | 10 smart contract bug classes, Foundry PoC template, pre-dive kill signals |
| `skills/report-writing/` | H1/Bugcrowd/Intigriti/Immunefi report templates, CVSS 3.1, human tone |
| `skills/triage-validation/` | 7-Question Gate, 4 gates, never-submit list, conditionally valid table |

### Reference Prompt Docs

| Doc | Purpose |
|---|---|
| `recon.md` | Reference prompts for full recon workflow |
| `hunt.md` | Reference prompts for active hunting |
| `validate.md` | Reference prompts for full finding validation |
| `report.md` | Reference prompts for submission-ready reports |
| `chain.md` | Reference prompts for exploit-chain building |
| `scope.md` | Reference prompts for scope checks |
| `triage.md` | Reference prompts for quick go/no-go validation |
| `web3-audit.md` | Reference prompts for smart contract review |

### Agents (Templates)

- `recon-agent` — subdomain enum + live host discovery
- `report-writer` — generates H1/Bugcrowd/Immunefi reports
- `validator` — 4-gate checklist on a finding
- `web3-auditor` — smart contract bug class analysis
- `chain-builder` — builds A→B→C exploit chains

### Rules (always active)

- `rules/hunting.md` — 17 critical hunting rules
- `rules/reporting.md` — report quality rules

### Tools (Python/shell — run directly)

Use the canonical scripts under `modules/*`:
- `modules/orchestrator/hunt.py` — master orchestrator
- `modules/recon/recon_engine.sh` — subdomain + URL discovery
- `modules/reporting/validate.py` — 4-gate finding validator
- `modules/reporting/report_generator.py` — report writer
- `modules/orchestrator/learn.py` — CVE + disclosure intel

## Critical Rules

1. READ FULL SCOPE before touching any asset
2. NEVER hunt theoretical bugs — "Can attacker do this RIGHT NOW?"
3. Run 7-Question Gate BEFORE writing any report
4. KILL weak findings fast — N/A hurts your validity ratio
5. 5-minute rule — nothing after 5 min = move on
