#!/usr/bin/env python3
"""Validate the shared Codex and Claude Code plugin package."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "design-reference-library"
MARKETPLACE_NAME = "jordanreighn-design"
PLUGIN_ROOT = ROOT / "plugins" / PLUGIN_NAME


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise AssertionError(f"Missing required file: {path.relative_to(ROOT)}") from None
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"Invalid JSON in {path.relative_to(ROOT)}: {exc.msg} at line {exc.lineno}"
        ) from None


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    codex_marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    codex_manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    claude_manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")

    require(codex_marketplace.get("name") == MARKETPLACE_NAME, "Codex marketplace name mismatch", errors)
    require(claude_marketplace.get("name") == MARKETPLACE_NAME, "Claude marketplace name mismatch", errors)
    require(codex_manifest.get("name") == PLUGIN_NAME, "Codex plugin name mismatch", errors)
    require(claude_manifest.get("name") == PLUGIN_NAME, "Claude plugin name mismatch", errors)

    versions = {
        codex_manifest.get("version"),
        claude_manifest.get("version"),
        claude_marketplace.get("version"),
        claude_marketplace.get("plugins", [{}])[0].get("version"),
    }
    require(len(versions) == 1 and None not in versions, "Plugin versions are not synchronized", errors)

    codex_entries = codex_marketplace.get("plugins", [])
    claude_entries = claude_marketplace.get("plugins", [])
    require(len(codex_entries) == 1, "Codex marketplace must contain exactly one plugin", errors)
    require(len(claude_entries) == 1, "Claude marketplace must contain exactly one plugin", errors)

    if codex_entries:
        source = codex_entries[0].get("source", {})
        require(source.get("path") == f"./plugins/{PLUGIN_NAME}", "Codex plugin source path mismatch", errors)
    if claude_entries:
        require(
            claude_entries[0].get("source") == f"./plugins/{PLUGIN_NAME}",
            "Claude plugin source path mismatch",
            errors,
        )

    skill = PLUGIN_ROOT / "skills" / PLUGIN_NAME / "SKILL.md"
    require(skill.is_file(), "Shared SKILL.md is missing", errors)
    require((PLUGIN_ROOT / "skills" / PLUGIN_NAME / "references" / "catalog.md").is_file(), "Catalog is missing", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    version = next(iter(versions))
    print(f"Validated Codex and Claude Code manifests for {PLUGIN_NAME} v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
