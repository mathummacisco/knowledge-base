# Knowledge Base

> Personal learning log — notes on tools and topics I'm learning or about to learn.

Built on the mkdocs-material knowledge-base pattern: full automation (CI,
validators, build hooks, templates, naming conventions) wired up the same
way a production team KB would be, scaled down to a single-owner learning
log. Starting topic: CNCF Graduated projects.

---

## 🚀 Start Here

- **New here?** → [docs/00-start-here/](docs/00-start-here/)
- **Looking for learning notes?** → [docs/10-learning/](docs/10-learning/)

---

## 📚 Knowledge Map

| #  | Section                                  | What's Inside                                |
| -- | ------------------------------------------ | ----------------------------------------------- |
| 00 | [Start Here](docs/00-start-here/)        | How this KB works, glossary, FAQ             |
| 10 | [Learning](docs/10-learning/)            | Notes by topic — starting with CNCF tools    |

---

## 🧭 Conventions

- All docs in Markdown with required frontmatter — see [CONTRIBUTING.md](CONTRIBUTING.md).
- Filenames use `lowercase-kebab-case.md`.
- Every folder has an `index.md`.
- Top-level numbering uses gaps of 10 (`00`, `10`, `20`, …) so new sections can be inserted without renumbering.
- **Numbers only at the top level of [docs/](docs/)** — never inside subfolders.

---

## 🛠 Doc-Type Vocabulary

`sop` · `runbook` · `troubleshooting` · `reference` · `analysis` · `migration` · `architecture` · `capacity` · `cost`

Most learning notes use `reference`.

---

## 🏁 Getting Started

```bash
make setup    # one-time: create .venv and install requirements-docs.txt
make serve    # live preview at http://127.0.0.1:8000
make check    # run all validators + strict build (same gate as CI)
make help     # list all targets
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for naming rules, frontmatter spec, and PR checklist.
Ownership is defined in [CODEOWNERS](CODEOWNERS).

---

## 🗂 Repository Layout

```
docs/
  00-start-here/          # How this KB works, glossary, FAQ
  10-learning/            # Learning notes by topic (cncf-tools, ...)
  _templates/             # Doc templates (SOP, runbook, etc.)
archive/                  # Deprecated content (kept for history)
scripts/                  # Repo automation (frontmatter/link/image validators, hooks)
.github/workflows/        # CI, GitHub Pages deploy, stale-docs report
```
