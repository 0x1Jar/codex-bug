<div align="center">

<img src="assets/image.png" alt="Codex Bug Bounty Logo" width="360" />

# Codex Bug Bounty

**Codex-first bug bounty project for Web2 + Web3 recon, hunting, validation, and reporting.**

<sub>Maintained by <a href="https://github.com/0x1Jar">0x1Jar</a></sub>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Shell](https://img.shields.io/badge/Shell-bash-4EAA25.svg?style=flat-square&logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-0B5FFF.svg?style=flat-square)](https://openai.com)

</div>

## What This Project Is

This repo helps you run a practical bug bounty workflow with Codex.

It gives you:
- Codex skills in `skills/`
- reference prompt docs in `commands/`
- canonical runtime scripts in `modules/*`
- helper docs, rules, and wrappers for compatibility

This project is **Codex-first**. That means the normal beginner flow is:
1. install Codex assets
2. install runtime tools
3. open Codex
4. prompt Codex in plain English
5. run the real scripts from `modules/*` when you want deterministic execution

## How This Project Works

These four pieces are the main mental model:

- `install.sh`: installs Codex assets such as skills and reference docs
- `install_tools.sh`: installs external security tools such as `subfinder`, `httpx`, `nuclei`, and `gf`
- `skills/`: teach Codex how to approach recon, validation, reporting, and bug classes
- `modules/*`: the real executable scripts that create recon data, findings, and reports

Two other folders are helpful, but often misunderstood:

- `commands/*.md`: reference prompt docs only, not runnable Codex slash commands
- `agents/*.md`: task templates, useful later, but not required to start using the project

Important: this repo does **not** add custom recon or hunt slash-style commands to the Codex CLI.

## Start Here

### 1) Clone the repo

```bash
git clone https://github.com/0x1Jar/codex-bug.git
cd codex-bug
```

### 2) Install Codex assets

```bash
./install.sh --target codex
```

This installs the repo's skills and reference docs into your Codex environment.

### 3) Install runtime tools

```bash
./install_tools.sh
```

This installs the external tools used by the recon and scanning scripts.

### 4) Prepare config

```bash
cp config.example.json config.json
```

Use `config.json` as your local config file. Keep in mind that **not every script auto-loads it yet**.

### 5) Set the Chaos API key

```bash
export CHAOS_API_KEY="your_chaos_api_key"
```

To make it persistent on macOS with `zsh`:

```bash
echo 'export CHAOS_API_KEY="your_chaos_api_key"' >> ~/.zshrc
source ~/.zshrc
```

### 6) Know how HackerOne tokens work

Most HackerOne-focused scripts currently expect tokens through CLI arguments, not automatic `config.json` loading.

Examples:

```bash
python3 modules/scanners/h1_idor_scanner.py --token-a "TOKEN_A" --token-b "TOKEN_B" --report-id 123456
python3 modules/scanners/h1_race.py --token-a "TOKEN_A" --test 2fa
python3 modules/scanners/h1_oauth_tester.py --token-a "TOKEN_A" --all
python3 modules/recon/hai_probe.py --api-name "H1_USERNAME" --token "H1_API_TOKEN"
```

Special case:

`modules/orchestrator/h1_run.sh` still expects tokens to be edited directly in the file:

```bash
TOKEN_A=""
TOKEN_B=""
```

### 7) Start using the project

You can use it in two ways:

- inside Codex with natural-language prompts
- directly from the terminal with scripts under `modules/*`

## Use In Codex

Open Codex:

```bash
codex
```

Then prompt it in plain English. Good beginner examples:

```text
Use the web2-recon skill to map example.com and summarize the best attack surface.
```

```text
Use the bug-bounty skill to plan the next hunting step for example.com.
```

```text
Use the triage-validation skill to decide whether this finding is reportable.
```

```text
Use the report-writing skill to turn this validated finding into a submission-ready report.
```

How skills work in practice:

- you do not manually "run" a skill from the shell
- you mention the skill in your prompt, or Codex auto-selects it by relevance
- skills guide Codex's reasoning and workflow
- files are only created when Codex actually runs scripts or writes outputs, not just because a skill was mentioned

## Direct Commands

If you want deterministic execution, use the canonical runtime scripts under `modules/*`.

```bash
python3 modules/orchestrator/hunt.py --status
python3 modules/orchestrator/target_selector.py --top 5
python3 modules/orchestrator/hunt.py --target example.com --quick
bash modules/recon/recon_engine.sh example.com
bash modules/scanners/vuln_scanner.sh recon/example.com
python3 modules/reporting/validate.py
python3 modules/reporting/report_generator.py findings/example.com
```

Recommended rule:

- use Codex prompts when you want guidance, planning, and skill-aware help
- use `modules/*` commands when you want exact script behavior and saved output

## Typical Workflows

### 1) Start from a target domain

Use this when you already know the domain you want to test.

```bash
bash modules/recon/recon_engine.sh example.com
bash modules/scanners/vuln_scanner.sh recon/example.com
python3 modules/reporting/validate.py
python3 modules/reporting/report_generator.py findings/example.com
```

In Codex, you can pair that flow with prompts like:

```text
Use the web2-recon skill to review recon/example.com and tell me the highest-ROI attack surface.
```

### 2) Start from a HackerOne-style target list

Use the target selector first:

```bash
python3 modules/orchestrator/target_selector.py --top 5
```

This creates `targets/selected_targets.json`.

Then choose one domain from that file and run recon:

```bash
bash modules/recon/recon_engine.sh chosen-domain.com
```

This is the right flow if you want help choosing a target before hunting.

### 3) Start from a suspected finding

If you already found something manually, use validation first:

```bash
python3 modules/reporting/validate.py
```

Then generate a report once you have enough evidence:

```bash
python3 modules/reporting/report_generator.py --manual --type xss --url "https://target/path?q=test" --param "q" --evidence "Proof of execution here"
```

This flow is useful when recon is already done and you mainly need triage plus reporting help.

## Where Files Go

This is one of the most important beginner sections.

### `targets/selected_targets.json`

Created by:

```bash
python3 modules/orchestrator/target_selector.py --top 5
```

What it contains:

- selected programs
- handles and URLs
- in-scope assets
- extracted `scope_domains`

How to use it:

- read it as a shortlist of possible targets
- choose a real in-scope domain from `scope_domains`
- run recon only on assets you have verified are allowed by the program policy

### `recon/<target>/`

Created by:

```bash
bash modules/recon/recon_engine.sh <target>
```

Common files inside:

- `subdomains/all.txt`: merged subdomain list
- `live/urls.txt`: live hosts found by `httpx`
- `urls/all.txt`: collected URLs
- `urls/with_params.txt`: URLs with parameters
- `urls/js_files.txt`: discovered JavaScript file URLs
- `urls/api_endpoints.txt`: URLs that look like API or GraphQL endpoints
- `js/endpoints.txt`: endpoints extracted from JavaScript
- `js/potential_secrets.txt`: possible secret-like strings from JavaScript, if found

So yes, the current recon workflow does collect JavaScript-related output and basic JS recon artifacts.

### `findings/<target>/`

Created by:

```bash
bash modules/scanners/vuln_scanner.sh recon/<target>
```

Common output buckets:

- `xss/`
- `takeover/`
- `misconfig/`
- `exposure/`
- `ssrf/`
- `cves/`
- `redirects/`
- `manual_review/`
- `summary.txt`

This is the main scanner output area.

### `reports/<target>/`

Created by:

```bash
python3 modules/reporting/report_generator.py findings/<target>
```

Common output:

- generated Markdown reports
- `SUMMARY.md`
- `SUMMARY.json`

### Important file-saving note

If you only ask Codex for advice, planning, or classification, it may not create any files.

Files are usually created when:

- a script in `modules/*` is executed
- Codex is explicitly asked to save output
- a reporting or validation flow writes a local artifact

## Skills Explained

These are the main skills beginners will use:

- `bug-bounty`: master workflow from recon to validation and reporting
- `web2-recon`: recon guidance for subdomains, live hosts, URLs, APIs, and JS
- `web2-vuln-classes`: bug-class reference for what to test next
- `security-arsenal`: payloads, gf pattern ideas, and testing helpers
- `triage-validation`: decide whether a finding is real and worth reporting
- `report-writing`: turn a validated issue into a cleaner bug bounty report
- `web3-audit`: smart contract and DeFi review workflow

Beginner shortcut:

- starting recon: use `web2-recon`
- not sure what to hunt next: use `bug-bounty`
- checking one bug class: use `web2-vuln-classes`
- deciding whether to submit: use `triage-validation`
- writing the report: use `report-writing`

## Commands Folder Explained

The `commands/` folder is easy to misunderstand.

What it is:

- a set of Markdown reference docs
- prompt cheatsheets you can read or reuse
- a place to keep repeatable prompt patterns

What it is not:

- not a Codex CLI slash-command system
- not something you execute as a slash-style terminal command
- not a replacement for the real scripts in `modules/*`

Example of correct use:

- read `commands/recon.md`
- reuse the prompt style inside Codex
- then run `modules/recon/recon_engine.sh` if you want actual recon output saved to disk

## Tools Used

### Core runtime tools

- `subfinder` — passive subdomain enumeration
- `assetfinder` — passive subdomain expansion
- `httpx` — live host probing and basic fingerprinting
- `nuclei` — template-based vulnerability checks
- `ffuf` — directory and endpoint fuzzing
- `nmap` — port and service discovery
- `gf` — URL and parameter classification by bug pattern
- `gau` — historical URL collection
- `dalfox` — XSS scanning
- `subjack` — subdomain takeover checks

### Base requirements

- `python3`
- `bash`
- `curl`
- standard Unix utilities such as `grep`, `sed`, `awk`, `sort`, and `timeout`

Install the main stack with:

```bash
./install_tools.sh
```

## Project Layout

```text
.
├── .codex-plugin/            # Codex local plugin metadata
├── modules/                  # canonical runtime scripts
│   ├── orchestrator/         # hunt, target selection, intel, mindmap
│   ├── recon/                # recon engine + probes
│   ├── scanners/             # scanners, fuzzers, specialized testers
│   ├── reporting/            # validation + report generation
│   └── support/              # shared helper space
├── skills/                   # Codex skill domains
├── commands/                 # reference prompt docs only
├── agents/                   # agent templates
├── docs/                     # supporting documentation
├── rules/                    # hunting and reporting rules
└── scripts/                  # smoke and audit scripts
```

Root-level scripts are mostly compatibility wrappers. Prefer `modules/*` for current usage.

## Common Beginner Mistakes

- trying a slash-style recon command directly in Codex CLI
- assuming `commands/*.md` are executable commands
- assuming every script automatically reads `config.json`
- using root wrappers when you actually want the canonical `modules/*` script
- assuming a skill mention automatically creates files on disk
- scanning a domain from `selected_targets.json` without checking the program policy first

## More Docs

- [CODEX.md](CODEX.md)
- [docs/project-structure.md](docs/project-structure.md)
- [modules/README.md](modules/README.md)

## Quality Checks

```bash
./scripts/smoke_codex_support.sh
./scripts/audit_runtime_paths.sh
```

## Final Notes

- This repo is optimized for Codex workflows.
- The beginner-friendly way to use it is: install, prompt Codex, then run `modules/*` when you want real output.
- Always verify scope before scanning or submitting anything.
