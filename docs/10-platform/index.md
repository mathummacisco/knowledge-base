---
title: Platform
owner: your-org/platform
status: active
type: reference
service: n/a
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [platform]
---

# Platform

Long-lived service and infrastructure knowledge — SOPs, runbooks,
troubleshooting, and architecture guides for the components we run.

This is a minimal example instance of the knowledge base with two sample
services wired up end-to-end. Add a new folder here per service, following
the same `sop/ runbook/ troubleshooting/` layout, to extend it.

## Components

<div class="grid cards" markdown>

-   :material-graph-outline:{ .lg .middle } **Istio**

    ---

    Service mesh: mTLS rollout, ingress-gateway incidents, sidecar-injection troubleshooting.

    [:octicons-arrow-right-24: Open](istio/index.md)

-   :material-gateway:{ .lg .middle } **Agent Gateway**

    ---

    AI agent request routing: rate-limit rollout, upstream-timeout incidents, auth-failure troubleshooting.

    [:octicons-arrow-right-24: Open](agent-gateway/index.md)

</div>
