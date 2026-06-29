# `.agile-v/` runtime templates (Phase 1 and 2)

Copy these files into your **project** `.agile-v/` directory and adjust `policy_version`, thresholds, and rules for your organization.


| Template                          | Target filename           | Purpose |
| --------------------------------- | ------------------------- | ------- |
| `POLICY.example.yaml`             | `POLICY.yaml`             | Tool-class allow/deny rules |
| `TRACE_LOG.example.md`            | `TRACE_LOG.md`            | Append-only trace spans |
| `EVAL_RESULTS.example.md`         | `EVAL_RESULTS.md`         | Eval runs and Gate 2 input |
| `CHECKPOINTS.example.md`          | `CHECKPOINTS.md`          | Durable HITL checkpoints |
| `CONTROL_MATRIX.example.yaml`     | `CONTROL_MATRIX.yaml`     | Operating control map for agentic execution |


Full schema definitions: [docs/agile-v-runtime/01_SCHEMAS.md](../../docs/agile-v-runtime/01_SCHEMAS.md).

Control matrix schema: [CONTROL_MATRIX.schema.json](CONTROL_MATRIX.schema.json).

## Quick start: control matrix

```bash
mkdir -p .agile-v
cp templates/agile-v/CONTROL_MATRIX.example.yaml .agile-v/CONTROL_MATRIX.yaml
# Edit: owners, vendor/model, data class, tool rules, cost limits, rollback, status: active
```