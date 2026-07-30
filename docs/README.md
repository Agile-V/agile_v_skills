# Agile V Skills -- Documentation Hub

> **Version**: 3.7.0
> **Date**: 2026-07-31
> **Classification**: Public
> **Status**: Current documentation; individual skills and profiles may be proposed or draft.

## Quick Navigation

### Runtime schemas (trace, eval, policy, checkpoints)


| Doc ID                                   | Title                       | Purpose                                                                     |
| ---------------------------------------- | --------------------------- | --------------------------------------------------------------------------- |
| [RUN-001](agile-v-runtime/01_SCHEMAS.md) | `.agile-v/` runtime schemas | Phase 1-2: TRACE_LOG, EVAL_RESULTS, POLICY.yaml, CHECKPOINTS, FT-* taxonomy |


### Compliance Documentation


| Doc ID                                                   | Title                                  | Purpose                                  |
| -------------------------------------------------------- | -------------------------------------- | ---------------------------------------- |
| [COMP-001](compliance/01_COMPLIANCE_POSTURE.md)          | Compliance Posture Overview            | Scope and limits per standard            |
| [COMP-002](compliance/02_ISO_9001_MATRIX.md)             | ISO 9001:2015 Compliance Matrix        | Clause status, evidence, gaps            |
| [COMP-003](compliance/03_ISO_13485_MATRIX.md)            | ISO 13485:2016 Compliance Matrix       | Medical device QMS clause status         |
| [COMP-004](compliance/04_AS9100D_MATRIX.md)              | AS9100D Compliance Matrix              | Aerospace QMS clause status              |
| [COMP-005](compliance/05_ISO_27001_MATRIX.md)            | ISO 27001:2022 Compliance Matrix       | Security controls status                 |
| [COMP-006](compliance/06_GXP_GAMP5_MATRIX.md)            | GxP / GAMP 5 Compliance Matrix         | Pharma/life sciences validation          |
| [COMP-007](compliance/07_GAP_ROADMAP.md)                 | Gap Analysis and Roadmap               | Prioritized actions toward certification |

### Standards Mappings

| Document | Title | Purpose |
| -------- | ----- | ------- |
| [Source Register](standards/SOURCE_REGISTER.md) | Public Standards Source Register | Source URLs, editions, status, and review boundaries |
| [AI Governance](standards/AI_GOVERNANCE_MAPPING.md) | AI Governance Mapping | AI governance evidence and Agile-V gate mapping |
| [Lifecycle](standards/SYSTEMS_SOFTWARE_LIFECYCLE_MAPPING.md) | Systems and Software Lifecycle Mapping | Lifecycle, requirements, test, and quality evidence mapping |
| [Safety](standards/SAFETY_ASSURANCE_PROFILES.md) | Safety Assurance Profiles | Sector safety profile and decision-point mapping |
| [EU AI Act](standards/EU_AI_ACT_APPLICABILITY.md) | EU AI Act Applicability Gate | Legal-review screening record and Gate 1 rule |


## Applicable Standards


| Standard     | Edition | Scope within Agile V                |
| ------------ | ------- | ----------------------------------- |
| ISO 9001     | 2015    | Design and development phase QMS    |
| ISO 13485    | 2016    | Medical device design controls only |
| AS9100       | Rev D   | Aerospace design and configuration  |
| ISO 27001    | 2022    | AI-augmented development security   |
| GxP / GAMP 5 | Current | Regulated CSV industries            |


## How to Read This Documentation

Each compliance matrix document contains:

1. **What Agile V covers** -- which skill(s) address each clause, with specific evidence
2. **What Agile V does NOT cover** -- honest gaps that require organizational action
3. **What you need to do** -- concrete steps to close each gap for your context

The [Gap Roadmap (COMP-007)](compliance/07_GAP_ROADMAP.md) consolidates all gaps into a prioritized action plan.

---

> This documentation describes the Agile V Skills Library v3.7.0. It is repository documentation, not a release or conformance record. Proposed/draft profiles are explicitly labeled and are not approved operational profiles until their accountable owner approves and baselines them.
> For the skills themselves, see the [repository README](../README.md).
