# Systems and Software Lifecycle Mapping

> **Status:** Informational public-scope mapping
> **Checked:** 2026-07-30
> **Sources:** [SRC-LC-01 to SRC-LC-05](SOURCE_REGISTER.md)

## Boundary

This crosswalk identifies useful lifecycle evidence only. It does not reproduce licensed text, select a required process, demonstrate conformance, or certify a project. Tailoring, contractual obligations, national adoptions, competence, supplier controls, and independent assurance require project-specific review of the applicable licensed standard.

## Lifecycle Mapping

| Source | Public-scope focus | Agile-V artifact / activity | Gate / evidence |
|---|---|---|---|
| ISO/IEC/IEEE 15288:2023 | Stakeholders through transition, operation, support, and retirement | Stakeholder needs and `REQUIREMENTS.md`; architecture decisions; lifecycle plan; change and operational feedback | Gate 1 approves needs/scope; lifecycle owner reviews transition and retirement responsibilities |
| ISO/IEC/IEEE 12207:2026 | Tailored software lifecycle processes and outcomes | Tailoring record; plans; build/configuration manifest; verification and maintenance/change records | Gate 1 approves tailoring; Gate 2 checks completed evidence and independent verification |
| ISO/IEC/IEEE 29148:2018 | Requirement quality and information items | `REQUIREMENTS.md`; acceptance criteria; trace matrix/ATM; ambiguity findings | Gate 1 blocks ambiguous, untraceable, or unapproved requirements |
| ISO/IEC 29119 family | Test policy, strategy, planning, design, data/environment, execution, incidents, closure | `TEST_SPEC.md`; test data/environment record; `EVAL_RESULTS.md`; defects/CAPA | Gate 2 requires pass/waiver plus independent Red Team evidence |
| ISO/IEC 25010:2023 | Product-quality characteristics expressed as measurable needs | Quality requirements and acceptance budgets; performance/security/usability tests | Gate 1 approves measurable quality targets; Gate 2 reviews outcomes and residual gaps |

## Agile-V Practical Flow

| Lifecycle need | Agile-V implementation |
|---|---|
| Define and validate intent | `requirement-architect`; `logic-gatekeeper`; Gate 1 approval |
| Design and implement under control | `BUILD_MANIFEST.md`; configuration identifiers; `DECISION_LOG.md`; `CONTROL_MATRIX.yaml` |
| Verify independently | `test-designer` creates tests; `red-team-verifier` reviews against requirements; no self-verification |
| Manage change and defects | Change request, `RISK_REGISTER.md`, `CAPA_LOG.md`, impacted-test and revalidation decision |
| Operate and retire | Project-owned operational monitoring, incident, support, retention, and retirement evidence; Agile-V does not supply these organizational controls |

Record the selected edition, tailoring decisions, exclusions, accountable owner, and evidence locations in the project plan. Do not represent this mapping as ISO/IEC certification or formal compliance assessment.
