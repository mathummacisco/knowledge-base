"""
MkDocs build hook: render a metadata strip below the page H1.

Reads `type`, `owner`, and `last_reviewed` from each page's YAML frontmatter
and injects a small HTML block right after the first H1. The result is that
every reader sees, at a glance:

  - what kind of doc this is (SOP / runbook / reference / analysis / …)
  - which team owns it
  - when it was last reviewed

This replaces a YAML-only signal with a UI signal without forcing authors
to write the strip by hand.

Pages that are intentionally chrome-only (the home hero, browse landing,
operations group landing, tags index, 404, the Best Practices landing) skip
the strip to keep their hand-tuned layouts intact.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Optional

# Pages where the strip would compete with bespoke layout. Paths are relative
# to docs_dir, posix style, including the .md suffix.
SKIP_PAGES: frozenset[str] = frozenset(
    {
        "index.md",
        "browse.md",
        "tags.md",
        "404.md",
        "10-learning/index.md",
        "00-start-here/index.md",
    }
)

# Frontmatter `type` enum (mirrors scripts/check-frontmatter.py). Each value
# carries a human label and an accent class wired up in extra.css.
TYPE_LABELS: dict[str, tuple[str, str]] = {
    "sop": ("SOP", "kb-chip--sop"),
    "runbook": ("Runbook", "kb-chip--runbook"),
    "troubleshooting": ("Troubleshooting", "kb-chip--troubleshooting"),
    "reference": ("Reference", "kb-chip--reference"),
    "analysis": ("Analysis", "kb-chip--analysis"),
    "migration": ("Migration", "kb-chip--migration"),
    "architecture": ("Architecture", "kb-chip--architecture"),
}

H1_RE = re.compile(r"^(#\s+.+?)$", re.MULTILINE)
MARKER = "<!-- kb-meta -->"


def _format_owner(owner: str) -> str:
    """`your-org/platform` → `platform`."""
    if "/" in owner:
        owner = owner.split("/", 1)[1]
    return owner.replace("-", " ")


def _format_date(raw: object) -> Optional[str]:
    """Accept date-typed values or ISO strings; emit `MMM D, YYYY`."""
    if isinstance(raw, date):
        return raw.strftime("%b %-d, %Y")
    if isinstance(raw, str):
        try:
            return date.fromisoformat(raw).strftime("%b %-d, %Y")
        except ValueError:
            return raw
    return None


def _word_count(markdown: str) -> int:
    """Approximate word count for reading-time estimation.

    Strips frontmatter, fenced code blocks, inline code, HTML, and markdown
    syntax markers (#, *, _, etc.) so we count user-facing words only.
    """
    text = markdown
    if text.startswith("---"):
        m = re.match(r"^---\s*\n.*?\n---\s*\n", text, flags=re.DOTALL)
        if m:
            text = text[m.end():]
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#*_>`~|=-]+", " ", text)
    return len(re.findall(r"\b[\w\u00C0-\uFFFF]+\b", text))


def _reading_time(markdown: str) -> Optional[int]:
    """Return rounded minutes at ~220 WPM, or None for short pages."""
    words = _word_count(markdown)
    if words < 240:  # <~1 min → no chip
        return None
    return max(1, round(words / 220))


def _render(meta: dict, markdown: str = "") -> str:
    typ = (meta.get("type") or "").strip().lower()
    label, css = TYPE_LABELS.get(typ, (typ.title() or "Doc", "kb-chip--reference"))
    owner = _format_owner((meta.get("owner") or "").strip())
    reviewed = _format_date(meta.get("last_reviewed"))
    minutes = _reading_time(markdown) if markdown else None

    parts = [f'<span class="kb-chip {css}">{label}</span>']
    if owner:
        parts.append(
            f'<span class="kb-chip__divider" aria-hidden="true">·</span>'
            f'<span class="kb-chip__meta">Owned by <strong>{owner}</strong></span>'
        )
    if reviewed:
        parts.append(
            f'<span class="kb-chip__divider" aria-hidden="true">·</span>'
            f'<span class="kb-chip__meta">Reviewed <time datetime="{meta.get("last_reviewed")}">{reviewed}</time></span>'
        )
    if minutes:
        parts.append(
            f'<span class="kb-chip__divider" aria-hidden="true">·</span>'
            f'<span class="kb-chip__meta">{minutes} min read</span>'
        )
    return f'<div class="kb-meta">{"".join(parts)}</div>'


def _extract_yaml_frontmatter(text: str) -> dict:
    """Fallback frontmatter parser for cases where page.meta is empty.

    Material loads frontmatter via mkdocs core, which runs after `on_page_markdown`
    in some versions. We re-parse the YAML directly so the meta strip is correct
    regardless of plugin ordering.
    """
    if not text.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not m:
        return {}
    body = m.group(1)
    out: dict = {}
    for line in body.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip().strip("\"'")
    return out


def on_page_markdown(markdown: str, *, page, config, files, **kwargs):  # noqa: ARG001
    if page.file.src_uri in SKIP_PAGES:
        return markdown
    # Author may opt out per-page via `hide_meta: true` in frontmatter.
    if page.meta.get("hide_meta") is True:
        return markdown
    # If the page has already been processed (idempotency / preview reloads),
    # don't double-inject.
    if MARKER in markdown:
        return markdown

    m = H1_RE.search(markdown)
    if not m:
        return markdown

    # Prefer page.meta (already type-coerced); fall back to a manual YAML scan
    # because hook ordering can leave page.meta empty on first pass.
    meta = dict(page.meta) if page.meta else {}
    if not meta.get("type") or not meta.get("owner"):
        fallback = _extract_yaml_frontmatter(markdown)
        for k in ("type", "owner", "last_reviewed"):
            if not meta.get(k) and fallback.get(k):
                meta[k] = fallback[k]

    insertion = _render(meta, markdown=markdown)
    head = markdown[: m.end()]
    tail = markdown[m.end():]
    return f"{head}\n\n{MARKER}\n{insertion}\n{tail}"
