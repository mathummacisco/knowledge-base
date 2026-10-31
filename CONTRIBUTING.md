# Contributing to the Knowledge Base

## 1. Where Does My Doc Go?

| Intent                                         | Section                                           |
| ---------------------------------------------- | ------------------------------------------------- |
| Onboarding / glossary / how to use this repo   | [docs/00-start-here/](docs/00-start-here/)        |
| Notes on a tool or topic you're learning       | [docs/10-learning/](docs/10-learning/)            |

---

## 2. Naming Rules

- **Folders:** `lowercase-kebab-case`
- **Files:** `lowercase-kebab-case.md`
- **Top-level numbering only:** `00-`, `10-`, `20-`, … **Never** number subfolders.
- **Use locked doc-type names:** `sop`, `runbook`, `troubleshooting`, `reference`, `analysis`, `migration`, `architecture`, `capacity`, `cost`.

---

## 3. Required Frontmatter

Every `.md` document must start with:

```yaml
---
title: Service Mesh
owner: mathummacisco
status: draft            # draft | active | deprecated
type: reference           # sop | runbook | troubleshooting | reference | analysis | migration | architecture
service: n/a              # topic-specific identifier, or "n/a"
last_reviewed: 2026-06-01
review_cadence: quarterly # monthly | quarterly | biannual | annual
tags: [cncf, cncf-tools, service-mesh]
---
```

CI will reject PRs missing required fields.

---

## 4. Folder Layout Inside a Topic

```
docs/10-learning/<topic>/
  index.md
  <notes>.md
  assets/
    img/
```

- Binaries (images, CSVs, shell scripts) live in `assets/<type>/`, never inline with prose.
- Every folder has an `index.md`.

---

## 5. Templates

Copy from [docs/_templates/](docs/_templates/):

- `template-sop.md`
- `template-runbook.md`
- `template-troubleshooting.md`
- `template-reference.md`
- `template-architecture.md`

---

## 6. PR Checklist

- [ ] File placed in the correct numbered section.
- [ ] Filename is `lowercase-kebab-case.md`.
- [ ] Frontmatter present and valid.
- [ ] `owner` set (not a placeholder).
- [ ] `last_reviewed` is today's date.
- [ ] Links use workspace-relative paths.
- [ ] Binaries placed in `assets/` (not inline).
- [ ] Folder `index.md` updated if you added a new doc.

---

## 7. Deprecating a Doc

1. Set `status: deprecated` in frontmatter.
2. Add a top note pointing to the replacement.
3. Move the file to `archive/` mirroring its original path.
4. Update any inbound links.
