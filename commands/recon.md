---
description: Reference prompt doc for full recon on a target. Use this as a Codex prompt template or adapt it to the canonical runtime scripts under modules/recon.
---

# Recon Reference Prompt

> Reference doc only. This repo does not add a built-in `/recon` slash command to Codex CLI.

Run the full recon pipeline on a target and produce a prioritized attack surface.

## What This Does

1. Enumerates subdomains (Chaos API + subfinder + assetfinder)
2. Resolves DNS and finds live hosts (dnsx + httpx with status/title/tech)
3. Crawls URLs (katana deep crawl + waybackurls + gau historical)
4. Classifies URLs by bug class (gf patterns)
5. Runs nuclei for known CVEs and misconfigs
6. Outputs prioritized attack surface summary

## Suggested Prompt

```
"Use the web2-recon skill to map target.com and summarize the highest-value attack surface."
```

Or with specific focus:
```
"Use the web2-recon skill to focus on API attack surface for target.com."
"Use the web2-recon skill to focus on auth flows for target.com."
"Run the canonical recon script in fast mode for target.com."
```

## Steps

### Step 1: Subdomain Enumeration

```bash
TARGET="$1"
mkdir -p recon/$TARGET

# Chaos API (ProjectDiscovery — most comprehensive)
curl -s "https://dns.projectdiscovery.io/dns/$TARGET/subdomains" \
  -H "Authorization: $CHAOS_API_KEY" \
  | jq -r '.[]' > recon/$TARGET/subdomains.txt

# subfinder + assetfinder
subfinder -d $TARGET -silent | anew recon/$TARGET/subdomains.txt
assetfinder --subs-only $TARGET | anew recon/$TARGET/subdomains.txt

echo "[+] Subdomains: $(wc -l < recon/$TARGET/subdomains.txt)"
```

### Step 2: Live Host Discovery

```bash
# DNS resolve + HTTP probe with tech detection
cat recon/$TARGET/subdomains.txt \
  | dnsx -silent \
  | httpx -silent -status-code -title -tech-detect \
  | tee recon/$TARGET/live-hosts.txt

echo "[+] Live hosts: $(wc -l < recon/$TARGET/live-hosts.txt)"
```

### Step 3: URL Crawl

```bash
# Active crawl
cat recon/$TARGET/live-hosts.txt | awk '{print $1}' \
  | katana -d 3 -jc -kf all -silent \
  | anew recon/$TARGET/urls.txt

# Historical URLs
echo $TARGET | waybackurls | anew recon/$TARGET/urls.txt
gau $TARGET --subs | anew recon/$TARGET/urls.txt

echo "[+] Total URLs: $(wc -l < recon/$TARGET/urls.txt)"
```

### Step 4: Classify URLs

```bash
# Bug class classification
cat recon/$TARGET/urls.txt | gf xss       > recon/$TARGET/xss-candidates.txt
cat recon/$TARGET/urls.txt | gf ssrf      > recon/$TARGET/ssrf-candidates.txt
cat recon/$TARGET/urls.txt | gf idor      > recon/$TARGET/idor-candidates.txt
cat recon/$TARGET/urls.txt | gf sqli      > recon/$TARGET/sqli-candidates.txt
cat recon/$TARGET/urls.txt | gf redirect  > recon/$TARGET/redirect-candidates.txt
cat recon/$TARGET/urls.txt | gf lfi       > recon/$TARGET/lfi-candidates.txt

# API endpoints
cat recon/$TARGET/urls.txt | grep -E "/api/|/v1/|/v2/|/graphql|/rest/" \
  > recon/$TARGET/api-endpoints.txt

echo "[+] IDOR candidates: $(wc -l < recon/$TARGET/idor-candidates.txt)"
echo "[+] SSRF candidates: $(wc -l < recon/$TARGET/ssrf-candidates.txt)"
echo "[+] API endpoints:   $(wc -l < recon/$TARGET/api-endpoints.txt)"
```

### Step 5: Nuclei Scan

```bash
nuclei -l recon/$TARGET/live-hosts.txt \
  -t ~/nuclei-templates/ \
  -severity critical,high,medium \
  -o recon/$TARGET/nuclei.txt

echo "[+] Nuclei findings: $(wc -l < recon/$TARGET/nuclei.txt)"
```

## Output

After running, you will have in `recon/<target>/`:
```
subdomains.txt          # All discovered subdomains
live-hosts.txt          # Live hosts with status/title/tech
urls.txt                # All crawled URLs
api-endpoints.txt       # API-specific paths
idor-candidates.txt     # URLs with ID parameters
ssrf-candidates.txt     # URLs with URL parameters
xss-candidates.txt      # URLs with reflection candidates
nuclei.txt              # Known CVE/misconfig findings
```

## What to Do Next

1. Review `live-hosts.txt` — open interesting ones in browser
2. Check `nuclei.txt` — any high/critical findings?
3. Review `api-endpoints.txt` — start IDOR testing
4. Check for admin panels: grep live-hosts for `/admin`, `/jenkins`, `/grafana`
5. Next, use the hunt reference prompt or run `python3 modules/orchestrator/hunt.py --target target.com --quick`

## 5-Minute Rule

If after running this pipeline:
- All hosts return 403 or static pages
- No API endpoints visible
- No interesting parameters in URLs
- nuclei returns 0 medium/high findings

**→ Move on to a different target.**
