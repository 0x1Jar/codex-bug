#!/usr/bin/env python3
"""
HackerOne Target Selector
Fetches public bug bounty programs, ranks them, and outputs top targets.

Usage:
    python3 target_selector.py [--top N] [--output FILE] [--asset-profile web|mobile]
                              [--prefer-fresh] [--prefer-low-competition]
"""

import json
import subprocess
import sys
import os
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_base_dir(script_dir):
    normalized = os.path.abspath(script_dir)
    if os.path.basename(normalized) == "tools":
        return os.path.dirname(normalized)
    if os.path.basename(os.path.dirname(normalized)) == "modules":
        return os.path.dirname(os.path.dirname(normalized))
    return normalized


BASE_DIR = find_base_dir(SCRIPT_DIR)
TARGETS_DIR = os.path.join(BASE_DIR, "targets")
DEFAULT_OUTPUT = os.path.join(TARGETS_DIR, "selected_targets.json")

# HackerOne directory API (public data)
WEB_ASSET_TYPES = {"URL", "WILDCARD", "DOMAIN"}
MOBILE_ASSET_TYPES = {
    "GOOGLE_PLAY_APP_ID",
    "APPLE_STORE_APP_ID",
    "OTHER_APK",
    "OTHER_IPA",
    "TESTFLIGHT",
}


def build_h1_directory_url(asset_profile):
    """Build the HackerOne directory URL for the requested asset profile."""
    asset_types = list(WEB_ASSET_TYPES)
    if asset_profile == "mobile":
        asset_types = list(MOBILE_ASSET_TYPES)

    parts = ["ordering=started_accepting_at", "limit=100"]
    parts.extend(f"asset_types={asset_type}" for asset_type in asset_types)
    return "https://hackerone.com/opportunities/all/search?" + "&".join(parts)


def is_mobile_identifier(identifier):
    """Best-effort mobile asset detection from asset identifiers."""
    identifier = (identifier or "").strip().lower()
    return any(
        hint in identifier
        for hint in (
            "play.google.com/store/apps",
            "apps.apple.com",
            "itunes.apple.com",
        )
    )


def is_mobile_asset(scope):
    """Return True if the scope entry is a mobile asset."""
    asset_type = (scope.get("asset_type") or "").upper()
    identifier = scope.get("asset_identifier", "")
    return asset_type in MOBILE_ASSET_TYPES or is_mobile_identifier(identifier)


def is_web_asset(scope):
    """Return True if the scope entry is a classic web recon asset."""
    asset_type = (scope.get("asset_type") or "").upper()
    identifier = scope.get("asset_identifier", "")
    return asset_type in WEB_ASSET_TYPES or "." in identifier


def fetch_programs(asset_profile="web"):
    """Fetch public HackerOne programs via their directory API."""
    print("[*] Fetching HackerOne programs...")

    programs = []

    # Method 1: HackerOne directory GraphQL-like endpoint
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-H", "Accept: application/json",
                build_h1_directory_url(asset_profile)
            ],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if "data" in data:
                for prog in data["data"]:
                    parsed = parse_h1_program(prog, asset_profile=asset_profile)
                    if parsed["assets"]:
                        programs.append(parsed)
                print(f"    [+] Fetched {len(programs)} programs from HackerOne directory")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        print(f"    [!] HackerOne directory fetch failed: {e}")

    # Method 2: Fallback - fetch from public program list
    if not programs:
        print("    [*] Trying fallback: HackerOne public program list...")
        try:
            result = subprocess.run(
                [
                    "curl", "-s",
                    "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/main/data/hackerone_data.json"
                ],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                for prog in data:
                    parsed = parse_bounty_targets_program(prog, asset_profile=asset_profile)
                    if parsed["assets"]:
                        programs.append(parsed)
                print(f"    [+] Fetched {len(programs)} programs from bounty-targets-data")
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            print(f"    [!] Fallback fetch failed: {e}")

    # Method 3: Second fallback - use curated list
    if not programs:
        print("    [*] Using curated fallback program list...")
        programs = get_curated_programs(asset_profile=asset_profile)

    return programs


def parse_h1_program(prog, asset_profile="web"):
    """Parse a program from HackerOne directory API."""
    bounty_max = prog.get("maximum_bounty_table_value", 0) or 0
    bounty_min = prog.get("minimum_bounty_table_value", 0) or 0
    raw_assets = prog.get("scopes", [])
    filtered_assets = []
    for scope in raw_assets:
        if not isinstance(scope, dict):
            continue
        if asset_profile == "mobile" and not is_mobile_asset(scope):
            continue
        if asset_profile == "web" and not is_web_asset(scope):
            continue
        filtered_assets.append(scope)

    return {
        "name": prog.get("name", "Unknown"),
        "handle": prog.get("handle", ""),
        "url": f"https://hackerone.com/{prog.get('handle', '')}",
        "managed": prog.get("triage_active", False),
        "bounty_min": bounty_min,
        "bounty_max": bounty_max,
        "offers_bounties": bounty_max > 0,
        "response_efficiency": prog.get("response_efficiency_percentage", 0) or 0,
        "assets": filtered_assets,
        "has_wildcard": any(
            "*" in (s.get("asset_identifier", "") if isinstance(s, dict) else str(s))
            for s in filtered_assets
        ),
        "started_accepting_at": prog.get("started_accepting_at", ""),
        "source": "hackerone_directory"
    }


def parse_bounty_targets_program(prog, asset_profile="web"):
    """Parse a program from bounty-targets-data."""
    targets = prog.get("targets", {})
    in_scope = targets.get("in_scope", [])

    # Extract only the relevant assets from in_scope.
    assets = []
    has_wildcard = False
    for scope in in_scope:
        identifier = scope.get("asset_identifier", "")
        asset_type = (scope.get("asset_type", "") or "").upper()
        if asset_profile == "mobile":
            keep = is_mobile_asset(scope)
        else:
            keep = is_web_asset(scope)

        if keep:
            assets.append({
                "asset_identifier": identifier,
                "asset_type": asset_type,
                "eligible_for_bounty": scope.get("eligible_for_bounty", False)
            })
            if "*" in identifier:
                has_wildcard = True

    return {
        "name": prog.get("name", "Unknown"),
        "handle": prog.get("handle", ""),
        "url": prog.get("url", f"https://hackerone.com/{prog.get('handle', '')}"),
        "managed": bool(prog.get("managed_program", False)),
        "bounty_min": 0,
        "bounty_max": 0,
        "offers_bounties": bool(prog.get("offers_bounties", False)),
        "response_efficiency": prog.get("response_efficiency_percentage", 0) or 0,
        "average_time_to_first_program_response": prog.get("average_time_to_first_program_response"),
        "average_time_to_report_resolved": prog.get("average_time_to_report_resolved"),
        "submission_state": prog.get("submission_state", ""),
        "assets": assets,
        "has_wildcard": has_wildcard,
        "started_accepting_at": prog.get("started_accepting_at", ""),
        "source": "bounty_targets_data"
    }


def get_curated_programs(asset_profile="web"):
    """Curated list of known good bug bounty targets for when APIs are down."""
    note = "Replace with actual targets - run with internet access to fetch real programs"
    return [
        {
            "name": "Example Mobile Program (placeholder)" if asset_profile == "mobile" else "Example Program (placeholder)",
            "handle": "example",
            "url": "https://hackerone.com/example",
            "managed": False,
            "bounty_min": 100,
            "bounty_max": 10000,
            "response_efficiency": 80,
            "assets": [],
            "has_wildcard": asset_profile == "web",
            "started_accepting_at": "",
            "source": "curated_fallback",
            "note": note
        }
    ]


def count_eligible_bounty_assets(prog):
    """Count in-scope assets explicitly marked eligible for bounty."""
    count = 0
    for asset in prog.get("assets", []):
        if isinstance(asset, dict) and asset.get("eligible_for_bounty"):
            count += 1
    return count


def get_mobile_platforms(prog):
    """Return the mobile platforms represented in a program's scope."""
    platforms = set()
    for asset in prog.get("assets", []):
        asset_type = (asset.get("asset_type", "") if isinstance(asset, dict) else "").upper()
        identifier = asset.get("asset_identifier", "") if isinstance(asset, dict) else str(asset)
        normalized = identifier.lower()

        if asset_type in {"GOOGLE_PLAY_APP_ID", "OTHER_APK"} or "play.google.com/store/apps" in normalized:
            platforms.add("android")
        if asset_type in {"APPLE_STORE_APP_ID", "OTHER_IPA", "TESTFLIGHT"} or "apps.apple.com" in normalized or "itunes.apple.com" in normalized:
            platforms.add("ios")

    return sorted(platforms)


def freshness_bonus(prog, prefer_fresh=False):
    """Return a score bonus for newer programs when launch date is available."""
    if not prefer_fresh:
        return 0

    start_date = prog.get("started_accepting_at", "")
    if not start_date:
        return 0

    try:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        age_days = (datetime.now(start.tzinfo) - start).days
    except (ValueError, TypeError):
        return 0

    if age_days < 45:
        return 25
    if age_days < 90:
        return 18
    if age_days < 180:
        return 10
    if age_days < 365:
        return 5
    return 0


def low_competition_bonus(prog, prefer_low_competition=False, asset_profile="web"):
    """Return a heuristic bonus for quieter, narrower targets.

    Public data does not expose "hunter count", so this is an inference:
    - fewer in-scope mobile assets usually means narrower attack surface
    - fast first-response / resolution can indicate lower queue pressure
    - non-managed programs may attract less broad researcher traffic
    """
    if not prefer_low_competition:
        return 0

    score = 0
    asset_count = len(prog.get("assets", []))
    eligible_asset_count = count_eligible_bounty_assets(prog)

    if asset_profile == "mobile":
        if asset_count <= 2:
            score += 18
        elif asset_count <= 4:
            score += 12
        elif asset_count <= 8:
            score += 6
        elif asset_count >= 20:
            score -= 10

        if eligible_asset_count <= 2:
            score += 8
        elif eligible_asset_count <= 4:
            score += 4
        elif eligible_asset_count >= 15:
            score -= 6
    else:
        if asset_count <= 5:
            score += 10
        elif asset_count >= 50:
            score -= 8

    first_response = prog.get("average_time_to_first_program_response")
    if isinstance(first_response, (int, float)):
        if first_response <= 12:
            score += 5
        elif first_response <= 24:
            score += 3
        elif first_response >= 72:
            score -= 3

    resolution_time = prog.get("average_time_to_report_resolved")
    if isinstance(resolution_time, (int, float)):
        if resolution_time <= 240:
            score += 5
        elif resolution_time <= 720:
            score += 3
        elif resolution_time >= 3000:
            score -= 4

    if not prog.get("managed"):
        score += 3

    return score


def score_program(
    prog,
    prefer_large_scope=False,
    asset_profile="web",
    prefer_fresh=False,
    prefer_low_competition=False,
):
    """Score a program for targeting priority (higher = better)."""
    score = 0

    # Prefer paid bug bounty programs over disclosure-only programs.
    if prog.get("offers_bounties"):
        score += 25
    else:
        score -= 15

    eligible_asset_count = count_eligible_bounty_assets(prog)
    asset_count = len(prog.get("assets", []))

    if asset_profile == "mobile":
        platforms = get_mobile_platforms(prog)
        if len(platforms) == 2:
            score += 20
        elif len(platforms) == 1:
            score += 10

        score += min(asset_count * 4, 28)

        if eligible_asset_count >= 10:
            score += 15
        elif eligible_asset_count >= 5:
            score += 10
        elif eligible_asset_count >= 2:
            score += 5

        if prefer_large_scope:
            if asset_count >= 15:
                score += 15
            elif asset_count >= 8:
                score += 10
            elif asset_count >= 4:
                score += 5
    else:
        # Wildcard scope is very valuable (more attack surface)
        if prog.get("has_wildcard"):
            score += 30

        # More assets = more attack surface
        score += min(asset_count * 2, 20)

        if eligible_asset_count >= 20:
            score += 10
        elif eligible_asset_count >= 5:
            score += 5

        # Optional mode for users who want the widest scope programs first.
        if prefer_large_scope:
            if asset_count >= 100:
                score += 35
            elif asset_count >= 60:
                score += 25
            elif asset_count >= 30:
                score += 15
            elif asset_count >= 15:
                score += 8

            if eligible_asset_count >= 50:
                score += 15
            elif eligible_asset_count >= 20:
                score += 10
            elif eligible_asset_count >= 10:
                score += 5

    # Higher bounties are better
    bounty_max = prog.get("bounty_max", 0)
    if bounty_max >= 10000:
        score += 25
    elif bounty_max >= 5000:
        score += 20
    elif bounty_max >= 1000:
        score += 15
    elif bounty_max > 0:
        score += 10

    # Good response efficiency means faster triage
    efficiency = prog.get("response_efficiency", 0)
    if efficiency >= 90:
        score += 15
    elif efficiency >= 70:
        score += 10
    elif efficiency >= 50:
        score += 5

    # Newer programs may have more low-hanging fruit.
    # If prefer_fresh is set, freshness gets extra weight later.
    start_date = prog.get("started_accepting_at", "")
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            age_days = (datetime.now(start.tzinfo) - start).days
            if age_days < 90:
                score += 20
            elif age_days < 365:
                score += 10
        except (ValueError, TypeError):
            pass

    # Managed programs have faster triage
    if prog.get("managed"):
        score += 5

    score += freshness_bonus(prog, prefer_fresh=prefer_fresh)
    score += low_competition_bonus(
        prog,
        prefer_low_competition=prefer_low_competition,
        asset_profile=asset_profile,
    )

    return score


def extract_scope_domains(prog):
    """Extract in-scope domains for scanning."""
    domains = []
    for asset in prog.get("assets", []):
        if isinstance(asset, dict):
            identifier = asset.get("asset_identifier", "")
        else:
            identifier = str(asset)

        # Clean up the identifier
        identifier = identifier.strip()
        if not identifier:
            continue

        # Remove protocol prefixes
        for prefix in ("https://", "http://", "*."):
            if identifier.startswith(prefix):
                identifier = identifier[len(prefix):]

        # Remove trailing paths
        identifier = identifier.split("/")[0]

        if "." in identifier and identifier not in domains:
            domains.append(identifier)

    return domains


def extract_mobile_assets(prog):
    """Extract mobile asset identifiers for printing and output."""
    assets = []
    for asset in prog.get("assets", []):
        if not isinstance(asset, dict):
            continue
        identifier = (asset.get("asset_identifier") or "").strip()
        asset_type = (asset.get("asset_type") or "").upper()
        if not identifier:
            continue
        assets.append({
            "asset_identifier": identifier,
            "asset_type": asset_type,
            "eligible_for_bounty": asset.get("eligible_for_bounty", False),
        })
    return assets


def select_targets(
    programs,
    top_n=10,
    prefer_large_scope=False,
    asset_profile="web",
    prefer_fresh=False,
    prefer_low_competition=False,
):
    """Score and rank programs, return top N."""
    print(f"\n[*] Scoring {len(programs)} programs...")
    if prefer_large_scope:
        print("    [*] Selection mode: prefer programs with many in-scope assets")
    if asset_profile == "mobile":
        print("    [*] Asset profile: mobile (iOS/Android app scope)")
    if prefer_fresh:
        print("    [*] Preference: newer programs when launch date is available")
    if prefer_low_competition:
        print("    [*] Preference: lower competition proxy (narrower scope + faster queue signals)")

    scored = []
    for prog in programs:
        prog["asset_count"] = len(prog.get("assets", []))
        prog["eligible_bounty_asset_count"] = count_eligible_bounty_assets(prog)
        prog["score"] = score_program(
            prog,
            prefer_large_scope=prefer_large_scope,
            asset_profile=asset_profile,
            prefer_fresh=prefer_fresh,
            prefer_low_competition=prefer_low_competition,
        )
        if asset_profile == "mobile":
            prog["mobile_assets"] = extract_mobile_assets(prog)
            prog["mobile_platforms"] = get_mobile_platforms(prog)
        else:
            prog["scope_domains"] = extract_scope_domains(prog)
        scored.append(prog)

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    selected = scored[:top_n]

    print(f"[+] Selected top {len(selected)} targets:\n")
    for i, prog in enumerate(selected, 1):
        print(f"  {i:2d}. [{prog['score']:3d} pts] {prog['name']}")
        print(f"      URL: {prog['url']}")
        if asset_profile == "mobile":
            mobile_assets = prog.get("mobile_assets", [])
            asset_str = ", ".join(asset["asset_identifier"] for asset in mobile_assets[:3])
            if len(mobile_assets) > 3:
                asset_str += f" (+{len(mobile_assets)-3} more)"
            platform_str = "/".join(prog.get("mobile_platforms", [])) or "unknown"
            print(f"      Platforms: {platform_str} | "
                  f"Bounty: ${prog.get('bounty_min', '?')}-${prog.get('bounty_max', '?')} | "
                  f"Mobile assets: {prog.get('asset_count', len(prog.get('assets', [])))} | "
                  f"Eligible: {prog.get('eligible_bounty_asset_count', 0)}")
            if asset_str:
                print(f"      App scope: {asset_str}")
            if prefer_low_competition:
                first_response = prog.get("average_time_to_first_program_response")
                resolution_time = prog.get("average_time_to_report_resolved")
                print(f"      Queue proxy: first response={first_response}h | resolved={resolution_time}h")
        else:
            domains = prog["scope_domains"]
            domain_str = ", ".join(domains[:3])
            if len(domains) > 3:
                domain_str += f" (+{len(domains)-3} more)"

            print(f"      Wildcard: {'Yes' if prog['has_wildcard'] else 'No'} | "
                  f"Bounty: ${prog.get('bounty_min', '?')}-${prog.get('bounty_max', '?')} | "
                  f"Assets: {prog.get('asset_count', len(prog.get('assets', [])))} | "
                  f"Eligible: {prog.get('eligible_bounty_asset_count', 0)}")
            if domain_str:
                print(f"      Domains: {domain_str}")
        print()

    return selected


def save_targets(targets, output_file, selection_profile="balanced", asset_profile="web"):
    """Save selected targets to JSON."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    output = {
        "generated_at": datetime.now().isoformat(),
        "selection_profile": selection_profile,
        "asset_profile": asset_profile,
        "total_targets": len(targets),
        "targets": targets,
        "scope_checklist": [
            "Verify each target's scope on their HackerOne page before scanning",
            "Check for out-of-scope domains and IP ranges",
            "Review program policy for rate limiting requirements",
            "Check if automated scanning is allowed",
            "Note any specific testing restrictions (no DoS, no social engineering, etc.)",
            "Verify bounty eligibility for asset types you plan to test"
        ]
    }

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"[+] Saved to {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="HackerOne Target Selector")
    parser.add_argument("--top", type=int, default=10, help="Number of top targets to select")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT, help="Output JSON file")
    parser.add_argument(
        "--asset-profile",
        choices=("web", "mobile"),
        default="web",
        help="Target profile to rank: classic web assets or mobile iOS/Android assets"
    )
    parser.add_argument(
        "--prefer-large-scope",
        action="store_true",
        help="Prioritize programs with many in-scope assets and larger attack surface"
    )
    parser.add_argument(
        "--prefer-fresh",
        action="store_true",
        help="Prefer newer programs when launch date is available in the source data"
    )
    parser.add_argument(
        "--prefer-low-competition",
        action="store_true",
        help="Prefer lower-competition proxies such as narrower scope and faster queue signals"
    )
    args = parser.parse_args()

    print("=============================================")
    print("  HackerOne Target Selector")
    print("=============================================")

    programs = fetch_programs(asset_profile=args.asset_profile)
    if not programs:
        print("[-] No programs found. Check your internet connection.")
        sys.exit(1)

    selected = select_targets(
        programs,
        top_n=args.top,
        prefer_large_scope=args.prefer_large_scope,
        asset_profile=args.asset_profile,
        prefer_fresh=args.prefer_fresh,
        prefer_low_competition=args.prefer_low_competition,
    )
    save_targets(
        selected,
        args.output,
        selection_profile=(
            "fresh_low_competition"
            if args.prefer_fresh and args.prefer_low_competition
            else "large_scope" if args.prefer_large_scope
            else "balanced"
        ),
        asset_profile=args.asset_profile,
    )

    print("\n=============================================")
    print("  IMPORTANT: Scope Checklist")
    print("=============================================")
    print("  Before scanning ANY target:")
    print("  1. Visit the program page and read the full policy")
    print("  2. Verify domains are in-scope")
    print("  3. Check for rate limiting / automation rules")
    print("  4. Note out-of-scope areas")
    print("  5. Only test assets eligible for bounty")
    print("=============================================")


if __name__ == "__main__":
    main()
