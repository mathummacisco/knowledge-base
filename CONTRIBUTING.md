# Contributing to the Knowledge Base

## 1. Where Does My Doc Go?

| Intent                                         | Section                                           |
| ---------------------------------------------- | ------------------------------------------------- |
| Onboarding / glossary / how to use this repo   | [docs/00-start-here/](docs/00-start-here/)        |
| AWS service knowledge (EKS, MSK, RDS, …)       | [docs/10-platform/](docs/10-platform/)            |
| Cross-service operational procedure            | [docs/20-operations/](docs/20-operations/)        |
| Security finding, policy, incident response    | [docs/30-security/](docs/30-security/)            |
| CI/CD, build/release, internal tooling         | [docs/40-devops/](docs/40-devops/)                |
| Local development environment setup            | [docs/50-devbox/](docs/50-devbox/)                |
| Standards, patterns, guidelines                | [docs/60-best-practices/](docs/60-best-practices/) |
| Tool evaluation or how-to                      | [docs/70-tools/](docs/70-tools/)                  |
| ADR, RFC, future-state proposal                | [docs/80-proposals/](docs/80-proposals/)          |
| Onboarding deck, handoff, brownbag             | [docs/90-knowledge-transfer/](docs/90-knowledge-transfer/) |

---

## 2. Naming Rules

- **Folders:** `lowercase-kebab-case`
- **Files:** `lowercase-kebab-case.md`
- **Top-level numbering only:** `00-`, `10-`, … `90-`. **Never** number subfolders.
- **Use canonical service names:** `eks`, `msk`, `rds`, `documentdb`, `elasticache`, `opensearch`.
- **Use locked doc-type names:** `sop`, `runbook`, `troubleshooting`, `reference`, `analysis`, `migration`, `architecture`, `capacity`, `cost`.

---

## 3. Required Frontmatter

Every `.md` document must start with:

```yaml
---
title: EKS Disaster Recovery SOP
owner: platform-eks@company.com
status: active            # draft | active | deprecated
type: sop                 # sop | runbook | troubleshooting | reference | analysis | migration | architecture
service: eks              # canonical service name, or "n/a"
last_reviewed: 2026-06-01
review_cadence: quarterly # monthly | quarterly | biannual | annual
tags: [eks, dr, kubernetes, aws]
related:
  - docs/10-platform/aws/disaster-recovery/sop/environment-recovery-from-backup.md
---
```

CI will reject PRs missing required fields.

---

## 4. Folder Layout Inside a Service

```
docs/10-platform/aws/<service>/
  index.md
  sop/
  runbook/
  troubleshooting/
  reference/
  capacity/
  migration/
  architecture/
  assets/
    img/
    scripts/
    data/
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
- [ ] `owner` set to a team or DL (not a person).
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
