---
title: Istio Sidecar Injection Troubleshooting
owner: your-org/service-mesh
status: active
type: troubleshooting
service: istio
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [istio, sidecar-injection, troubleshooting]
related:
  - docs/10-platform/istio/sop/istio-mtls-rollout-sop.md
---

# Troubleshooting: Istio Sidecar Injection Failures

## Quick Triage
1. **Status:** `kubectl get pods -n <namespace>` — pods show `1/1` instead of `2/2` ready.
2. **Logs:** Check the namespace's `istio-injection` label and the webhook's logs.
3. **Metrics:** None specific — this is a configuration issue, not a runtime one.

## Symptoms
- **Alert:** None (usually caught in CI or at rollout time).
- **Impact:** Workload traffic bypasses the mesh — no mTLS, no mesh telemetry, no traffic policy enforcement.
- **Signs:** New pods come up with only the application container; no `istio-proxy` container present.

## Likely Causes

### Cause 1: Namespace missing the injection label
- **Check:** `kubectl get namespace <namespace> -o jsonpath='{.metadata.labels}'`
- **Tools:** `kubectl`

### Cause 2: Pod-level annotation opts out of injection
- **Check:** Look for `sidecar.istio.io/inject: "false"` in the pod template.
- **Tools:** `kubectl get pod <pod> -o yaml`

### Cause 3: Mutating webhook unavailable at pod creation time
- **Check:** Confirm `istiod`'s injection webhook pods are healthy and the `MutatingWebhookConfiguration` is registered.
- **Tools:** `kubectl get mutatingwebhookconfigurations`, `kubectl get pods -n istio-system`

## Investigation Steps
1. **Status:** Confirm the namespace label `istio-injection=enabled` (or the revision-tag equivalent) is present.
2. **Logs:** Check `istiod` logs for webhook admission errors around the pod's creation timestamp.
3. **Metrics:** N/A.
4. **Recent Changes:** Check whether the namespace label or a Helm values file was recently changed.

## Resolution
- **If Cause 1:** Label the namespace and roll the deployment (`kubectl rollout restart`).
- **If Cause 2:** Remove the opt-out annotation and roll the deployment.
- **If Cause 3:** Restart `istiod`, confirm the webhook re-registers, then roll the affected deployment.

## Verification
- Pods report `2/2` ready with an `istio-proxy` container present.
- `istioctl proxy-status` shows the workload as `SYNCED`.

## Escalation
- **Timeout:** 20 minutes without resolution.
- **Contact:** `your-org/service-mesh` on-call.
- **Info to provide:** Namespace, affected deployment, and `istiod` logs around the pod creation time.

## Reference Links
- Monitoring: mesh control-plane dashboard
- Logs: `istiod` namespace logs
- Related runbooks: [Ingress gateway 5xx runbook](../runbook/istio-ingress-gateway-5xx-runbook.md)
