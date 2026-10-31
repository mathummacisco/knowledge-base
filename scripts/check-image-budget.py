#!/usr/bin/env python3
"""
Image size budget guard.

Walks every image under `docs/` and fails the build when any file exceeds the
per-image budget. Existing oversized files are listed in an explicit exemption
set so the budget can be tightened without breaking the workflow on day one.

Run locally:
    python3 scripts/check-image-budget.py

Add new exemptions sparingly. The right move is almost always to compress the
image (WebP/AVIF at 85-90 quality) instead.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# Per-image budget in bytes (200 KB)
BUDGET = 200 * 1024

# Image suffixes we count toward the budget.
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"}

# Explicit exemptions: paths relative to DOCS that are allowed to be larger
# than the budget. Add a one-line justification when adding to this list.
EXEMPTIONS: set[str] = {
    # No exemptions; compress new uploads to WebP/AVIF before merging.
}


def main() -> int:
    if not DOCS.is_dir():
        print(f"docs/ not found at {DOCS}", file=sys.stderr)
        return 2

    violations: list[tuple[Path, int]] = []
    inventory: list[tuple[Path, int]] = []

    for path in DOCS.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        size = path.stat().st_size
        rel = path.relative_to(DOCS)
        inventory.append((rel, size))
        if size <= BUDGET:
            continue
        if str(rel) in EXEMPTIONS:
            continue
        violations.append((rel, size))

    if violations:
        print(f"FAIL  {len(violations)} image(s) exceed the {BUDGET // 1024} KB per-image budget:")
        print()
        for rel, size in sorted(violations, key=lambda x: -x[1]):
            kb = size / 1024
            over = (size - BUDGET) / 1024
            print(f"   {kb:7.1f} KB  (+{over:6.1f} KB over)   docs/{rel}")
        print()
        print("Compress the offenders (WebP/AVIF @ 85-90 quality) or add an")
        print("explicit exemption with justification to scripts/check-image-budget.py.")
        return 1

    total = sum(s for _, s in inventory)
    print(f"OK    {len(inventory)} image(s) under {BUDGET // 1024} KB budget. Total {total/1024:.1f} KB.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
