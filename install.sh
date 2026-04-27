#!/usr/bin/env bash
# Codex Bug Bounty - install support files for Codex and Claude Code.

set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: ./install.sh [--codex|--claude|--all]

Options:
  --codex   Install standalone Codex skills and custom agents
  --claude  Install standalone Claude Code skills, commands, and agents
  --all     Install both Codex and Claude Code support (default)
  -h, --help
USAGE
}

TARGET="all"

case "${1:---all}" in
    --codex)
        TARGET="codex"
        ;;
    --claude)
        TARGET="claude"
        ;;
    --all)
        TARGET="all"
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        echo "Unknown option: $1" >&2
        usage
        exit 2
        ;;
esac

copy_dir_contents() {
    local src="$1"
    local dst="$2"

    mkdir -p "$dst"
    cp -R "$src"/. "$dst"/
}

install_codex() {
    local skills_dir="${HOME}/.codex/skills"
    local agents_dir="${HOME}/.codex/agents"

    echo "Installing Codex Bug Bounty support..."
    mkdir -p "$skills_dir" "$agents_dir"

    for skill_dir in skills/*/; do
        local skill_name
        skill_name="$(basename "$skill_dir")"
        copy_dir_contents "$skill_dir" "${skills_dir}/${skill_name}"
        echo "  installed Codex skill: ${skill_name}"
    done

    for agent_file in .codex/agents/*.toml; do
        cp "$agent_file" "${agents_dir}/$(basename "$agent_file")"
        echo "  installed Codex agent: $(basename "$agent_file")"
    done

    echo ""
    echo "Codex plugin metadata is available in .codex-plugin/plugin.json"
    echo "Local Codex marketplace: .agents/plugins/marketplace.json"
    echo "In Codex, open /plugins or run a new session from this repo to use the local plugin."
}

install_claude() {
    local skills_dir="${HOME}/.claude/skills"
    local commands_dir="${HOME}/.claude/commands"
    local agents_dir="${HOME}/.claude/agents"

    echo "Installing Claude Code Bug Bounty support..."
    mkdir -p "$skills_dir" "$commands_dir" "$agents_dir"

    for skill_dir in skills/*/; do
        local skill_name
        skill_name="$(basename "$skill_dir")"
        copy_dir_contents "$skill_dir" "${skills_dir}/${skill_name}"
        echo "  installed Claude skill: ${skill_name}"
    done

    for cmd_file in commands/*.md; do
        cp "$cmd_file" "${commands_dir}/$(basename "$cmd_file")"
        echo "  installed Claude command: $(basename "$cmd_file")"
    done

    for agent_file in agents/*.md; do
        cp "$agent_file" "${agents_dir}/$(basename "$agent_file")"
        echo "  installed Claude agent: $(basename "$agent_file")"
    done

    echo ""
    echo "Claude Code plugin metadata is available in .claude-plugin/plugin.json"
    echo "Local Claude marketplace: .claude-plugin/marketplace.json"
    echo "From this repo, Claude Code can also load the plugin with: claude --plugin-dir ."
}

case "$TARGET" in
    codex)
        install_codex
        ;;
    claude)
        install_claude
        ;;
    all)
        install_codex
        echo ""
        install_claude
        ;;
esac

echo ""
echo "Done. Only test assets that are explicitly in scope, and validate findings before reporting."
