# EU AI Act Applicability Gate

> **Status:** Informational screening aid; not legal advice
> **Checked:** 2026-07-30
> **Sources:** [SRC-EU-01 and SRC-EU-02](SOURCE_REGISTER.md)

## Boundary

Regulation (EU) 2024/1689 must be assessed from the current official text, amendments, implementing acts, guidance, harmonized-standard citations, and applicable transition dates. This screen does not determine legal status, conformity, product classification, or market access. A lawyer or other qualified EU regulatory reviewer must approve the conclusion for an EU-relevant system. ISO/IEC 42001, other standards, and Agile-V artifacts do not automatically create a presumption of EU conformity.

## Gate Rule

Run this screen before Gate 1 requirement approval when an AI-enabled system may have an EU nexus. An unresolved classification blocks Gate 1. A prohibited intended use or unresolved prohibited-practice screen halts the affected scope pending legal review. Re-run on intended-purpose, deployment geography, operator-role, model, capability, data, or product-law change.

## Required Applicability Record

```yaml
intended_purpose: ""
foreseeable_misuse: []
eu_nexus: ""
operator_roles: []
ai_system_determination: ""
prohibited_practice_screening: ""
high_risk_basis: ""
transparency_obligations: []
gpai_role: ""
sector_and_product_law: []
applicable_dates: []
reviewer: ""
source_versions: []
reclassification_triggers: []
```

## Agile-V Mapping

| Screening question | Agile-V record | Gate outcome |
|---|---|---|
| What is the intended purpose and foreseeable misuse? | `REQUIREMENTS.md`; `DECISION_LOG.md`; risk register | Gate 1 blocks if incomplete or internally inconsistent |
| Is there an EU nexus and what operator roles apply? | Applicability record; commercial/deployment record | Legal reviewer confirms scope or documents rationale |
| Is it an AI system; is a prohibited practice implicated? | Applicability record; capability and use-case evidence | Halt affected work if prohibited or unresolved |
| Could high-risk, transparency, GPAI, or sector/product rules apply? | Legal assessment; risk/impact assessment; source-version record | Scope required technical-file/conformity work or record inapplicability |
| What evidence and changes need control? | `AI_RUN_MANIFEST.yaml`; `CONTROL_MATRIX.yaml`; test/evaluation and revalidation evidence | Gate 2 cannot substitute for legal or conformity assessment approval |

## Evidence and Claim Controls

Keep the signed/legal-approved applicability conclusion, sources and access dates, assumptions, excluded uses, reviewer authority, and reclassification triggers with the release evidence. Any public EU-AI-Act, certification, conformity, or standards claim requires separate approved wording that records scheme or law, scope, issuer/authority where relevant, version, validity, exclusions, and evidence. Do not call a voluntary framework, management-system certificate, assessment, or Agile-V mapping an EU conformity assessment.
