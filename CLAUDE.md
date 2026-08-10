# Agile V for Claude Code

Agile V is a library of AgentSkills.io contracts for traceable, human-governed engineering. The individual `SKILL.md` files are authoritative; this guide only covers installation and shared operating rules.

## Install the Plugin

In Claude Code, add this repository as a marketplace and install its plugin:

```text
/plugin marketplace add Agile-V/agile_v_skills
/plugin install agile-v-skills@agile-v-skills
```

The plugin exposes the current stable skills and supported domain build skills. Skills whose frontmatter contains `metadata.status: draft` remain preview contracts and require local review.

## Choose a Profile

Load `agile-v-core` first, then use the smallest complete [installation profile](docs/INSTALL_PROFILES.md) appropriate to the work:

| Profile | Use |
|---|---|
| `core-minimal` | Requirements, review, and lifecycle guidance |
| `verified-build` | Baselined implementation, independent test design, and verification |
| `existing-repo` | Existing-code understanding, impact, regression, and diff evidence |
| `regulated` | Risk, controls, safety, security, intended-use validation, and release evidence |
| `business-preview` | Locally reviewed draft business and C-Suite contracts |

For implementation, also load the relevant domain build skill. Follow the [Golden Journey](docs/GOLDEN_JOURNEY.md) for the canonical evidence flow and use the [routing guide](SKILL_ROUTING_GUIDE.md) for stage-specific skills.

## Shared Rules

| Rule | Required behavior |
|---|---|
| Halt | Stop and ask on ambiguous or conflicting requirements, missing typed lineage, unknown material constraints, or unclear acceptance criteria. Do not guess. |
| Baseline | Persist and independently review requirements, obtain Human Gate 1 approval, and freeze the approved revision before synthesis. Chat text and drafts are not build input. |
| Trace | Record synthesis lineage as `ART-XXXX -> implements -> REQ-XXXX@revision` plus the baseline reference. Use the applicable typed lineage for tests, risks, findings, validation, and governance records. |
| Independence | The Build Agent does not verify its own work. Test design and `red-team-verifier` use the approved baseline and an appropriately independent context. |
| Verification | Record independent results in `.agile-v/VERIFICATION_SUMMARY.md`; failures require correction and re-verification. Verification asks whether the specified output was built correctly. |
| Validation | When risk and intended use require it, `validation-agent` separately records representative-use evidence in `VALIDATION_REPORT.md`. Verification is not intended-use validation. |
| Gates | Stop at Human Gates. Gate 1 authorizes the baseline; Gate 2 reviews verification, applicable validation, risk, rollback, and release evidence. Never deploy without explicit approval. |
| Decisions | Persist significant choices and rationale in the durable project records; files, not chat, are authoritative. |

## Verify

Ask Claude Code to load `agile-v-core`, then request an ambiguous implementation. Correct behavior is to classify risk, request missing context, and persist requirements before synthesis.

See [examples](EXAMPLES.md), [tutorials](docs/tutorials/README.md), and the [full documentation](README.md).

**License:** CC-BY-SA-4.0 | **Author:** Agile V™
