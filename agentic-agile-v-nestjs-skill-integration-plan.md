# Integration Plan: `agent_nestjs_skills` as a NestJS Skill for Agentic Agile-V

## 1. Objective

Integrate [`Kadajett/agent-nestjs-skills`](https://github.com/Kadajett/agent-nestjs-skills) into Agile-V as a **technology-specific Agentic Agile-V skill** for NestJS backend development.

The integration should treat `agent_nestjs_skills` as a concrete execution skill used by agents during SCOPE-V tasks.

It must **not** be merged into the generic Agile-V core lifecycle.

## 2. Positioning

The intended architecture is:

```text
Agile-V
└── Defines lifecycle, gates, traceability, audit evidence, and human approval.

Agentic Agile-V / SCOPE-V
└── Defines task-level agent execution:
    Specify → Constrain → Orchestrate → Prove → Evolve → Verify.

agent_nestjs_skills
└── Supplies NestJS-specific implementation constraints, review rules,
    evidence expectations, and best practices.
```

Recommended final positioning:

> `nestjs-best-practices` is a technology-specific Agentic Agile-V skill for NestJS backend development. Agile-V controls lifecycle, gates, traceability, and audit evidence; SCOPE-V controls task execution; this skill supplies NestJS-specific constraints, implementation guidance, verification checks, and evidence expectations.

---

## 3. Licence Compliance for Kadajett's Skill

The integration should preserve attribution and licence information for `Kadajett/agent-nestjs-skills`.

Recommended handling:

- preserve the upstream `SKILL.md`;
- preserve the upstream `README.md`;
- preserve the upstream `AGENTS.md`;
- preserve the original rule files under `upstream/rules/`;
- add a `NOTICE.md` identifying the upstream source;
- include the MIT licence text if the integrated package is redistributed;
- document that Agile-V / Agentic Agile-V wrapper files are integration additions.

Recommended `NOTICE.md`:

```markdown
# Notice

This skill integrates content from:

- Upstream repository: https://github.com/Kadajett/agent-nestjs-skills
- Upstream skill: NestJS Best Practices
- Author: Kadajett
- Declared licence: MIT

Agile-V / Agentic Agile-V wrapper files, SCOPE-V mappings, evidence templates,
traceability templates, review checklists, and registry metadata are integration
additions.
```

---

## 4. Target Repository Structure

Create the following structure inside the Agile-V / Agentic Agile-V skills repository:

```text
skills/
└── technology/
    └── nestjs-best-practices/
        ├── SKILL.md
        ├── AGENTS.md
        ├── agile-v.skill.yaml
        ├── scope-v-mapping.md
        ├── constraints.md
        ├── evidence.md
        ├── review-checklist.md
        ├── traceability-template.md
        ├── task-brief-template.md
        ├── NOTICE.md
        ├── LICENSE
        ├── upstream/
        │   ├── README.md
        │   ├── SKILL.md
        │   ├── AGENTS.md
        │   ├── metadata.json
        │   └── rules/
        └── tests/
            ├── validate-skill-metadata.test.ts
            ├── validate-scope-v-mapping.test.ts
            └── validate-evidence-gates.test.ts
```

## Design Rule

Use an **upstream mirror + Agile-V adapter** pattern.

```text
skills/technology/nestjs-best-practices/upstream/
```

contains the original imported content from `Kadajett/agent-nestjs-skills`.

The files directly under:

```text
skills/technology/nestjs-best-practices/
```

are Agile-V-specific adapter files.

This keeps the original skill reusable and makes future upstream synchronization easier.

---

## 5. Skill Activation Metadata

Create:

```text
skills/technology/nestjs-best-practices/agile-v.skill.yaml
```

Suggested content:

```yaml
id: technology.nestjs-best-practices
name: NestJS Best Practices
version: 1.1.0-agile-v.1

source:
  repository: Kadajett/agent-nestjs-skills
  upstream_version: "1.1.0"
  license: MIT

type: technology-skill

domain:
  - software
  - backend
  - typescript
  - nestjs

applies_when:
  package_json_dependencies:
    - "@nestjs/core"
    - "@nestjs/common"

  file_globs:
    - "src/**/*.module.ts"
    - "src/**/*.controller.ts"
    - "src/**/*.service.ts"
    - "src/**/*.guard.ts"
    - "src/**/*.interceptor.ts"
    - "src/**/*.filter.ts"
    - "src/**/*.dto.ts"
    - "src/**/*.entity.ts"

  task_keywords:
    - NestJS
    - controller
    - service
    - module
    - provider
    - dependency injection
    - guard
    - interceptor
    - DTO
    - pipe
    - TypeORM
    - Prisma
    - microservice

scope_v_phases:
  - Specify
  - Constrain
  - Orchestrate
  - Prove
  - Evolve
  - Verify

default_risk_level: R1

risk_escalation:
  R2:
    - public_api_change
    - database_migration
    - authentication_or_authorization_change
    - production_bug_fix
    - dependency_upgrade
    - performance_sensitive_change

  R3:
    - regulated_system
    - patient_or_medical_data
    - payment_or_financial_data
    - security_boundary_change
    - production_release_gate
    - audit_relevant_change

required_outputs:
  - task_brief
  - affected_files
  - implementation_plan
  - diff_summary
  - evidence_bundle
  - residual_risk_note
  - traceability_entries

human_gate:
  R0: optional
  R1: normal_code_review
  R2: mandatory_reviewer_approval
  R3: explicit_signoff_and_release_gate
```

---

## 6. Agile-V Wrapper Skill

Create:

```text
skills/technology/nestjs-best-practices/SKILL.md
```

Suggested content:

```markdown
---
name: nestjs-best-practices-agile-v
description: NestJS technology skill for Agentic Agile-V tasks. Use when writing, reviewing, refactoring, testing, or verifying NestJS backend code.
license: MIT
metadata:
  upstream: Kadajett/agent-nestjs-skills
  upstream_version: "1.1.0"
  agile_v_role: technology-skill
---

# NestJS Best Practices for Agentic Agile-V

Use this skill when an Agentic Agile-V task touches a NestJS backend.

This skill adapts the upstream NestJS best-practices rule pack into the Agile-V / SCOPE-V execution model.

## Role in Agentic Agile-V

- Agile-V controls lifecycle, gates, traceability, and audit evidence.
- SCOPE-V controls the task loop.
- This skill supplies NestJS-specific constraints, implementation rules, review checks, and evidence expectations.

## Apply During SCOPE-V

### Specify

Add NestJS-specific acceptance criteria:

- module boundaries are clear;
- public API behavior is explicit;
- DTO validation behavior is specified;
- authentication and authorization expectations are stated;
- database and migration behavior is defined.

### Constrain

Apply `constraints.md`.

### Orchestrate

Use upstream `AGENTS.md` and the rule files in `upstream/rules/`.

### Prove

Apply `evidence.md`.

### Verify

Apply `review-checklist.md`.

### Evolve

When a validated lesson emerges:

- add or update a rule in `upstream/rules/`;
- update Agile-V adapter constraints if required;
- regenerate the compiled agent document;
- record the change in the decision log.

## Upstream Source

The upstream skill is maintained in `upstream/`.

The original upstream `SKILL.md` and `AGENTS.md` remain available for direct agent use.
```

---

## 7. SCOPE-V Mapping

Create:

```text
skills/technology/nestjs-best-practices/scope-v-mapping.md
```

Suggested content:

```markdown
# SCOPE-V Mapping: NestJS Best Practices

## Specify

The agent must convert the user request into a task brief containing:

- objective;
- scope;
- non-goals;
- affected modules;
- affected APIs;
- affected database entities or migrations;
- authentication and authorization impact;
- expected behavior;
- error cases;
- acceptance criteria;
- required evidence;
- risk level.

## Constrain

The agent must apply these NestJS constraints:

- no unrelated files;
- no broad refactor during a bug fix;
- no public API change without approval;
- no new dependency without justification;
- no database schema change without migration evidence;
- no authentication or authorization change without explicit security review;
- no controller input without DTO validation;
- no service-to-service circular dependency;
- no duplicate providers across feature modules;
- no untested business-critical branch.

## Orchestrate

The agent must:

1. inspect the existing module structure;
2. summarize the current design;
3. identify affected controllers, services, modules, DTOs, repositories, guards, and tests;
4. propose a small implementation plan;
5. implement in small slices;
6. run relevant checks;
7. produce a diff summary and residual-risk note.

## Prove

The agent must provide evidence according to risk level:

| Risk Level | Required Evidence |
|---|---|
| R0 | Smoke check or manual run |
| R1 | Targeted tests, lint/typecheck, diff summary |
| R2 | Regression tests, CI result, static/security check, rollback plan |
| R3 | Traceable requirements, independent test design, explicit sign-off, audit artifact |

## Evolve

If the task reveals a reusable NestJS lesson:

- add or modify a rule;
- include incorrect and correct examples;
- update tags and impact;
- rebuild `AGENTS.md`;
- record the change in the decision log.

## Verify

A reviewer or verification agent must check:

- rule compliance;
- test evidence;
- acceptance criteria coverage;
- residual risks;
- traceability;
- rollback path where applicable.
```

---

## 8. NestJS Constraints

Create:

```text
skills/technology/nestjs-best-practices/constraints.md
```

Suggested content:

```markdown
# NestJS Constraints for Agentic Agile-V

## Architecture

- Organize by feature modules, not technical layers.
- Avoid circular dependencies.
- Extract shared logic into dedicated shared or core modules.
- Use events for decoupling when direct dependencies would create cycles.
- Keep services focused on a single responsibility.
- Use repository or data-access abstraction where business logic would otherwise depend directly on ORM details.

## Dependency Injection

- Prefer constructor injection.
- Do not use service locator patterns.
- Do not register the same provider in multiple modules unless intentional and documented.
- Use injection tokens for interface-like abstractions.
- Consider provider scope carefully; request-scoped providers require justification.

## API and DTOs

- Validate all external input through DTOs and pipes.
- Use explicit response DTOs or serialization rules.
- Do not expose internal entities directly unless explicitly accepted.
- Treat API versioning as mandatory for breaking public API changes.

## Security

- Use guards for authentication and authorization.
- Sanitize output where user-generated content can be returned.
- Apply rate limiting to sensitive or high-volume endpoints.
- Any auth, permission, token, session, or identity change escalates to at least R2.

## Database

- Database schema changes require migrations.
- Multi-step state changes require transaction analysis.
- Query changes must consider N+1 risks.
- Migration tasks require rollback or recovery notes.

## Testing

- Unit-test services with NestJS TestingModule where appropriate.
- API behavior changes require e2e or integration tests.
- External services must be mocked or isolated in tests.
- Bug fixes require a regression test that fails before the fix where feasible.

## DevOps

- Configuration must use ConfigModule or the project-approved equivalent.
- Logging must be structured for production diagnostics.
- Application shutdown behavior must be safe for production services.
```

---

## 9. Evidence Requirements

Create:

```text
skills/technology/nestjs-best-practices/evidence.md
```

Suggested content:

```markdown
# Evidence Requirements: NestJS Agentic Agile-V Skill

## R0: Exploratory

Typical tasks:

- prototype;
- local experiment;
- throwaway script;
- spike.

Required evidence:

- short result summary;
- no production credentials;
- no production code path changed.

## R1: Routine

Typical tasks:

- small refactor;
- documentation update;
- non-critical API polish;
- internal-only cleanup.

Required evidence:

- affected files;
- diff summary;
- targeted tests or explanation why not applicable;
- lint/typecheck result where available;
- residual-risk note.

## R2: Production

Typical tasks:

- feature change;
- bug fix;
- public API change;
- database migration;
- dependency update;
- auth-related behavior;
- performance-sensitive change.

Required evidence:

- task brief with requirement IDs;
- implementation plan;
- affected files;
- executed commands;
- test results;
- regression coverage;
- acceptance criteria to test mapping;
- security/static check where relevant;
- rollback or recovery path;
- reviewer decision.

## R3: High Assurance

Typical tasks:

- regulated system;
- medical, patient, payment, or security-critical behavior;
- production release gate;
- security boundary change.

Required evidence:

- all R2 evidence;
- independent verification agent review;
- traceability matrix;
- explicit human sign-off;
- audit artifact;
- release decision rationale.
```

---

## 10. Review Checklist

Create:

```text
skills/technology/nestjs-best-practices/review-checklist.md
```

Suggested content:

```markdown
# NestJS Review Checklist

## Task Control

- [ ] Task brief exists.
- [ ] Risk level is assigned.
- [ ] Scope and non-goals are clear.
- [ ] Affected modules and files are listed.
- [ ] Required evidence is present.

## Architecture

- [ ] Feature-module boundaries are preserved.
- [ ] No circular dependencies introduced.
- [ ] No duplicate providers introduced.
- [ ] Services remain focused.
- [ ] Shared logic is placed in an appropriate module.

## API Behavior

- [ ] Public API changes are explicit.
- [ ] DTOs validate external input.
- [ ] Error behavior is documented.
- [ ] Response serialization is intentional.
- [ ] Versioning is considered for breaking changes.

## Security

- [ ] Authentication behavior is unchanged or explicitly reviewed.
- [ ] Authorization behavior is unchanged or explicitly reviewed.
- [ ] Sensitive endpoints use guards.
- [ ] User-generated output is sanitized where needed.
- [ ] Rate limiting is considered for sensitive endpoints.

## Database

- [ ] Schema changes include migrations.
- [ ] Data changes include rollback or recovery notes.
- [ ] Transactions are used where consistency requires them.
- [ ] Query changes consider N+1 behavior.

## Testing and Evidence

- [ ] Unit tests cover changed business logic.
- [ ] E2E or integration tests cover changed API behavior.
- [ ] Regression test exists for bug fix where feasible.
- [ ] Lint/typecheck results are included.
- [ ] Residual risks are documented.

## Agile-V Verification

- [ ] Acceptance criteria map to evidence.
- [ ] Requirement IDs map to changed files and tests.
- [ ] Reviewer decision is recorded.
- [ ] Human gate is satisfied for R2/R3 tasks.
```

---

## 11. Task Brief Template

Create:

```text
skills/technology/nestjs-best-practices/task-brief-template.md
```

Suggested content:

```markdown
# NestJS Task Brief

## Task ID

REQ-NESTJS-____

## Objective

Describe the requested behavior or change.

## Scope

List files, modules, APIs, services, DTOs, entities, migrations, and tests.

## Non-Goals

List what must not be changed.

## Current Behavior

Describe current behavior, including logs or reproduction steps if this is a bug.

## Desired Behavior

Describe expected behavior.

## Affected Architecture

- Modules:
- Controllers:
- Services:
- Repositories:
- DTOs:
- Guards/interceptors/filters:
- Database entities/migrations:
- External integrations:

## Constraints

- Public API change allowed: yes/no
- New dependency allowed: yes/no
- Database migration allowed: yes/no
- Auth/security behavior affected: yes/no
- Broad refactor allowed: yes/no

## Acceptance Criteria

- AC1:
- AC2:
- AC3:

## Required Evidence

- Tests:
- Lint/typecheck:
- Security/static analysis:
- Migration proof:
- Rollback path:
- Reviewer approval:

## Risk Level

R0 / R1 / R2 / R3

## Human Gate

Required: yes/no

Approver:
```

---

## 12. Traceability Template

Create:

```text
skills/technology/nestjs-best-practices/traceability-template.md
```

Suggested content:

```markdown
# NestJS Traceability Matrix

| Requirement ID | Acceptance Criteria | Changed Files | Tests | Evidence | Reviewer Decision | Residual Risk |
|---|---|---|---|---|---|---|
| REQ-NESTJS-0001 | AC1, AC2 | `src/...` | `test/...` | command output / CI link | approved / rejected | none / listed |
```

---

## 13. Agent Work Order

Use the following work order for the integrating agent:

```markdown
# Agent Task: Integrate agent-nestjs-skills into Agentic Agile-V

## Objective

Integrate `Kadajett/agent-nestjs-skills` as a technology-specific Agentic Agile-V skill for NestJS backend work.

## Constraints

- Do not modify the Agile-V lifecycle core.
- Do not treat NestJS rules as generic Agile-V process rules.
- Preserve upstream content under `skills/technology/nestjs-best-practices/upstream/`.
- Add Agile-V adapter files at the skill root.
- Ensure SCOPE-V mapping, evidence gates, traceability, and review checklists are present.
- Preserve attribution and licence information for Kadajett's upstream skill.
- Add validation tests for metadata, evidence levels, and SCOPE-V phase coverage.

## Steps

1. Create `skills/technology/nestjs-best-practices/`.
2. Import upstream `README.md`, `SKILL.md`, `AGENTS.md`, `metadata.json`, and `rules/` into `upstream/`.
3. Create root-level `SKILL.md` as the Agile-V wrapper.
4. Create `agile-v.skill.yaml`.
5. Create `scope-v-mapping.md`.
6. Create `constraints.md`.
7. Create `evidence.md`.
8. Create `review-checklist.md`.
9. Create `task-brief-template.md`.
10. Create `traceability-template.md`.
11. Create `NOTICE.md`.
12. Include MIT licence text if redistributing the integrated package.
13. Add tests that validate:
    - required metadata exists;
    - all six SCOPE-V phases are mapped;
    - R0/R1/R2/R3 evidence levels exist;
    - R2 and R3 require human approval;
    - upstream version is recorded;
    - root `SKILL.md` links to upstream material;
    - upstream attribution is present.
14. Update the skills index or registry to include `technology.nestjs-best-practices`.
15. Run formatting, tests, and documentation checks.
16. Produce an evidence bundle for this integration.

## Acceptance Criteria

- The NestJS skill appears in the Agentic Agile-V skill registry.
- The skill activates for NestJS repositories.
- The skill maps to all SCOPE-V phases.
- The skill defines constraints, evidence, review checklist, task brief, and traceability template.
- R2/R3 tasks require evidence and human approval.
- Upstream source and version are preserved.
- Kadajett attribution and licence information are preserved.
- CI validates the skill metadata and required files.
- Documentation clearly states that this is a technology skill, not the Agile-V core process.
```

---

## 14. Integration Evidence Bundle Template

The integration PR should include the following evidence bundle:

```text
Integration Evidence Bundle

Task ID:
REQ-SKILL-NESTJS-0001

Changed files:
- skills/technology/nestjs-best-practices/SKILL.md
- skills/technology/nestjs-best-practices/agile-v.skill.yaml
- skills/technology/nestjs-best-practices/scope-v-mapping.md
- skills/technology/nestjs-best-practices/constraints.md
- skills/technology/nestjs-best-practices/evidence.md
- skills/technology/nestjs-best-practices/review-checklist.md
- skills/technology/nestjs-best-practices/task-brief-template.md
- skills/technology/nestjs-best-practices/traceability-template.md
- skills/technology/nestjs-best-practices/NOTICE.md
- skills/technology/nestjs-best-practices/LICENSE
- skills/technology/nestjs-best-practices/upstream/...

Checks:
- metadata validation: pass/fail
- markdown lint: pass/fail
- SCOPE-V phase coverage: pass/fail
- evidence level coverage: pass/fail
- attribution/licence check: pass/fail
- registry update: pass/fail

Traceability:
- REQ-SKILL-NESTJS-0001 → skill metadata → registry entry → tests
- REQ-SKILL-NESTJS-0002 → SCOPE-V mapping → scope-v-mapping.md → validation test
- REQ-SKILL-NESTJS-0003 → evidence gates → evidence.md → validation test
- REQ-SKILL-NESTJS-0004 → review process → review-checklist.md
- REQ-SKILL-NESTJS-0005 → task execution input → task-brief-template.md
- REQ-SKILL-NESTJS-0006 → upstream attribution → NOTICE.md / LICENSE

Residual risks:
- Upstream repository may evolve independently.
- Rule conflicts may appear with organization-specific NestJS standards.
- Evidence commands may need per-repository customization.
- Upstream repository may not include a standalone root LICENSE file; preserve declared MIT metadata and add licence text in the integrated package.

Rollback:
- Remove registry entry.
- Remove `skills/technology/nestjs-best-practices/`.
- Re-run skill registry tests.
```

---

## 15. Definition of Done

The integration is complete when the following conditions are met:

| Area | Done Condition |
|---|---|
| Skill location | NestJS skill exists under `skills/technology/nestjs-best-practices/`. |
| Upstream preservation | Original upstream material is stored under `upstream/`. |
| Agile-V adapter | Root `SKILL.md` explains its role in Agile-V and SCOPE-V. |
| SCOPE-V mapping | All six phases are explicitly covered. |
| Evidence model | R0/R1/R2/R3 evidence requirements are defined. |
| Human gates | R2 and R3 approval expectations are encoded. |
| Traceability | A template exists for requirement → code → test → evidence. |
| Review | NestJS-specific review checklist exists. |
| Registry | Skill is discoverable by the Agentic Agile-V skill loader. |
| Licence | Kadajett attribution and MIT licence information are preserved. |
| CI | Metadata, SCOPE-V coverage, evidence-level tests, and attribution checks pass. |
| Documentation | The skill is described as a technology skill, not as the Agile-V core process. |

---

## 16. Non-Goals

The integration must not:

- rewrite the Agile-V lifecycle;
- make NestJS rules mandatory for non-NestJS projects;
- flatten upstream rules into the core process;
- remove upstream attribution;
- bypass risk-based evidence requirements;
- allow R2/R3 tasks without explicit review gates;
- treat generated code as acceptable without evidence;
- imply that Kadajett endorses Agile-V unless explicitly approved.

---

## 17. Recommended Registry Entry

Add an entry similar to this to the Agentic Agile-V skill registry:

```yaml
- id: technology.nestjs-best-practices
  name: NestJS Best Practices
  path: skills/technology/nestjs-best-practices
  type: technology-skill
  applies_to:
    - nestjs
    - typescript
    - backend
  scope_v_phases:
    - Specify
    - Constrain
    - Orchestrate
    - Prove
    - Evolve
    - Verify
  default_risk_level: R1
  upstream:
    repository: Kadajett/agent-nestjs-skills
    version: "1.1.0"
    license: MIT
```

---

## 18. Final Summary

Integrating `agent_nestjs_skills` into Agentic Agile-V is sensible and strategically useful.

The correct integration model is:

```text
Agile-V = lifecycle and compliance backbone
Agentic Agile-V / SCOPE-V = task execution model
agent_nestjs_skills = NestJS-specific technology skill
```

The implementation should preserve the upstream skill, add an Agile-V adapter layer, map the skill to all SCOPE-V phases, define evidence requirements by risk level, make the skill discoverable through the Agentic Agile-V skill registry, and preserve Kadajett attribution and licence information.
