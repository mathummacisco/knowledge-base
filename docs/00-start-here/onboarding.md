---
title: How to Use This Knowledge Base
owner: mathummacisco
status: active
type: reference
service: n/a
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [onboarding, getting-started]
---

# How to Use This Knowledge Base

A personal learning log — notes on tools and topics I'm learning or about
to learn, organized so they're easy to search and revisit later.

## Day-to-day workflow

- [ ] Install the local preview toolchain and start the dev server:

    ```bash
    make setup    # one-time: creates .venv and installs requirements-docs.txt
    make serve    # live preview at http://127.0.0.1:8000
    ```

    Run `make help` any time to see all supported targets.

- [ ] Before committing, run the same checks CI runs:

    ```bash
    make check    # runs all validators + strict build
    ```

- [ ] Ship a change directly from the terminal:

    ```bash
    make ship MSG="learning(cncf): add notes on Helm"
    ```

## Adding a new topic

1.  Pick (or create) a folder under [`10-learning/`](../10-learning/index.md)
    for the subject area, e.g. `10-learning/cncf-tools/`.
2.  Add a file with a kebab-case filename — `service-mesh.md`, not
    `Service Mesh.md`.
3.  Add YAML frontmatter. Templates live in
    [`docs/_templates/`](https://github.com/mathummacisco/knowledge-base/tree/main/docs/_templates).
    `reference` is the right `type` for most learning notes.
4.  Set `status: draft` while you're still learning it, and flip to
    `active` once you consider the notes solid.

## Adding a new section

Add a new top-level folder under `docs/` (next free ten, e.g.
`20-<topic>/`) if a subject doesn't fit under `10-learning/`. Give it an
`index.md` and link it from [the home page](../index.md) and
[Browse](../browse.md).

## Want to find something later?

- The [home page](../index.md) links to every top-level section.
- The [Tags page](../tags.md) groups docs by topic.
- Site search (top right) matches titles, headings, and body content.
