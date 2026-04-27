---
name: mobile-dynamic
description: "Dynamic mobile app testing for Android and iOS: device or emulator setup, proxy and MITM, certificate trust, Frida or Objection, SSL pinning bypass, auth and session flows, runtime storage checks, deep links, IPC, WebViews, logs, and resilience verification. Use for live app runtime analysis and instrumentation."
---

# MOBILE DYNAMIC

Runtime testing for Android and iOS apps.

Use this when you need to observe or modify app behavior on a device, emulator, or test harness.

## Core Workflow

Work in this order unless the user asks for a specific check:

1. Choose the test environment: real device, emulator, or simulator replacement strategy.
2. Establish proxy visibility and certificate trust.
3. Confirm whether pinning, root or jailbreak checks, or anti-hooking block analysis.
4. Test runtime behavior: auth, session, API calls, WebViews, deep links, IPC, local data, logs, and clipboard.
5. Separate resilience observations from real exploitable findings.

Keep evidence concrete: request or response, screen state, Frida hook result, or device-side artifact.

## Environment Setup

Android:

- prefer a rooted test device or emulator when advanced runtime inspection is needed
- configure proxy and install trust material
- use `adb`, Frida, and optional Objection for runtime hooks

iOS:

- use a jailbroken device when runtime instrumentation is required
- do not treat the iOS simulator as equivalent to a real device for black-box security testing
- configure proxy visibility and trust material before deeper testing

## Runtime Checks

Prioritize these areas:

- auth and session behavior
- network traffic, API hosts, and pinning bypass
- deep links, app links, URL schemes, and universal links
- IPC and platform interaction
- WebViews and JavaScript bridges
- runtime storage, keychain or keystore access patterns, logs, pasteboard or clipboard, and backups
- root, jailbreak, emulator, debugger, anti-hooking, and tamper responses

Useful tool patterns:

```bash
adb devices
adb logcat
frida-ps -U
objection -g <app> explore
```

## Reference Loading

Load only the chapters needed for the current runtime check.

- cross-cutting reversing and tampering:
  - `Refrence/mastg/Document/0x04c-Tampering-and-Reverse-Engineering.md`
- Android runtime guidance:
  - `Refrence/mastg/Document/0x05b-Android-Security-Testing.md`
  - `Refrence/mastg/Document/0x05g-Testing-Network-Communication.md`
  - `Refrence/mastg/Document/0x05h-Testing-Platform-Interaction.md`
  - `Refrence/mastg/Document/0x05j-Testing-Resiliency-Against-Reverse-Engineering.md`
- iOS runtime guidance:
  - `Refrence/mastg/Document/0x06b-iOS-Security-Testing.md`
  - `Refrence/mastg/Document/0x06g-Testing-Network-Communication.md`
  - `Refrence/mastg/Document/0x06h-Testing-Platform-Interaction.md`
  - `Refrence/mastg/Document/0x06j-Testing-Resiliency-Against-Reverse-Engineering.md`
- weakness and control mapping:
  - `Refrence/maswe/weaknesses`
  - `Refrence/OWASP_MASVS.cdx.json`
- Android practical operator references:
  - `Refrence/Learn-android-bug-bounty/AllDrozer-Commands.md`
  - `Refrence/Learn-android-bug-bounty/General-Commands.md`
  - `Refrence/Learn-android-bug-bounty/Objection-All-Commands.md`
  - `Refrence/Learn-android-bug-bounty/Pidcat-For-Logging.md`
  - `Refrence/Learn-android-bug-bounty/frida-ssl-certificate-issue.md`
  - `Refrence/Learn-android-bug-bounty/Android16-CertInstall.md`
  - `Refrence/Learn-android-bug-bounty/mobsf_docker_usage.md`

Useful searches:

```bash
rg -n "pinning|proxy|certificate|deep link|universal link|WebView|jailbreak|root|debugger|dynamic" Refrence/mastg/Document
rg -n "^id: MASWE-|masvs-v2:|platform:" Refrence/maswe/weaknesses
rg -n "drozer|objection|frida|ssl|cert|pidcat|adb" Refrence/Learn-android-bug-bounty
```

## Reporting Rules

- Do not report a resilience gap by default just because you bypassed pinning, root detection, or anti-hooking.
- MASVS-RESILIENCE gaps are assessment findings unless they chain into real impact such as data theft, auth bypass, or backend compromise.
- When runtime testing reveals backend hosts, undocumented APIs, GraphQL, uploads, or callback endpoints, pivot to `web2-recon` and then `bug-bounty`.
