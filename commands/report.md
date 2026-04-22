---
description: Reference prompt doc for writing a submission-ready bug bounty report after validation. Use this in Codex chat or pair it with the canonical report_generator.py runtime.
---

# Report Reference Prompt

> Reference doc only. This repo does not add a built-in `/report` slash command to Codex CLI.

Generate a submission-ready bug bounty report.

## Pre-Conditions

Run the validation workflow first. All 4 gates must pass before using this reference prompt.

Never write a report before validating. N/A submissions hurt your validity ratio.

## Suggested Prompt

```
"Use the report-writing skill to turn this validated finding into a submission-ready report."
```

Provide when prompted:
- Platform (HackerOne / Bugcrowd / Intigriti / YesWeHack / Immunefi)
- Bug class
- Affected endpoint
- Your two test accounts and their IDs
- The exact HTTP request that demonstrates the bug
- The exact response that shows the impact
- Tech stack (for CVSS and remediation advice)

## What This Generates

1. Title following the formula: `[Bug Class] in [Endpoint] allows [actor] to [impact]`
2. Summary paragraph (impact-first, no "could potentially")
3. Vulnerability details with CVSS 3.1 score and vector string
4. Steps to Reproduce with copy-paste HTTP requests
5. Impact statement with quantification
6. Recommended fix (1-2 sentences, specific)
7. Supporting materials section

## Platform Selection

### HackerOne Format
- Markdown sections: Summary, Vulnerability Details, Steps to Reproduce, Impact, Recommended Fix
- Include CVSS 3.1 score + vector string
- Include two test account setup instructions
- Keep under 600 words

### Bugcrowd Format
- Title with VRT category: `[VRT Category] > [Subcategory] > P[1-4]`
- Expected vs Actual Behavior section
- Severity Justification section referencing Bugcrowd VRT

### Intigriti Format
- CVSS score prominent at top
- Clear reproduction steps
- Business impact focused

### YesWeHack Format
- Keep the report concise and reproducible (triager-first flow)
- Include: Summary, Prerequisites, Steps to Reproduce, Impact, Remediation
- Explicitly state attacker profile (unauthenticated / authenticated low-priv)
- Add clear evidence blocks (HTTP requests/responses, screenshots, short PoC)
- Mention scope asset exactly as listed in program policy

### Immunefi Format (Web3)
- Root cause in Solidity code
- Foundry PoC test included
- Economic impact quantified in $ value
- Comparison evidence (same check present elsewhere, missing here)

## Writing Rules

1. **Never use:** "could potentially", "may allow", "might be possible"
2. **Always prove:** show actual data/action, not just "200 OK"
3. **Impact first:** sentence 1 = what attacker gets, not what the bug is
4. **Quantify:** how many users affected, what data type, $ amount
5. **Short:** triagers skim. < 600 words.
6. **Human:** write to a person, not a system

## CVSS 3.1 Calculation Guide

Common patterns:
```
IDOR read PII (any user, auth needed):
→ AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N = 6.5 Medium

Auth bypass → admin (no auth):
→ AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H = 9.8 Critical

SSRF → cloud metadata:
→ AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N = 9.1 Critical

Stored XSS (any user, scope changed):
→ AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N = 8.2 High
```

## Escalation Language

Use when payout is being downgraded:
```
"This requires only a free account — no special privileges."
"The exposed data includes [PII type], subject to GDPR/CCPA requirements."
"An attacker can automate this — all [N] records in [X] minutes with a simple loop."
"This is exploitable externally without any internal network access."
"The impact is equivalent to a full data breach of [feature/data type]."
```

## Final Checklist Before Submitting

```
[ ] Title follows formula
[ ] First sentence states exact impact
[ ] HTTP request is copy-pasteable
[ ] Response showing impact included
[ ] Two accounts used (not self-testing)
[ ] CVSS calculated and included
[ ] Fix: 1-2 sentences
[ ] No typos in endpoint/param names
[ ] Under 600 words
[ ] Severity matches impact (no overclaiming)
[ ] NEVER used "could potentially"
```
