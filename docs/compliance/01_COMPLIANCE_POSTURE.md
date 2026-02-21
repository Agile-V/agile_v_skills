# Compliance Posture Overview

> **Document ID**: COMP-001
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [Next: ISO 9001 Matrix →](02_ISO_9001_MATRIX.md)

---

## 1. What This Document Is

This document provides an honest, auditable assessment of the Agile V Skills Library's compliance posture. It states clearly what the skills cover, what they do not cover, and what users must do themselves to achieve full certification against each claimed standard.

## 2. Compliance Claim

The Agile V Skills Library v1.3 claims:

```
compliance: "ISO 9001 / ISO 27001 Aligned (Design Phase); GxP-Aware"
```

This means:
- **ISO 9001 / ISO 27001 Aligned:** The skills structurally implement the intent of these standards for the design and development phase. They are not a certification -- they are a framework that, when used within an organization's QMS, supports compliance.
- **Design Phase:** The skills cover requirements, design, synthesis, verification, and acceptance. They do NOT cover production, manufacturing, distribution, or post-market surveillance.
- **GxP-Aware:** The skills include controls relevant to GxP (decision logging, traceability, human gates, CAPA, revalidation), but do not implement 21 CFR Part 11 electronic signatures or closed-system controls. These require organizational infrastructure.

## 3. What the Skills Cover

| Capability | Standard Clauses Addressed | Skill(s) |
|---|---|---|
| Requirements decomposition and traceability | ISO 9001 8.2, 8.5; ISO 13485 7.3.2, 7.5.3; AS9100D 8.5.2 | requirement-architect, build-agent, compliance-auditor |
| Independent verification (Red Team Protocol) | ISO 9001 8.3; ISO 13485 7.3.5; AS9100D 8.3.4 | test-designer, red-team-verifier |
| Human-in-the-loop approval gates | ISO 9001 5.1; ISO 13485 7.3.4; 21 CFR Part 11 (partial) | agile-v-core (Human Gates) |
| Decision logging with rationale | ISO 9001 7.5; Principle #9; GxP ALCOA+ | compliance-auditor |
| Automated Traceability Matrix | ISO 9001 8.5; ISO 13485 7.5.3; GxP | compliance-auditor |
| Change Request protocol | ISO 9001 8.3.5; ISO 13485 7.3.7; ISO 27001 A.8.32 | agile-v-core, requirement-architect, logic-gatekeeper |
| Risk register and assessment | ISO 9001 6.1; AS9100D 8.1.1 | agile-v-core |
| CAPA protocol | ISO 13485 8.5; ISO 9001 10.1-10.2 | agile-v-core, compliance-auditor |
| Document versioning and archival | ISO 9001 7.5; ISO 13485 4.2.4-4.2.5 | agile-v-core (Iteration Lifecycle) |
| Nonconformity disposition | ISO 9001 8.7; ISO 13485 8.3 | red-team-verifier |
| Quality metrics and KPIs | ISO 9001 9.1; AS9100D 9.1.1 | compliance-auditor |
| Secure coding practices | ISO 27001 A.8.28 | build-agent |
| LLM provider security controls | ISO 27001 A.5.23 | agile-v-core |
| Periodic review and revalidation | GxP / GAMP 5 | agile-v-core |
| Configuration management | ISO 27001 A.8.9; AS9100D 8.1.2 | agile-v-core (State Persistence) |
| Secure development lifecycle | ISO 27001 A.8.25-A.8.27 | agile-v-core (Pipeline), red-team-verifier |

## 4. What the Skills Do NOT Cover

These are organizational responsibilities that the skills cannot fulfill. Users must implement these independently.

| Gap | Why It's Out of Scope | Standards Affected |
|---|---|---|
| Production and manufacturing controls | Skills are a design-phase toolchain, not a production system | ISO 13485 7.5.1 |
| Electronic signatures (21 CFR Part 11) | Requires organizational PKI, signature infrastructure | 21 CFR Part 11, Annex 11 |
| Supplier/LLM provider audits | Skills document requirements; auditing is an organizational activity | AS9100D 8.4 |
| IQ/OQ/PQ for the AQMS platform | Validating the AI tooling is an organizational responsibility | ISO 13485 4.1.6, GxP |
| Customer feedback and satisfaction | Skills have no external customer interface | ISO 9001 5.1.2, ISO 13485 7.2 |
| Employee competency and training | Skills assume a competent operator | ISO 9001 7.1.2 |
| Physical infrastructure and environment | Skills run on user-provided infrastructure | ISO 9001 7.1.3 |
| Unique Device Identification (UDI) | Design artifacts are not manufactured devices | ISO 13485 7.5.8 |
| Design transfer to manufacturing | Skills end at acceptance, not production handoff | ISO 13485 7.3.8 |
| Management review of QMS effectiveness | Requires organizational management structures | ISO 9001 9.3 |
| Agent access control enforcement | Protocol-based separation (honor system); runtime enforcement is environment-specific | ISO 27001 A.8.3 |

## 5. Summary by Standard

| Standard | Skills Posture | Compliance Level | Details |
|---|---|---|---|
| ISO 9001:2015 | Aligned (Design Phase) | 3 Compliant, 9 Partial, 2 Non-Compliant | [COMP-002](02_ISO_9001_MATRIX.md) |
| ISO 13485:2016 | Partial (Design Controls) | 2 Compliant, 6 Partial, 6 Non-Compliant | [COMP-003](03_ISO_13485_MATRIX.md) |
| AS9100D | Partial (Design + CM) | 2 Compliant, 4 Partial, 2 Non-Compliant | [COMP-004](04_AS9100D_MATRIX.md) |
| ISO 27001:2022 | Aligned (Dev Controls) | 5 Compliant, 10 Partial, 2 Non-Compliant | [COMP-005](05_ISO_27001_MATRIX.md) |
| GxP / GAMP 5 | Aware | 3 Compliant, 3 Partial, 2 Non-Compliant | [COMP-006](06_GXP_GAMP5_MATRIX.md) |

For a consolidated gap-closing action plan, see [COMP-007: Gap Roadmap](07_GAP_ROADMAP.md).

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release with v1.3 audit findings |

[← Back to Documentation Hub](../README.md) | [Next: ISO 9001 Matrix →](02_ISO_9001_MATRIX.md)
