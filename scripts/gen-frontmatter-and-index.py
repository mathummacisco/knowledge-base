#!/usr/bin/env python3
"""
Phase 2/3 automation:
  1. Add YAML frontmatter to every .md under docs/ that lacks it.
     - title  : inferred from first H1 or filename
     - type   : inferred from folder (sop/runbook/troubleshooting/reference/...)
     - service: inferred from path under docs/10-platform/aws/<service>/
     - owner, status, last_reviewed, review_cadence, tags get sensible defaults
  2. Generate index.md for every folder under docs/ that lacks one,
     listing all .md files (excluding index) and child folders.

Idempotent: safe to re-run.
"""
from __future__ import annotations
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

TYPE_BY_FOLDER = {
    "sop": "sop",
    "runbook": "runbook",
    "troubleshooting": "troubleshooting",
    "reference": "reference",
    "analysis": "analysis",
    "migration": "migration",
    "architecture": "architecture",
    "capacity": "analysis",
    "cost": "analysis",
    "version-upgrade": "migration",
    "deep-dives": "reference",
    "tls-authentication": "reference",
    "agentic-gateway": "analysis",
}

OWNER_BY_TOP = {
    "00-start-here": "your-org/platform",
    "10-platform": "your-org/platform",
    "20-operations": "your-org/operations",
    "30-security": "your-org/security",
    "40-devops": "your-org/devops",
    "50-devbox": "your-org/devex",
    "60-best-practices": "your-org/platform",
    "70-tools": "your-org/platform",
    "80-proposals": "your-org/architects",
    "90-knowledge-transfer": "your-org/platform",
}

H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)

ACRONYMS = {
    "aws", "eks", "msk", "rds", "iam", "sop", "dr", "mcd", "waf", "ses",
    "csi", "nfs", "efs", "hpa", "tls", "cicd", "adr", "rfc", "opa", "pvc",
    "ip", "vpc", "kms", "ec2", "s3", "ses", "ssl", "ssh", "sns", "sqs",
    "ecs", "ecr", "alb", "nlb", "elb", "api", "url", "uri", "json", "yaml",
    "html", "css", "js", "ts", "ci", "cd", "qa", "ux", "ui", "k8s",
    "documentdb", "opensearch", "elasticache", "splunk", "grafana",
    "argocd", "kyverno", "valkey", "redis", "kafka", "postgres", "aurora",
    "karpenter", "istio", "falco", "wiz", "cognito", "lcp", "bes",
}

def smart_title(s: str) -> str:
    """Title-case but preserve known acronyms in uppercase."""
    words = re.split(r"[-_\s]+", s)
    out = []
    for w in words:
        if not w:
            continue
        lw = w.lower()
        if lw in ACRONYMS:
            out.append(lw.upper() if len(lw) <= 4 else lw.capitalize())
        else:
            out.append(lw.capitalize())
    return " ".join(out)


def has_frontmatter(text: str) -> bool:
    return text.startswith("---") and FRONTMATTER_RE.match(text) is not None


def infer_title(path: Path, text: str) -> str:
    m = H1_RE.search(text)
    if m:
        return m.group(1).strip()
    return smart_title(path.stem)


def infer_type(path: Path) -> str:
    for part in reversed(path.parts):
        if part in TYPE_BY_FOLDER:
            return TYPE_BY_FOLDER[part]
    return "reference"


def infer_service(path: Path) -> str:
    parts = path.parts
    try:
        i = parts.index("aws")
        if i + 1 < len(parts):
            cand = parts[i + 1]
            # Skip when path IS docs/10-platform/aws (no service yet)
            if cand in ("x", "index.md") or cand.endswith(".md"):
                return "n/a"
            return cand
    except ValueError:
        pass
    return "n/a"


def infer_owner(path: Path) -> str:
    rel = path.relative_to(DOCS)
    top = rel.parts[0] if rel.parts else ""
    return OWNER_BY_TOP.get(top, "your-org/platform")


def infer_tags(path: Path) -> list[str]:
    parts = list(path.relative_to(DOCS).parts[:-1])
    tags = []
    for p in parts:
        if p.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_")):
            continue
        if p in tags or p == "assets":
            continue
        tags.append(p)
    return tags[:8]


def build_frontmatter(path: Path, text: str) -> str:
    title = infer_title(path, text)
    typ = infer_type(path)
    service = infer_service(path)
    owner = infer_owner(path)
    tags = infer_tags(path)
    tags_inline = "[" + ", ".join(tags) + "]" if tags else "[]"
    return (
        "---\n"
        f"title: {title}\n"
        f"owner: {owner}\n"
        "status: active\n"
        f"type: {typ}\n"
        f"service: {service}\n"
        f"last_reviewed: {TODAY}\n"
        "review_cadence: quarterly\n"
        f"tags: {tags_inline}\n"
        "---\n\n"
    )


def add_frontmatter_to_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if has_frontmatter(text):
        return False
    fm = build_frontmatter(path, text)
    # Strip a leading H1 if it matches inferred title (avoid duplication)
    new_text = fm + text.lstrip()
    path.write_text(new_text, encoding="utf-8")
    return True


def _is_stub_index(index: Path) -> bool:
    """An index is a stub if it has no body beyond frontmatter / a single H1."""
    if not index.exists():
        return True
    text = index.read_text(encoding="utf-8")
    # Strip frontmatter
    body = FRONTMATTER_RE.sub("", text, count=1).strip()
    # Strip a leading H1
    body = re.sub(r"^#\s+.+?\n", "", body).strip()
    return len(body) < 40  # essentially empty


def generate_index_for(folder: Path) -> bool:
    index = folder / "index.md"
    if index.exists() and not _is_stub_index(index):
        return False
    rel = folder.relative_to(DOCS)
    raw = rel.parts[-1] if rel.parts else "Docs"
    # Strip leading numeric prefix like "10-"
    raw_clean = re.sub(r"^\d+-", "", raw)
    title = smart_title(raw_clean) if raw_clean else "Docs"
    children_dirs = sorted(
        d for d in folder.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_")) and d.name != "assets"
    )
    children_files = sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name != "index.md"
    )
    lines = [
        "---",
        f"title: {title}",
        f"owner: {infer_owner(folder / 'x')}",
        "status: active",
        "type: reference",
        f"service: {infer_service(folder / 'x')}",
        f"last_reviewed: {TODAY}",
        "review_cadence: quarterly",
        f"tags: {infer_tags(folder / 'x')}".replace("'", ""),
        # Generated stubs stay out of search until a human writes real content.
        # Remove the two lines below once the index has been hand-curated.
        "search:",
        "  exclude: true",
        "---",
        "",
        f"# {title}",
        "",
        f"Index of `{rel}` — auto-generated by `scripts/gen-frontmatter-and-index.py`.",
        "",
    ]
    if children_dirs:
        lines.append("## Sub-Sections")
        lines.append("")
        for d in children_dirs:
            lines.append(f"- [{d.name}/]({d.name}/index.md)")
        lines.append("")
    if children_files:
        lines.append("## Documents")
        lines.append("")
        for f in children_files:
            lines.append(f"- [{f.stem}]({f.name})")
        lines.append("")
    index.write_text("\n".join(lines), encoding="utf-8")
    return True


def main() -> int:
    fm_added = 0
    idx_added = 0
    for md in DOCS.rglob("*.md"):
        if "/_templates/" in str(md) or "/assets/" in str(md):
            continue
        if add_frontmatter_to_file(md):
            fm_added += 1
            print(f"  frontmatter: {md.relative_to(ROOT)}")
    for folder in [p for p in DOCS.rglob("*") if p.is_dir()]:
        if folder.name.startswith((".", "_")) or folder.name == "assets":
            continue
        # Skip asset subfolders
        if "assets" in folder.parts:
            continue
        if generate_index_for(folder):
            idx_added += 1
            print(f"  index.md   : {folder.relative_to(ROOT)}/index.md")
    print(f"\nAdded frontmatter to {fm_added} file(s).")
    print(f"Generated {idx_added} index.md file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
