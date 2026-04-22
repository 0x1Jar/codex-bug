#!/usr/bin/env python3
"""Validate repo SKILL.md frontmatter for Codex compatibility."""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_DESCRIPTION_LENGTH = 1024


try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - fallback for minimal environments
    yaml = None


def parse_frontmatter(frontmatter: str) -> dict[str, str]:
    if yaml is not None:
        data = yaml.safe_load(frontmatter)
        if not isinstance(data, dict):
            raise ValueError("frontmatter must be a YAML mapping")
        return data

    data: dict[str, str] = {}
    for lineno, line in enumerate(frontmatter.splitlines(), start=1):
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line {lineno}: missing ':'")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.lstrip()

        if not key or not raw_value:
            raise ValueError(f"invalid frontmatter line {lineno}: empty key or value")

        if raw_value[0] in {'"', "'"}:
            quote = raw_value[0]
            if not raw_value.endswith(quote):
                raise ValueError(f"invalid quoted value on line {lineno}")
            value = raw_value[1:-1]
        else:
            if re.search(r":(\s|$)", raw_value):
                raise ValueError(f"possible unquoted ':' in value on line {lineno}")
            value = raw_value

        data[key] = value

    return data


def validate_skill(skill_path: Path) -> list[str]:
    errors: list[str] = []
    text = skill_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return [f"{skill_path}: missing YAML frontmatter"]

    try:
        meta = parse_frontmatter(match.group(1))
    except Exception as exc:  # pragma: no cover - simple CLI validator
        return [f"{skill_path}: invalid YAML frontmatter: {exc}"]

    name = meta.get("name")
    description = meta.get("description")

    if not isinstance(name, str) or not name.strip():
        errors.append(f"{skill_path}: missing or invalid name")

    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_path}: missing or invalid description")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"{skill_path}: description exceeds {MAX_DESCRIPTION_LENGTH} characters"
        )

    return errors


def iter_skill_files(root: Path) -> list[Path]:
    if root.name == "SKILL.md":
        return [root]
    if root.is_dir() and root.name == "skills":
        return sorted(root.glob("*/SKILL.md"))
    if root.is_dir():
        return sorted(root.rglob("SKILL.md"))
    return []


def main(argv: list[str]) -> int:
    targets = [Path(arg) for arg in argv] if argv else [Path("skills")]
    skill_files: list[Path] = []
    for target in targets:
        skill_files.extend(iter_skill_files(target))

    if not skill_files:
        print("FAIL: no SKILL.md files found")
        return 1

    errors: list[str] = []
    for skill_file in sorted(set(skill_files)):
        errors.extend(validate_skill(skill_file))

    if errors:
        print("FAIL: invalid SKILL.md frontmatter detected")
        for error in errors:
            print(error)
        return 1

    print(f"PASS: validated {len(skill_files)} SKILL.md files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
