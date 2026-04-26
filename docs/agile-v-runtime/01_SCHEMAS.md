# Agile V Runtime Schemas (Phase 1 and 2)

> **Purpose:** Machine-readable contracts for trace, evaluation, policy, failure taxonomy, and durable Human Gate checkpoints under `.agile-v/`.
> **Normative references:** `agile-v-core`, `red-team-verifier`, `compliance-auditor`, `agile-v-compliance` skills (v1.4+).

## File placement

Copy templates from [templates/agile-v/](../../templates/agile-v/) into the project `.agile-v/` directory (same level as `STATE.md`, `DECISION_LOG.md`).


| File              | Phase | Description                                                  |
| ----------------- | ----- | ------------------------------------------------------------ |
| `POLICY.yaml`     | 2     | Policy-as-code: tool classes, allow/deny, fail mode, version |
| `TRACE_LOG.md`    | 1     | Append-only trace spans (optional, recommended)              |
| `EVAL_RESULTS.md` | 1     | Eval runs and thresholds; Human Gate 2 input                 |
| `CHECKPOINTS.md`  | 2     | Durable HITL: pending/resumed/expired interrupts             |


---

## 1. Trace (`TRACE_LOG.md`)

**Format:** One record per line; append-only. Pipe-delimited (recommended):

```text
TRACE-ID|ISO8601_UTC|agent_id|span_name|parent_TRACE-ID|event_type|REQ-IDs|ref_path_or_uri|notes
```


| Field           | Required | Description                           |
| --------------- | -------- | ------------------------------------- |
| TRACE-ID        | Yes      | TR-0001 monotonic per project         |
| ISO8601_UTC     | Yes      | Event timestamp                       |
| agent_id        | Yes      | Role or tool session id               |
| span_name       | Yes      | e.g. build, verify, tool:Read         |
| parent_TRACE-ID | No       | — if root                             |
| event_type      | Yes      | start; end; tool; gate; policy; error |
| REQ-IDs         | No       | Comma-separated or —                  |
| ref_path_or_uri | No       | Path or external trace id             |
| notes           | No       | Short free text                       |


---

## 2. Eval (`EVAL_RESULTS.md`)

**Purpose:** Evidence eval gates ran before Human Gate 2. Offline suites and/or online hooks.

**YAML frontmatter (optional),** updated each eval run:

```yaml
eval_run_id: "ER-2026-04-26-001"
eval_timestamp: "2026-04-26T12:00:00Z"
policy_version_ref: "1.0.0"
eval_gate_status: "PASS"
eval_gate_rationale: "Thresholds met; see table."
thresholds:
  critical_max_fail: 0
  major_max_fail: 0
  minor_max_fail: 3
```

**Append-only body rows:**

```text
ER-XXXX|suite_id|mode|PASS_count|FAIL_count|threshold_met|linked_cycle|notes
```


| mode    | Meaning                                     |
| ------- | ------------------------------------------- |
| offline | Curated dataset / regression eval           |
| online  | Live/sampled scoring (note sampling policy) |
| waived  | Waiver; needs APPROVALS.md ref in notes     |


**Human Gate 2:** `eval_gate_status` must be `PASS` or `WAIVED` (with approver evidence) or Gate 2 cannot approve release.

---

## 3. Policy (`POLICY.yaml`)

**Purpose:** Tool-class pre/post rules; version for audit.


| Key            | Type   | Description                          |
| -------------- | ------ | ------------------------------------ |
| policy_version | string | Semver/org; VSR/ATM footers          |
| fail_mode      | string | closed=block on error; open=log only |
| effective_from | string | ISO8601 optional                     |
| rules          | list   | Rule objects below                   |


**Rule object:**


| Key         | Type   | Description                                           |
| ----------- | ------ | ----------------------------------------------------- |
| id          | string | R001 unique in file                                   |
| description | string | Human-readable                                        |
| match       | object | tool_pattern, optional paths                          |
| action      | string | allow; deny; require_checkpoint; require_approval_ref |
| risk_weight | int    | 1–5; optional run aggregate                           |
| fail_closed | bool   | Override top-level fail_mode                          |


**Post-execution:** Append `POLICY_EVENT` lines to `TRACE_LOG.md` with `event_type=policy` when a rule fires.

---

## 4. Failure taxonomy (FT codes)

Each finding/eval failure SHOULD include one **FT** code.


| Code         | Meaning                 | Typical use                             |
| ------------ | ----------------------- | --------------------------------------- |
| FT-PLAN      | Plan deviation          | Skipped step or unplanned work          |
| FT-TOOL      | Invalid tool invocation | Bad args, disallowed tool, schema error |
| FT-MISP      | Misinterpretation       | Wrong read of tool output or context    |
| FT-UNSUPPORT | Unsupported intent      | No tool/skill for action                |
| FT-POLICY    | Policy block            | POLICY.yaml or host policy              |
| FT-SYS       | System/runtime          | Network, timeout, outage                |


**VER record (pipe):**

```text
VER-XXXX|TC-XXXX|REQ-XXXX|PASS/FAIL/FLAG|FT-CODE|description
```

Optional seventh field `severity` (CRITICAL/MAJOR/MINOR) if split from PASS/FAIL/FLAG.

Stub/anti-pattern: FT-TOOL or FT-PLAN; hardcoded secret: FT-POLICY or FT-TOOL + CRITICAL.

---

## 5. Checkpoints (`CHECKPOINTS.md`) — durable HITL

**Purpose:** Pause/resume Human Gates without chat-only state.

**Append-only pipe format:**

```text
INTERRUPT-ID|cycle|gate|status|opened_at|due_at|assignee_hint|resume_token|scope_ref|escalation_ref|closed_at|decision_ref
```


| Field        | Description                                        |
| ------------ | -------------------------------------------------- |
| INTERRUPT-ID | INT-0001 monotonic                                 |
| gate         | G1, G2, or custom label                            |
| status       | PENDING; RESUMED; EXPIRED; ESCALATED; CANCELLED    |
| resume_token | Opaque; must match APPROVALS.md/STATE.md on resume |
| scope_ref    | Artifact path under review                         |
| decision_ref | GATE-XXXX when closed                              |


**Resume:** (1) Pause: append PENDING + resume_token + due_at. (2) Decision: append RESUMED + decision_ref=GATE-XXXX (or INT-0001-R1 child row). (3) Timeout: EXPIRED/ESCALATED + escalation_ref. (4) Resume from CHECKPOINTS.md + STATE.md only—not chat alone.

---

## Cross-references

- Templates: [templates/agile-v/](../../templates/agile-v/)

