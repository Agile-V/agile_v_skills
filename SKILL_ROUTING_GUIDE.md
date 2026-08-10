# Agile V Skills: Routing Guide

> **Repository version:** 3.8.x
> **Catalog:** 45 skills currently present. **[Preview]** means the skill's current YAML frontmatter contains `metadata.status: draft`; presence on `main` does not make that contract stable.

Load `agile-v-core` first, then only the stage and risk-relevant skills. See [Installation Profiles](docs/INSTALL_PROFILES.md) and the [Golden Journey](docs/GOLDEN_JOURNEY.md).

## Complete Catalog

| Intent | Skill | Location | Status |
|---|---|---|---|
| Foundation, directives, context and lifecycle rules | `agile-v-core` | `agile-v-core/` | Current |
| Multi-agent waves and handoffs | `agile-v-pipeline` | `agile-v-pipeline/` | Current |
| Cycle 2+, change requests, archival | `agile-v-lifecycle` | `agile-v-lifecycle/` | Current |
| Risk, CAPA, approvals, security, revalidation | `agile-v-compliance` | `agile-v-compliance/` | Current |
| Runtime control matrix | `agile-v-control-matrix` | `agile-v-control-matrix/` | Current |
| Interface, test, data-type, and time-allocation checks | `agile-v-quality-gates` | `agile-v-quality-gates/` | Current |
| Coding anti-pattern prevention | `agile-v-behavioral` | `agile-v-behavioral/` | Current |
| AI run provenance and AI/ML-BOM | `agile-v-aibom` | `agile-v-aibom/` | **[Preview]** |
| User research to candidate requirements | `discovery-analyst` | `discovery-analyst/` | Current |
| Security/privacy threat analysis | `threat-modeler` | `threat-modeler/` | Current |
| UX, accessibility, interaction constraints | `ux-spec-author` | `ux-spec-author/` | Current |
| Formal requirements and baselines | `requirement-architect` | `requirement-architect/` | Current |
| Independent ambiguity/constraint findings | `logic-gatekeeper` | `logic-gatekeeper/` | Current |
| Language-agnostic implementation | `build-agent` | `build-agent/` | Current |
| Python implementation | `build-agent-python` | `domains/build-agent-python/` | Current |
| JavaScript/TypeScript/Web implementation | `build-agent-js` | `domains/build-agent-js/` | Current |
| NestJS implementation | `build-agent-nestjs` | `domains/build-agent-nestjs/` | Current |
| Dart/Flutter implementation | `build-agent-dart` | `domains/build-agent-dart/` | Current |
| Embedded C/C++ and firmware | `build-agent-embedded` | `domains/build-agent-embedded/` | Current |
| Hardware schematics, netlists, HDL | `schematic-generator` | `schematic-generator/` | Current |
| Independent test design from baseline | `test-designer` | `test-designer/` | Current |
| Independent execution and verification | `red-team-verifier` | `red-team-verifier/` | Current |
| Representative intended-use validation | `validation-agent` | `validation-agent/` | Current |
| Hazard analysis and safety assurance | `safety-engineer` | `safety-engineer/` | Current |
| Decision logs, traceability, audit evidence | `compliance-auditor` | `compliance-auditor/` | Current |
| Standards-based repository documentation | `documentation-agent` | `documentation-agent/` | Current |
| Backlog, sprint, and Product Owner work | `agile-v-product-owner` | `agile-v-product-owner/` | Current |
| Rollout, rollback, and deployment plan | `release-manager` | `release-manager/` | Current |
| Metrics, dashboards, alerts, SLOs | `observability-planner` | `observability-planner/` | Current |
| Existing-system Gate 0 overview | `system-understanding-agent` | `skills/system-understanding-agent/` | Current |
| Pre-change impact map | `impact-analysis-agent` | `skills/impact-analysis-agent/` | Current |
| Impact-based regression selection | `regression-selection-agent` | `skills/regression-selection-agent/` | Current |
| Requirement/component/test graph links | `graph-traceability-agent` | `skills/graph-traceability-agent/` | Current |
| Predicted-versus-actual diff evidence | `diff-evidence-agent` | `skills/diff-evidence-agent/` | Current |
| Business vision, model, portfolio | `venture-strategist` | `venture-strategist/` | **[Preview]** |
| R&D pipeline, radar, prototypes, IP | `rd-innovator` | `rd-innovator/` | **[Preview]** |
| Go-to-market, launch, growth | `gtm-executor` | `gtm-executor/` | **[Preview]** |
| Finance, OKRs, resources, vendors | `business-operations` | `business-operations/` | **[Preview]** |
| Shared C-Suite governance primitives | `c-suite-foundation` | `c-suite-foundation/` | **[Preview]** |
| CEO orchestration and strategic alignment | `chief-exec` | `chief-exec/` | **[Preview]** |
| CTO architecture governance | `chief-tech` | `chief-tech/` | **[Preview]** |
| CFO financial governance | `chief-finance` | `chief-finance/` | **[Preview]** |
| CHRO people governance | `chief-people` | `chief-people/` | **[Preview]** |
| COO operational governance | `chief-ops` | `chief-ops/` | **[Preview]** |
| Periodic executive briefing aggregation | `c-suite-update` | `c-suite-update/` | **[Preview]** |

## Key Routing Distinctions

| User asks for | Route | Boundary |
|---|---|---|
| “Check the requirements” | `logic-gatekeeper` | Records independent findings; never rewrites the draft or baseline |
| “Build this” | `build-agent` + one domain build skill | Requires Gate 1-approved, frozen baseline |
| “Design the tests” | `test-designer` | Reads the baseline, not implementation |
| “Verify it works as specified” | `red-team-verifier` | Produces `.agile-v/VERIFICATION_SUMMARY.md` and `VER-XXXX` evidence |
| “Validate it with users/in operations” | `validation-agent` | Produces intended-use validation plan/protocol/report after verification |
| “Run Eval Gate / prepare Gate 2” | `red-team-verifier` + `compliance-auditor` | `EVAL_RESULTS.md` status must be `PASS` or authorized `WAIVED`; link it from `VERIFICATION_SUMMARY.md` |
| “Assess hazards or unacceptable harm” | `safety-engineer` | Tailors safety methods and assurance; does not replace verification or validation |
| “Can the agent/tool execute?” | `agile-v-control-matrix` + `agile-v-compliance` | Check data, tool, model, rights, approval, rollback, and evidence controls |
| “Understand this existing repo/change impact” | `system-understanding-agent` then impact/regression skills | Complete Gate 0 before requirements and build |
| “Plan a release” | `release-manager` | Starts after Gate 2 approval; no autonomous production release |
| “Set strategy/govern the business” | relevant preview business/C-Suite skill | Preview contracts require local approval and baselining |

## Canonical Workflows

### New or Changed Feature

`agile-v-core -> risk classification -> requirement-architect (persist draft) -> logic-gatekeeper (independent findings) -> architect revision -> Human Gate 1 -> frozen baseline -> build-agent + test-designer (independent) -> red-team-verifier -> Eval Gate -> validation-agent when intended-use validation is required -> AI manifest/evidence bundle -> Human Gate 2 -> release-manager -> observability-planner`

Follow the evidence and stop conditions in the [Golden Journey](docs/GOLDEN_JOURNEY.md).

### Existing Repository

1. `system-understanding-agent` creates the Gate 0 system overview.
2. `impact-analysis-agent` predicts affected components, interfaces, risks, and tests.
3. `regression-selection-agent` selects existing regression coverage and flags gaps.
4. Continue the canonical feature flow through a persisted draft and Gate 1 baseline.
5. After implementation, `graph-traceability-agent` links requirements, components, changes, and tests.
6. `diff-evidence-agent` compares predicted and actual impact before independent verification and Gate 2.

### Regulated or Safety-Relevant Work

Use the `regulated` install profile. Classify `L0`-`L4`; add `threat-modeler`, `safety-engineer`, and `validation-agent` according to scope; maintain control, trace, approval, verification, applicable validation, release, and AI influence evidence. Skills and templates support an assurance process but do not establish certification or regulatory conformity.

### Business Preview

Load `c-suite-foundation` before a relevant `chief-*` skill. C-Suite skills govern and delegate; functional skills execute strategy, R&D, GTM, and operations. Use `c-suite-update` only to aggregate already controlled domain evidence. Do not treat preview outputs as approved decisions without accountable human review.

## Loading Rules

1. Load `agile-v-core` first.
2. Use the smallest applicable [installation profile](docs/INSTALL_PROFILES.md).
3. Preserve independence with separate fresh contexts; if one context is unavoidable, design tests before implementation.
4. Pass durable file references, not chat-only handoffs.
5. Requirement changes after Gate 1 require a change request, independent review, approval, and a new baseline.
6. Keep verification and intended-use validation evidence separate.
7. A skill's frontmatter status controls preview labeling; branch location does not override it.
