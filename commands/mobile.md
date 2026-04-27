---
description: "General mobile app assessment for Android and iOS. Routes APK/AAB/IPA/source targets to static analysis, live apps to dynamic analysis, and backend/API leads to recon and validation. Usage: /mobile <apk|aab|ipa|source path|package|bundle id|app name>"
---

# /mobile

Start a general Android or iOS mobile security review.

Use this when you have a mobile target but have not decided whether static or dynamic analysis is the right first step.

## Usage

```text
/mobile app.apk
/mobile app.aab
/mobile app.ipa
/mobile ./mobile-source
/mobile com.target.app
/mobile target.bundle.id
/mobile "Target App"
```

## What This Does

1. Identifies the target type: APK, AAB, IPA, source tree, package name, bundle ID, or app name.
2. Chooses the first mode:
   - static analysis for APK, AAB, IPA, or source
   - dynamic analysis for a live installed app, package name, bundle ID, or app name
3. Routes detailed checks to `/mobile-static` or `/mobile-dynamic`.
4. Captures backend hosts, API paths, GraphQL routes, upload flows, and callbacks found during mobile analysis.
5. Hands backend/API leads to `/recon`, then `/validate`, before report writing.

## Routing Rules

| Target input | Start with | Next command |
|:---|:---|:---|
| `.apk` or `.aab` | Android static analysis | `/mobile-static <file>` |
| `.ipa` | iOS static analysis | `/mobile-static <file>` |
| source directory | static source review | `/mobile-static <path>` |
| Android package name | Android runtime testing | `/mobile-dynamic <package>` |
| iOS bundle ID | iOS runtime testing | `/mobile-dynamic <bundle-id>` |
| app name only | runtime triage first | `/mobile-dynamic "<app name>"` |

## Output Format

```text
Target:
Platform:
Recommended mode:
Why:
Run next:
Evidence to collect:
Backend/API leads:
Validation path:
```

## Rules

- Read program scope before testing any app or backend asset.
- Do not treat anti-reversing, root detection, jailbreak detection, or pinning bypass as a bounty finding by itself.
- If the app exposes backend hosts or APIs, confirm the backend assets are in scope before probing.
- Keep static and dynamic evidence separate, then validate real impact before reporting.
