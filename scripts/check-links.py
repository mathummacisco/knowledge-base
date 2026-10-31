#!/usr/bin/env python3
"""
Validate internal Markdown links and image references across docs/ and root *.md.

Strict (fails CI)
-----------------
- Relative file links and images MUST resolve to an existing file.

Best-effort (warnings only, does not fail CI)
---------------------------------------------
- Heading anchors (#foo). Markdown slug algorithms vary across renderers
  (GitHub vs MkDocs vs pymdownx) and many docs use HTML id="..." anchors.
  We report anchor mismatches as warnings so authors can investigate, but
  the exit code only reflects real broken file references.

Not checked
-----------
- External http(s) URLs (slow and noisy without a network policy).
- mailto: and other non-file schemes.

Designed as a stdlib-only, allowlist-friendly replacement for
lycheeverse/lychee-action.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SKIP_DIR_NAMES = {"_templates", "node_modules", ".git"}

# Markdown image: ![alt](src "title")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# Markdown link: [text](href "title")  — avoid matching image syntax
LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# ATX headings: # Heading, ## Heading, ...
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)

# Explicit anchor via attr_list:  ## Title { #custom-id }
# IDs may start with a digit when they mirror an auto-generated slug like
# `7-proposed-cicd-standardization`.
EXPLICIT_ID_RE = re.compile(r"\{[^}]*#([\w][\w\-:.]*)[^}]*\}")

# Explicit HTML anchor:  <a id="foo"> or <h2 id="foo">
HTML_ID_RE = re.compile(r'<(?:a|h[1-6])\b[^>]*\bid\s*=\s*"([^"]+)"', re.IGNORECASE)
HTML_NAME_RE = re.compile(r'<a\b[^>]*\bname\s*=\s*"([^"]+)"', re.IGNORECASE)


def slugify(text: str) -> str:
    """Match the GitHub-flavored Markdown heading-anchor slug algorithm.

    Notes:
    - Lowercases the text.
    - Removes punctuation other than hyphens (kept) and spaces (turned to hyphens).
    - Does NOT collapse runs of hyphens — that's how `—` (em-dash + spaces)
      produces `--` in real GitHub/MkDocs anchors.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.lower()
    # Strip inline code / markdown emphasis markers and zero-width chars
    text = re.sub(r"[`*_~\u200b]", "", text)
    # Keep only word chars, spaces, and existing hyphens; drop everything else
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    # Spaces become hyphens; runs are NOT collapsed
    text = text.strip().replace(" ", "-")
    return text.strip("-")


def extract_anchors(path: Path) -> set[str]:
    """Return the set of valid heading-anchors for a markdown file."""
    if not path.is_file() or path.suffix.lower() != ".md":
        return set()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    anchors: set[str] = set()
    seen_counts: dict[str, int] = {}
    for m in HEADING_RE.finditer(text):
        raw = m.group(2)
        # Explicit `{ #id }` overrides the auto-slug; record both the
        # explicit id and the heading-text-derived slug.
        for em in EXPLICIT_ID_RE.finditer(raw):
            anchors.add(em.group(1))
        # Strip attr_list `{...}` from the heading text before slugifying
        cleaned = EXPLICIT_ID_RE.sub("", raw).strip()
        slug = slugify(cleaned)
        if not slug:
            continue
        # MkDocs/GitHub disambiguate duplicate slugs with -1, -2, ...
        n = seen_counts.get(slug, 0)
        anchors.add(slug if n == 0 else f"{slug}-{n}")
        seen_counts[slug] = n + 1
    # HTML anchors: <a id="...">, <a name="...">, <h2 id="...">
    for m in HTML_ID_RE.finditer(text):
        anchors.add(m.group(1))
    for m in HTML_NAME_RE.finditer(text):
        anchors.add(m.group(1))
    # Material `tags` plugin replaces `<!-- material/tags -->` with the full
    # tag listing at build time. The rendered HTML carries `id="tag:NAME"`
    # for every tag declared in any doc's frontmatter, so accept those.
    if "<!-- material/tags -->" in text:
        anchors.update(_collect_all_tag_anchors())
    return anchors


def _collect_all_tag_anchors() -> set[str]:
    """Read every doc's frontmatter and return `tag:NAME` anchors."""
    out: set[str] = set()
    inline_tags_re = re.compile(r"tags:\s*\[([^\]]*)\]")
    quoted_chars = "\"'"
    for md_path in DOCS.rglob("*.md"):
        try:
            doc = md_path.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", doc, flags=re.DOTALL)
        if not fm:
            continue
        m = inline_tags_re.search(fm.group(1))
        if not m:
            continue
        for raw in m.group(1).split(","):
            tag = raw.strip().strip(quoted_chars)
            if tag:
                out.add(f"tag:{tag}")
    return out


def is_external(href: str) -> bool:
    parsed = urlparse(href)
    return bool(parsed.scheme) and parsed.scheme.lower() not in {"", "file"}


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    # Root-level markdown
    for md in ROOT.glob("*.md"):
        files.append(md)
    # All markdown under docs/
    for md in DOCS.rglob("*.md"):
        if any(part in SKIP_DIR_NAMES for part in md.relative_to(ROOT).parts):
            continue
        files.append(md)
    return sorted(set(files))


def check_one(src_file: Path, href: str) -> tuple[str | None, str | None]:
    """Return (hard_error, soft_warning); each may be None."""
    if not href or href.startswith("#"):
        anchor = unquote(href.lstrip("#"))
        if not anchor:
            return None, None
        anchors = extract_anchors(src_file)
        if anchor not in anchors:
            return None, f"missing anchor #{anchor} in self"
        return None, None

    if is_external(href):
        return None, None

    target, _, fragment = href.partition("#")
    target = unquote(target)

    target_path = (src_file.parent / target).resolve()

    if not target_path.exists():
        return f"broken link → {href}", None

    if fragment and target_path.suffix.lower() == ".md":
        anchor = unquote(fragment)
        anchors = extract_anchors(target_path)
        if anchor not in anchors:
            return None, f"missing anchor #{anchor} in {target}"

    return None, None


def main() -> int:
    files = iter_markdown_files()
    failures: dict[str, list[str]] = {}
    warnings: dict[str, list[str]] = {}
    total_links = 0

    for md in files:
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            failures[str(md.relative_to(ROOT))] = [f"read error: {exc}"]
            continue
        hrefs = [m.group(1) for m in LINK_RE.finditer(text)]
        hrefs += [m.group(1) for m in IMAGE_RE.finditer(text)]
        for href in hrefs:
            total_links += 1
            err, warn = check_one(md, href)
            if err:
                failures.setdefault(str(md.relative_to(ROOT)), []).append(err)
            if warn:
                warnings.setdefault(str(md.relative_to(ROOT)), []).append(warn)

    if warnings:
        warn_count = sum(len(v) for v in warnings.values())
        print(f"⚠️  {warn_count} anchor warning(s) across {len(warnings)} file(s) (best-effort; not failing CI):\n")
        for path, ws in sorted(warnings.items()):
            print(f"  {path}")
            for w in ws:
                print(f"    - {w}")
        print()

    if failures:
        broken = sum(len(v) for v in failures.values())
        print(f"❌ Link validation FAILED. {broken} broken file reference(s) across {len(failures)} file(s):\n")
        for path, errs in sorted(failures.items()):
            print(f"  {path}")
            for e in errs:
                print(f"    - {e}")
        return 1

    print(f"✅ All {total_links} internal file references resolve cleanly across {len(files)} markdown file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
