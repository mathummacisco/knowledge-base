---
title: Istio Ingress Gateway 5xx Runbook
owner: your-org/service-mesh
status: active
type: runbook
service: istio
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [istio, ingress-gateway, runbook, incident]
related:
  - docs/10-platform/istio/sop/istio-mtls-rollout-sop.md
---

# Runbook: Istio Ingress Gateway 5xx Spike

## Trigger
Alert fires when the ingress-gateway's 5xx response rate exceeds 2% over a 5-minute window.

## Impact
External requests fail or time out; user-facing availability degrades for every service behind the affected gateway.

## Quick Triage
1. **Status:** Check the ingress-gateway dashboard for request volume and error-rate trend.
2. **Logs:** Search `istio-ingressgateway` pod logs for `UC`/`UF`/`UT` response flags.
3. **Metrics:** Check upstream (sidecar) p99 latency and connection-pool exhaustion.

## Resolution Steps
1. Identify the failing upstream via the response-flag breakdown (`UC` = upstream connection failure, `UF` = upstream failure, `UT` = upstream timeout).
2. If a single backend is unhealthy, drain it from the destination rule / scale up replicas.
3. If connection-pool exhaustion (`UC`/`UO`), temporarily raise `DestinationRule` `connectionPool` limits for the affected service.
4. If a recent `PeerAuthentication` or `DestinationRule` change correlates with the spike, roll it back first.

## Verification
- 5xx rate back under 1% for 10 consecutive minutes.
- No new `UC`/`UF`/`UT` flags for the affected upstream.

## Escalation
- **Timeout:** 15 minutes without improvement.
- **Contact:** `your-org/service-mesh` on-call.
- **Info to provide:** Affected upstream service, response-flag breakdown, and any recent mesh config changes.

## Reference
- Dashboard: ingress-gateway overview (Grafana)
- Logs: `istio-ingressgateway` namespace logs
- Related SOPs: [Istio mTLS rollout SOP](../sop/istio-mtls-rollout-sop.md)
