---
title: Home
owner: your-org/platform
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

-   <span class="kb-card__eyebrow">Platform</span>

    :material-graph-outline:{ .lg .middle } **Istio Service Mesh**

    ---

    mTLS rollout, ingress-gateway incident runbook, and sidecar-injection troubleshooting for the service mesh layer.

    [:octicons-arrow-right-24: Open section](10-platform/istio/index.md)

-   <span class="kb-card__eyebrow">Platform</span>

    :material-gateway:{ .lg .middle } **Agent Gateway**

    ---

    Rate-limit rollout SOP, upstream-timeout runbook, and auth-failure troubleshooting for the AI agent request gateway.

    [:octicons-arrow-right-24: Open section](10-platform/agent-gateway/index.md)

-   <span class="kb-card__eyebrow">Start Here</span>

    :material-rocket-launch-outline:{ .lg .middle } **Onboarding Checklist**

    ---

    A week-by-week plan for new contributors — day 1 through month 1.

    [:octicons-arrow-right-24: Read the checklist](00-start-here/onboarding.md)

</div>

---

## Browse by topic

<div class="kb-pillars" markdown>

[Start Here](00-start-here/index.md){ .kb-pillar }
[Platform](10-platform/index.md){ .kb-pillar }
[Operations](20-operations/index.md){ .kb-pillar }
[Security](30-security/index.md){ .kb-pillar }
[DevOps](40-devops/index.md){ .kb-pillar }
[Devbox](50-devbox/index.md){ .kb-pillar }
[Best Practices](60-best-practices/index.md){ .kb-pillar }
[Tools](70-tools/index.md){ .kb-pillar }
[Proposals](80-proposals/index.md){ .kb-pillar }
[Knowledge Transfer](90-knowledge-transfer/index.md){ .kb-pillar }

</div>

---

## Conventions

- All docs are Markdown with required YAML frontmatter (`title`, `owner`, `status`, `type`, `service`, `last_reviewed`, `review_cadence`, `tags`).
- Filenames use `lowercase-kebab-case.md`.
- Top-level numbering uses gaps of 10 (`00`, `10`, … `90`) so new sections can be inserted without renumbering.
- Doc-type folders: `sop/` · `runbook/` · `troubleshooting/` · `reference/` · `analysis/` · `migration/` · `architecture/` · `capacity/` · `cost/`.

See the [contributing guide](https://github.com/your-org/knowledge-base/blob/main/CONTRIBUTING.md) for the full ruleset and the [frontmatter templates](https://github.com/your-org/knowledge-base/tree/main/docs/_templates) for a copy-pasteable starting point.
