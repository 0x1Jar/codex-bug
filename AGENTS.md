# BountyForge - Codex Guide

This repository is a dual Codex and Claude Code bug bounty plugin. These instructions are for Codex sessions started in this repo.

## How Codex Should Use This Repo

- Treat `skills/` as the main workflow library. Prefer `$bug-bounty`, `$web2-recon`, `$web2-vuln-classes`, `$security-arsenal`, `$web3-audit`, `$triage-validation`, `$report-writing`, `$mobile`, `$mobile-static`, and `$mobile-dynamic` when the task matches.
- Use `rules/hunting.md` and `rules/reporting.md` as always-on security guidance.
- Use `commands/*.md` as reference prompt docs. They document slash-style workflows, but Codex users should normally invoke installed skills with `$skill-name` or describe the task naturally.
- Use `.codex/agents/*.toml` for Codex custom subagents when the user explicitly asks for agent delegation.
- Use `docs/hackerone-disclosed-reports.md` to study public report patterns before choosing bug classes.
- Use the Python and shell tools directly only for authorized targets and only after scope is clear.

## Safety Rules

1. Read full program scope before touching any asset.
2. Never test out-of-scope, third-party, staging, or excluded paths unless the program explicitly allows it.
3. Do not report theoretical bugs. Ask: "Can an attacker do this right now?"
4. Run the 7-Question Gate before writing any report.
5. Kill weak findings fast. N/A submissions hurt validity ratio.
6. Keep recon output in `recon/`, evidence in `findings/`, and reports in `reports/`.

## Validation

After support-file changes, prefer:

```bash
python3 -m json.tool .codex-plugin/plugin.json
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool .codex/hooks.json
bash -n install.sh
```

For hunting-tool changes, run the narrowest safe syntax or smoke check for the touched tool.
