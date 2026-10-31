---
title: Onboarding checklist
owner: your-org/platform
status: active
type: reference
service: n/a
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [onboarding, getting-started]
---

# Onboarding checklist

A concrete week-by-week plan for new platform / SRE / DevOps engineers joining
the team. Treat the checkboxes as the minimum bar — go deeper wherever your
team's roadmap takes you.

## Day 1 — Get oriented

- [ ] Clone the repo locally: `git clone git@github.com:your-org/knowledge-base.git`
- [ ] Read the [repo README](https://github.com/your-org/knowledge-base#readme) — what this knowledge base is, how it's structured, why it exists.
- [ ] Skim the [landing page](../index.md) to see the ten top-level sections.
- [ ] Open the [Tags page](../tags.md) and click into any pillar that maps to your team's work.
- [ ] Install the local preview toolchain and start the dev server:

    ```bash
    make setup    # one-time: creates .venv and installs requirements-docs.txt
    make serve    # live preview at http://127.0.0.1:8000
    ```

    Run `make help` any time to see all supported targets.

## Week 1 — Learn the shape

- [ ] Read the [Contributing guide](https://github.com/your-org/knowledge-base/blob/main/CONTRIBUTING.md) end-to-end. It covers frontmatter, file naming, doc-type taxonomy, review cadence, and the PR workflow.
- [ ] Read the [glossary](glossary.md) so internal jargon stops being a barrier.
- [ ] Read three docs from the [Platform](../10-platform/index.md) section:
    - One **SOP** to learn how planned changes are described.
    - One **Runbook** to learn the incident format.
    - One **Troubleshooting** guide to learn the symptom → cause → fix format.
- [ ] Find your team's service folder (e.g. `10-platform/istio/` or `10-platform/agent-gateway/`) and the docs marked with your team's `owner` in the metadata strip.

## Week 2 — Make your first edit

- [ ] Fix a small issue you spotted in week 1: a typo, an outdated link, a tag that should have been there. Use [the contributing guide](https://github.com/your-org/knowledge-base/blob/main/CONTRIBUTING.md) to format the PR.
- [ ] Run the CI checks locally before opening the PR:

    ```bash
    make check    # runs all validators + strict build (matches CI exactly)
    ```

    To ship directly without leaving the terminal:

    ```bash
    make ship MSG="docs(istio): fix outdated link in mtls-rollout-sop"
    ```

- [ ] Request review from someone on your team's owner alias.

## Month 1 — Own your domain

- [ ] Write at least one new doc — most teams need a fresh SOP or troubleshooting note far more than they need a polished analysis.
- [ ] Audit the docs owned by your team for staleness. Anything past its `review_cadence` window? Fix it or hand it off.
- [ ] Skim the "What's new" feed on the [home page](../index.md) weekly to stay in the loop on adjacent teams' work.

## Ongoing — Stay current

- [ ] Watch the stale-docs report — the weekly job opens issues for docs past their review window (see the `Stale Docs Report` workflow).
- [ ] When you join an incident, ask "is there a runbook for this?" If yes, follow it and improve it. If no, write one before the on-call rotation rolls.
- [ ] Anytime you find yourself answering a question for the second time, file the answer as a doc.

## Want feedback on a doc you're writing?

Drop a draft PR, tag your owner alias, and link the [Contributing guide](https://github.com/your-org/knowledge-base/blob/main/CONTRIBUTING.md) checklist. Most reviewers will respond within a day.
