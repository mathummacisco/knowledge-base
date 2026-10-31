---
title: Glossary
owner: mathummacisco
status: active
type: reference
service: n/a
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [onboarding, glossary, reference]
---

# Glossary

Terms used across the knowledge base, in the order new joiners typically meet
them. Edit freely: if a term is missing or ambiguous, add it and open the PR.

## Doc types

The `type:` field in every doc's frontmatter is one of:

| Type | When to use it | Typical lifespan |
|---|---|---|
| **`sop`** | A planned, repeatable procedure (e.g. a rolling mTLS enforcement change). Step-by-step, expected to run cleanly. | Months to years. |
| **`runbook`** | An emergency procedure executed under stress. Optimised for speed and clarity, not completeness. | Reviewed quarterly. |
| **`troubleshooting`** | "When you see _symptom X_, the cause is usually _Y_." Reactive lookup, not a script. | Weeks to months. |
| **`reference`** | Durable explanatory content. Architecture notes, design context, configuration tables. | Long. |
| **`analysis`** | Point-in-time investigation. Data, charts, recommendations from a specific moment. | Short — usually stale after 1-2 quarters. |
| **`migration`** | A one-shot change-of-state procedure. Lives until the migration is done. | Project lifetime. |
| **`architecture`** | High-level design decisions (ADRs, RFCs). | Indefinite. |

## Process terms

- **Frontmatter** — the YAML block at the top of every `.md` file. Required fields are validated by `scripts/check-frontmatter.py` on every PR. Owner, review cadence, type, and tags drive every UI affordance in this site.
- **Review cadence** — how often a doc needs an owner to re-verify it. Valid values: `monthly`, `quarterly`, `biannual`, `annual`. The stale-docs report opens issues when the window passes.
- **Stale-docs** — a report generated automatically for docs past their cadence window.
- **What's new** — the feed on the home page generated from the last N git commits, filtered to substantive doc changes.
- **Owner** — the GitHub username/team that owns a doc, written in frontmatter.

## Topic shorthand

These show up in URLs, tags, and frontmatter `service:` fields. They map to the [Learning landing](../10-learning/index.md).

- **CNCF** — Cloud Native Computing Foundation, the organization that stewards projects like Kubernetes, Istio, and Envoy.
- **Graduated project** — a CNCF project that has met the foundation's maturity bar (wide adoption, diverse maintainership, etc.), as opposed to Sandbox or Incubating.
- **Service mesh** — a dedicated infrastructure layer (e.g. Istio, Linkerd) that handles service-to-service traffic: mTLS, routing, observability.
- **GitOps** — declarative infrastructure/app state stored in git, reconciled continuously by a controller (e.g. Argo CD, Flux).
