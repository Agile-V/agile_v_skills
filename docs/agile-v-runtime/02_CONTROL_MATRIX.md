# Agile-V Control Matrix Runtime Contract

> **Purpose:** Normative reference for `.agile-v/CONTROL_MATRIX.yaml`. Explains placement, relation to existing runtime files, field semantics, Human Gate mapping, evidence bundle mapping, and downstream enforcement requirements.
> **Normative references:** `agile-v-control-matrix`, `agile-v-core`, `compliance-auditor`, `red-team-verifier` skills (v1.0+).

The control matrix is the operating control record for agentic execution. It answers: Which data may this agent process? Which tools may it call? Which model/vendor may it use? Where are logs stored? What are the maximum permissions? Which Human Gates are required? Which tests must pass? What is the cost limit? How can the change be rolled back? Who owns the risk?

`POLICY.yaml` is still used for low-level tool-class rules. `CONTROL_MATRIX.yaml` is the higher-level control map that binds task scope, skill use, data class, model, logs, rights, gates, tests, costs, rollback, and ownership.

---

## 1. Purpose

The control matrix enforces governance over agentic execution at the task level. It is machine-readable so consuming runtimes (CLIs, hooks, CI gates, evidence validators) can check policy without relying solely on agent instructions.

Skills instruct agents how to behave. The control matrix is the record they check and the contract that consuming runtimes enforce. An agent may ignore a skill; it cannot bypass a fail-closed hook or CI gate without leaving evidence.

---

## 2. Placement

| Location | Purpose |
|---|---|
| `.agile-v/CONTROL_MATRIX.yaml` | Project runtime instance (highest precedence) |
| `config/control_matrix.yaml` | Repository default (consuming repo fallback) |
| `templates/agile-v/CONTROL_MATRIX.example.yaml` | Starter template (this skills repo) |

Copy the example template, fill all `TBD` fields, and set `status: active` before enabling fail-closed enforcement.

---

## 3. Relation to `POLICY.yaml`

`POLICY.yaml` defines fine-grained tool-class rules (allow/deny/require_checkpoint per matched tool pattern). It fires per tool call and posts `POLICY_EVENT` lines to `TRACE_LOG.md`.

`CONTROL_MATRIX.yaml` operates at a higher level. It binds: scope, data class, tool allowlist/denylist, model/vendor, log routing, max permissions, Human Gates, test requirements, cost limits, rollback plans, and owner accountability. The two files are complementary. Use both.

---

## 4. Relation to `TRACE_LOG.md`

Every control matrix decision (allow, deny, require_human_gate, warn) should append a `POLICY_EVENT` or `CONTROL_EVENT` span to `TRACE_LOG.md`.

Format:

```text
TR-XXXX|ISO8601_UTC|control-matrix|control_check|—|policy|REQ-IDs|config/control_matrix.yaml|control_id=cm-XXX decision=allow tool=read_file
```

---

## 5. Relation to `EVAL_RESULTS.md`

Gate 2 cannot pass unless matrix-required tests pass. The `tests.required` field in each control entry defines which test suites must appear in `EVAL_RESULTS.md` with `threshold_met: true`.

For `L3+`, `required_for_l3_plus` tests must also appear. For `L4`, `required_for_l4` tests must appear.

---

## 6. Relation to `CHECKPOINTS.md`

When a control matrix decision is `require_human_gate`, the agent must append a PENDING checkpoint row before halting.

Format:

```text
INT-XXXX|C1|CONTROL_MATRIX_GATE|PENDING|2026-06-28T10:00:00Z|2026-06-29T10:00:00Z|technical_owner|rt-abc123|config/control_matrix.yaml|none|-|-
```

Resume only after a matching approval row exists in `APPROVALS.md` and the resume token matches.

---

## 7. Relation to `APPROVALS.md`

Gate approvals must be durable rows in `APPROVALS.md`. Chat-only approval is not sufficient for regulated, L3, or L4 work.

Format:

```text
GATE-XXXX|2026-06-28T10:15:00Z|technical_owner|approved|rt-abc123|shell_exec approved for task AAV-0001|INT-XXXX
```

---

## 8. Field Reference

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Unique control ID. Pattern: `cm-[a-z0-9-]+` |
| `status` | Yes | `draft`, `active`, `deprecated`, `disabled` |
| `scope` | Yes | `global`, `task`, `agent`, `skill`, `tool`, `repo` |
| `minimum_risk_level` | Yes | `L0`–`L4`; entry applies only at this level or higher |
| `applies_to` | Yes | `task_types`, `agent_modes`, `skills`; `*` matches all |
| `data_class.allowed` | Yes | Permitted data classes |
| `data_class.forbidden` | Yes | Blocked data classes |
| `data_class.unknown_action` | Yes | `deny`, `allow`, or `require_human_gate` |
| `tools.allowed` | Yes | Allowlisted tool classes |
| `tools.forbidden` | Yes | Denylisted tool classes (may not overlap `allowed`) |
| `tools.requires_gate` | Yes | Tool classes requiring Human Gate approval |
| `model.vendor` | Yes | Permitted vendor identifier |
| `model.model_name` | Yes | Permitted model identifier |
| `model.allow_external_vendor` | Yes | `false` blocks all unlisted vendors |
| `logs.storage_location` | Yes | JSONL log path for control events |
| `logs.retention_days` | Yes | Minimum retention in days |
| `max_permissions` | Yes | Object; per-dimension access limits |
| `human_gates.required_before` | Yes | Array of `{action, gate, approver_role}` |
| `human_gates.checkpoint_file` | Yes | Path to durable CHECKPOINTS.md |
| `human_gates.approvals_file` | Yes | Path to durable APPROVALS.md |
| `tests.required` | Yes | Suites required for all risk levels |
| `cost_limit` | Yes | Per-run, per-day, per-month limits with currency |
| `rollback` | Yes | Strategy, required risk levels, max time, owner role |
| `owner` | Yes | `business_owner`, `technical_owner`, `security_owner`, `reviewer` |
| `review` | Yes | `last_reviewed`, `review_cycle_days`, `reviewer_role` |

---

## 9. Human Gate Examples

### Gate on shell execution

Control entry:

```yaml
tools:
  requires_gate:
    - "shell_exec"
human_gates:
  required_before:
    - action: "external_effect"
      gate: "G2"
      approver_role: "technical_owner"
```

Agent behavior:

1. Shell tool requested → decision: `require_human_gate`
2. Append PENDING checkpoint row to `.agile-v/CHECKPOINTS.md`
3. Halt and request approval from `technical_owner`
4. On approval: matching `APPROVALS.md` row + resume token unlocks gate
5. Proceed; log control event to `.agile-v/logs/control-events.jsonl`

### Gate on unknown data class

Control entry:

```yaml
data_class:
  unknown_action: "require_human_gate"
```

Agent behavior:

1. Data class unknown → decision: `require_human_gate` (G1, security_owner)
2. Halt; append checkpoint
3. Resume only after security owner durable approval

---

## 10. Evidence Bundle Mapping

The evidence bundle for `L2+` tasks should include a `control_matrix` section:

```json
{
  "control_matrix": {
    "control_id": "cm-default-agentic-task",
    "matrix_path": "config/control_matrix.yaml",
    "policy_version": "1.0.0",
    "decisions": [
      {
        "timestamp": "2026-06-28T10:00:00Z",
        "check": "tool",
        "decision": "allow",
        "reason": "Tool allowed: read_file"
      }
    ],
    "owner": {"technical_owner": "team-platform"},
    "rollback": {"strategy": "revert_commit", "path": "git revert HEAD"},
    "cost": {"run_cost": 0.42, "currency": "EUR"},
    "log_refs": [".agile-v/logs/control-events.jsonl"]
  }
}
```

Validation rules:

- `L0`/`L1`: warn if missing; require after migration date.
- `L2+`: require immediately.
- `L3+`: require at least one approval reference when gates are triggered.

---

## 11. Consuming Runtime Requirements

The skills repo publishes the template and schema. The consuming agentic runtime must enforce:

| Mechanism | Purpose |
|---|---|
| CLI validator (`agilev controls validate`) | Schema + semantic validation on PR and locally |
| Pre-tool-use hook | Block forbidden/gated tools before execution |
| Stop hook | Validate evidence bundle includes control matrix section |
| Evidence bundle validator | Enforce `L2+` control matrix presence |
| CI gate | Block merge when matrix is invalid or tests fail |

Skill instructions alone are not sufficient enforcement. An agent may ignore a skill; it cannot bypass a fail-closed hook or CI gate.

---

## 12. Agentic Repo Integration Example

```bash
# Copy template into project runtime
mkdir -p .agile-v
cp templates/agile-v/CONTROL_MATRIX.example.yaml .agile-v/CONTROL_MATRIX.yaml
# Edit: owners, vendor/model, data class, tools, cost limits, rollback, status: active

# Validate (requires agilev CLI from agentic_agile_v repo)
agilev controls validate

# Check a tool call
agilev controls check-tool --task AAV-0001 --tool shell_exec --json

# Explain selected control
agilev controls explain --task-type feature --risk L2 --mode builder --skill agile-v-builder
```

The agentic repo (`Agile-V/agentic_agile_v`) enforces the matrix via `agilev controls`, OpenHands hooks, evidence adapter, and CI gates. This skills repo provides the normative skill, template, and schema.

---

## Cross-references

- Template: [templates/agile-v/CONTROL_MATRIX.example.yaml](../../templates/agile-v/CONTROL_MATRIX.example.yaml)
- Schema: [templates/agile-v/CONTROL_MATRIX.schema.json](../../templates/agile-v/CONTROL_MATRIX.schema.json)
- Schemas index: [01_SCHEMAS.md](01_SCHEMAS.md)
- Skill: [agile-v-control-matrix/SKILL.md](../../agile-v-control-matrix/SKILL.md)
