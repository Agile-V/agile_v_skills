# Agile V™ Agent Skills Library

**Open Agent Skills for turning AI-assisted engineering into a reviewable chain from approved requirements to implementation, tests, independent verification, and human release decisions.**

[![Standard: Agile V™](https://img.shields.io/badge/Standard-Agile--V™-blueviolet)](https://agile-v.org/)
[![Spec: AgentSkills.io](https://img.shields.io/badge/Spec-AgentSkills.io-green)](https://agentskills.io/specification)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey)](LICENSE)
[![Version](https://img.shields.io/github/v/release/Agile-V/agile_v_skills?label=version)](https://github.com/Agile-V/agile_v_skills/releases)
[![Validate Skills and Contracts](https://github.com/Agile-V/agile_v_skills/actions/workflows/validate-control-matrix.yml/badge.svg)](https://github.com/Agile-V/agile_v_skills/actions/workflows/validate-control-matrix.yml)
[![Stars](https://img.shields.io/github/stars/Agile-V/agile_v_skills?style=social)](https://github.com/Agile-V/agile_v_skills/stargazers)

[![ISO 9001 Aligned](https://img.shields.io/badge/ISO_9001-Aligned-blue)](docs/compliance/02_ISO_9001_MATRIX.md)
[![ISO 27001 Aligned](https://img.shields.io/badge/ISO_27001-Aligned-blue)](docs/compliance/05_ISO_27001_MATRIX.md)
[![GxP Aware](https://img.shields.io/badge/GxP-Aware-blue)](docs/compliance/06_GXP_GAMP5_MATRIX.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-orange)](CLAUDE.md)
[![Cursor](https://img.shields.io/badge/Cursor-Rules-orange)](CURSOR.md)

Agile V is a tool-agnostic, human-governed assurance layer for AI-assisted engineering. It gives agents explicit roles, durable evidence, typed traceability, independent challenge, risk-scaled controls, and stop points where accountable people approve requirements and release.

It does not replace your coding agent, engineering process, or judgment. It makes their inputs, outputs, checks, and decisions easier to inspect.

| Without an assurance layer | With Agile V |
|---|---|
| Chat context becomes implicit build input | A reviewed requirement revision becomes the frozen baseline |
| Tests may mirror implementation assumptions | Test design is derived independently from requirements |
| The builder grades its own output | A separate verifier challenges specified behavior |
| Approval is implied by agent completion | Human Gates record authority, evidence, and residual risk |
| Traceability is reconstructed later | Typed links connect requirements, artifacts, tests, and evidence |
| Tool access follows runtime defaults | Risk-scaled controls bound data, tools, permissions, and side effects |

## Start in 60 Seconds

Install the minimal requirements profile into a project-level Agent Skills directory:

```bash
git clone https://github.com/Agile-V/agile_v_skills.git
mkdir -p .agents/skills
cp -R agile_v_skills/agile-v-core \
  agile_v_skills/requirement-architect \
  agile_v_skills/logic-gatekeeper \
  .agents/skills/
```

Ask your agent:

```text
Load agile-v-core. Classify the risk of this change, identify missing context,
and create reviewable requirements before implementation: [describe change]
```

Correct behavior includes halting on material ambiguity, persisting requirements, and waiting for approval before treating a revision as the build baseline. For implementation, select a complete [installation profile](docs/INSTALL_PROFILES.md), then follow the [Golden Journey](docs/GOLDEN_JOURNEY.md).

## Who It Is For

**Use Agile V when:**

- AI-assisted changes need reviewable requirements and explicit acceptance criteria.
- Implementation should be challenged independently rather than self-graded.
- Security, safety, regulatory, contractual, or operational risk requires durable evidence.
- Multiple agents or sessions need a stable baseline and reproducible handoffs.
- Humans must authorize requirements, waivers, residual risk, or release.

**It is not:**

- A certification, conformity assessment, legal opinion, or regulatory approval product.
- A substitute for domain experts, accountable engineering judgment, or organizational controls.
- A reason to add heavy process to every prototype or low-consequence experiment.
- An autonomous deployment system or a guarantee that an AI-generated result is correct.

Choose the smallest profile appropriate to the risk.

## Repository Evidence

| Proof point | Inspect it |
|---|---|
| **45 skills** | Machine-readable [`catalog/skills.json`](catalog/skills.json) and the [Skill Routing Guide](SKILL_ROUTING_GUIDE.md) |
| **347 contract tests** | Deterministic schema and repository tests under [`tests/`](tests/) |
| **18 evidence schemas** | Requirements, risk, builds, tests, verification, validation, approvals, traceability, controls, delegation, and AI provenance in [`schemas/`](schemas/) |
| **Five build domains** | [Python](domains/build-agent-python/SKILL.md), [JavaScript/TypeScript](domains/build-agent-js/SKILL.md), [NestJS](domains/build-agent-nestjs/SKILL.md), [Dart/Flutter](domains/build-agent-dart/SKILL.md), and [embedded C/C++](domains/build-agent-embedded/SKILL.md) |
| **Public runtime contracts** | [Lifecycle](docs/agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md), [risk classification](docs/agile-v-runtime/04_RISK_CLASSIFICATION.md), and [tool/delegation controls](docs/agile-v-runtime/05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md) |
| **Reproducible claims policy** | Measurement inputs and methods are defined in [`PERFORMANCE.md`](PERFORMANCE.md) |

The repository is currently on the **v3.9.x** line. [`package.json`](package.json) is the repository-version source; each skill also carries its own contract version in YAML frontmatter.

### Assurance Controls

| Control | Practical effect |
|---|---|
| Halt and ask | Agents stop rather than inventing missing material requirements or constraints |
| Immutable baseline | Build and test roles consume the same approved revision |
| Independent contexts | Test design and verification avoid implementation-led confirmation bias |
| Human Gates | Accountable people approve requirements, exceptions, residual risk, and release |
| Risk scaling | Delivery levels `L0`-`L4` select proportionate review and evidence |
| Decision logging | Significant choices retain rationale, alternatives, owner, and evidence links |
| Typed traceability | Records use appropriate lineage instead of forcing every item under one REQ link |
| Machine validation | JSON Schemas catch malformed structured evidence before release review |
| AI provenance | Material AI influence is recorded without secrets or hidden chain-of-thought |

These are contracts and records, not proof by themselves. Teams must operate the controls, review the resulting evidence, and resolve failures.

## Canonical Workflow

```text
Intent
  -> risk classification
  -> persisted draft requirements
  -> independent ambiguity and constraint findings
  -> revision and Human Gate 1 approval
  -> frozen requirement baseline
  -> implementation + independent test design
  -> independent verification + Eval Gate
  -> intended-use validation when required
  -> evidence bundle + Human Gate 2
  -> release and monitoring
```

| Stage | Role and boundary | Evidence |
|---|---|---|
| Requirements | `requirement-architect` persists and revises; `logic-gatekeeper` records findings but does not rewrite the draft | Approved `REQ-XXXX` revisions and baseline registration |
| Build | `build-agent` and one domain skill implement only from the frozen baseline | `ART-XXXX -> implements -> REQ-XXXX` lineage |
| Test design | `test-designer` derives tests from the baseline, not from implementation | `TC-XXXX -> verifies -> REQ-XXXX` lineage |
| Verification | `red-team-verifier` independently asks **“Was the specified output built correctly?”** | `.agile-v/VERIFICATION_SUMMARY.md`, test logs, `VER-XXXX`, and eval results |
| Intended-use validation | `validation-agent`, when required, separately asks **“Was the right system built for representative users and conditions?”** | `VALIDATION_PLAN.md`, `VALIDATION_PROTOCOL.md`, and `VALIDATION_REPORT.md` |
| Release | An authorized human reviews evidence and residual risk before `release-manager` proceeds | Gate 2 approval, release and rollback evidence |

Verification does not prove intended-use acceptance. Intended-use validation does not close failed verification. Keep their roles and records separate. See the [canonical lifecycle contract](docs/agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md) for states, lineage, and stop conditions.

When separate agents are unavailable, design tests before implementation and use a fresh context for verification to reduce contamination. Never let the Build Agent verify its own work.

## Installation Profiles

| Profile | Use when |
|---|---|
| `core-minimal` | Requirements, independent review, and lifecycle guidance |
| `verified-build` | Baselined implementation, independent test design, and verification |
| `existing-repo` | Gate 0 understanding, impact analysis, regression selection, and diff evidence |
| `regulated` | L3/L4, safety-relevant, sensitive, regulated, or externally assured work |
| `business-preview` | Locally evaluating draft business and executive-governance contracts |

The [Installation Profiles](docs/INSTALL_PROFILES.md) document lists exact skill directories and copy commands. Add one implementation domain when building. Agent Skills may be installed at project or user level, depending on the platform.

## Platforms

| Platform | Typical project directory | Guide |
|---|---|---|
| Claude Code | `.claude/skills/` | [Repository guide](CLAUDE.md) · [Official docs](https://code.claude.com/docs/en/skills) |
| Cursor | `.cursor/skills/` | [Repository guide](CURSOR.md) · [Official docs](https://cursor.com/docs/context/skills) |
| VS Code | `.github/skills/` or `.agents/skills/` | [Official docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |
| GitHub Copilot | `.github/skills/` or `.agents/skills/` | [Official docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Other compatible agents | Platform-specific skills directory | [AgentSkills.io integration guide](https://agentskills.io/integrate-skills) |

For detailed scenarios and retained platform examples, see [`EXAMPLES.md`](EXAMPLES.md), [`CLAUDE.md`](CLAUDE.md), and [`CURSOR.md`](CURSOR.md).

## Skill Catalog

Load `agile-v-core` first, then only the roles needed for the stage and risk.

| Category | Scope | Start here |
|---|---|---|
| Foundation and orchestration | Core directives, pipelines, lifecycle, quality gates, behavioral rules | [`agile-v-core`](agile-v-core/SKILL.md) |
| Discovery and requirements | Research, threats, UX constraints, formal requirements, independent findings | [`requirement-architect`](requirement-architect/SKILL.md) |
| Build and test | Language-agnostic build, five domains, hardware, independent test design | [`build-agent`](build-agent/SKILL.md) |
| Assurance | Independent verification, intended-use validation, safety, compliance | [`red-team-verifier`](red-team-verifier/SKILL.md) |
| Delivery and operations | Product ownership, release, observability | [`release-manager`](release-manager/SKILL.md) |
| Existing repositories | System understanding, impact, regression, graph, and diff evidence | [`skills/`](skills/) |
| Business and C-Suite | Functional business execution and executive orchestration | [Preview catalog](SKILL_ROUTING_GUIDE.md#business-preview) |

Use the [complete routing guide](SKILL_ROUTING_GUIDE.md) for all 45 skills, prerequisites, status, and intent-to-skill mappings. The machine-readable source is [`catalog/skills.json`](catalog/skills.json).

## Preview Boundary

A skill is preview/draft only when its current frontmatter contains `metadata.status: draft`. Presence on `main` does not make its contract stable.

Current preview contracts are:

- AI influence workflow: `agile-v-aibom`.
- Functional Business Track: `venture-strategist`, `rd-innovator`, `gtm-executor`, `business-operations`.
- C-Suite: `c-suite-foundation`, `chief-exec`, `chief-tech`, `chief-finance`, `chief-people`, `chief-ops`, `c-suite-update`.

Review, tailor, approve, and baseline preview outputs locally before operational use. C-Suite skills govern and coordinate; functional skills execute. Current status is maintained in the [routing guide](SKILL_ROUTING_GUIDE.md).

## Standards and Compliance

Agile V provides engineering controls, evidence structures, and public-scope mappings. These materials may support an organization’s assurance work, but **do not establish certification, regulatory approval, legal compliance, product safety, or organizational conformity**. Applicability, tailoring, validation, qualified personnel, and accountable approval remain your responsibility.

| Resource | Scope |
|---|---|
| [Compliance posture](docs/compliance/01_COMPLIANCE_POSTURE.md) | Coverage, boundaries, assumptions, and gaps |
| [Compliance matrices](docs/compliance/) | ISO 9001, ISO 13485, AS9100D, ISO 27001, and GxP/GAMP 5 |
| [Standards mappings](docs/standards/) | Lifecycle, AI governance, safety profiles, source register, and EU AI Act screening |
| [Runtime schemas](docs/agile-v-runtime/01_SCHEMAS.md) | Machine-readable evidence contracts and validation model |
| [Control matrix](docs/agile-v-runtime/02_CONTROL_MATRIX.md) | Data, tool, model, rights, gate, test, cost, and rollback controls |
| [AI influence traceability](docs/ai-influence-traceability.md) | Model, runtime, context, tool, skill, artifact, and revalidation provenance |

Sector terms such as ASIL, SIL, DAL, GxP, and regulatory risk categories are not interchangeable with Agile V delivery levels `L0`-`L4`. Use the [risk classification contract](docs/agile-v-runtime/04_RISK_CLASSIFICATION.md) and an applicable sector profile.

## Learn and Compare

| Resource | What it provides |
|---|---|
| [Tutorials](docs/tutorials/README.md) | Verified authentication, independent-agent verification, AI manifests, and regulated adoption |
| [Golden Journey](docs/GOLDEN_JOURNEY.md) | Canonical end-to-end onboarding and evidence flow |
| [Comparisons](docs/COMPARISONS.md) | Bounded comparisons with adjacent methods and tools |
| [Examples](EXAMPLES.md) | Concrete usage scenarios |
| [Documentation hub](docs/README.md) | Runtime, standards, compliance, and integration documentation |
| [Showcase](docs/SHOWCASE.md) | Evidence-based case-study requirements and submission format |

## Repository Structure

```text
agile-v-core/                 foundation skill; load first
agile-v-*/                    lifecycle, governance, and quality skills
requirement-architect/        formal requirements and baselines
build-agent/                  language-agnostic implementation contract
domains/                      five language/platform build skills
test-designer/                independent baseline-derived test design
red-team-verifier/            independent verification
validation-agent/             separate intended-use validation
skills/                       existing-repository evidence agents
catalog/                      machine-readable skill catalog
schemas/                      18 JSON evidence schemas
templates/                    reusable project evidence records
tests/                        deterministic contract tests and fixtures
docs/                         tutorials, runtime, standards, and compliance
```

Each skill lives in one directory with one `SKILL.md` using the [AgentSkills.io specification](https://agentskills.io/specification). Projects normally persist lifecycle evidence under `.agile-v/`; copy and tailor records from [`templates/agile-v/`](templates/agile-v/) rather than editing library templates in place.

## Troubleshooting

If skills do not load or the agent starts coding without requirements:

1. Confirm the selected directory is supported by your platform and contains `<skill-name>/SKILL.md`.
2. Restart or reload the agent after installing skills.
3. Ask the agent to list or explicitly load `agile-v-core`.
4. Verify that you copied a complete [installation profile](docs/INSTALL_PROFILES.md), not isolated files.
5. Test with an ambiguous request; expected behavior is to classify risk and ask for missing context before synthesis.

See the platform guides for [Claude Code](CLAUDE.md) and [Cursor](CURSOR.md), the [examples](EXAMPLES.md), or [open an issue](https://github.com/Agile-V/agile_v_skills/issues) with the platform, install path, skill names, and observed behavior.

## Community and Contributions

[GitHub Discussions](https://github.com/Agile-V/agile_v_skills/discussions) is the community forum. Use [Issues](https://github.com/Agile-V/agile_v_skills/issues) for reproducible defects and focused proposals, and follow the [Showcase guide](docs/SHOWCASE.md) for case studies.

Contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md), [`AGENTS.md`](AGENTS.md), the [Code of Conduct](CODE_OF_CONDUCT.md), and the [Security Policy](SECURITY.md) before submitting a pull request. New or changed skills must preserve traceability, halt-on-ambiguity behavior, independent verification, human gates, decision rationale, valid frontmatter, and applicable attribution.

## License and Attribution

The Agile V™ Agent Skills Library is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](LICENSE). Contributions are accepted under the same license.

Selected context-engineering patterns are adapted from [Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done) by Lex Christopherson under the [MIT License](https://github.com/gsd-build/get-shit-done/blob/main/LICENSE). Skill-level adaptations and source details are recorded in YAML `metadata.adapted_from` fields and the [standards source register](docs/standards/SOURCE_REGISTER.md).

Agile V™ is maintained by [agile-v.org](https://agile-v.org/).
