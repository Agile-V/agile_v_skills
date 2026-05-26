# Example: Regression Test Selection Output

## Input

- Impact map: from CR-001 (rate limiting change)
- Affected components: `auth.controller.ts`, `auth.module.ts`, new guard
- Test inventory: `test/` and `src/**/*.spec.ts`

---

## Required Regression Tests

| Test | Linked Component | Linked Requirement | Risk Covered | Priority |
|---|---|---|---|---|
| `test/auth/auth.e2e-spec.ts::should login with valid credentials` | `src/auth/auth.controller.ts` | REQ-001 | Core login path not broken | High |
| `test/auth/auth.e2e-spec.ts::should reject invalid credentials` | `src/auth/auth.controller.ts` | REQ-001 | Error handling not broken | High |
| `src/auth/auth.controller.spec.ts::login unit tests` | `src/auth/auth.controller.ts` | REQ-001, REQ-002 | Controller logic not broken | High |
| `test/auth/auth.e2e-spec.ts::should return 429 after 5 attempts` | `src/auth/guards/rate-limit.guard.ts` | REQ-003 | Rate limiting enforced | High |
| `test/auth/auth.e2e-spec.ts::rate limit resets after 60s` | `src/auth/guards/rate-limit.guard.ts` | REQ-004 | Reset behavior correct | Medium |
| `test/app/app.e2e-spec.ts` | `src/app.module.ts` | — | App module not broken | Medium |

### New Tests Required

| Required behavior | Reason | Suggested test |
|---|---|---|
| 5th attempt succeeds, 6th returns 429 | Core rate limit boundary | `auth.e2e-spec.ts::boundary test` |
| 429 response includes Retry-After header | Acceptance criterion | `auth.e2e-spec.ts::headers test` |
| Rate limit events are logged | Observability requirement | `auth.controller.spec.ts::log test` |
| Other endpoints are not rate limited | Scope boundary | `app.e2e-spec.ts::other endpoints` |

---

## Regression Coverage Rationale

The selected tests cover:

1. **Core login path** — existing tests verify that valid and invalid credentials still work
   after the guard is added.
2. **New rate-limiting behavior** — new tests verify the `429` response, the reset, and the
   `Retry-After` header.
3. **Module wiring** — the app-level e2e test catches module registration errors.
4. **Scope boundary** — tests confirm that only the login endpoint is rate limited.

---

## Not Covered (known gaps)

| Behavior | Gap reason | Risk |
|---|---|---|
| Multi-instance Redis behavior | No integration environment in CI | Medium — requires manual staging test |
| NAT/proxy IP behavior | No test infrastructure for shared IPs | Low — document in release notes |
