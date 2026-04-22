# Codex Bug Bounty — Compatibility Guide

This repo is now **Codex-first** for professional bug bounty hunting across HackerOne, Bugcrowd, Intigriti, and Immunefi, while keeping Claude compatibility.

## Primary Mode (Codex)

Use skills-first flow in Codex:

```bash
codex
# /recon target.com
# /hunt target.com
# /validate
# /report
```

Install to Codex paths:

```bash
./install.sh --target codex
```

## Claude Fallback

Claude users are still supported:

```bash
./install.sh --target claude
```

or install both:

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

### Commands (Cheatsheet Prompts)

| Command | Usage |
|---|---|
| `/recon` | `/recon target.com` — full recon pipeline |
| `/hunt` | `/hunt target.com` — start hunting |
| `/validate` | `/validate` — run 7-Question Gate on current finding |
| `/report` | `/report` — write submission-ready report |
| `/chain` | `/chain` — build A→B→C exploit chain |
| `/scope` | `/scope <asset>` — verify asset is in scope |
| `/triage` | `/triage` — quick 7-Question Gate |
| `/web3-audit` | `/web3-audit <contract.sol>` — smart contract audit |

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

Located in repo root:
- `hunt.py` — master orchestrator
- `recon_engine.sh` — subdomain + URL discovery
- `validate.py` — 4-gate finding validator
- `report_generator.py` — report writer
- `learn.py` — CVE + disclosure intel

## Critical Rules

1. READ FULL SCOPE before touching any asset
2. NEVER hunt theoretical bugs — "Can attacker do this RIGHT NOW?"
3. Run 7-Question Gate BEFORE writing any report
4. KILL weak findings fast — N/A hurts your validity ratio
5. 5-minute rule — nothing after 5 min = move on
