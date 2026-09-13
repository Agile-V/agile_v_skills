# Agile V Runtime Schemas (Phase 1 and 2)

> **Purpose:** Machine-readable contracts for required Gate 1/Gate 2 records, trace, evaluation, policy, failure taxonomy, and durable Human Gate checkpoints under `.agile-v/`.
> **Normative references:** `agile-v-core`, `red-team-verifier`, `compliance-auditor`, `agile-v-compliance` skills (v1.4+).

## File placement

Copy runtime starters from the repository source directory [`templates/agile-v/`](../../templates/agile-v/) into the consuming project's `.agile-v/` directory (same level as `STATE.md`, `DECISION_LOG.md`). Root AI-provenance templates are separate: [`templates/`](../../templates/).


| File                    | Phase | Description                                                  |
| ----------------------- | ----- | ------------------------------------------------------------ |
| `POLICY.yaml`           | 2     | Policy-as-code: tool classes, allow/deny, fail mode, version |
| `TRACE_LOG.md`          | 1     | Append-only trace spans (optional, recommended)              |
| `EVAL_RESULTS.md`       | 1     | Eval runs and thresholds; Human Gate 2 input                 |
| `CHECKPOINTS.md`        | 2     | Durable HITL: pending/resumed/expired interrupts             |
| `CONTROL_MATRIX.yaml`   | 2     | Operating control map: data class, tools, model/vendor, logs, rights, Human Gates, tests, costs, rollback, owners |
| `AGENT_TOOL_RECORD.yaml` | 3 | Per-tool/MCP identity, schema, auth, scope, side-effect, and execution evidence; source: [`templates/AGENT_TOOL_RECORD.yaml`](../../templates/AGENT_TOOL_RECORD.yaml) |
| `AGENT_DELEGATION_RECORD.yaml` | 3 | Authenticated A2A handoff, delegation scope, correlation, expiry, and acceptance evidence; source: [`templates/AGENT_DELEGATION_RECORD.yaml`](../../templates/AGENT_DELEGATION_RECORD.yaml) |
| `BUILD_MANIFEST.md` | 1 | Build artifact lineage to a specific baselined requirement revision |
| `VERIFICATION_SUMMARY.md` | 1 | Independent verification aggregate and EvalGate handoff for Human Gate 2 |


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

## 6. Control Matrix (`CONTROL_MATRIX.yaml`)

See [02_CONTROL_MATRIX.md](02_CONTROL_MATRIX.md). The matrix is required for non-trivial agentic execution and should be checked before implementation, high-impact tool use, model/vendor changes, and release gates.

`POLICY.yaml` controls tool-class rules at the rule level. `CONTROL_MATRIX.yaml` is the higher-level operating control record that binds task scope, data class, model, logs, rights, gates, tests, costs, rollback, and ownership into a single reviewable artifact.

---

## 7. Canonical structured equivalents

The Draft 2020-12 contracts in [`schemas/`](../../schemas/) validate structured equivalents used by integrations. Markdown records may retain their documented presentation while parsers map them to these shapes.

| Record | Schema | Gate role |
|---|---|---|
| `POLICY.yaml` | [`POLICY.schema.json`](../../schemas/POLICY.schema.json) | Policy evidence used at both gates |
| `EVAL_RESULTS.md` | [`EVAL_RESULTS.schema.json`](../../schemas/EVAL_RESULTS.schema.json) | Eval prerequisite for Gate 2 |
| `CONTROL_MATRIX.yaml` | [`CONTROL_MATRIX.schema.json`](../../schemas/CONTROL_MATRIX.schema.json) | Required control map for non-trivial work |
| `BUILD_MANIFEST.md` | [`BUILD_MANIFEST.schema.json`](../../schemas/BUILD_MANIFEST.schema.json) | Post-Gate-1 synthesis lineage |
| `VERIFICATION_SUMMARY.md` | [`VERIFICATION_SUMMARY.schema.json`](../../schemas/VERIFICATION_SUMMARY.schema.json) | Independent verification handoff for Gate 2 |

`VERIFICATION_SUMMARY` aggregates requirement-conformance evidence. Intended-use validation is separate and remains governed by [`VALIDATION_REPORT.schema.json`](../../schemas/VALIDATION_REPORT.schema.json); a verification summary may reference validation reports but must not represent them as verification results.

### 7.1 Evidence Bundle v2

[`EVIDENCE_BUNDLE.v2.schema.json`](../../schemas/EVIDENCE_BUNDLE.v2.schema.json) upgrades the v1 container contract into typed claims and evidence: each claim declares its `required_evidence_properties`; each evidence item declares which claim(s) it `supports`, its `producer`, `state_binding`, `integrity` digest, and — for `L2`+ bundles — a `policy_binding`. `admission.status` records the gate outcome. Subject binding (`baseline.subject_state` / `evidence[].state_binding`) is domain-agnostic: `subject_type` may be `source_control_commit`, `document_revision`, `hardware_revision`, `dataset_version`, `configuration_baseline`, or `other`, with any domain-specific identifiers (e.g. a Git commit and build digest) carried under an optional `profile_specific` object rather than as normative top-level fields. v1 (`schema_version: "1.0"`) remains unchanged and valid for existing consumers; **new `L2`+ gate decisions MUST use v2** (current `schema_version` per `contracts/versions.yaml`); v1 remains valid only for historical records and migration reads (see "v1/v2 transition" below). Structural validity does not by itself prove `state_binding.subject_ref` matches `baseline.subject_state.subject_ref` — that is a semantic admissibility check per `07_EVIDENCE_ADMISSION_CONTRACT.md`, not a JSON Schema constraint.

#### v1/v2 transition

From this contract version forward: any **new** `L2`+ gate decision MUST be recorded as `EVIDENCE_BUNDLE.v2`. `EVIDENCE_BUNDLE` v1 instances remain valid for two purposes only — (a) historical records produced before this rule existed, and (b) migration reads that normalize a legacy record without inventing missing v2 fields. A runtime MUST NOT accept a newly produced v1 bundle as sufficient for a new `L2`+ decision; doing so bypasses the typed-claim/state-binding model this contract exists to enforce. The same rule applies to `APPROVAL` v1 vs. `APPROVAL.v2` (`schemas/APPROVAL.v2.schema.json`): new `L2`+ approvals MUST use v2's scope/expiry/binding fields.

### 7.2 Gate Receipt and Approval v2

[`GATE_RECEIPT.schema.json`](../../schemas/GATE_RECEIPT.schema.json) records why a lifecycle transition was permitted or denied: required/admitted/rejected/stale claims, consulted approvals, verifier `independence_class` (`I0`–`I4`, see `08_INDEPENDENCE_CLASSES.md`), residual risk, and a `PASS`/`WAIVED`/`FAIL`/`NEEDS_HUMAN`/`STALE`/`CONFLICT` decision. `subject_state` is gate-specific (`requirement_revision_ref` pre-baseline at `gate_1`; `requirement_baseline_id` + exact `subject_digest` at `eval_gate`/`gate_2`/`qualification_stage`, so a receipt cannot bind to "the baseline" in the abstract while leaving which exact delivered artifact was verified unspecified). A `WAIVED` decision requires non-empty `exception_refs`; `gate_1`/`gate_2` `PASS`/`WAIVED` require a non-empty `approvals` array. Structural presence of these fields is necessary but not sufficient — resolving them against real, currently-valid, correctly-scoped `EXCEPTION_DECISION`/`APPROVAL` records is a semantic check (`contracts/semantics.py`: `gate_receipt_waiver_is_justified`, `gate_receipt_has_valid_human_approval`), not a JSON Schema constraint. [`APPROVAL.v2.schema.json`](../../schemas/APPROVAL.v2.schema.json) upgrades v1 with explicit `scope`, `expires_at`, exact artifact/policy `binding`, and `usage.reusable`/`consumed_at` (a non-reusable, already-consumed approval is no longer valid even before it expires). A Gate Receipt's `approvals` array only references `APPROVAL` records by ID; it does not embed or replace them. **A Human Gate approval and a Gate Receipt are different objects: approval records authority, Gate Receipt records decision basis. Neither substitutes for the other.** v1 `APPROVAL.schema.json` (`schema_version: "1.0"`) remains unchanged and valid.

### 7.3 Exception and Waiver contract

[`EXCEPTION_DECISION.schema.json`](../../schemas/EXCEPTION_DECISION.schema.json) is the structured form of waiver, concession, dispensation, residual-risk acceptance, and defer — see `09_EXCEPTION_AND_WAIVER_CONTRACT.md` for the normative rules (non-waivable meta-controls, expiry, no propagation to later cycles). A Gate Receipt with a `WAIVED`-equivalent decision references the relevant `EXC-XXXX` id(s); it must not present a waived decision as an unqualified `PASS`.

### 7.4 Change-aware revalidation

[`REVALIDATION_ASSESSMENT.schema.json`](../../schemas/REVALIDATION_ASSESSMENT.schema.json) records, per changed dependency (source, requirement, policy, environment, tool, model, hardware), whether each admitted evidence item is `UNCHANGED`, `REVALIDATION_REQUIRED`, `STALE`, or `UNKNOWN` — see `10_CHANGE_AWARE_REVALIDATION.md`. Only `UNCHANGED` is reuse-eligible; `UNKNOWN` coverage requires `conservative_fallback_applied: true` and is never treated as `UNCHANGED`, especially at `L3`/`L4`. This generalizes the AI-BOM-specific triggers in `../ai-bom-revalidation-triggers.md`.

### 7.5 Risk Assessment v2

[`RISK_ASSESSMENT.schema.json`](../../schemas/RISK_ASSESSMENT.schema.json) adds dimension-based scoring and deterministic risk floors to the `L0`–`L4` model — see `11_RISK_ASSESSMENT_V2.md`. A floor cannot be silently lowered; doing so requires an authorized `EXCEPTION_DECISION` referenced by `exception_ref`.

### 7.6 Governance conversion

[`GOVERNANCE_CONVERSION.schema.json`](../../schemas/GOVERNANCE_CONVERSION.schema.json) records how a recurrent/severe finding becomes a new or changed control — see `12_GOVERNANCE_CONVERSION.md`. `proposed -> approved -> deployed -> validated`; the proposer is never the approving authority, and activation does not retroactively change an already-frozen task baseline.

### 7.7 Skill preview/draft graduation

[`SKILL_STATUS.schema.json`](../../schemas/SKILL_STATUS.schema.json) validates the `metadata.status`/`metadata.preview` block every draft/experimental/candidate skill must declare (owner, graduation target, graduation criteria reference, compatibility declaration, known limitations) — see `13_SKILL_GRADUATION_POLICY.md`. A skill does not graduate by self-declaration; graduation requires the evidence listed there and an external recorded decision.

---

## Cross-references

- Templates: [templates/agile-v/](../../templates/agile-v/)
- Control Matrix spec: [02_CONTROL_MATRIX.md](02_CONTROL_MATRIX.md)
- Agent tool and delegation contract: [05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md](05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md)
- Skills <-> runtime compatibility declaration: [contracts/AGILE_V_RUNTIME_COMPATIBILITY.yaml](../../contracts/AGILE_V_RUNTIME_COMPATIBILITY.yaml); canonical contract version registry: [contracts/versions.yaml](../../contracts/versions.yaml)
