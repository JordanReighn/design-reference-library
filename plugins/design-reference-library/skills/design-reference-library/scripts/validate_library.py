#!/usr/bin/env python3
"""Validate the vendored design-reference catalog and provenance."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    references = skill_root / "references"
    catalog = references / "catalog.md"
    designs_dir = references / "designs"
    required = [
        catalog,
        references / "synthesis.md",
        references / "upstream.md",
        references / "upstream-license.txt",
    ]
    errors: list[str] = []

    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty required file: {path}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    design_files = sorted(designs_dir.glob("*.md"))
    catalog_text = catalog.read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\(designs/([^)]+\.md)\)", catalog_text))
    present = {path.name for path in design_files}

    if len(design_files) < 50:
        errors.append(f"Expected at least 50 design references, found {len(design_files)}")
    for missing in sorted(present - linked):
        errors.append(f"Design is not linked from catalog: {missing}")
    for missing in sorted(linked - present):
        errors.append(f"Catalog links to a missing design: {missing}")

    for path in design_files:
        content = path.read_text(encoding="utf-8-sig").lstrip()
        if not content.startswith(("---", "#")):
            errors.append(f"Unexpected document start: {path.name}")

    provenance = (references / "upstream.md").read_text(encoding="utf-8")
    if not re.search(r"Resolved commit: `[0-9a-f]{40}`", provenance):
        errors.append("Upstream provenance does not contain a full commit hash")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(design_files)} design references and {len(linked)} catalog links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
