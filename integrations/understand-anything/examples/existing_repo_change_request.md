# Example: Change Request for an Existing Repository

## Context

This is an example change request for the `agilev understand` workflow applied to an existing
NestJS API. The repository has a knowledge graph at `.understand-anything/knowledge-graph.json`.

---

## Change Request: CR-001

**Title:** Add rate limiting to the login endpoint

**Repository:** `my-org/auth-service`

**Requested by:** Security team

**Priority:** High

**Risk level:** L3 (security-visible, customer-facing endpoint)

---

## Description

The login endpoint (`POST /auth/login`) currently has no rate limiting. An attacker can perform
unlimited credential stuffing attacks. We need to limit login attempts to 5 per IP per minute.
Accounts that exceed the limit should receive a `429 Too Many Requests` response.

---

## Acceptance criteria

1. A caller submitting more than 5 login attempts within 60 seconds from the same IP address
   receives a `429 Too Many Requests` response with a `Retry-After` header.
2. A caller submitting 5 or fewer login attempts within 60 seconds is not affected.
3. The rate limit counter resets after 60 seconds.
4. The rate limit applies only to the login endpoint, not to other endpoints.
5. Rate limit events are logged with the originating IP address.
6. Existing integration tests for the login flow continue to pass.

---

## Out of scope

- Rate limiting other endpoints (separate change request required).
- Persistent blocking of IPs (future enhancement).
- User-level rate limiting (IP-based only for this change).

---

## Known risks

- Shared IP addresses (NAT, corporate proxies) may cause false positives.
- Redis dependency may be introduced if in-memory rate limiting is insufficient.
- Existing tests may need updates if they hammer the login endpoint in loops.

---

## Expected Agile V behavior

When this change request is submitted to an Agile V agent with a knowledge graph available:

1. Gate 0 identifies `src/auth/auth.controller.ts` and `src/auth/auth.service.ts` as directly
   affected.
2. The impact map identifies `src/app.module.ts` as indirectly affected (module registration).
3. Regression tests for `test/auth/auth.e2e-spec.ts` are flagged.
4. Requirements are generated linking to the graph nodes.
5. The Build Agent receives the impacted component list and avoids unrelated changes.
6. The evidence bundle includes a traceability chain from CR-001 to the changed files to the
   test results.
