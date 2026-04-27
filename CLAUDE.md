# BountyForge - Claude Code Guide

This repository is a dual Codex and Claude Code bug bounty plugin. These instructions are for Claude Code sessions.

## How Claude Code Should Use This Repo

- Load the plugin from this repo with `claude --plugin-dir .`, or install it through the local marketplace in `.claude-plugin/marketplace.json`.
- Claude Code can use the root `skills/`, `commands/`, `agents/`, and `hooks/` directories as plugin components.
- Plugin skills may be namespaced when installed as a plugin. Standalone copied skills and commands keep their short names.
- Use slash commands such as `/recon`, `/hunt`, `/validate`, `/report`, `/triage`, `/scope`, `/chain`, `/web3-audit`, `/mobile`, `/mobile-static`, and `/mobile-dynamic` only for authorized work.
- Use `docs/mcp-burp-suite.md` only for authorized Burp Suite MCP traffic, and use `docs/hackerone-disclosed-reports.md` to study public report patterns before choosing bug classes.
- Keep `rules/hunting.md` and `rules/reporting.md` active as the project safety baseline.

## Safety Rules

1. Read full program scope before touching any asset.
2. Never test out-of-scope, third-party, staging, or excluded paths unless the program explicitly allows it.
3. Do not report theoretical bugs. Ask: "Can an attacker do this right now?"
4. Run `/validate` or the 7-Question Gate before writing any report.
5. Kill weak findings fast. N/A submissions hurt validity ratio.
6. Keep recon output in `recon/`, evidence in `findings/`, and reports in `reports/`.

## Validation

After support-file changes, prefer:

```bash
python3 -m json.tool .claude-plugin/plugin.json
python3 -m json.tool .claude-plugin/marketplace.json
python3 -m json.tool hooks/hooks.json
bash -n install.sh
```

If Claude Code is installed, also run:

```bash
claude plugin validate .
```
