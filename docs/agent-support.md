# Dual Agent Support

This repo supports both Codex and Claude Code without duplicating the bug bounty knowledge. The shared source of truth stays in `skills/`, `commands/`, `agents/`, `rules/`, and the root tools.

## Use With Codex

Codex reads `AGENTS.md` for repo instructions and can install this repo as a local plugin through `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`.

Quick path:

```bash
chmod +x install.sh
./install.sh --codex
codex
```

Use natural language or explicit skill mentions:

```text
$web2-recon example.com
$mobile-static app.apk
$mobile-dynamic com.target.app
$triage-validation validate this finding before report writing
$report-writing draft a HackerOne report from this confirmed evidence
```

Codex custom agents live in `.codex/agents/`. Use them only when you explicitly want Codex to delegate work to subagents.

## Use With Claude Code

Claude Code reads `CLAUDE.md` and can load this repo as a plugin through `.claude-plugin/plugin.json`.

Quick path:

```bash
chmod +x install.sh
./install.sh --claude
claude --plugin-dir .
```

Standalone copied commands keep their short names:

```text
/recon target.com
/hunt target.com
/mobile-static app.apk
/mobile-dynamic com.target.app
/validate
/report
```

When installed as a plugin, Claude Code may namespace skills by plugin name. If so, use the namespaced entry shown by `/help`.

## Installer

Use one installer for both platforms:

```bash
./install.sh --codex
./install.sh --claude
./install.sh --all
```

The default is `--all`.

## Safety Baseline

- Only test assets that are explicitly in scope.
- Keep output in `recon/`, confirmed evidence in `findings/`, and reports in `reports/`.
- Validate every finding with the 7-Question Gate before report writing.
- Do not submit theoretical, excluded, or unproven findings.
