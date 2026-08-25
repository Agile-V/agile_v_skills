# `.agile-v/` runtime templates (Phase 1 and 2)

Copy these files into your **project** `.agile-v/` directory and adjust `policy_version`, thresholds, and rules for your organization.


| Template                          | Target filename           | Purpose |
| --------------------------------- | ------------------------- | ------- |
| `POLICY.example.yaml`             | `POLICY.yaml`             | Tool-class allow/deny rules |
| `TRACE_LOG.example.md`            | `TRACE_LOG.md`            | Append-only trace spans |
| `EVAL_RESULTS.example.md`         | `EVAL_RESULTS.md`         | Eval runs and Gate 2 input |
| `CHECKPOINTS.example.md`          | `CHECKPOINTS.md`          | Durable HITL checkpoints |
| `CONTROL_MATRIX.example.yaml`     | `CONTROL_MATRIX.yaml`     | Operating control map for agentic execution |
| `HUMAN_OVERSIGHT_CASE.example.yaml` | `HUMAN_OVERSIGHT_CASE_<task_id>.yaml` | Bainbridge-aware Human Oversight Case (claims, independence, surprises, recovery) |
| `SOP_BINDING.example.yaml`         | `SOP_BINDING.yaml`        | Bind controlled SOPs to Agile-V controls/gates |
| `QUALIFICATION_PLAN.example.yaml`  | `qualification/QUALIFICATION_PLAN.yaml`  | **[Draft]** GxP qualification plan and tailoring |
| `SYSTEM_DESCRIPTION.example.yaml`  | `qualification/SYSTEM_DESCRIPTION.yaml`  | **[Draft]** System context; standard/configured/custom functionality |
| `SYSTEM_BASELINE.example.yaml`     | `qualification/SYSTEM_BASELINE.yaml`     | **[Draft]** Controlled installation/configuration baseline (no secrets) |
| `QUALIFICATION_PROTOCOL.example.yaml` | `qualification/<STAGE>_PROTOCOL.yaml`  | **[Draft]** DQ/IQ/OQ/PQ protocol (approve before execution) |
| `QUALIFICATION_EXECUTION.example.yaml` | `qualification/<STAGE>_EXECUTION.yaml` | **[Draft]** Execution record; expected-vs-actual, preserves failures |
| `QUALIFICATION_DEVIATION.example.yaml` | `qualification/QUALIFICATION_DEVIATION.yaml` | **[Draft]** Qualification deviation and disposition |
| `QUALIFICATION_SUMMARY.example.yaml` | `qualification/QUALIFICATION_SUMMARY.yaml` | **[Draft]** Qualification summary; distinguishes tests/stage/intended-use/release |
| `REQUALIFICATION_ASSESSMENT.example.yaml` | `qualification/REQUALIFICATION_ASSESSMENT.yaml` | **[Draft]** Change-triggered requalification assessment |


Full schema definitions: [docs/agile-v-runtime/01_SCHEMAS.md](../../docs/agile-v-runtime/01_SCHEMAS.md). These are source templates in the skills repository; use the path to your checked-out skills repository when copying them into a consuming project.

Control matrix schema: [CONTROL_MATRIX.schema.json](CONTROL_MATRIX.schema.json).

## Quick start: control matrix

```bash
mkdir -p .agile-v
cp <skills-repo>/templates/agile-v/CONTROL_MATRIX.example.yaml .agile-v/CONTROL_MATRIX.yaml
# Edit: owners, vendor/model, data class, tool rules, cost limits, rollback, status: active
```
