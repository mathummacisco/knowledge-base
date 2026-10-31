---
title: Home
owner: mathummacisco
status: active
type: reference
service: n/a
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [home, index]
template: home.html
hide:
  - navigation
  - toc
---

## How it works

<div class="kb-steps" markdown>

<div class="kb-step" markdown>
<div class="kb-step__number">01</div>
<div class="kb-step__body" markdown>
### Find the right doc
Use the search bar at the top, [browse every section](browse.md), or jump to a [tag](tags.md).
</div>
</div>

<div class="kb-step" markdown>
<div class="kb-step__number">02</div>
<div class="kb-step__body" markdown>
### Read with context
Every page shows when it was last updated, who owns it, and what tags it belongs to — so you know what to trust.
</div>
</div>

<div class="kb-step" markdown>
<div class="kb-step__number">03</div>
<div class="kb-step__body" markdown>
### Suggest improvements
Every doc has an **Edit** action at the bottom. Click it and your fix lands as a PR in seconds.
</div>
</div>

</div>

---

<!-- whats-new -->

---

## Featured guides

<div class="grid cards kb-featured" markdown>

-   <span class="kb-card__eyebrow">Learning</span>

    :material-graph-outline:{ .lg .middle } **CNCF Tools**

    ---

    CNCF Graduated projects grouped by category, with a status table and notes per tool.

    [:octicons-arrow-right-24: Open section](10-learning/cncf-tools/index.md)

-   <span class="kb-card__eyebrow">Start Here</span>

    :material-rocket-launch-outline:{ .lg .middle } **How to Use This Knowledge Base**

    ---

    How the structure works and how to add a new topic.

    [:octicons-arrow-right-24: Read it](00-start-here/onboarding.md)

</div>

---

## Browse by topic

<div class="kb-pillars" markdown>

[Start Here](00-start-here/index.md){ .kb-pillar }
[Learning](10-learning/index.md){ .kb-pillar }

</div>

---

## Conventions

- All docs are Markdown with required YAML frontmatter (`title`, `owner`, `status`, `type`, `service`, `last_reviewed`, `review_cadence`, `tags`).
- Filenames use `lowercase-kebab-case.md`.
- Top-level numbering uses gaps of 10 (`00`, `10`, … `90`) so new sections can be inserted without renumbering.
- Doc-type folders: `sop/` · `runbook/` · `troubleshooting/` · `reference/` · `analysis/` · `migration/` · `architecture/` · `capacity/` · `cost/`.

See the [contributing guide](https://github.com/mathummacisco/knowledge-base/blob/main/CONTRIBUTING.md) for the full ruleset and the [frontmatter templates](https://github.com/mathummacisco/knowledge-base/tree/main/docs/_templates) for a copy-pasteable starting point.
