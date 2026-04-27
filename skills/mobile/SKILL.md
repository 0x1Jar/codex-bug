---
name: mobile
description: Mobile app assessment orchestrator for Android and iOS. Routes work by artifact type (APK/AAB, IPA, source tree, live app) and by mode (static or dynamic). Use when starting a general mobile security review, when the user has not chosen static vs dynamic yet, or when mobile testing needs handoff into web2-recon or bug-bounty for backend/API assessment.
---

# MOBILE

Start here for a general Android or iOS app assessment.

This skill is an orchestrator. It decides the path, keeps outputs structured, and hands off to the right focused skill.

## Decide The Starting Point

Classify the target first:

- `APK` or `AAB` -> Android static-first
- `IPA` -> iOS static-first
- source tree -> static-first
- installed app with no package/source -> dynamic-first

Then choose the mode:

- `static` when you need unpacking, decompilation, manifest/plist review, secrets, storage, crypto, deep links, entitlements, or reverse engineering
- `dynamic` when you need live traffic, runtime hooks, pinning bypass, auth/session testing, WebViews, logs, or device behavior

If the user did not choose a mode, default to:

- static-first for `APK`, `AAB`, `IPA`, or source
- dynamic-first for a live installed app only

## Route To The Right Skill

- Use `mobile-static` for offline artifact or source inspection.
- Use `mobile-dynamic` for runtime verification on device or emulator.
- Use `web2-recon` when the mobile app reveals backend hosts, API paths, GraphQL endpoints, file upload flows, or web callbacks.
- Use `bug-bounty` after recon when the goal shifts from mobile assessment into server-side bug hunting and impact validation.

## Minimum Output Shape

Produce findings in a compact operator format:

```text
Target: <app / package / bundle id>
Platform: android | ios
Mode: static | dynamic
Evidence: <file, screen, request, response, or runtime observation>
Issue: <plain-language finding>
MASVS: <control IDs>
MASWE: <weakness IDs if applicable>
Next step: <confirm dynamically / trace statically / hand off to web2-recon / validate in bug-bounty>
```

If nothing substantial is found, say so plainly and leave a short list of the highest-value next checks.

## Reference Loading

Do not copy OWASP content into the answer. Load only the files needed for the current task.

- Primary references:
  - `Refrence/mastg/Document` -> workflow and platform testing procedures
  - `Refrence/maswe/weaknesses` -> weakness naming and MASVS-linked mapping
  - `Refrence/OWASP_MASVS.cdx.json` -> MASVS control taxonomy
  - `Refrence/OWASP_MAS_Checklist.xlsx` -> checklist grouping and review flow
- Secondary references:
  - `Refrence/Learn-android-bug-bounty` -> practical Android bug bounty commands, deep link discovery, MobSF usage, Drozer, Frida, and Objection notes
  - `Refrence/skills` -> reusable skill patterns and targeted follow-up references such as Firebase APK scanning and source-code static analysis

## Handoff Rule

Do not duplicate the full web recon workflow here.

When mobile testing exposes backend behavior, pivot like this:

1. Extract hostnames, paths, headers, auth flows, and upload points from the app.
2. Use `web2-recon` to map the reachable backend surface.
3. Use `bug-bounty` to hunt and validate real server-side impact.
