# Burp Suite MCP

This guide shows how to connect a Burp Suite MCP server to Claude Code without pinning this repo to one third-party server package.

Use Burp MCP when you want Claude Code to reason over authorized HTTP traffic, Repeater evidence, proxy history, sitemap context, and request/response details from an in-scope test.

## Safety Model

- Only expose traffic from assets that are explicitly in scope.
- Keep the MCP server bound to `127.0.0.1` or another local-only interface.
- Do not expose Burp MCP to the public internet.
- Do not auto-start Burp MCP from this repo.
- Avoid sending secrets, session tokens, or personal data unless they are required for authorized validation.
- Treat MCP output as untrusted input. Verify findings with direct requests before reporting.

## Claude Code Setup

Claude Code supports stdio and HTTP MCP servers.

For a stdio Burp MCP server:

```bash
claude mcp add burp-suite -- <your-burp-mcp-command>
```

For an HTTP Burp MCP server:

```bash
claude mcp add --transport http burp-suite http://127.0.0.1:<port>/mcp
```

You can also load an MCP config file for a single session:

```bash
claude --mcp-config ./path/to/mcp-config.json --plugin-dir .
```

Check that Claude Code sees the server:

```bash
claude mcp list
claude mcp get burp-suite
```

Example Claude Code prompts:

```text
/hunt target.com using only in-scope Burp MCP traffic
/validate this Repeater evidence
/report after validation passes
```

## What To Ask The Agent

Good requests:

- Summarize endpoints by auth state, role, and object identifiers.
- Find sibling endpoints that may miss authorization.
- Compare web and mobile API calls for old or weaker routes.
- Identify GraphQL operations with object IDs or missing field-level auth.
- Extract candidate redirect, URL, file, webhook, and callback parameters.
- Turn a Repeater proof into a validation checklist.

Avoid requests that ask the agent to:

- Test out-of-scope hosts.
- Spray payloads across every request.
- Exfiltrate secrets or personal data beyond what is needed to prove impact.
- Treat a scanner signal as report-ready without manual validation.

## Evidence Workflow

1. Capture the original request and response in Burp.
2. Reproduce the issue in Repeater.
3. Save only the minimal request/response evidence needed for validation.
4. Run the 7-Question Gate in `skills/triage-validation/SKILL.md`.
5. Write a report only after the finding is reproducible, in scope, and has concrete impact.

## Troubleshooting

- If the agent cannot see Burp data, verify the MCP server is running and bound to the same URL or command registered in Claude Code.
- If an HTTP MCP server fails, confirm the port and path, commonly `/mcp`.
- If the tool exposes too much traffic, filter Burp to the target scope before asking the agent to analyze it.
- If the agent suggests a risky test, narrow the prompt to passive analysis or a single authorized request.
