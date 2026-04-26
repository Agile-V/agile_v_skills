# CHECKPOINTS.md — durable Human Gate interrupts (Phase 2)

Append-only pipe format:

`INTERRUPT-ID | cycle | gate | status | opened_at | due_at | assignee_hint | resume_token | scope_ref | escalation_ref | closed_at | decision_ref`

## Examples

```text
INT-0001 | C1 | G1 | PENDING | 2026-04-26T09:00:00Z | 2026-04-28T09:00:00Z | engineering-lead | rtok-7f3a9b2c | REQUIREMENTS.md | — | — | —
INT-0001 | C1 | G1 | RESUMED | — | — | — | rtok-7f3a9b2c | REQUIREMENTS.md | — | 2026-04-27T14:00:00Z | GATE-0007
```

Resume: next agent turn reads this file + `STATE.md`, validates `resume_token` matches `APPROVALS.md` / `STATE.md`, then continues pipeline.

See [01_SCHEMAS.md](../../docs/agile-v-runtime/01_SCHEMAS.md#5-checkpoints-checkpointsmd--durable-hitl).