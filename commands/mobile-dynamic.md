---
description: "Dynamic mobile app testing for Android and iOS. Covers device or emulator setup, proxy and MITM, certificate trust, Frida or Objection, SSL pinning bypass, auth/session flows, runtime storage, deep links, IPC, WebViews, logs, and resilience checks. Usage: /mobile-dynamic <package|bundle id|app name>"
---

# /mobile-dynamic

Run a focused runtime review of an Android or iOS mobile app.

## Usage

```text
/mobile-dynamic com.target.app
/mobile-dynamic target.bundle.id
/mobile-dynamic "Target App"
```

## What This Does

1. Chooses the runtime environment: real device, emulator, or jailbroken/rooted test device.
2. Establishes proxy visibility and certificate trust.
3. Checks for SSL pinning, root or jailbreak detection, anti-debugging, and anti-hooking.
4. Tests auth, session, API calls, WebViews, deep links, IPC, local data, logs, and clipboard behavior.
5. Separates resilience notes from real exploitable findings.

## Android Runtime Checks

Prioritize:

- proxy and CA certificate setup
- Frida and Objection attachment
- SSL pinning bypass
- exported activity, service, receiver, and provider behavior
- deep links and app links
- WebView and JavaScript bridge behavior
- local storage, logs, clipboard, and backup behavior

Useful starting commands:

```bash
adb devices
adb logcat
frida-ps -U
objection -g <package> explore
```

## iOS Runtime Checks

Prioritize:

- real jailbroken device when instrumentation is required
- proxy visibility and certificate trust
- pinning bypass and jailbreak detection behavior
- URL schemes and universal links
- keychain, pasteboard, caches, logs, and local files
- WebViews and native bridge behavior

Useful starting commands:

```bash
frida-ps -Uai
objection -g <bundle-id> explore
```

## Output Format

```text
Target:
Platform:
Mode: dynamic
Evidence:
Issue:
MASVS:
MASWE:
Next step:
```

## Rules

- Do not report pinning bypass, root detection bypass, or anti-hooking bypass by itself unless it enables real impact.
- Keep evidence concrete: request, response, screen state, hook result, log, or device-side artifact.
- If runtime testing exposes backend hosts, GraphQL, uploads, or callback endpoints, pivot to `/recon` and then `/validate`.
