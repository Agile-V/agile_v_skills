# AI Governance Mapping

> **Status:** Informational public-scope mapping
> **Checked:** 2026-07-30
> **Sources:** [SRC-AI-01 to SRC-AI-08](SOURCE_REGISTER.md)

## Boundary

This is a planning and evidence crosswalk, not a reproduction of licensed ISO/IEC text, legal advice, an audit, or a certification determination. ISO/IEC 42001 can be used for organizational management-system certification, but Agile-V artifacts alone cannot establish, maintain, or claim that certification. NIST AI RMF, OWASP, and MITRE materials are voluntary evidence views, not certifications or proof of legal conformity. Review controlled/licensed text and engage qualified legal, privacy, security, and management-system reviewers.

## Public-Scope Mapping

| Source | Public-scope concern | Agile-V artifact / control | Gate or evidence |
|---|---|---|---|
| ISO/IEC 42001:2023 | AIMS policy, objectives, accountability, continual improvement | `CONTROL_MATRIX.yaml`; `RISK_REGISTER.md`; `DECISION_LOG.md`; `CAPA_LOG.md` | Human approval of policy/owners; management review remains organizational |
| ISO/IEC 23894:2023 | AI risk identification, treatment, monitoring | Linked AI/security/privacy risks; `REVALIDATION_LOG.md` | Risk acceptance before Gate 2; review after material model/runtime change |
| ISO/IEC 5338:2023 | AI lifecycle process selection and lifecycle evidence | `REQUIREMENTS.md`; `BUILD_MANIFEST.md`; `TEST_SPEC.md`; `VALIDATION_SUMMARY.md` | Gate 1 approves intended use and requirements; Gate 2 reviews independent evidence |
| ISO/IEC 42005:2025 | AI impact assessment | Impact assessment linked to stakeholders, intended purpose, harms, mitigations | Gate 1 blocks when assessment or accountable reviewer is unresolved |
| ISO/IEC 22989 / 23053 | Shared AI/ML terminology and concept boundaries | Glossary, system boundary, data/model/pipeline inventory | Architecture/requirements review; no taxonomy claim without source review |
| NIST AI RMF 1.0 / GenAI Profile | Govern, Map, Measure, Manage evidence view | Risk register, evaluation rubric/results, incidents, monitoring and CAPA links | Independent review of evaluation evidence; record framework version used |
| ISO/IEC 27001:2022 / 27701:2025 | Information-security and privacy management links | Data classification, provider registry, `CONTROL_MATRIX.yaml`, access/log evidence | Security/privacy owner approval; organization supplies ISMS/PIMS controls |
| OWASP / MITRE | Threat-to-test traceability | Threat model; abuse cases; `TEST_SPEC.md`; red-team findings | Red Team verifies mitigations; record source version and test result |

## Minimum AI Governance Record

| Record | Minimum content |
|---|---|
| Intended-purpose record | Users, use context, exclusions, foreseeable misuse, affected stakeholders |
| AI inventory | Model, provider, runtime, tools, data/context sources, versions, confidence and evidence locators |
| Impact/risk record | Harm, likelihood or classification, uncertainty, controls, owner, residual decision, review trigger |
| Evaluation record | Dataset/rubric version, acceptance threshold, results, limitations, independent verifier |
| Change record | Baseline diff, affected artifacts, revalidation scope, approver decision |

For AI-influenced work, use `AI_RUN_MANIFEST.yaml` and the evidence-bundle fragment described by `agile-v-aibom`. Do not store hidden chain-of-thought, secrets, or unredacted proprietary prompts.
