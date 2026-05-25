# EVAL_RESULTS.md — eval flywheel + Human Gate 2 prerequisite (Phase 1)

```yaml
eval_run_id: "ER-2026-04-26-001"
eval_timestamp: "2026-04-26T12:00:00Z"
policy_version_ref: "1.0.0"
eval_gate_status: "PASS"
eval_gate_rationale: "Example: offline suite green; see table."
thresholds:
  critical_max_fail: 0
  major_max_fail: 0
  minor_max_fail: 3
```

## Runs (append-only)

```text
ER-XXXX | suite_id | mode | PASS_count | FAIL_count | threshold_met | linked_cycle | notes
ER-2026-04-26-001 | suite-core-1 | offline | 42 | 0 | yes | C1 | linked to TC-XXXX
```

`eval_gate_status` must be **PASS** or **WAIVED** (with `APPROVALS.md` ref in notes) before Human Gate 2 release approval.

See [01_SCHEMAS.md](../../docs/agile-v-runtime/01_SCHEMAS.md#2-eval-eval_resultsmd).