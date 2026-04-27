<div align="center">

<img src="assets/image.png" alt="BountyForge logo" width="360" />

# BountyForge

**Agent-powered bug bounty workflow for Codex and Claude Code.**

Web2, Web3, mobile, recon, validation, and report writing in one repo.

<sub>Maintained at <a href="https://github.com/0x1Jar/codex-bug">0x1Jar/codex-bug</a></sub>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Shell](https://img.shields.io/badge/Shell-bash-4EAA25.svg?style=flat-square&logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-10A37F.svg?style=flat-square&logo=openai&logoColor=white)](https://developers.openai.com/codex)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-D97706.svg?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/claude-code)

[Quick Start](#quick-start) | [Codex](#use-with-codex) | [Claude Code](#use-with-claude-code) | [Workflows](#workflows) | [Skills](#skills) | [Commands](#claude-commands) | [Tools](#tools) | [Docs](#more-documentation) | [Safety](#safety)

</div>

---

## What Is BountyForge?

BountyForge is a dual-agent bug bounty toolkit. It gives Codex and Claude Code a shared set of skills, commands, agents, rules, and scripts for practical security testing.

Use it when you want help with:

- Web2 recon and attack-surface mapping
- mobile static analysis for APK, AAB, IPA, and source trees
- mobile dynamic testing with proxying, Frida, Objection, logs, storage, IPC, and WebViews
- Claude Code Burp Suite MCP-assisted review of authorized proxy traffic and Repeater evidence
- bug-class hunting for IDOR, auth bypass, XSS, SSRF, GraphQL, OAuth, upload bugs, race conditions, and more
- Web3 smart contract audit workflow and Foundry PoC structure
- HackerOne disclosed-report study for bug-class selection and duplicate checks
- finding validation before report writing
- HackerOne, Bugcrowd, Intigriti, Immunefi, and similar report drafts

The repo is not just a script dump. The main value is the workflow knowledge in `skills/`, `commands/`, `agents/`, and `rules/`, with Python and shell tools available when deterministic execution is useful.

> For authorized security testing only. Read the program scope before touching any asset.

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/0x1Jar/codex-bug.git
cd codex-bug
```

### 2. Install Agent Support

```bash
chmod +x install.sh
./install.sh --all
```

Use `--all` for both platforms, or choose one:

```bash
./install.sh --codex
./install.sh --claude
```

### 3. Install Runtime Tools

```bash
chmod +x install_tools.sh
./install_tools.sh
```

This installs common recon and testing tools such as `subfinder`, `httpx`, `dnsx`, `nuclei`, `katana`, `gau`, `ffuf`, `gf`, and related helpers.

### 4. Configure Optional API Keys

```bash
cp config.example.json config.json
```

For better subdomain coverage, export a ProjectDiscovery Chaos API key:

```bash
export CHAOS_API_KEY="your-key-here"
```

For persistence:

```bash
echo 'export CHAOS_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

---

## Use With Codex

Codex uses:

- `AGENTS.md` for repo instructions
- `.codex-plugin/plugin.json` for plugin metadata
- `.agents/plugins/marketplace.json` for local plugin discovery
- `.codex/agents/` for optional custom agent configs
- `skills/` as the shared workflow knowledge

Start Codex from the repo:

```bash
codex
```

Useful prompts:

```text
$web2-recon example.com
$bug-bounty start a scoped hunt for example.com
$mobile-static ./app.apk
$mobile-dynamic com.example.app
$triage-validation validate this finding before report writing
$report-writing draft a HackerOne report from this evidence
```

Codex works best with natural-language instructions plus skill names. The `commands/*.md` files are reference docs for Codex, not Codex slash commands.

---

## Use With Claude Code

Claude Code uses:

- `CLAUDE.md` for repo instructions
- `.claude-plugin/plugin.json` for plugin metadata
- `.claude-plugin/marketplace.json` for local marketplace discovery
- `commands/` for slash commands
- `agents/` for Claude Code subagents
- `hooks/hooks.json` for non-destructive session reminders
- `skills/` as the shared workflow knowledge

Start Claude Code with this repo as a plugin:

```bash
claude --plugin-dir .
```

Common slash commands:

```text
/recon target.com
/hunt target.com
/mobile ./app.apk
/mobile-static ./app.apk
/mobile-dynamic com.example.app
/validate
/report
```

When installed through a marketplace or plugin namespace, Claude Code may show namespaced commands or skills in `/help`. Use the exact names shown there.

---

## Workflows

### Web2 Recon To Report

```text
1. Confirm scope and rules of engagement.
2. Run recon on approved assets.
3. Map live hosts, URLs, JS, parameters, and technologies.
4. Pick high-ROI bug classes.
5. Validate impact with the 7-Question Gate.
6. Write the report only after validation passes.
```

Codex:

```text
$web2-recon example.com
$bug-bounty hunt only in-scope assets from recon/example.com
$triage-validation validate this evidence
$report-writing write the final report
```

Claude Code:

```text
/recon example.com
/hunt example.com
/validate
/report
```

Direct tools:

```bash
./recon_engine.sh example.com
python3 hunt.py --target example.com
python3 validate.py
python3 report_generator.py findings/
```

### Burp MCP And Disclosed Report Learning

Use Burp Suite MCP with Claude Code when you want agent help over in-scope HTTP traffic, Repeater evidence, sitemap context, or proxy history. BountyForge documents safe Claude Code setup without auto-starting a server from this repo.

Use HackerOne disclosed reports before deep hunting to learn accepted impact patterns, common duplicates, and bug classes that have paid on similar features.

```text
$bug-bounty compare this target against HackerOne disclosed report patterns
/hunt target.com using only in-scope Burp MCP traffic
/validate after checking Hacktivity for duplicates
```

References:

- `docs/mcp-burp-suite.md`
- `docs/hackerone-disclosed-reports.md`

### Mobile Static Analysis

Use this for APK, AAB, IPA, extracted apps, or source trees.

Codex:

```text
$mobile-static ./target.apk
```

Claude Code:

```text
/mobile-static ./target.apk
```

Focus areas:

- Android manifest, iOS plist, entitlements, permissions
- local storage, secrets, keys, tokens, and hardcoded URLs
- crypto usage and certificate handling
- network security config and ATS
- deep links, exported components, WebViews, and IPC
- MASVS and MASWE mapping

### Mobile Dynamic Analysis

Use this for a live app on a device, emulator, or test harness.

Codex:

```text
$mobile-dynamic com.example.app
```

Claude Code:

```text
/mobile-dynamic com.example.app
```

Focus areas:

- proxy and MITM setup
- Frida and Objection instrumentation
- SSL pinning validation or authorized bypass testing
- auth and session flows
- runtime storage and logs
- deep links, IPC, WebViews, and backend API behavior

### Web3 Audit

Codex:

```text
$web3-audit review this Solidity project
```

Claude Code:

```text
/web3-audit ./contracts
```

Focus areas:

- accounting desync
- access control
- incomplete code paths
- off-by-one bugs
- oracle manipulation
- ERC4626 issues
- reentrancy
- flash-loan paths
- signature replay
- proxy and upgrade risks

---

## Skills

Skills are the shared source of truth for Codex and Claude Code.

| Skill | Use It For |
|:---|:---|
| `bug-bounty` | End-to-end bug bounty workflow from recon to report |
| `web2-recon` | subdomains, live hosts, URL crawling, JS analysis, monitoring |
| `web2-vuln-classes` | IDOR, auth bypass, XSS, SSRF, GraphQL, OAuth, upload bugs, race conditions, cache poisoning, SAML, and more |
| `security-arsenal` | payloads, bypass tables, wordlists, gf patterns, and never-submit rules |
| `web3-audit` | smart contract audit workflow, bug classes, grep patterns, Foundry PoC structure |
| `report-writing` | H1, Bugcrowd, Intigriti, YesWeHack, and Immunefi report writing |
| `triage-validation` | 7-Question Gate, validation gates, severity guidance, pre-submit checklist |
| `mobile` | mobile assessment router for Android and iOS |
| `mobile-static` | offline APK, AAB, IPA, and source review |
| `mobile-dynamic` | runtime mobile testing with proxying, instrumentation, logs, storage, and IPC |

Skill files live in `skills/*/SKILL.md`.

---

## Claude Commands

Claude Code discovers these from `commands/`.

| Command | Purpose |
|:---|:---|
| `/recon <target>` | run full recon workflow |
| `/hunt <target>` | start active hunting on in-scope assets |
| `/scope <asset>` | check whether an asset is in scope |
| `/triage` | quick go/no-go validation |
| `/validate` | full finding validation |
| `/report` | write a submission-ready report |
| `/chain` | reason about A -> B -> C exploit chains |
| `/web3-audit <path>` | audit smart contract code |
| `/mobile <target>` | route general mobile analysis to static or dynamic review |
| `/mobile-static <apk/aab/ipa/source>` | static mobile review |
| `/mobile-dynamic <package/bundle/app>` | dynamic mobile testing |

---

## Agents

Claude Code agent files live in `agents/`. Codex agent configs live in `.codex/agents/`.

| Agent | Role |
|:---|:---|
| `recon-agent` | runs recon and summarizes attack surface |
| `validator` | applies validation gates to a finding |
| `report-writer` | turns confirmed evidence into a platform-ready report |
| `web3-auditor` | reviews smart contract code against Web3 bug classes |
| `chain-builder` | explores realistic exploit chains from an initial bug |

---

## Tools

You can run the scripts directly when you want deterministic output.

### Core

| Tool | Purpose |
|:---|:---|
| `hunt.py` | master hunt orchestrator |
| `recon_engine.sh` | subdomain and URL discovery |
| `learn.py` | CVE and disclosure intel |
| `mindmap.py` | attack surface mapper |
| `validate.py` | finding validation helper |
| `report_generator.py` | report generator |

### Scanners And Helpers

| Tool | Purpose |
|:---|:---|
| `h1_idor_scanner.py` | IDOR checks |
| `h1_mutation_idor.py` | GraphQL mutation IDOR checks |
| `h1_oauth_tester.py` | OAuth testing |
| `h1_race.py` | race-condition testing |
| `zero_day_fuzzer.py` | logic and edge-case fuzzing |
| `cve_hunter.py` | CVE matching |
| `vuln_scanner.sh` | nuclei, dalfox, sqlmap wrapper |
| `hai_probe.py` | AI chatbot and LLM feature testing |
| `hai_payload_builder.py` | prompt injection payload builder |
| `hai_browser_recon.js` | browser-side AI endpoint recon |
| `sneaky_bits.py` | JavaScript secret and endpoint finder |
| `target_selector.py` | bug bounty program scoring |

---

## Output Folders

| Folder | Contents |
|:---|:---|
| `recon/` | recon output per target |
| `findings/` | confirmed evidence and validation notes |
| `reports/` | submission-ready report drafts |

These folders are for local work output. Review `.gitignore` before committing generated data.

---

## More Documentation

| File | Use It For |
|:---|:---|
| `docs/agent-support.md` | Codex and Claude Code setup details |
| `docs/mcp-burp-suite.md` | Burp Suite MCP setup and safe usage for Claude Code |
| `docs/hackerone-disclosed-reports.md` | curated HackerOne disclosed-report study workflow |
| `docs/payloads.md` | payload reference |
| `docs/advanced-techniques.md` | chaining, mobile, CI/CD, and deeper testing notes |
| `docs/smart-contract-audit.md` | Web3 audit guide |
| `AGENTS.md` | Codex-specific repo behavior |
| `CLAUDE.md` | Claude Code-specific repo behavior |
| `CHANGELOG.md` | release history |

---

## Project Map

```text
codex-bug/
├── assets/image.png                 # README logo
├── AGENTS.md                        # Codex instructions
├── CLAUDE.md                        # Claude Code instructions
├── README.md                        # main documentation
├── install.sh                       # Codex and Claude installer
├── install_tools.sh                 # external security tools installer
├── .codex-plugin/plugin.json        # Codex plugin manifest
├── .claude-plugin/plugin.json       # Claude Code plugin manifest
├── .agents/plugins/marketplace.json # Codex local marketplace
├── .claude-plugin/marketplace.json  # Claude local marketplace
├── .codex/                          # Codex config, hooks, agents
├── skills/                          # shared AI-agent skills
├── commands/                        # Claude slash commands and Codex references
├── agents/                          # Claude Code agent definitions
├── hooks/hooks.json                 # Claude Code hooks
├── rules/                           # hunting and reporting rules
├── docs/                            # extra guides
├── web3/                            # smart contract audit references
├── scripts/                         # helper scripts
├── wordlists/                       # wordlists
├── *.py                             # Python tools
└── *.sh                             # shell tools
```

---

## Validate The Repo

After changes, these checks are useful:

```bash
python3 -m json.tool .codex-plugin/plugin.json
python3 -m json.tool .claude-plugin/plugin.json
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool .claude-plugin/marketplace.json
python3 -m json.tool hooks/hooks.json
python3 -m json.tool .codex/hooks.json
bash -n install.sh recon_engine.sh vuln_scanner.sh h1_run.sh scripts/full_hunt.sh
```

If Claude Code is installed:

```bash
claude plugin validate .
```

---

## Safety

This repo is for authorized security testing only.

Rules that should never be skipped:

1. Read the full scope before sending traffic.
2. Only test assets that are explicitly allowed.
3. Do not test third-party systems unless the program allows it.
4. Do not submit theoretical findings.
5. Validate impact before report writing.
6. Keep evidence clear, minimal, and reproducible.
7. Stop if a test could harm availability, privacy, or data integrity.

More detail:

- `rules/hunting.md`
- `rules/reporting.md`
- `skills/triage-validation/SKILL.md`

---

## Contributing

Good contributions:

- new skills or improved methodology
- safer validation workflows
- platform-specific command docs
- scanner improvements
- report-writing templates
- mobile or Web3 test coverage
- documentation that makes the project easier for beginners

Keep generated recon output, findings, reports, and large reference dumps out of normal commits unless they are intentionally part of the change.

---

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">

**Built by bug hunters, for bug hunters.**

If BountyForge helps you find a valid bug, consider leaving a star.

</div>
