---
title: Glossary
owner: your-org/platform
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
- **Stale-docs** — a report (and GitHub issue) generated automatically for docs past their cadence window.
- **What's new** — the feed on the home page generated from the last N git commits, filtered to substantive doc changes.
- **Owner alias** — the GitHub team that owns a doc, written as `org/team-slug` in frontmatter. Mentioning the alias on a PR pings the right reviewers.

## Platform component shorthand

These show up in URLs, tags, and frontmatter `service:` fields. They map 1:1 to the [Platform landing](../10-platform/index.md).

- **Istio** — the service mesh. mTLS, traffic routing, and ingress gateway.
- **Agent Gateway** — the routing layer in front of AI agent workloads. Provides identity, request shaping, and observability for downstream LLM workers.
- **DR** / **disaster recovery** — playbooks for region or cluster loss.
- **DORA metrics** — Deployment frequency, Lead time, Change failure rate, MTTR. Used in DevOps reviews.
- **Shift-left** — moving validation (security, perf, contract tests) earlier in the pipeline.
- **Brownbag** — lightweight internal teaching session, usually recorded in `90-knowledge-transfer/`.
