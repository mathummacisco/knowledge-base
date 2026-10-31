#!/usr/bin/env python3
"""
Validates required frontmatter on all .md files under docs/.
Exits non-zero if any file is missing fields or has invalid values.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TEMPLATE_DIR = DOCS / "_templates"

SKIP_DIR_NAMES = {"_templates", "assets"}

REQUIRED = ["title", "owner", "status", "type", "service", "last_reviewed", "review_cadence", "tags"]
VALID_STATUS = {"draft", "active", "deprecated"}
VALID_TYPE = {"sop", "runbook", "troubleshooting", "reference", "analysis", "migration", "architecture"}
VALID_CADENCE = {"monthly", "quarterly", "biannual", "annual"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        data[k.strip()] = v.strip()
    return data


def validate_file(path: Path) -> list[str]:
    errs: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        return ["missing frontmatter"]
    for field in REQUIRED:
        if field not in fm or not fm[field]:
            errs.append(f"missing field: {field}")
    if "status" in fm and fm["status"] not in VALID_STATUS:
        errs.append(f"invalid status: {fm['status']} (must be {sorted(VALID_STATUS)})")
    if "type" in fm and fm["type"] not in VALID_TYPE:
        errs.append(f"invalid type: {fm['type']} (must be {sorted(VALID_TYPE)})")
    if "review_cadence" in fm and fm["review_cadence"] not in VALID_CADENCE:
        errs.append(f"invalid review_cadence: {fm['review_cadence']}")
    if "last_reviewed" in fm and not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["last_reviewed"]):
        errs.append(f"invalid last_reviewed format (need YYYY-MM-DD): {fm['last_reviewed']}")
    # Reject leftover template placeholders for owner and title — these
    # almost always mean someone copy-pasted a template without filling
    # the values in. _templates/ is already skipped above.
    if "owner" in fm:
        owner = fm["owner"].strip().strip('"').strip("'")
        if owner.startswith("<") or "team-or-dl" in owner or owner.endswith("@company.com"):
            errs.append(f"placeholder owner: {fm['owner']} (replace with a real GitHub team handle)")
    if "title" in fm:
        title = fm["title"].strip().strip('"').strip("'")
        bad_markers = ("[YOUR-", "[Your ", "<your-", "<YOUR-", "TODO", "TBD", "FIXME")
        for marker in bad_markers:
            if marker in title:
                errs.append(f"placeholder text in title: contains {marker!r}")
                break
    return errs


def main() -> int:
    failures: dict[str, list[str]] = {}
    checked = 0
    for md in DOCS.rglob("*.md"):
        if any(part in SKIP_DIR_NAMES for part in md.relative_to(DOCS).parts):
            continue
        checked += 1
        errs = validate_file(md)
        if errs:
            failures[str(md.relative_to(ROOT))] = errs
    if failures:
        print(f"❌ Frontmatter validation FAILED for {len(failures)} of {checked} files:\n")
        for path, errs in sorted(failures.items()):
            print(f"  {path}")
            for e in errs:
                print(f"    - {e}")
        return 1
    print(f"✅ Frontmatter valid on all {checked} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
