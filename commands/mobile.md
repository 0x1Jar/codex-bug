---
description: Reference prompt doc for Android and iOS mobile app assessment. Use this as a Codex prompt template and pair it with the mobile, mobile-static, and mobile-dynamic skills.
---

# Mobile Reference Prompt

> Reference doc only. This repo does not add a built-in `/mobile` slash command to Codex CLI.

Use this when you want Codex to assess an Android or iOS app and choose the right static or dynamic workflow.

## What This Does

1. Classifies the target as Android or iOS
2. Chooses static or dynamic analysis based on the available artifact
3. Maps findings to MASVS and MASWE when possible
4. Hands off backend or API work to `web2-recon`
5. Hands off exploit validation to `bug-bounty`

## Suggested Prompt

General mobile assessment:

```text
"Use the mobile skill to assess this Android app from the APK and produce findings mapped to MASVS and MASWE."
"Use the mobile skill to assess this iOS app from the IPA and note when to switch from static to dynamic testing."
```

Static-only assessment:

```text
"Use the mobile-static skill to review this APK for exported components, backup risk, WebView issues, secrets, and network configuration."
"Use the mobile-static skill to inspect this IPA for ATS exceptions, entitlements, URL schemes, keychain usage, and embedded secrets."
```

Dynamic-only assessment:

```text
"Use the mobile-dynamic skill to test this Android app with proxying, Frida, and SSL pinning bypass."
"Use the mobile-dynamic skill to test this iOS app on a jailbroken device and focus on auth flows, WebViews, URL handlers, and runtime storage."
```

Backend handoff:

```text
"Use the mobile skill to extract backend hosts and API paths from this app, then continue with web2-recon on the discovered targets."
"Use the mobile-dynamic skill to observe the app's API traffic, summarize the backend surface, then pivot into bug-bounty for server-side validation."
```

## Operating Notes

- Start with `mobile` when the user has not chosen static vs dynamic yet.
- Use `mobile-static` for `APK`, `AAB`, `IPA`, extracted app files, or source trees.
- Use `mobile-dynamic` for installed apps, emulator or device testing, proxying, and instrumentation.
- Do not duplicate full backend recon here. When the app reveals web targets, continue with the existing `web2-recon` workflow.

## Expected Output

Keep output compact and operator-friendly:

```text
Target
Platform
Mode
Evidence
Issue
MASVS
MASWE
Next step
```
