# Example: Impact Analysis Output

## Input

- Change request: CR-001 (Add rate limiting to login endpoint)
- Repository: `my-org/auth-service`
- Knowledge graph: `.understand-anything/knowledge-graph.json`

---

## Impact Map

### Change Request

Add rate limiting to the login endpoint (`POST /auth/login`). Limit: 5 attempts per IP per
60 seconds. Return `429 Too Many Requests` on breach.

### Directly Affected Components

| Component ID | File | Symbol | Reason | Confidence |
|---|---|---|---|---|
| node-042 | `src/auth/auth.controller.ts` | `AuthController.login` | Login endpoint handler — primary target of rate limiting. | High |
| node-043 | `src/auth/auth.module.ts` | `AuthModule` | Must register rate limiting guard or interceptor. | High |
| node-044 | `src/auth/guards/rate-limit.guard.ts` | — | New file. Rate limiting guard to be created. | High |

### Indirectly Affected Components

| Component ID | Relationship | Reason | Confidence |
|---|---|---|---|
| node-001 | imports | `app.module.ts` imports `AuthModule`; module config may change. | Medium |
| node-099 | calls | `auth.service.ts::validateUser` is called by the controller; may need rate-limit awareness. | Low |
| node-120 | tests | `test/auth/auth.e2e-spec.ts` tests the login flow; must be updated for rate limit behavior. | High |

### Tests Likely Affected

| Test file | Reason | Required action |
|---|---|---|
| `test/auth/auth.e2e-spec.ts` | Tests the login endpoint directly. | Update: add rate limit test cases. |
| `src/auth/auth.controller.spec.ts` | Unit tests for `AuthController`. | Update: mock rate limiter. |

### Documentation Likely Affected

| Document | Reason | Required action |
|---|---|---|
| `docs/api/auth.md` | Login endpoint docs. | Update: document rate limit behavior and 429 response. |
| `README.md` | Lists dependencies. | Review: if Redis added, document. |

### Risks

| Risk ID | Risk | Severity | Mitigation | Verification |
|---|---|---|---|---|
| RISK-001 | Shared IP (NAT/proxy) causes false positives for legitimate users. | Medium | Document behavior. Consider configurable threshold. | Manual review of acceptance criteria. |
| RISK-002 | In-memory rate limiter does not work behind multiple instances. | High | Use Redis-backed rate limiter for production. | Integration test with two instances. |
| RISK-003 | Existing test loops may trigger rate limit, breaking CI. | Medium | Increase threshold in test environment or mock the guard. | CI run post-implementation. |

### Assumptions

- The repository uses NestJS with a guard-based middleware pattern.
- The rate limiter will be implemented using `@nestjs/throttler` or equivalent.
- Redis is already available in the production environment (or will be added).

### Confidence

- Overall impact confidence: **High**
- Reason: The login endpoint is clearly identified in the graph. Direct dependencies are small
  and well-defined.

---

## Affected Components JSON (excerpt)

```json
[
  {
    "component_id": "node-042",
    "path": "src/auth/auth.controller.ts",
    "symbol": "AuthController.login",
    "impact_type": "modify",
    "reason": "Login endpoint handler — primary target of rate limiting.",
    "confidence": "high"
  },
  {
    "component_id": "node-043",
    "path": "src/auth/auth.module.ts",
    "symbol": "AuthModule",
    "impact_type": "modify",
    "reason": "Must register rate limiting guard or interceptor.",
    "confidence": "high"
  },
  {
    "component_id": "node-044",
    "path": "src/auth/guards/rate-limit.guard.ts",
    "symbol": null,
    "impact_type": "add",
    "reason": "New rate limiting guard.",
    "confidence": "high"
  }
]
```
