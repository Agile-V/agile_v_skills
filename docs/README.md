# Agile V Skills Documentation Hub

> **Version:** 3.8.x
> **Updated:** 2026-08-10
> **Status:** Current repository documentation. A skill with `metadata.status: draft` is a preview even when present on `main`.

## Start Here

| Document | Purpose |
|---|---|
| [Installation Profiles](INSTALL_PROFILES.md) | Install `core-minimal`, `verified-build`, `existing-repo`, `regulated`, or `business-preview` |
| [Golden Journey](GOLDEN_JOURNEY.md) | Canonical risk-to-release lifecycle and evidence flow |
| [Skill Routing Guide](../SKILL_ROUTING_GUIDE.md) | Complete current skill catalog and intent routing |
| [Performance Measurement](../PERFORMANCE.md) | Reproducible size, token, runtime, and outcome methodology |

## Runtime Contracts

| Document | Purpose |
|---|---|
| [Schemas](agile-v-runtime/01_SCHEMAS.md) | Trace, eval, policy, failure taxonomy, and durable checkpoints |
| [Control Matrix](agile-v-runtime/02_CONTROL_MATRIX.md) | Operating controls for data, tools, models, rights, gates, tests, cost, and rollback |
| [Canonical Lifecycle](agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md) | Draft, independent findings, Gate 1, baseline, and typed lineage |
| [Risk Classification](agile-v-runtime/04_RISK_CLASSIFICATION.md) | `L0`-`L4` classification and minimum evidence |
| [Tool and Delegation](agile-v-runtime/05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md) | MCP/tool and A2A authorization, scope, side effects, and evidence |

## Verification and Validation

Independent verification asks whether specified outputs were built correctly and is performed by `red-team-verifier`. Its Gate 2 handoff is `.agile-v/VERIFICATION_SUMMARY.md`, supported by `VER-XXXX`, test logs, and `.agile-v/EVAL_RESULTS.md`.

Intended-use validation asks whether the right system was built for representative users and operational conditions. It is performed by `validation-agent` when required and produces `VALIDATION_PLAN.md`, `VALIDATION_PROTOCOL.md`, and `VALIDATION_REPORT.md`. Verification does not prove intended-use acceptance; validation does not close failed verification.

## Standards and Compliance

| Collection | Scope |
|---|---|
| [Compliance posture and matrices](compliance/) | ISO 9001, ISO 13485, AS9100D, ISO 27001, and GxP/GAMP 5 support and gaps |
| [Standards mappings](standards/) | Source register, lifecycle, AI governance, safety profiles, and EU AI Act screening |
| [AI influence traceability](ai-influence-traceability.md) | AI run provenance and evidence boundaries |

These materials support engineering and governance processes; they do not establish certification, regulatory approval, or organizational conformity. Proposed profiles and all draft skills require accountable local review and baselining before operational use.
