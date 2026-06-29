# Skills Repo Implementation Plan: Kontrollmatrix / Control Matrix Skill and Templates

Repo: `Agile-V/agile_v_skills`

Purpose: add a reusable Agile-V control matrix skill, templates, schemas, and tests so downstream agentic runtimes, especially `Agile-V/agentic_agile_v`, can enforce data class, allowed tools, model/vendor, log storage, max permissions, Human Gates, tests, cost limits, rollback, and owner accountability.

Important dependency direction: the agentic repo uses the skills. Therefore the skills repo should define the canonical instructions and templates, while the agentic repo performs runtime enforcement with CLI, hooks, evidence validation, and CI.

---

## 1. Existing repo facts to preserve

The skills repo already provides:

- an official Agile-V Agent Skills Library
- `SKILL.md` based skill folders
- root skills such as `agile-v-core`, `requirement-architect`, `logic-gatekeeper`, `build-agent`, `test-designer`, `red-team-verifier`, `compliance-auditor`, and `documentation-agent`
- domain build agents under `domains/`
- runtime governance contracts under `.agile-v/`, including policy-as-code, trace logs, eval results, and durable Human Gate checkpoints
- templates under `templates/agile-v/`
- rules that agents halt on missing requirements, ambiguity, missing traceability, and Human Gates
- rules that the Build Agent does not verify its own work
- model tier guidance and state persistence under `.agile-v/`

The control matrix must fit into that model instead of creating a parallel governance vocabulary.

---

## 2. Ten implementation refinement iterations

| Iteration | Question | Decision |
|---|---|---|
| 1 | Should this be a new skill or only a template? | Add both: a dedicated skill plus reusable templates. |
| 2 | Should the skill enforce runtime behavior? | No. Skills instruct; runtime tools enforce. The agentic repo enforces. |
| 3 | Where should the matrix live in projects? | Project runtime: `.agile-v/CONTROL_MATRIX.yaml`; example: `templates/agile-v/CONTROL_MATRIX.example.yaml`. |
| 4 | How does it relate to `POLICY.yaml`? | `POLICY.yaml` controls tool-class rules; `CONTROL_MATRIX.yaml` is the higher-level operating control record. |
| 5 | How does it relate to Human Gates? | Matrix gates must write to `CHECKPOINTS.md` and `APPROVALS.md`. |
| 6 | How does it relate to traceability? | Every matrix decision should append a policy/control event to `TRACE_LOG.md`. |
| 7 | How does it relate to eval gates? | Gate 2 cannot pass unless matrix-required tests and evals pass. |
| 8 | What should agents do when no matrix exists? | Halt for non-trivial work and instruct creation from the template. |
| 9 | What should downstream runtimes consume? | Template, schema, routing guidance, and skill instructions. |
| 10 | What proves the skills repo is correct? | Frontmatter tests, schema tests, example validation, routing tests, and doc link checks. |

---

## 3. Target repository changes

```text
agile_v_skills/
├── agile-v-control-matrix/
│   └── SKILL.md
├── agile-v-core/
│   └── SKILL.md                              # add reference to control matrix
├── compliance-auditor/
│   └── SKILL.md                              # add control matrix audit duties
├── red-team-verifier/
│   └── SKILL.md                              # add matrix conformance checks
├── documentation-agent/
│   └── SKILL.md                              # document matrix outputs
├── templates/
│   └── agile-v/
│       ├── CONTROL_MATRIX.example.yaml
│       ├── CONTROL_MATRIX.schema.json
│       ├── CONTROL_MATRIX.md
│       └── README.md                         # update index
├── docs/
│   └── agile-v-runtime/
│       ├── 01_SCHEMAS.md                     # add cross-reference
│       └── 02_CONTROL_MATRIX.md              # new detailed spec
├── SKILL_ROUTING_GUIDE.md                    # route governance requests
├── README.md                                 # add included skill and quick use
├── tests/
│   ├── test_control_matrix_template.py
│   ├── test_skill_frontmatter.py
│   └── fixtures/
│       ├── CONTROL_MATRIX.valid.yaml
│       └── CONTROL_MATRIX.invalid.yaml
└── .github/
    └── workflows/
        └── validate-control-matrix.yml
```

If the repo intentionally avoids Python test code today, keep the test plan as a GitHub Action using `python - <<'PY'` or add a lightweight `scripts/validate_templates.py`. Prefer a reusable script when possible.

---

## 4. New skill: `agile-v-control-matrix/SKILL.md`

The skill should be concise, machine-readable, and consistent with existing skill style.

Proposed content:

```markdown
---
name: agile-v-control-matrix
description: Defines and checks the Agile-V control matrix for agentic tasks, skills, model use, tools, logs, rights, Human Gates, tests, costs, rollback, and owners. Load when creating, reviewing, or enforcing `.agile-v/CONTROL_MATRIX.yaml` or runtime governance for agentic execution.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  compliance: "ISO 9001 / ISO 27001 Aligned (Design Phase); GxP-Aware"
  sections_index:
    - Purpose
    - Load Conditions
    - Required Matrix Fields
    - Agent Duties
    - Halt Conditions
    - Human Gate Rules
    - Evidence Rules
    - Runtime Contract
---

# Instructions

You are the Agile-V Control Matrix Governor. Your job is to ensure every non-trivial agentic task has an explicit, reviewable, machine-readable control record before implementation or high-impact tool use.

## Purpose

The control matrix maps agentic execution to operational controls: data class, allowed tools, model/vendor, log location, maximum rights, Human Gates, tests, cost limits, rollback, and owners.

## Load Conditions

Load this skill when the user asks to:

- create or update a Kontrollmatrix / control matrix
- define allowed tools or forbidden tools
- define model/vendor policy
- define Human Gates
- define rollback, owner, cost, or log policy
- audit whether an agent or skill is safe to run
- prepare an agentic runtime for OpenHands, Cursor, Claude Code, VS Code, Copilot, or another execution engine

## Required Matrix Fields

Every active control entry MUST define:

- `id`
- `scope`
- `applies_to`
- `minimum_risk_level`
- `data_class.allowed`
- `data_class.forbidden`
- `tools.allowed`
- `tools.forbidden`
- `tools.requires_gate`
- `model.vendor`
- `model.model_name`
- `logs.storage_location`
- `max_permissions`
- `human_gates.required_before`
- `tests.required`
- `cost_limit`
- `rollback`
- `owner.business_owner`
- `owner.technical_owner`
- `owner.security_owner`
- `owner.reviewer`

## Agent Duties

1. Before implementation, verify that `.agile-v/CONTROL_MATRIX.yaml` exists for non-trivial work.
2. If missing, halt and propose creating it from `templates/agile-v/CONTROL_MATRIX.example.yaml`.
3. Never infer owner approval from chat alone. Require durable approval evidence.
4. Never treat a skill instruction as runtime enforcement. Hooks, policies, validators, or CI must enforce.
5. For every gated action, write or request a checkpoint in `.agile-v/CHECKPOINTS.md`.
6. For every approval, require a reference in `.agile-v/APPROVALS.md`.
7. For every matrix decision, append traceable evidence to `.agile-v/TRACE_LOG.md` or the runtime's equivalent.

## Halt Conditions

Halt if:

- no matrix exists for non-trivial work
- active matrix entry has unresolved owner fields
- data class is unknown and no rule exists
- requested tool is forbidden
- requested tool requires a gate and no approval exists
- model/vendor is not allowed
- cost limit is exceeded
- rollback is required but missing
- required tests are missing
- Human Gate is required but no durable checkpoint or approval exists

## Human Gate Rules

Human Gates must be durable. A gate pause should create a pending checkpoint. A gate resume must reference a matching approval and resume token. Chat-only approval is not sufficient for regulated, L3, or L4 work.

## Evidence Rules

Control matrix evidence should include:

- selected control ID
- matrix path and version
- decisions made
- denied or gated actions
- approval references
- log paths
- model/vendor used
- cost records
- rollback path
- owner fields

## Runtime Contract

This skill defines the expected behavior. Runtime enforcement belongs in the consuming repo, for example:

- CLI validator
- pre-tool-use hook
- stop hook
- evidence-bundle validator
- CI workflow
- policy-as-code engine
```

---

## 5. Template: `CONTROL_MATRIX.example.yaml`

File: `templates/agile-v/CONTROL_MATRIX.example.yaml`

```yaml
# Agile-V Control Matrix. Copy to `.agile-v/CONTROL_MATRIX.yaml`.
version: "1.0.0"
effective_from: "2026-06-28T00:00:00Z"
default_fail_mode: "closed"
default_log_storage: ".agile-v/logs/control-events.jsonl"
default_retention_days: 90

controls:
  - id: "cm-default-agentic-task"
    status: "draft"
    description: "Default control record for Agile-V agentic task execution."
    scope: "task"
    applies_to:
      task_types: ["feature", "bug", "hardware", "firmware", "test", "refactor", "docs", "security", "other"]
      agent_modes: ["builder", "verifier", "risk_classifier", "manual"]
      skills: ["*"]
    minimum_risk_level: "L1"

    data_class:
      allowed: ["public", "internal"]
      forbidden: ["secret", "regulated_health", "payment_card", "production_secret"]
      default_if_unknown: "internal"
      unknown_action: "require_human_gate"
      redaction_required: true

    tools:
      allowed:
        - "read_file"
        - "write_file"
        - "list_files"
        - "run_tests"
        - "git_diff"
        - "git_status"
        - "static_analysis"
        - "schema_validation"
      forbidden:
        - "deploy_production"
        - "send_email_external"
        - "delete_data"
        - "rotate_secrets"
        - "change_iam"
      requires_gate:
        - "shell_exec"
        - "network_egress"
        - "dependency_install"
        - "database_migration"
        - "public_api_change"

    model:
      vendor: "TBD"
      model_name: "TBD"
      fallback_model: null
      allow_external_vendor: false
      require_vendor_review_for_data_classes: ["confidential", "secret", "regulated_health"]
      record_model_in_evidence: true

    logs:
      storage_location: ".agile-v/logs/control-events.jsonl"
      tool_log_location: ".agile-v/logs/tool-usage.jsonl"
      include_prompt: false
      include_response: false
      include_tool_calls: true
      include_decision_rationale: true
      redact_personal_data: true
      retention_days: 90

    max_permissions:
      file_access: "repo_scoped"
      write_access: "task_allowed_paths_only"
      network_access: "blocked_unless_approved"
      database_access: "none"
      email_access: "none"
      credential_access: "none"
      code_execution: "tests_and_local_tools_only"
      git_access: "diff_status_only"

    human_gates:
      required_before:
        - action: "external_effect"
          gate: "G2"
          approver_role: "domain_owner"
        - action: "production_change"
          gate: "G2"
          approver_role: "technical_owner"
        - action: "l3_or_higher"
          gate: "G2"
          approver_role: "domain_owner"
        - action: "forbidden_data_class_exception"
          gate: "G1"
          approver_role: "security_owner"
        - action: "cost_limit_exception"
          gate: "G2"
          approver_role: "business_owner"
      checkpoint_file: ".agile-v/CHECKPOINTS.md"
      approvals_file: ".agile-v/APPROVALS.md"
      require_resume_token: true

    tests:
      required:
        - "schema_validation"
        - "unit_tests"
        - "evidence_bundle_validation"
        - "control_matrix_validation"
      required_for_l3_plus:
        - "security_privacy_check"
        - "rollback_test"
        - "independent_verifier_report"
      required_for_l4:
        - "simulation_or_hil_evidence"
        - "traceability_matrix"
        - "formal_approval"
      minimum_coverage_percent: 80

    cost_limit:
      currency: "EUR"
      max_run_cost: 2.00
      max_daily_cost: 25.00
      max_monthly_cost: 500.00
      action_on_limit: "stop_and_request_approval"
      cost_log: ".agile-v/logs/costs.jsonl"

    rollback:
      required: true
      strategy: "revert_commit_or_disable_feature_flag"
      rollback_path_required_for: ["L2", "L3", "L4"]
      feature_flag_required_for: ["L3", "L4"]
      max_rollback_time_minutes: 30
      rollback_owner_role: "technical_owner"

    owner:
      business_owner: "TBD"
      technical_owner: "TBD"
      security_owner: "TBD"
      reviewer: "TBD"
      backup_owner: "TBD"

    review:
      last_reviewed: "TBD"
      review_cycle_days: 90
      reviewer_role: "security_owner"
```

Keep the template status as `draft`. Consuming repos should make a production copy and replace all `TBD` values before active enforcement.

---

## 6. Template schema

File: `templates/agile-v/CONTROL_MATRIX.schema.json`

Use the same schema as the agentic repo so the downstream runtime can consume it directly.

Minimum requirements:

- JSON Schema draft 2020-12.
- Validate required fields.
- Enforce risk enum: `L0`, `L1`, `L2`, `L3`, `L4`.
- Enforce gate object shape.
- Enforce cost limit object shape.
- Enforce owner object shape.
- Enforce fail mode enum: `closed`, `open`.

Add note: semantic checks such as allowed/forbidden overlap and unresolved owner placeholders must be enforced by consuming runtime or test script.

---

## 7. Runtime documentation

File: `docs/agile-v-runtime/02_CONTROL_MATRIX.md`

Required sections:

1. Purpose
2. Placement
3. Relation to `POLICY.yaml`
4. Relation to `TRACE_LOG.md`
5. Relation to `EVAL_RESULTS.md`
6. Relation to `CHECKPOINTS.md`
7. Relation to `APPROVALS.md`
8. Field reference
9. Human Gate examples
10. Evidence bundle mapping
11. Consuming runtime requirements
12. Agentic repo integration example

Core wording:

```markdown
# Agile-V Control Matrix Runtime Contract

The control matrix is the operating control record for agentic execution. It answers: Which data may this agent process? Which tools may it call? Which model/vendor may it use? Where are logs stored? What are the maximum permissions? Which Human Gates are required? Which tests must pass? What is the cost limit? How can the change be rolled back? Who owns the risk?

`POLICY.yaml` is still used for low-level tool-class rules. `CONTROL_MATRIX.yaml` is the higher-level control map that binds task scope, skill use, data class, model, logs, rights, gates, tests, costs, rollback, and ownership.
```

---

## 8. Update `docs/agile-v-runtime/01_SCHEMAS.md`

Add `CONTROL_MATRIX.yaml` to the file placement table.

```markdown
| `CONTROL_MATRIX.yaml` | 2 | Operating control map: data class, tools, model/vendor, logs, rights, Human Gates, tests, costs, rollback, owners |
```

Add cross-reference:

```markdown
## 6. Control Matrix (`CONTROL_MATRIX.yaml`)

See `02_CONTROL_MATRIX.md`. The matrix is required for non-trivial agentic execution and should be checked before implementation, high-impact tool use, model/vendor changes, and release gates.
```

---

## 9. Update `agile-v-core/SKILL.md`

Add one directive after Policy + Trace:

```markdown
| 10 | Control Matrix | For non-trivial work, honor `.agile-v/CONTROL_MATRIX.yaml` when present. If absent, halt and propose creating it from `templates/agile-v/CONTROL_MATRIX.example.yaml`. Do not exceed data, tool, model, log, rights, cost, gate, rollback, or owner constraints. |
```

Update state persistence list to include:

```text
CONTROL_MATRIX.yaml
```

Update companion skills:

```markdown
Load on demand: `agile-v-control-matrix` for runtime control records and governance gates.
```

---

## 10. Update `compliance-auditor/SKILL.md`

Add duties:

- Check every active control entry has non-placeholder owners.
- Check every `L2+` evidence bundle references a control ID.
- Check that Human Gates have checkpoint and approval references.
- Check log retention is defined.
- Check rollback path exists for `L2+` when matrix requires it.
- Check cost limit is recorded for agentic execution.
- Include matrix status in VSR / audit output.

Suggested audit finding format:

```text
CM-001|CONTROL_MATRIX.yaml|PASS/FAIL/FLAG|field|description|evidence_ref
```

---

## 11. Update `red-team-verifier/SKILL.md`

Add verification checks:

- Verify Build Agent did not use forbidden tools.
- Verify claimed tests match evidence.
- Verify model/vendor was recorded when required.
- Verify rollback evidence exists.
- Verify no unresolved owner placeholders remain for active controls.
- Verify cost limit was not exceeded or has approval.
- Verify every Human Gate requirement has durable approval evidence.

Add failure taxonomy mapping:

| Condition | FT code | Severity |
|---|---|---|
| forbidden tool used | FT-POLICY | CRITICAL |
| missing control matrix | FT-POLICY | MAJOR for L2, CRITICAL for L3/L4 |
| missing owner | FT-POLICY | MAJOR |
| missing rollback | FT-PLAN | MAJOR or CRITICAL |
| self-approved L3/L4 | FT-POLICY | CRITICAL |
| cost limit exceeded without approval | FT-POLICY | MAJOR |

---

## 12. Update `documentation-agent/SKILL.md`

Add capability:

- Generate `docs/control-matrix.md` from `.agile-v/CONTROL_MATRIX.yaml`.
- Include control summary table.
- Include owner table.
- Include Human Gate table.
- Include tool allowlist and denylist.
- Include rollback and cost summary.
- Include review cycle and status.

Generated docs should not expose secrets. If a log location or owner field is sensitive, redact according to the matrix.

---

## 13. Update routing guide

File: `SKILL_ROUTING_GUIDE.md`

Add routing rules:

```markdown
| User intent | Load skills |
|---|---|
| Create a control matrix / Kontrollmatrix | `agile-v-core`, `agile-v-control-matrix`, `compliance-auditor` |
| Define allowed tools or model/vendor rules | `agile-v-control-matrix`, `logic-gatekeeper` |
| Review whether an agent may execute | `agile-v-control-matrix`, `red-team-verifier` |
| Prepare OpenHands / agentic runtime governance | `agile-v-core`, `agile-v-control-matrix`, `compliance-auditor` |
| Audit Human Gates or approvals | `agile-v-control-matrix`, `compliance-auditor`, `red-team-verifier` |
```

---

## 14. Update README

Add to Included Skills table:

```markdown
| agile-v-control-matrix | Governance | `agile-v-control-matrix/` | Defines data class, tool, model/vendor, log, rights, Human Gate, test, cost, rollback, and owner controls for agentic execution. |
```

Add to runtime governance section:

```markdown
- **Control Matrix** (`CONTROL_MATRIX.yaml` + templates): operating control map for agentic execution. Defines data classes, allowed tools, model/vendor, logs, max rights, Human Gates, required tests, cost limits, rollback, and owners.
```

Add quick usage:

```bash
mkdir -p .agile-v
cp templates/agile-v/CONTROL_MATRIX.example.yaml .agile-v/CONTROL_MATRIX.yaml
# Edit owner, vendor/model, data class, tool rules, cost limits, rollback, and gates before active use.
```

---

## 15. Test plan for the skills repo

### 15.1 Frontmatter test

File: `tests/test_skill_frontmatter.py`

Validate:

- every skill folder has `SKILL.md`
- every `SKILL.md` has YAML frontmatter
- new skill has `name: agile-v-control-matrix`
- new skill has `metadata.version`
- new skill has `sections_index`

### 15.2 Template schema test

File: `tests/test_control_matrix_template.py`

Validate:

- `templates/agile-v/CONTROL_MATRIX.example.yaml` parses as YAML
- `templates/agile-v/CONTROL_MATRIX.schema.json` parses as JSON
- example validates against schema
- all required top-level sections exist
- every active control has owner fields
- draft example may contain `TBD`, but active fixtures may not
- allowed and forbidden tools do not overlap
- every gated action has `gate` and `approver_role`

Example test skeleton:

```python
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def test_control_matrix_example_matches_schema():
    schema = json.loads((ROOT / "templates/agile-v/CONTROL_MATRIX.schema.json").read_text())
    data = yaml.safe_load((ROOT / "templates/agile-v/CONTROL_MATRIX.example.yaml").read_text())
    Draft202012Validator(schema).validate(data)


def test_no_allowed_forbidden_overlap():
    data = yaml.safe_load((ROOT / "templates/agile-v/CONTROL_MATRIX.example.yaml").read_text())
    for control in data["controls"]:
        allowed = set(control["tools"]["allowed"])
        forbidden = set(control["tools"]["forbidden"])
        assert not allowed.intersection(forbidden)
```

If the repo does not want `jsonschema` as a dependency, run this check in CI with `pip install pyyaml jsonschema`.

### 15.3 Documentation link test

Check that:

- README links to `agile-v-control-matrix/`
- README links to `templates/agile-v/CONTROL_MATRIX.example.yaml`
- `docs/agile-v-runtime/01_SCHEMAS.md` links to `02_CONTROL_MATRIX.md`
- `templates/agile-v/README.md` lists the matrix template

### 15.4 Agent behavior test cases

Add examples to docs or fixtures:

1. Missing matrix on L2 task -> halt.
2. Forbidden tool -> halt.
3. Shell execution requiring gate -> checkpoint required.
4. Unknown data class -> security owner gate.
5. Cost limit exceeded -> business owner gate.
6. L3 change with no rollback -> halt.
7. Active control with `TBD` owner -> fail.
8. Matrix present with allowed tool and approved gate -> proceed.

---

## 16. GitHub Actions

File: `.github/workflows/validate-control-matrix.yml`

```yaml
name: Validate Control Matrix Templates
on:
  pull_request:
  push:
    branches: [main]

jobs:
  validate-control-matrix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install --upgrade pip
      - run: pip install pyyaml jsonschema pytest
      - run: pytest tests/test_control_matrix_template.py tests/test_skill_frontmatter.py -q
```

---

## 17. Downstream contract for `Agile-V/agentic_agile_v`

The skills repo must make the downstream contract clear:

- The agentic repo consumes the skills.
- The matrix template and schema are published here.
- The agentic repo should copy or pin the skill in `.agents/skills/`.
- The agentic repo should place runtime matrix at `.agile-v/CONTROL_MATRIX.yaml` or `config/control_matrix.yaml`.
- The agentic repo should enforce via:
  - `agilev controls validate`
  - pre-tool-use hook
  - stop hook
  - evidence bundle validator
  - CI gates
- Skill instructions alone are not sufficient enforcement.

Add a compatibility section:

```markdown
## Compatibility

| Skills repo artifact | Consuming runtime responsibility |
|---|---|
| `agile-v-control-matrix/SKILL.md` | Load during governance, planning, verification, and audit tasks. |
| `CONTROL_MATRIX.example.yaml` | Copy into `.agile-v/CONTROL_MATRIX.yaml` and fill owners/model/vendor before active use. |
| `CONTROL_MATRIX.schema.json` | Validate in CLI and CI. |
| `02_CONTROL_MATRIX.md` | Runtime implementation reference. |
| Human Gate wording | Persist gates in `CHECKPOINTS.md` and `APPROVALS.md`. |
```

---

## 18. PR plan

### PR 1: Template and schema

Files:

- `templates/agile-v/CONTROL_MATRIX.example.yaml`
- `templates/agile-v/CONTROL_MATRIX.schema.json`
- `templates/agile-v/README.md`

Acceptance:

- example parses as YAML
- schema parses as JSON
- example validates against schema

### PR 2: New skill

Files:

- `agile-v-control-matrix/SKILL.md`
- `SKILL_ROUTING_GUIDE.md`
- `README.md`

Acceptance:

- skill has valid frontmatter
- routing guide includes control matrix cases
- README includes the skill

### PR 3: Runtime docs

Files:

- `docs/agile-v-runtime/02_CONTROL_MATRIX.md`
- `docs/agile-v-runtime/01_SCHEMAS.md`
- `docs/README.md`

Acceptance:

- docs explain placement, relation to existing runtime files, and downstream enforcement
- links are valid

### PR 4: Existing skill updates

Files:

- `agile-v-core/SKILL.md`
- `compliance-auditor/SKILL.md`
- `red-team-verifier/SKILL.md`
- `documentation-agent/SKILL.md`

Acceptance:

- core skill says to honor control matrix
- compliance auditor includes matrix audit
- red team verifier checks matrix conformance
- documentation agent can generate matrix docs

### PR 5: Tests and CI

Files:

- `tests/test_control_matrix_template.py`
- `tests/test_skill_frontmatter.py`
- `.github/workflows/validate-control-matrix.yml`

Acceptance:

- CI passes
- invalid fixture fails as expected
- no allowed/forbidden overlap

---

## 19. Acceptance criteria

The skills repo work is complete when:

- `agile-v-control-matrix/SKILL.md` exists.
- The new skill has valid frontmatter and clear halt conditions.
- `CONTROL_MATRIX.example.yaml` exists.
- `CONTROL_MATRIX.schema.json` exists.
- The example validates against the schema.
- Runtime docs explain placement and relation to `POLICY.yaml`, `TRACE_LOG.md`, `EVAL_RESULTS.md`, `CHECKPOINTS.md`, and `APPROVALS.md`.
- README lists the new skill.
- Routing guide maps governance/control requests to the new skill.
- `agile-v-core` references the matrix as a runtime control contract.
- `compliance-auditor` and `red-team-verifier` include matrix checks.
- Tests cover template validity and skill frontmatter.
- CI validates control matrix templates on PR.
- The downstream agentic repo can consume the template and schema without translation.

---

## 20. Developer commands

```bash
# validate YAML and schema with pytest
pip install pyyaml jsonschema pytest
pytest tests/test_control_matrix_template.py tests/test_skill_frontmatter.py -q

# inspect new skill
sed -n '1,120p' agile-v-control-matrix/SKILL.md

# copy template into a project runtime
mkdir -p .agile-v
cp templates/agile-v/CONTROL_MATRIX.example.yaml .agile-v/CONTROL_MATRIX.yaml
```

---

## 21. Important design rule

Do not make the skills repo responsible for blocking tool execution. The skills repo teaches agents how to behave and publishes templates. The consuming agentic runtime must enforce with hooks, validators, evidence gates, and CI. This separation prevents false security: an agent may ignore a skill, but it cannot bypass a fail-closed hook or CI gate without leaving evidence.
