---
title: Agent Gateway Rate Limit Rollout SOP
owner: your-org/agent-platform
status: active
type: sop
service: agent-gateway
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [agent-gateway, rate-limiting, rollout]
related:
  - docs/10-platform/agent-gateway/troubleshooting/agent-gateway-auth-failures-troubleshooting.md
---

# SOP: Agent Gateway Rate Limit Rollout

## 1. Purpose & Scope
**Objective:** Apply a new per-client request rate limit at the agent gateway without disrupting existing well-behaved clients.

**Applies to:** The agent gateway's per-API-key rate-limit policy.
**Excludes:** Global gateway-wide throttling (handled by a separate capacity SOP).

## 2. Prerequisites
- Target client's current traffic baseline (p50/p95 requests-per-minute) pulled from the gateway dashboard.
- New limit set at least 20% above the client's p95 baseline.
- Change window approved.

## 3. Risks & Mitigation

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Limit set too low, legitimate traffic throttled | Medium | Base the new limit on measured p95, not a guess |
| Policy change doesn't propagate to all gateway replicas | Low | Confirm config sync across replicas before closing the change |

## 4. Procedure

### Entry Criteria
- [ ] All prerequisites verified
- [ ] No blocking incidents active

### Steps *(Estimated time: 15 minutes)*
1. **Prepare:** Confirm the client's current p95 request rate from the gateway dashboard.
2. **Execute:** Update the client's rate-limit policy in the gateway config and apply.
3. **Monitor:** Watch the client's `429` rate for 15 minutes post-change.
4. **Verify:** Confirm no unexpected `429`s for traffic under the new limit.

### Exit Criteria
- [ ] New limit active on all gateway replicas
- [ ] No `429` spike for in-policy traffic
- [ ] System stable for 15 minutes

## 5. Success / Failure Criteria
**Success:** Client traffic flows normally under the new limit with no legitimate requests throttled.
**Failure:** Legitimate traffic receiving `429`s after the change.

## 6. Rollback Procedure
**Trigger:** Unexpected `429` spike for in-policy traffic.
**Steps:**
1. Revert the rate-limit policy to its previous value.
2. Confirm `429` rate returns to baseline.
3. Re-measure the client's traffic baseline before retrying with a corrected limit.

## 7. Communication
- **Before:** Notify the client-facing team of the change window.
- **During:** Post status updates every 5 minutes.
- **After:** Send a completion notice confirming no throttling impact.
- **If Failed:** Escalate to `your-org/agent-platform` on-call.

## 8. Post-Procedure
- [ ] Document any issues encountered
- [ ] Update the client's documented rate limit in source control
- [ ] Schedule a follow-up review in 30 days

**Emergency Contact:** `your-org/agent-platform` on-call rotation.
