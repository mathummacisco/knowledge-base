"""
MkDocs build hook: inject a "What's new" panel into pages that contain the
HTML marker `<!-- whats-new -->`.

Mechanism
---------
- Runs `git log` once per build (cached on the hook instance) to learn the
  most recent commit per `.md` file under `docs/`.
- Picks the top N by mtime (default 6), skipping index pages, asset READMEs,
  and the homepage itself.
- Renders a grid of cards inline-replacing the marker. Falls back to a
  small, friendly placeholder if git history is unavailable (e.g. shallow
  clone, source tarball builds).

Why a hook and not a plugin?
- A hook is a single self-contained file. No need to publish a package, no
  new pip dependency in requirements-docs.txt, no plugin discovery dance.
- The cost is portability: hooks live in `mkdocs.yml` via the `hooks:` key
  and aren't reusable across repos. That's acceptable for an in-repo
  utility.

Activation
----------
Add to `mkdocs.yml`:

    hooks:
      - scripts/whats_new_hook.py

Then drop `<!-- whats-new -->` anywhere in a page (typically the homepage
hero).
"""
from __future__ import annotations

import datetime as _dt
import logging
import re
import subprocess
from pathlib import Path
from typing import Iterable

log = logging.getLogger("mkdocs.hooks.whats_new")

MARKER_RE = re.compile(r"<!--\s*whats-new\s*-->", re.IGNORECASE)
SKIP_PATTERNS = (
    "/_templates/",
    "/assets/",
    "/index.md",
    "/404.md",
    "/operations.md",
    "/browse.md",
    "/tags.md",
)
HOW_MANY = 6


def _safe_title(md_path: Path) -> str:
    """First H1 if present, else humanise filename."""
    try:
        text = md_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return md_path.stem.replace("-", " ").title()
    # Strip YAML frontmatter to avoid title: in frontmatter being picked up
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
    m = re.search(r"^\s*#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if m:
        # Strip MkDocs attr_list `{ #anchor }` tail if present
        return re.sub(r"\s*\{[^}]*\}\s*$", "", m.group(1)).strip()
    return md_path.stem.replace("-", " ").title()


def _git_recent_files(docs_dir: Path, limit: int) -> list[tuple[Path, _dt.date, str]]:
    """Return up to `limit` (path, last-commit-date, commit-subject) tuples,
    most recent first. Returns [] on failure (shallow clone, missing git, etc.)."""
    try:
        # %H short, %ci ISO date, %s subject — one commit per line
        # `--name-only` then emits the changed files until the next blank line.
        out = subprocess.check_output(
            [
                "git",
                "-C",
                str(docs_dir.parent),
                "log",
                "--pretty=format:__COMMIT__%ad|%s",
                "--date=short",
                "--name-only",
                "--",
                "docs/",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=15,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return []

    seen: set[Path] = set()
    results: list[tuple[Path, _dt.date, str]] = []
    current_date: _dt.date | None = None
    current_subject: str = ""

    for raw_line in out.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("__COMMIT__"):
            header = line.removeprefix("__COMMIT__")
            date_str, _, subject = header.partition("|")
            try:
                current_date = _dt.date.fromisoformat(date_str)
            except ValueError:
                current_date = None
            current_subject = subject
            continue

        # It's a path
        if not line.endswith(".md"):
            continue
        if any(skip in "/" + line for skip in SKIP_PATTERNS):
            continue
        p = Path(line)
        if p in seen:
            continue
        full = docs_dir.parent / p
        if not full.exists():
            # File was renamed/deleted later — skip
            continue
        if current_date is None:
            continue
        seen.add(p)
        results.append((full, current_date, current_subject))
        if len(results) >= limit:
            break

    return results


def _render_panel(entries: Iterable[tuple[Path, _dt.date, str]], docs_dir: Path) -> str:
    cards = []
    for full_path, ddate, _subject in entries:
        rel = full_path.relative_to(docs_dir)
        href = str(rel).removesuffix(".md") + "/"
        if rel.name == "index.md":
            href = str(rel.parent) + "/"
        title = _safe_title(full_path)
        # Pretty section badge: top-level folder, stripping numeric prefix
        top = rel.parts[0] if rel.parts else ""
        badge = re.sub(r"^\d+-", "", top).replace("-", " ").title() if top else ""
        cards.append(
            f'<a class="kb-whatsnew__card" href="{href}">'
            f'<span class="kb-whatsnew__badge">{badge}</span>'
            f'<span class="kb-whatsnew__title">{title}</span>'
            f'<time class="kb-whatsnew__date" datetime="{ddate.isoformat()}">{ddate.strftime("%b %-d, %Y")}</time>'
            f"</a>"
        )

    if not cards:
        return (
            '<div class="kb-whatsnew kb-whatsnew--empty">'
            "Recent updates will appear here once changes land on <code>main</code>."
            "</div>"
        )

    return (
        '<section class="kb-whatsnew" aria-label="Recently updated pages">'
        '<header class="kb-whatsnew__head">'
        '<h2 class="kb-whatsnew__h">What\'s new</h2>'
        '<p class="kb-whatsnew__sub">The six pages that changed most recently on <code>main</code>.</p>'
        "</header>"
        '<div class="kb-whatsnew__grid">' + "".join(cards) + "</div>"
        "</section>"
    )


def on_page_markdown(markdown: str, *, page, config, files, **kwargs) -> str:  # noqa: ARG001
    """MkDocs lifecycle hook — runs once per page during build."""
    if not MARKER_RE.search(markdown):
        return markdown

    docs_dir = Path(config["docs_dir"]).resolve()
    entries = _git_recent_files(docs_dir, HOW_MANY)
    if not entries:
        log.info("whats_new: no git history available, rendering empty panel")
    panel_html = _render_panel(entries, docs_dir)
    return MARKER_RE.sub(panel_html, markdown)
