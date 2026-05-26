# Example: Evidence Bundle with Understanding Artifacts

## Change request

CR-001: Add rate limiting to the login endpoint.

---

## Graph Traceability Matrix

| Requirement | Graph Node | File/Symbol | Change Type | Test Evidence | Status |
|---|---|---|---|---|---|
| REQ-001: Login continues to work | node-042 | `src/auth/auth.controller.ts::login` | Modified | `auth.e2e-spec.ts::should login with valid credentials` | Verified |
| REQ-002: 5 attempts allowed | node-044 | `src/auth/guards/rate-limit.guard.ts` | Added | `auth.e2e-spec.ts::boundary test` | Verified |
| REQ-003: 6th attempt returns 429 | node-044 | `src/auth/guards/rate-limit.guard.ts` | Added | `auth.e2e-spec.ts::should return 429` | Verified |
| REQ-004: Retry-After header present | node-044 | `src/auth/guards/rate-limit.guard.ts` | Added | `auth.e2e-spec.ts::headers test` | Verified |
| REQ-005: Counter resets after 60s | node-044 | `src/auth/guards/rate-limit.guard.ts` | Added | `auth.e2e-spec.ts::rate limit resets` | Verified |
| REQ-006: Rate limit events logged | node-042 | `src/auth/auth.controller.ts::login` | Modified | `auth.controller.spec.ts::log test` | Verified |

### Orphan Requirements

None.

### Orphan Changes

| File/Symbol | Issue |
|---|---|
| `src/auth/auth.module.ts::AuthModule` | Changed (throttler registration) but not linked to a requirement. Justified: module wiring required by REQ-002. |

### Traceability Decision

- **Pass**
- All requirements have linked components and test evidence.
- The one orphan change is justified as implementation scaffolding for REQ-002.

---

## Diff Impact Report (excerpt)

### Summary

Added `@nestjs/throttler` rate limiting to the login endpoint. A new `RateLimitGuard` was
created and registered in `AuthModule`. The controller was updated to apply the guard.

### Predicted vs Actual Impact

| Component | Predicted | Changed | Explanation |
|---|---|---:|---|
| `src/auth/auth.controller.ts` | Yes | Yes | Expected — guard applied here. |
| `src/auth/auth.module.ts` | Yes | Yes | Expected — throttler registered. |
| `src/auth/guards/rate-limit.guard.ts` | Yes (new) | Yes | Expected — new guard. |
| `src/auth/auth.service.ts` | Low confidence | No | Not required; guard runs before service. |
| `src/app.module.ts` | Medium | No | `ThrottlerModule` registered in `AuthModule`, not globally. |

### Unexpected Changes

None.

### Regression Evidence

| Risk | Test Evidence | Result |
|---|---|---|
| Core login broken | `auth.e2e-spec.ts::should login with valid credentials` | Pass |
| Error handling broken | `auth.e2e-spec.ts::should reject invalid credentials` | Pass |
| Rate limit not enforced | `auth.e2e-spec.ts::should return 429` | Pass |
| Multi-instance Redis | Not tested in CI | Manual — see release notes |

### Decision

- **Accept**
- All acceptance criteria verified. One known gap (multi-instance) documented in release notes.

---

## Evidence manifest (excerpt)

```json
{
  "schema_version": "1.1.0",
  "bundle_id": "EVB-2026-0001",
  "change_request_id": "CR-001",
  "includes_understanding": true,
  "understanding": {
    "source": "understand-anything",
    "source_graph_path": ".understand-anything/knowledge-graph.json",
    "source_graph_hash": "sha256:a3f2c1...",
    "normalized_graph_path": "00_understanding/normalized_graph.json",
    "impact_map_path": "01_impact/impact_map.md",
    "graph_traceability_path": "07_traceability/graph_traceability_matrix.md"
  },
  "artifacts": {
    "00_understanding": [
      "knowledge_graph_hash.txt",
      "normalized_graph.json",
      "system_overview.md",
      "architecture_map.md",
      "understanding_gate_decision.md"
    ],
    "01_impact": [
      "impact_map.md",
      "affected_components.json",
      "required_regression_tests.md",
      "change_risk_assessment.md"
    ],
    "07_traceability": [
      "graph_traceability_matrix.md",
      "req_to_component_links.json",
      "component_to_test_links.json",
      "diff_impact_report.md"
    ]
  }
}
```
