---
title: Agent Gateway Authentication Failures Troubleshooting
owner: your-org/agent-platform
status: active
type: troubleshooting
service: agent-gateway
last_reviewed: 2026-10-31
review_cadence: quarterly
tags: [agent-gateway, authentication, troubleshooting]
related:
  - docs/10-platform/agent-gateway/runbook/agent-gateway-upstream-timeout-runbook.md
---

# Troubleshooting: Agent Gateway Authentication Failures

## Quick Triage
1. **Status:** Check the gateway dashboard for the client's 401/403 rate.
2. **Logs:** Search gateway access logs for the client's API key and the specific auth error reason.
3. **Metrics:** Check whether the failure is isolated to one client or affects all clients (points to the gateway's identity provider).

## Symptoms
- **Alert:** Client-reported 401/403 responses, or a dashboard spike in auth-failure rate.
- **Impact:** Affected client's agent requests are rejected outright.
- **Signs:** Gateway logs show `invalid_token`, `expired_token`, or `key_not_found` for the client.

## Likely Causes

### Cause 1: Expired or rotated API key
- **Check:** Confirm the client is using the currently active key, not a rotated-out one.
- **Tools:** Gateway admin console, access logs

### Cause 2: Clock skew causing token expiry mismatches
- **Check:** Compare the client's token `exp` claim against gateway server time.
- **Tools:** `jwt` decode of a sample token, gateway logs

### Cause 3: Identity provider outage or latency
- **Check:** Confirm the gateway's upstream identity provider is healthy and responding within SLA.
- **Tools:** Identity provider status dashboard

## Investigation Steps
1. **Status:** Confirm whether the issue is client-specific or gateway-wide.
2. **Logs:** Pull the exact auth-failure reason from gateway access logs for the affected client.
3. **Metrics:** Check identity-provider latency/error-rate metrics.
4. **Recent Changes:** Check for recent key rotations or identity-provider config changes.

## Resolution
- **If Cause 1:** Issue the client a new key and confirm the old one is properly deprecated, not deleted mid-use.
- **If Cause 2:** Correct the clock skew or widen the token validation window temporarily.
- **If Cause 3:** Escalate to the identity provider's on-call; failover if a secondary is available.

## Verification
- Client's 401/403 rate returns to baseline.
- A sample request from the client succeeds end-to-end.

## Escalation
- **Timeout:** 20 minutes without resolution.
- **Contact:** `your-org/agent-platform` on-call.
- **Info to provide:** Affected client, exact auth-failure reason, and timestamps.

## Reference Links
- Monitoring: agent gateway auth dashboard
- Logs: gateway access logs
- Related runbooks: [Upstream timeout runbook](../runbook/agent-gateway-upstream-timeout-runbook.md)
