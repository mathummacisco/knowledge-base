---
title: Agent Gateway Upstream Timeout Runbook
owner: your-org/agent-platform
status: active
type: runbook
service: agent-gateway
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [agent-gateway, runbook, incident]
related:
  - docs/10-platform/agent-gateway/sop/agent-gateway-rate-limit-rollout-sop.md
---

# Runbook: Agent Gateway Upstream Timeout Spike

## Trigger
Alert fires when the gateway's upstream-timeout rate to any model-worker backend exceeds 5% over a 5-minute window.

## Impact
Agent requests routed through the gateway fail or hang, degrading response times for every client calling that backend.

## Quick Triage
1. **Status:** Check the gateway dashboard for per-backend timeout rate and latency.
2. **Logs:** Search gateway access logs for the affected backend's timeout entries.
3. **Metrics:** Check the backend's own queue depth / concurrency metrics for saturation.

## Resolution Steps
1. Identify whether the timeout is isolated to one backend or affects all backends (points to the gateway itself).
2. If one backend is saturated, scale it up or temporarily shed load by lowering its routed traffic weight.
3. If a recent deploy to the backend correlates with the spike, roll it back.
4. If the gateway's own timeout setting is too aggressive for a slower backend, raise the per-route timeout.

## Verification
- Upstream-timeout rate back under 1% for 10 consecutive minutes.
- Backend latency returns to baseline.

## Escalation
- **Timeout:** 15 minutes without improvement.
- **Contact:** `your-org/agent-platform` on-call.
- **Info to provide:** Affected backend, timeout rate, and any recent deploys to that backend.

## Reference
- Dashboard: agent gateway overview (Grafana)
- Logs: gateway access logs
- Related SOPs: [Rate limit rollout SOP](../sop/agent-gateway-rate-limit-rollout-sop.md)
