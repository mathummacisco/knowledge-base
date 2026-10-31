"""
MkDocs build hook: auto-inject a "Related reading" footer on long docs.

For every content page that:

  - is not an index/landing/tag/browse/home page, and
  - has at least 500 words of body content, and
  - has not opted out via \`hide_related: true\` in its frontmatter,

we append a small footer block listing up to 5 other docs in the corpus
that share the most YAML tags with the current page. Common tags like
"aws", "sop", and "reference" are deweighted because they're too broad
to indicate true relatedness — meaningful overlap means specific tags
like \`eks\`, \`disaster-recovery\`, or \`agentic-gateway\`.

The hook runs only on \`on_files\` once (to build the corpus index) and
then \`on_page_markdown\` per page. Idempotent — won't double-inject if
the marker is already present.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import yaml

MARKER = "<!-- related-reading -->"

# These tags appear on so many docs that they don't signal real relatedness.
DEWEIGHTED = frozenset(
    {
        "aws", "sop", "reference", "index", "home", "meta", "landing",
        "tags", "404", "operations", "operations-hub",
    }
)

# Pages that should never get an auto-related footer regardless of length.
SKIP_PAGES = frozenset(
    {
        "index.md",
        "browse.md",
        "operations.md",
        "tags.md",
        "404.md",
    }
)

# Min words of body content before a doc is "long enough" for the footer.
WORD_FLOOR = 500
# Min shared score to be considered related.
SCORE_FLOOR = 2

_corpus: dict[str, dict] = {}


def _word_count(text: str) -> int:
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL, count=1)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]+`", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"[#*_>`~|=-]+", " ", body)
    return len(re.findall(r"\b[\w\u00C0-\uFFFF]+\b", body))


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not m:
        return {}
    try:
        out = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return out if isinstance(out, dict) else {}


def on_files(files, *, config, **kwargs):  # noqa: ARG001
    """Index every markdown file's tags + title for fast lookup later."""
    _corpus.clear()
    docs_dir = Path(config["docs_dir"])
    for f in files:
        if not f.is_documentation_page() or not f.src_uri.endswith(".md"):
            continue
        path = docs_dir / f.src_path
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = _frontmatter(text)
        if not fm:
            continue
        tags = set(fm.get("tags") or [])
        if not tags:
            continue
        # Get the URL the doc will be served at
        _corpus[f.src_uri] = {
            "title": fm.get("title") or _derive_title(text) or f.src_uri,
            "tags": tags,
            "url": f.url,
            "type": (fm.get("type") or "reference").strip().lower(),
            "words": _word_count(text),
        }
    return files


def _derive_title(text: str) -> Optional[str]:
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
    m = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


_TYPE_ICONS = {
    "sop": "material-clipboard-check-outline",
    "runbook": "material-fire-alert",
    "troubleshooting": "material-fire-alert",
    "reference": "material-book-open-page-variant-outline",
    "analysis": "material-chart-line",
    "migration": "material-truck-fast-outline",
    "architecture": "material-file-tree-outline",
}


def _score(my_tags: set, their_tags: set) -> int:
    shared = my_tags & their_tags
    weight = 0
    for t in shared:
        weight += 1 if t in DEWEIGHTED else 3
    return weight


def on_page_markdown(markdown: str, *, page, config, files, **kwargs):  # noqa: ARG001
    if page.file.src_uri in SKIP_PAGES:
        return markdown
    if Path(page.file.src_uri).name == "index.md":
        return markdown
    if MARKER in markdown:
        return markdown
    if page.meta.get("hide_related") is True:
        return markdown

    me = _corpus.get(page.file.src_uri)
    if not me or not me["tags"]:
        return markdown
    if me["words"] < WORD_FLOOR:
        return markdown

    ranked: list[tuple[int, str, dict]] = []
    for uri, entry in _corpus.items():
        if uri == page.file.src_uri:
            continue
        score = _score(me["tags"], entry["tags"])
        if score < SCORE_FLOOR:
            continue
        ranked.append((score, uri, entry))
    ranked.sort(key=lambda x: (-x[0], x[2]["title"]))
    top = ranked[:5]
    if not top:
        return markdown

    rel_root = "/".join([".."] * page.file.src_uri.count("/")) or "."
    lines = ["", "", MARKER, "", "## Related reading", "", "<div class=\"grid cards\" markdown>", ""]
    for score, uri, entry in top:
        icon = _TYPE_ICONS.get(entry["type"], "material-file-document-outline")
        rel_path = f"{rel_root}/{uri}"
        lines.append(
            f"-   :{icon}:{{ .lg .middle }} __[{entry['title']}]({rel_path})__\n"
            f"\n    ---\n\n"
            f"    Shared tags: " + ", ".join(f"`{t}`" for t in sorted(me['tags'] & entry['tags']))
        )
        lines.append("")
    lines.append("</div>")
    return markdown.rstrip() + "\n".join(lines) + "\n"
