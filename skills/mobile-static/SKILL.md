---
name: mobile-static
description: "Static mobile app review for Android and iOS: APK/AAB/IPA/source analysis, manifest or plist or entitlements review, permissions, storage, crypto, network config, deep links, WebViews, secrets, and reverse-engineering-heavy checks. Use for offline package or source inspection and for mapping findings to MASVS and MASWE."
---

# MOBILE STATIC

Offline review of Android and iOS apps.

Use this when you have an `APK`, `AAB`, `IPA`, extracted app files, or a mobile source tree.

## Core Workflow

Work in this order unless the user asks for a narrower pass:

1. Fingerprint the artifact or codebase.
2. Unpack or decompile enough to inspect metadata and code.
3. Review app metadata and exposed entry points.
4. Check storage, crypto, network configuration, and local trust boundaries.
5. Hunt hardcoded secrets and backend clues.
6. Assess reverse-engineering friction and note whether it is only a resilience observation or part of a real exploit chain.

Keep notes short and map each real issue to `MASVS` and `MASWE` where possible.

## Android Static Flow

Prioritize these checks:

- `AndroidManifest.xml`
  - exported activities, services, receivers, providers
  - permissions
  - `android:debuggable`
  - `android:allowBackup`
  - `android:usesCleartextTraffic`
  - `android:networkSecurityConfig`
- deep links and app links
- WebView configuration and JavaScript bridges
- local storage, shared preferences, databases, files, logs, and clipboard usage
- keystore and crypto usage
- bundled secrets, API keys, tokens, certificates, and test endpoints
- anti-tamper and anti-static-analysis measures

Useful starting commands:

```bash
apktool d app.apk -o out/apktool
jadx -d out/jadx app.apk
rg -n "allowBackup|debuggable|usesCleartextTraffic|networkSecurityConfig|exported" out/apktool
rg -n "WebView|addJavascriptInterface|setJavaScriptEnabled|SharedPreferences|Cipher|KeyStore" out/jadx
```

## iOS Static Flow

Prioritize these checks:

- `Info.plist`
  - ATS exceptions
  - URL schemes
  - universal links
  - privacy permission usage strings
- entitlements
  - keychain access groups
  - associated domains
  - push, file sharing, app groups, and other high-trust capabilities
- local storage, keychain usage, plist files, SQLite, caches, and logs
- local authentication use
- binary inspection, symbols, strings, and embedded secrets
- anti-tamper and anti-static-analysis measures

Useful starting commands:

```bash
unzip app.ipa -d out/ipa
plutil -p Payload/*.app/Info.plist
codesign -d --entitlements :- Payload/*.app 2>/dev/null
strings -a Payload/*.app/* | rg "https://|apikey|token|secret|client_id"
```

## Reference Loading

Load only the sections you need.

- Android platform and testing:
  - `Refrence/mastg/Document/0x05a-Platform-Overview.md`
  - `Refrence/mastg/Document/0x05d-Testing-Data-Storage.md`
  - `Refrence/mastg/Document/0x05g-Testing-Network-Communication.md`
  - `Refrence/mastg/Document/0x05h-Testing-Platform-Interaction.md`
  - `Refrence/mastg/Document/0x05i-Testing-Code-Quality-and-Build-Settings.md`
  - `Refrence/mastg/Document/0x05j-Testing-Resiliency-Against-Reverse-Engineering.md`
- iOS platform and testing:
  - `Refrence/mastg/Document/0x06a-Platform-Overview.md`
  - `Refrence/mastg/Document/0x06d-Testing-Data-Storage.md`
  - `Refrence/mastg/Document/0x06g-Testing-Network-Communication.md`
  - `Refrence/mastg/Document/0x06h-Testing-Platform-Interaction.md`
  - `Refrence/mastg/Document/0x06i-Testing-Code-Quality-and-Build-Settings.md`
  - `Refrence/mastg/Document/0x06j-Testing-Resiliency-Against-Reverse-Engineering.md`
- Weakness mapping:
  - `Refrence/maswe/weaknesses`
  - `Refrence/OWASP_MASVS.cdx.json`
  - `Refrence/OWASP_MAS_Checklist.xlsx`
- Android practical operator references:
  - `Refrence/Learn-android-bug-bounty/General-Commands.md`
  - `Refrence/Learn-android-bug-bounty/deeplink_discovery_methods.md`
  - `Refrence/Learn-android-bug-bounty/mobsf_docker_usage.md`
  - `Refrence/Learn-android-bug-bounty/Grep-Sensitive-Words.sh`
  - `Refrence/Learn-android-bug-bounty/Know-Minimum-SDK-Version-of-APK.txt`

Useful searches:

```bash
rg -n "^id: MASWE-|masvs-v2:|platform:" Refrence/maswe/weaknesses
rg -n "backup|keychain|cleartext|ATS|WebView|deep link|universal link|obfus|tamper" Refrence/mastg/Document
rg -n "adb|frida|objection|mobsf|deeplink" Refrence/Learn-android-bug-bounty
```

## Reporting Rules

- A hardcoded secret, exported component, unsafe deep link, or weak local storage issue can be a real finding if you can show realistic impact.
- Missing anti-reversing alone is not automatically reportable. Treat it as a resilience assessment note unless it enables a real exploit chain.
- If you uncover backend hosts or API paths, hand off to `web2-recon` instead of rebuilding web recon here.
