# HackerOne Disclosed Report Reference

Use disclosed reports to learn how valid bugs were framed, validated, fixed, and triaged. Do not copy old reports. Use them to build better hypotheses, avoid duplicates, and understand which impacts a program actually accepts.

Primary source:

- HackerOne Hacktivity: https://hackerone.com/hacktivity

## Pre-Hunt Workflow

1. Search the target program name or handle in Hacktivity.
2. Read at least the five most recent disclosed reports for the program.
3. Search for the feature, endpoint, technology, and bug class you plan to test.
4. Record accepted impact language, rejected edge cases, affected asset types, and common remediation.
5. Convert the pattern into a fresh hypothesis for the current in-scope asset.
6. Before reporting, search again by endpoint name and bug title to reduce duplicate risk.

## Search Patterns

Use these as Hacktivity, browser, or search-engine queries:

```text
PROGRAM_NAME IDOR
PROGRAM_NAME BOLA
PROGRAM_NAME authorization bypass
PROGRAM_NAME OAuth redirect_uri
PROGRAM_NAME SSRF webhook
PROGRAM_NAME stored XSS
PROGRAM_NAME GraphQL node
PROGRAM_NAME file upload
PROGRAM_NAME race condition
PROGRAM_NAME business logic
PROGRAM_NAME cache poisoning
PROGRAM_NAME Android
PROGRAM_NAME iOS
PROGRAM_NAME information disclosure
```

Search by endpoint when you have one:

```text
PROGRAM_NAME /api/orders
PROGRAM_NAME GraphQL mutation
PROGRAM_NAME reset password
PROGRAM_NAME invoice export
PROGRAM_NAME webhook URL
```

## Bug-Class Study Map

| Bug class | What to learn from disclosed reports | Search terms |
|:---|:---|:---|
| IDOR / BOLA | Object IDs, ownership checks, cross-tenant impact, read vs write severity | `IDOR`, `BOLA`, `object level authorization`, `tenant` |
| Auth bypass | Missing middleware, old API versions, role confusion, admin-only routes | `auth bypass`, `access control`, `privilege escalation` |
| OAuth / OIDC | Redirect validation, missing PKCE, state handling, account linking | `OAuth`, `redirect_uri`, `PKCE`, `state` |
| SSRF | URL fetchers, webhooks, PDF/image processors, internal-data proof | `SSRF`, `webhook`, `metadata`, `callback` |
| XSS | Stored sinks, sensitive pages, account takeover chains, CSP bypass context | `XSS`, `stored`, `DOM`, `CSP` |
| GraphQL | Introspection, node IDOR, mutation auth, batching and rate limits | `GraphQL`, `mutation`, `node`, `introspection` |
| File upload | MIME confusion, parser behavior, SVG/HTML rendering, storage impact | `file upload`, `MIME`, `SVG`, `polyglot` |
| Race condition | Limit bypass, coupon reuse, double actions, timing windows | `race condition`, `TOCTOU`, `limit bypass` |
| Business logic | Workflow skips, pricing abuse, state-machine gaps, refund/credit abuse | `business logic`, `workflow`, `price`, `refund` |
| Cache poisoning | Unkeyed inputs, CDN behavior, host/header variance, cache deception | `cache poisoning`, `unkeyed`, `cache deception` |
| Mobile | API version drift, deep links, exported components, storage, pinning context | `Android`, `iOS`, `mobile`, `deep link` |
| Info disclosure | Data sensitivity, public-vs-private distinction, accepted low impact | `information disclosure`, `PII`, `sensitive data` |

## Report Study Checklist

For each useful report, capture:

```text
Program:
Bug class:
Affected feature:
Affected endpoint or object type:
Required attacker account level:
Victim action required:
Impact accepted by triage:
Evidence style:
Severity:
Duplicate or prior-art clues:
Fresh hypothesis for my target:
```

## How To Use This During Hunting

- Start with the highest-value feature, not the bug class.
- Compare disclosed patterns against the current app's auth boundaries.
- Look for sibling endpoints and old API versions near a previously paid pattern.
- Use Burp Suite MCP or saved Repeater evidence to map real request flows.
- Prefer fresh proof on current in-scope assets over historical similarity.

## What Not To Do

- Do not submit copycat reports without new proof.
- Do not claim severity just because an old report had that severity.
- Do not assume an old bug still exists without direct reproduction.
- Do not copy private details, personal data, or long report text into this repo.
- Do not report a known issue unless the program explicitly pays for regression findings.

## Validation Tie-In

Before submitting, run `skills/triage-validation/SKILL.md` and confirm:

- the asset is in scope
- the bug is reproducible from scratch
- the impact is concrete
- the report is not a known duplicate
- the issue is not on the never-submit list
