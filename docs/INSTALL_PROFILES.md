# Agile V Installation Profiles

> **Repository version:** 3.9.x
> **Status:** Profile definitions are documentation, not package manifests. Copy each listed skill directory into a skill-discovery directory supported by your agent.

Use the smallest profile that meets the work's risk and lifecycle needs. Add one domain build agent from `domains/` when implementation is in scope.

| Profile | Use when | Skill directories |
|---|---|---|
| `core-minimal` | Requirements, review, or lifecycle guidance without implementation | `agile-v-core`, `requirement-architect`, `logic-gatekeeper` |
| `verified-build` | Building from an approved baseline with independently designed tests and independent verification | `agile-v-core`, `requirement-architect`, `logic-gatekeeper`, `build-agent`, `test-designer`, `red-team-verifier`, `agile-v-quality-gates` |
| `existing-repo` | Changing an existing codebase with impact and regression evidence | `core-minimal` + `skills/system-understanding-agent`, `skills/impact-analysis-agent`, `skills/regression-selection-agent`, `skills/graph-traceability-agent`, `skills/diff-evidence-agent` + the build/verification skills from `verified-build` |
| `regulated` | L3/L4, safety-relevant, sensitive, regulated, or externally assured work | `verified-build` + `agile-v-compliance`, `agile-v-control-matrix`, `compliance-auditor`, `validation-agent`, `safety-engineer`, `threat-modeler`, `release-manager`, `observability-planner`; add preview `agile-v-aibom` and preview `agile-v-human-oversight` only under an approved local policy |
| `business-preview` | Evaluating unreleased business and executive-governance contracts | `agile-v-core`, `c-suite-foundation`, relevant `chief-*` orchestrators, relevant functional skills (`venture-strategist`, `rd-innovator`, `gtm-executor`, `business-operations`), optionally `c-suite-update` |
| `gxp-lean-csa` **[Draft]** | Lower-risk, configurable, or well-understood software where approved local procedures permit a lean risk-based approach | `agile-v-core`, `agile-v-gxp-qualification`, `agile-v-control-matrix`, `agile-v-compliance`, `requirement-architect`, `logic-gatekeeper`, `test-designer`, `red-team-verifier`, `validation-agent`, `compliance-auditor`, `release-manager` |
| `gxp-standard` **[Draft]** | Regulated computerized systems requiring explicit DQ/IQ/OQ/PQ packaging | `gxp-lean-csa` + system description, qualification plan, DQ report, IQ/IOQ protocol+report, OQ protocol+report, PQ/intended-use plan+protocol+report, qualification summary, supplier suitability assessment, requalification strategy |
| `gxp-high-assurance` **[Draft]** | L4, safety-relevant, high data-integrity risk, externally assured, or critical operational systems | `gxp-standard` + independent quality approval, stronger role separation, signed/integrity-protected records (in the consuming environment), recovery demonstration, witnessed/independently reviewed critical executions, supplier/service-continuity evidence, periodic review + requalification evidence, reference fault-injection/seeded-defect challenge where feasible |

`business-preview` and any individually marked preview skill are not stable operational contracts. Review and baseline their outputs locally before relying on them.

## Install

Choose a destination supported by your tool, for example `.claude/skills/`, `.cursor/skills/`, `.github/skills/`, `.agents/skills/`, or the corresponding user-level directory. From a checkout of this repository:

```bash
mkdir -p <skills-dir>
cp -R agile-v-core requirement-architect logic-gatekeeper <skills-dir>/
```

For a verified Python build, extend that installation:

```bash
cp -R build-agent test-designer red-team-verifier agile-v-quality-gates <skills-dir>/
cp -R domains/build-agent-python <skills-dir>/
```

Replace `build-agent-python` with `build-agent-js`, `build-agent-nestjs`, `build-agent-dart`, or `build-agent-embedded` as appropriate. For nested existing-repository skills, copy the individual directories from `skills/` into the destination.

## Verify Installation

Ask the agent to list or load `agile-v-core`, then request an ambiguous implementation. Correct behavior is to classify risk, request missing context, and persist requirements before synthesis. Skill discovery and invocation details are tool-specific; installation alone does not prove lifecycle conformance.

Proceed with the [Golden Journey](GOLDEN_JOURNEY.md) for the canonical end-to-end flow.
