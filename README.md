# Knowledge Base

> Single source of truth for platform, operations, security, and engineering knowledge.

This is a **minimal, working example** of the knowledge base pattern — the
full automation (CI, validators, build hooks, templates, naming
conventions) is wired up exactly as it would be in production, with just
two example services (`istio`, `agent-gateway`) populated under
`10-platform/` to demonstrate the doc-type layout end to end. Extend it by
copying that pattern into your own services and sections.

---

## 🚀 Start Here

- **New to the team?** → [docs/00-start-here/](docs/00-start-here/)
- **Looking for a service runbook?** → [docs/10-platform/](docs/10-platform/)
- **Need to run a procedure?** → [docs/20-operations/](docs/20-operations/)

---

## 📚 Knowledge Map

| #  | Section                                                    | What's Inside                                    |
| -- | ---------------------------------------------------------- | ------------------------------------------------- |
| 00 | [Start Here](docs/00-start-here/)                          | Onboarding, glossary, conventions, FAQ           |
| 10 | [Platform](docs/10-platform/)                              | Service SOPs, runbooks, troubleshooting          |
| 20 | [Operations](docs/20-operations/)                          | Identity, security ops, process procedures       |
| 30 | [Security](docs/30-security/)                              | Findings, policy, incident response              |
| 40 | [DevOps](docs/40-devops/)                                  | CI/CD, build/release, internal tooling           |
| 50 | [Devbox](docs/50-devbox/)                                  | Local development environment setup              |
| 60 | [Best Practices](docs/60-best-practices/)                  | Standards, patterns, guidelines                  |
| 70 | [Tools](docs/70-tools/)                                    | Tool evaluations & how-to guides                 |
| 80 | [Proposals](docs/80-proposals/)                            | ADRs, RFCs, future-state designs                 |
| 90 | [Knowledge Transfer](docs/90-knowledge-transfer/)          | Onboarding decks, handoffs, brownbags            |

---

## 🧭 Conventions

- All docs in Markdown with required frontmatter — see [CONTRIBUTING.md](CONTRIBUTING.md).
- Filenames use `lowercase-kebab-case.md`.
- Every folder has an `index.md`.
- Top-level numbering uses gaps of 10 (`00`, `10`, … `90`) so new sections can be inserted without renumbering.
- **Numbers only at the top level of [docs/](docs/)** — never inside subfolders.

---

## 🛠 Doc-Type Vocabulary

Used as folder names inside service trees (e.g., `docs/10-platform/istio/sop/`):

`sop` · `runbook` · `troubleshooting` · `reference` · `analysis` · `migration` · `architecture` · `capacity` · `cost`

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
  00-start-here/          # Onboarding, glossary, conventions
  10-platform/            # Long-lived service/infra knowledge (istio, agent-gateway)
  20-operations/          # Cross-service operational procedures
  30-security/            # Security posture, findings, policy
  40-devops/              # CI/CD, build/release
  50-devbox/              # Local dev environment
  60-best-practices/      # Standards & patterns
  70-tools/               # Tool evaluations
  80-proposals/           # ADRs, RFCs
  90-knowledge-transfer/  # Onboarding decks, brownbags
  _templates/             # Doc templates (SOP, runbook, etc.)
archive/                  # Deprecated content (kept for history)
scripts/                  # Repo automation (frontmatter/link/image validators, hooks)
.github/workflows/        # CI, GitHub Pages deploy, stale-docs report
```
