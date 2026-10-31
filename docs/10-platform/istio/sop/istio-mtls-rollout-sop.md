---
title: Istio mTLS Rollout SOP
owner: your-org/service-mesh
status: active
type: sop
service: istio
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [istio, mtls, service-mesh, rollout]
related:
  - docs/10-platform/istio/troubleshooting/istio-sidecar-injection-troubleshooting.md
---

# SOP: Istio mTLS Rollout

## 1. Purpose & Scope
**Objective:** Enforce `STRICT` mutual TLS for a namespace's mesh traffic without dropping in-flight connections.

**Applies to:** Namespaces running under the shared Istio mesh with sidecar injection enabled.
**Excludes:** Traffic originating outside the mesh (ingress-gateway to external clients) — covered by the gateway TLS config, not this SOP.

## 2. Prerequisites
- Sidecar injection already enabled and healthy for every workload in the namespace.
- `PeerAuthentication` currently set to `PERMISSIVE` (default) for the namespace.
- Change window approved; no active incidents affecting the namespace.

## 3. Risks & Mitigation

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| A workload without a sidecar starts rejecting plaintext traffic | Medium | Verify 100% sidecar injection coverage before flipping to `STRICT` |
| External health checks bypass the sidecar | Low | Confirm health-check probes are routed through the proxy or exempted via `PeerAuthentication` port-level overrides |

## 4. Procedure

### Entry Criteria
- [ ] All prerequisites verified
- [ ] No blocking incidents active

### Steps *(Estimated time: 20 minutes)*
1. **Prepare:** Confirm every pod in the namespace shows 2/2 containers ready (app + `istio-proxy`).
2. **Execute:** Apply a namespace-scoped `PeerAuthentication` with `mtls.mode: STRICT`.
3. **Monitor:** Watch mesh error rates and `503`/`TLS handshake` errors in the ingress-gateway and sidecar logs for 15 minutes.
4. **Verify:** Confirm traffic continues flowing and no plaintext connections are logged as rejected.

### Exit Criteria
- [ ] `STRICT` mode active and confirmed via `istioctl authn tls-check`
- [ ] No `503`/handshake error increase
- [ ] System stable for 15 minutes

## 5. Success / Failure Criteria
**Success:** Namespace traffic is 100% mTLS-encrypted with no error-rate regression.
**Failure:** Sustained `503`s or handshake failures following the change.

## 6. Rollback Procedure
**Trigger:** Error-rate regression or handshake failures persisting past 5 minutes.
**Steps:**
1. Revert `PeerAuthentication` to `PERMISSIVE`.
2. Confirm error rates return to baseline.
3. Investigate missing-sidecar or misconfigured workloads before retrying.

## 7. Communication
- **Before:** Notify the namespace's on-call channel of the change window.
- **During:** Post status updates in the same channel every 5 minutes.
- **After:** Send a completion notice summarizing error-rate impact (none expected).
- **If Failed:** Escalate to `your-org/service-mesh` on-call.

## 8. Post-Procedure
- [ ] Document any issues encountered
- [ ] Update the namespace's `PeerAuthentication` baseline in source control
- [ ] Schedule a follow-up review in 30 days

**Emergency Contact:** `your-org/service-mesh` on-call rotation.
