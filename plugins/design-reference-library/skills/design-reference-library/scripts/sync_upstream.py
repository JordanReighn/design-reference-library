#!/usr/bin/env python3
"""Vendor DESIGN.md references from VoltAgent/awesome-design-md.

This script intentionally updates only the fixed references/designs directory and
the generated catalog, provenance, and upstream license inside this skill.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_REPOSITORY = "https://github.com/VoltAgent/awesome-design-md.git"
DEFAULT_REF = "main"


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}\n{detail}")
    return result.stdout.strip()


def compress(value: str, limit: int = 260) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("|", "\\|")
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def source_slug(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc.lower() not in {"getdesign.md", "www.getdesign.md"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    return parts[0] if parts else None


def parse_collection(readme: str, valid_slugs: set[str]) -> tuple[list[str], dict[str, tuple[str, str, str]]]:
    category_order: list[str] = []
    entries: dict[str, tuple[str, str, str]] = {}
    in_collection = False
    current_category = "Uncategorized"
    bullet = re.compile(r"^\s*[-*]\s+\[([^]]+)]\(([^)]+)\)\s*(?:[-–—]\s*)?(.*)$")

    for line in readme.splitlines():
        if line.strip() == "## Collection":
            in_collection = True
            continue
        if in_collection and line.startswith("## "):
            break
        if not in_collection:
            continue
        if line.startswith("### "):
            current_category = line[4:].strip()
            if current_category not in category_order:
                category_order.append(current_category)
            continue
        match = bullet.match(line)
        if not match:
            continue
        display_name, url, summary = match.groups()
        slug = source_slug(url)
        if slug and slug in valid_slugs:
            display_name = re.sub(r"[*_`]", "", display_name).strip()
            entries[slug] = (display_name, current_category, compress(summary))

    return category_order, entries


def fallback_metadata(slug: str, content: str) -> tuple[str, str]:
    name_match = re.search(r"^name:\s*[\"']?(.+?)[\"']?\s*$", content, re.MULTILINE)
    if name_match:
        name = re.sub(r"[-_]design-analysis$", "", name_match.group(1), flags=re.IGNORECASE).strip()
    else:
        heading = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        name = heading.group(1).strip() if heading else slug.replace("-", " ").title()

    paragraphs = re.split(r"\n\s*\n", content)
    summary = ""
    for paragraph in paragraphs:
        clean = paragraph.strip()
        if not clean or clean.startswith(("---", "#", "- ", "|")):
            continue
        summary = compress(re.sub(r"[*_`]", "", clean))
        break
    return name, summary or "Design-language reference."


def write_catalog(
    target: Path,
    commit: str,
    designs: dict[str, str],
    category_order: list[str],
    readme_entries: dict[str, tuple[str, str, str]],
) -> None:
    grouped: OrderedDict[str, list[tuple[str, str, str, bool]]] = OrderedDict(
        (category, []) for category in category_order
    )
    grouped.setdefault("Uncategorized", [])

    for slug, content in sorted(designs.items()):
        structured = content.lstrip().startswith("---")
        if slug in readme_entries:
            display, category, summary = readme_entries[slug]
        else:
            display, summary = fallback_metadata(slug, content)
            category = "Uncategorized"
        grouped.setdefault(category, []).append((display, slug, summary, structured))

    lines = [
        "# Design reference catalog",
        "",
        f"Generated from `VoltAgent/awesome-design-md` at commit `{commit}`.",
        "",
        "Use this catalog to resolve names or discover styles by mood and product type. Open only the selected files. `structured` references contain token frontmatter; `prose` references use the older narrative format.",
        "",
    ]
    for category, items in grouped.items():
        if not items:
            continue
        lines.extend([f"## {category}", ""])
        for display, slug, summary, structured in sorted(items, key=lambda item: item[0].lower()):
            format_name = "structured" if structured else "prose"
            lines.append(f"- [{display}](designs/{slug}.md) — `{format_name}` — {summary}")
        lines.append("")
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def sync(repository: str, ref: str) -> int:
    skill_root = Path(__file__).resolve().parents[1]
    references_root = skill_root / "references"
    designs_target = references_root / "designs"
    if designs_target.parent.resolve() != references_root.resolve() or designs_target.name != "designs":
        raise RuntimeError(f"Refusing unsafe designs target: {designs_target}")

    git = shutil.which("git")
    if not git:
        raise RuntimeError("git is required to synchronize the upstream library")

    with tempfile.TemporaryDirectory(prefix="design-reference-sync-") as temp_name:
        checkout = Path(temp_name) / "upstream"
        checkout.mkdir()
        run([git, "init", "--quiet"], cwd=checkout)
        run([git, "remote", "add", "origin", repository], cwd=checkout)
        run([git, "fetch", "--depth", "1", "origin", ref], cwd=checkout)
        run([git, "checkout", "--quiet", "--detach", "FETCH_HEAD"], cwd=checkout)
        commit = run([git, "rev-parse", "HEAD"], cwd=checkout)

        source_root = checkout / "design-md"
        source_files = sorted(source_root.glob("*/DESIGN.md"))
        if len(source_files) < 50:
            raise RuntimeError(f"Expected at least 50 DESIGN.md files, found {len(source_files)}")

        designs = {path.parent.name: path.read_text(encoding="utf-8-sig") for path in source_files}
        if len(designs) != len(source_files):
            raise RuntimeError("Duplicate design slugs detected")

        readme = (checkout / "README.md").read_text(encoding="utf-8-sig")
        category_order, readme_entries = parse_collection(readme, set(designs))

        if designs_target.exists():
            shutil.rmtree(designs_target)
        designs_target.mkdir(parents=True)
        for slug, content in designs.items():
            (designs_target / f"{slug}.md").write_text(content, encoding="utf-8")

        license_source = checkout / "LICENSE"
        if not license_source.exists():
            raise RuntimeError("Upstream LICENSE is missing")
        shutil.copy2(license_source, references_root / "upstream-license.txt")

        synced = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        provenance = (
            "# Upstream provenance\n\n"
            f"- Repository: `{repository}`\n"
            f"- Requested ref: `{ref}`\n"
            f"- Resolved commit: `{commit}`\n"
            f"- Synchronized: `{synced}`\n"
            f"- Vendored design files: `{len(designs)}`\n"
            "- License: `references/upstream-license.txt`\n\n"
            "The files in `references/designs/` are unmodified textual analyses from the upstream repository. Brand names identify sources of visual inspiration and do not imply affiliation.\n"
        )
        (references_root / "upstream.md").write_text(provenance, encoding="utf-8")
        write_catalog(references_root / "catalog.md", commit, designs, category_order, readme_entries)

    print(f"Synchronized {len(designs)} design references at {commit}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--ref", default=DEFAULT_REF)
    args = parser.parse_args()
    try:
        return sync(args.repository, args.ref)
    except (OSError, RuntimeError) as error:
        print(f"sync_upstream: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
