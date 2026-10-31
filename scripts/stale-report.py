#!/usr/bin/env python3
"""
Stale doc report: lists docs whose `last_reviewed` is older than their `review_cadence`.

Usage:
  python3 scripts/stale-report.py            # human-readable list
  python3 scripts/stale-report.py --json     # JSON output for dashboards
  python3 scripts/stale-report.py --fail     # exit 1 if any stale (for CI)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

CADENCE_DAYS = {
    "monthly": 30,
    "quarterly": 92,
    "biannual": 183,
    "annual": 366,
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_fm(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail", action="store_true", help="exit 1 if any stale")
    args = ap.parse_args()

    today = date.today()
    stale = []
    for md in DOCS.rglob("*.md"):
        if "/_templates/" in str(md):
            continue
        fm = parse_fm(md.read_text(encoding="utf-8"))
        lr_str = fm.get("last_reviewed")
        cadence = fm.get("review_cadence", "quarterly")
        if not lr_str:
            continue
        try:
            lr = date.fromisoformat(lr_str)
        except ValueError:
            continue
        max_age = CADENCE_DAYS.get(cadence, 92)
        age = (today - lr).days
        if age > max_age:
            stale.append({
                "path": str(md.relative_to(ROOT)),
                "last_reviewed": lr_str,
                "cadence": cadence,
                "age_days": age,
                "overdue_days": age - max_age,
                "owner": fm.get("owner", ""),
            })

    if args.json:
        print(json.dumps(stale, indent=2))
    else:
        if not stale:
            print(f"✅ No stale docs (checked {len(list(DOCS.rglob('*.md')))} files).")
        else:
            print(f"⚠️  {len(stale)} stale doc(s):\n")
            stale.sort(key=lambda d: -d["overdue_days"])
            for d in stale:
                print(f"  {d['overdue_days']:>4}d overdue | {d['cadence']:>9} | {d['owner']:<40} | {d['path']}")

    if args.fail and stale:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
