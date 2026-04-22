#!/bin/bash
# Codex-first installer with Claude compatibility.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$(basename "$SCRIPT_DIR")" = "tools" ]; then
    REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
else
    REPO_DIR="$SCRIPT_DIR"
fi

TARGET="auto"
DRY_RUN=false
FORCE=false

usage() {
    cat <<'USAGE'
Usage: ./install.sh [--target codex|claude|both] [--dry-run] [--force]

Options:
  --target   Install target: codex, claude, or both. Default: auto-detect.
  --dry-run  Show planned actions without writing files.
  --force    Overwrite existing installed files.
  -h, --help Show this help.
USAGE
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
            TARGET="${2:-}"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if [[ "$TARGET" != "auto" && "$TARGET" != "codex" && "$TARGET" != "claude" && "$TARGET" != "both" ]]; then
    echo "Invalid --target: $TARGET"
    usage
    exit 1
fi

RAW_CODEX_HOME="${CODEX_HOME:-}"
RAW_CLAUDE_HOME="${CLAUDE_HOME:-}"
CODEX_HOME="${RAW_CODEX_HOME:-$HOME/.codex}"
CLAUDE_HOME="${RAW_CLAUDE_HOME:-$HOME/.claude}"

CODEX_SKILLS_DIR="$CODEX_HOME/skills"
CODEX_COMMANDS_DIR="$CODEX_HOME/commands"
CLAUDE_SKILLS_DIR="$CLAUDE_HOME/skills"
CLAUDE_COMMANDS_DIR="$CLAUDE_HOME/commands"

codex_detected=false
claude_detected=false
[[ -n "$RAW_CODEX_HOME" || -d "$HOME/.codex" ]] && codex_detected=true
[[ -n "$RAW_CLAUDE_HOME" || -d "$HOME/.claude" ]] && claude_detected=true

if [[ "$TARGET" == "auto" ]]; then
    if [[ "$codex_detected" == true && "$claude_detected" == true ]]; then
        TARGET="both"
    elif [[ "$codex_detected" == true ]]; then
        TARGET="codex"
    elif [[ "$claude_detected" == true ]]; then
        TARGET="claude"
    else
        TARGET="codex"
    fi
fi

run_cmd() {
    if [[ "$DRY_RUN" == true ]]; then
        echo "[dry-run] $*"
    else
        "$@"
    fi
}

copy_file() {
    local src="$1"
    local dst="$2"

    if [[ -f "$dst" && "$FORCE" != true ]]; then
        echo "- Skip existing: $dst (use --force to overwrite)"
        return 0
    fi

    run_cmd mkdir -p "$(dirname "$dst")"
    run_cmd cp "$src" "$dst"
    echo "+ Installed: $dst"
}

install_skills() {
    local dest_root="$1"
    echo "Installing skills -> $dest_root"
    run_cmd mkdir -p "$dest_root"

    for skill_dir in "$REPO_DIR"/skills/*/; do
        [[ -d "$skill_dir" ]] || continue
        local skill_name
        skill_name="$(basename "$skill_dir")"
        copy_file "$skill_dir/SKILL.md" "$dest_root/$skill_name/SKILL.md"
    done
}

install_commands() {
    local dest_root="$1"
    echo "Installing command cheatsheet -> $dest_root"
    run_cmd mkdir -p "$dest_root"

    for cmd_file in "$REPO_DIR"/commands/*.md; do
        [[ -f "$cmd_file" ]] || continue
        local cmd_name
        cmd_name="$(basename "$cmd_file")"
        copy_file "$cmd_file" "$dest_root/$cmd_name"
    done
}

summary() {
    echo
    echo "Install target: $TARGET"
    echo "Repo: $REPO_DIR"
    echo "Dry-run: $DRY_RUN"
    echo "Force overwrite: $FORCE"
    echo
}

summary

echo "Starting Codex-First Bug Bounty installer..."

if [[ "$TARGET" == "codex" || "$TARGET" == "both" ]]; then
    install_skills "$CODEX_SKILLS_DIR"
    install_commands "$CODEX_COMMANDS_DIR"
fi

if [[ "$TARGET" == "claude" || "$TARGET" == "both" ]]; then
    install_skills "$CLAUDE_SKILLS_DIR"
    install_commands "$CLAUDE_COMMANDS_DIR"
fi

echo
if [[ "$DRY_RUN" == true ]]; then
    echo "Dry-run complete. No files were changed."
else
    echo "Install complete."
fi

echo
echo "Quick start (Codex):"
echo "  codex"
echo "  /recon target.com"
echo "  /hunt target.com"

echo
echo "Claude compatibility is still supported through --target claude or --target both."
