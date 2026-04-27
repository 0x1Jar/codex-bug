---
description: "Static mobile app review for Android and iOS. Reviews APK/AAB/IPA/source artifacts for manifest or plist issues, permissions, storage, crypto, network config, deep links, WebViews, secrets, and MASVS/MASWE mapping. Usage: /mobile-static <apk|aab|ipa|source path>"
---

# /mobile-static

Run a focused static review of an Android or iOS mobile artifact.

## Usage

```text
/mobile-static app.apk
/mobile-static app.aab
/mobile-static app.ipa
/mobile-static ./mobile-source
```

## What This Does

1. Identifies platform and artifact type.
2. Unpacks or decompiles enough to inspect metadata and code.
3. Reviews exposed entry points, storage, crypto, network config, deep links, WebViews, and secrets.
4. Maps real issues to MASVS and MASWE where possible.
5. Hands backend/API leads to `/recon` or the `web2-recon` skill.

## Android Static Checks

Prioritize:

- `AndroidManifest.xml`
- exported activities, services, receivers, and providers
- `debuggable`, `allowBackup`, `usesCleartextTraffic`, and `networkSecurityConfig`
- deep links and app links
- WebView settings and JavaScript bridges
- local storage and logs
- crypto and keystore usage
- bundled secrets, API keys, certificates, and test endpoints

Useful starting commands:

```bash
apktool d app.apk -o out/apktool
jadx -d out/jadx app.apk
rg -n "allowBackup|debuggable|usesCleartextTraffic|networkSecurityConfig|exported" out/apktool
rg -n "WebView|addJavascriptInterface|setJavaScriptEnabled|SharedPreferences|Cipher|KeyStore" out/jadx
```

## iOS Static Checks

Prioritize:

- `Info.plist`
- ATS exceptions
- URL schemes and universal links
- entitlements and keychain access groups
- app groups, file sharing, associated domains, and push capabilities
- plist files, SQLite, caches, logs, and keychain use
- symbols, strings, and embedded secrets

Useful starting commands:

```bash
unzip app.ipa -d out/ipa
plutil -p Payload/*.app/Info.plist
codesign -d --entitlements :- Payload/*.app 2>/dev/null
strings -a Payload/*.app/* | rg "https://|apikey|token|secret|client_id"
```

## Output Format

```text
Target:
Platform:
Mode: static
Evidence:
Issue:
MASVS:
MASWE:
Next step:
```

## Rules

- Do not report missing anti-reversing alone as a bounty finding.
- Treat hardcoded secrets, exported components, unsafe deep links, or weak local storage as findings only when realistic impact is shown.
- If static review exposes backend hosts or APIs, pivot to `/recon` and then `/validate` before report writing.
