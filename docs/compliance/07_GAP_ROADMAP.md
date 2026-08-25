# Gap Analysis and Roadmap to Full Compliance

> **Document ID**: COMP-007
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [← Previous: GxP / GAMP 5 Matrix](06_GXP_GAMP5_MATRIX.md)

---

## 1. Purpose

This document consolidates all compliance gaps from the per-standard matrices (COMP-002 through COMP-006) into a single prioritized roadmap. Each gap includes what it is, why it matters, which standards require it, and concrete steps to close it.

> **Non-certification statement:** This Agile V profile supports structured qualification and validation evidence. It does not determine legal applicability, replace controlled procedures, provide technical Part 11 controls, or establish regulatory compliance.

> **Scope note:** Qualification splits into two independent scopes — **target-system qualification** (the regulated product built with Agile V) and **assurance-toolchain qualification** (the Agile V skills + runtime + model configuration). DQ/IQ/OQ/PQ apply to each scope separately. A skill or JSON schema is at most a **NORMATIVE CONTRACT** or **SCHEMA-BACKED** artifact — not proof of operational compliance or certification.

## 2. Gap Priority Levels

| Priority | Definition | Action Timeline |
|----------|-----------|----------------|
| **P1 -- Blocking** | Prevents certification or regulatory submission. Must be addressed before claiming compliance. | Before first regulated release |
| **P2 -- Significant** | Weakens compliance posture materially. Auditors will flag as a major finding. | Within first 2 cycles |
| **P3 -- Enhancement** | Strengthens compliance but absence is unlikely to block certification. Minor finding risk. | Within 6 months |
| **P4 -- Advisory** | Best practice. Improves maturity but not strictly required. | When capacity allows |

---

## 3. Consolidated Gap Register

### P1 -- Blocking Gaps

#### GAP-001: Electronic Signatures for Human Gates
| Attribute | Detail |
|-----------|--------|
| **Standards** | 21 CFR Part 11, Annex 11, ISO 13485 4.2.5 |
| **Current State** | APPROVALS.md captures name, role, timestamp, and signature method. No actual e-signature mechanism. |
| **Risk** | **External-control gap (preserved):** skills cannot provide authenticated identity, non-repudiable e-signatures, or secure audit-trail infrastructure by themselves. Gate approvals are non-repudiable only if signature infrastructure exists. Without it, any GxP submission is indefensible. |
| **Action Required** | 1. Implement PKI or digital signature infrastructure (GPG, organizational PKI, or qualified e-signature service). 2. Mandate `git commit -S` for all Gate approval commits. 3. Create a Signature Meaning Table (e.g., "Approved for release," "Reviewed," "Authored"). 4. Bind each GATE-XXXX record to a signed commit hash. 5. Verify signatures in the Compliance Auditor cycle boundary audit. |
| **Owner** | IT / Quality / DevOps |
| **Verification** | Attempt to forge a Gate approval; verify it is detected by signature verification. |

#### GAP-002: IQ/OQ/PQ for the AQMS Platform
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 13485 4.1.6, GxP / GAMP 5 |
| **Current State** | **Partially addressed (SCHEMA-BACKED, draft).** `agile-v-gxp-qualification` establishes DQ/IQ/OQ/PQ as **evidence stages** (not agent names) with schema-backed contracts: `QUALIFICATION_PLAN`, `SYSTEM_DESCRIPTION`, `SYSTEM_BASELINE`, `QUALIFICATION_PROTOCOL`, `QUALIFICATION_EXECUTION`, `QUALIFICATION_DEVIATION`, `QUALIFICATION_SUMMARY`, `REQUALIFICATION_ASSESSMENT`. IQ/configuration execution evidence is the remaining gap. |
| **Scope note** | Distinguish **target-system** qualification from **assurance-toolchain** qualification (Agile V skills + runtime + model config). Qualify each scope separately. |
| **Risk** | Regulators can challenge whether the AI tooling itself is a validated system if IQ/configuration evidence is not captured and baselined. |
| **Action Required** | 1. Instantiate `QUALIFICATION_PLAN` (scope, approach, acceptance criteria) for the chosen scope. 2. **IQ (proposed solution):** capture installation/configuration evidence via `SYSTEM_BASELINE` (installed skill/schema versions, model config, runtime identity) plus an IQ `QUALIFICATION_PROTOCOL` → `QUALIFICATION_EXECUTION` confirming components are installed, version-matched, and configured as specified. 3. OQ: design tests (test-designer) and execute/challenge (red-team-verifier). 4. PQ: intended-use validation via `validation-agent`. 5. Record `QUALIFICATION_SUMMARY` (compliance-auditor). 6. Trigger `REQUALIFICATION_ASSESSMENT` per the Periodic Review schedule. Draft contracts require local baselining. |
| **Owner** | Quality / Engineering |
| **Verification** | Present QUALIFICATION_SUMMARY to auditor; demonstrate REQUALIFICATION_ASSESSMENT trigger when model changes. |

#### GAP-003: LLM Provider Supplier Qualification
| Attribute | Detail |
|-----------|--------|
| **Standards** | AS9100D 8.4, ISO 13485 7.4 (if applicable) |
| **Current State** | `config.json` documents provider attributes. Supplier-suitability expectations are now expressed as a **NORMATIVE CONTRACT** (draft) in `agile-v-gxp-qualification`; evaluation/selection/monitoring remain external activities. |
| **Risk** | LLM providers process requirements and code. An unqualified provider is a supply chain risk. |
| **Action Required** | 1. Define supplier evaluation criteria (data handling, SOC 2/ISO 27001 certification, data residency, SLA). 2. Evaluate each LLM provider against criteria; document in supplier register. 3. Define monitoring procedure (annual re-evaluation, incident tracking). 4. Flow down data handling requirements contractually (DPA). 5. Define fallback plan if provider becomes unavailable. |
| **Owner** | Procurement / IT / Quality |
| **Verification** | Supplier register exists with evaluation scores; DPA on file for each provider. |

---

### P2 -- Significant Gaps

#### GAP-004: Audit Trail Integrity Enforcement
| Attribute | Detail |
|-----------|--------|
| **Standards** | 21 CFR Part 11, GxP ALCOA+ (Original, Accurate), ISO 27001 A.8.9 |
| **Current State** | Append-only design intent. No technical enforcement at file level. |
| **Action Required** | 1. Implement per-entry hashing in Decision Log and Change Log (SHA-256 hash chain). 2. Write-protect archived cycle directories at the file system level. 3. Add integrity verification step to Compliance Auditor cycle boundary audit. 4. Consider database-backed logging for high-assurance environments. |
| **Owner** | Engineering / DevOps |

#### GAP-005: Validation Plan and System Description
| Attribute | Detail |
|-----------|--------|
| **Standards** | GxP / GAMP 5, ISO 13485 7.1 |
| **Current State** | **Addressed (SCHEMA-BACKED, draft).** `validation-agent` provides validation planning, protocol, report, and deviation behavior (VALIDATION_PLAN/PROTOCOL/REPORT). `agile-v-gxp-qualification` adds `QUALIFICATION_PLAN` and `SYSTEM_DESCRIPTION` schemas with matching `templates/agile-v/*.example.yaml`. |
| **Action Required** | 1. Instantiate `QUALIFICATION_PLAN` referencing Agile V pipeline stages. 2. Instantiate `SYSTEM_DESCRIPTION` (system boundaries, data flows, user roles, interfaces). 3. Make these mandatory inputs before Stage 1 in regulated projects. Draft contracts require local baselining. |
| **Owner** | Quality |

#### GAP-006: Design Validation (Distinct from Verification)
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 13485 7.3.6, GxP |
| **Current State** | **Addressed.** Verification and validation are **no longer conflated**: `red-team-verifier` independently verifies specified outputs (VERIFICATION_SUMMARY); `validation-agent` separately assesses intended use in representative conditions (VALIDATION_REPORT) with its own plan, protocol, and deviation behavior. |
| **Action Required** | 1. Require intended-use validation via `validation-agent` for regulated projects (PQ stage). 2. Ensure validation is performed in the intended-use environment (simulated or real), separate from verification. 3. Retain VALIDATION_REPORT alongside VERIFICATION_SUMMARY. |
| **Owner** | Quality / Engineering |

#### GAP-007: Customer-Related Processes
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 9001 5.1.2, ISO 13485 7.2 |
| **Current State** | No customer communication, regulatory requirement determination, or contract review. |
| **Action Required** | 1. Define a pre-pipeline phase: "Customer Requirements Review" that captures applicable regulations, customer needs, and contractual requirements. 2. Feed outputs into Requirement Architect as input constraints. 3. Implement customer feedback loop that generates CRs for next cycle. |
| **Owner** | Product / Quality |

#### GAP-008: Backup and Disaster Recovery
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 27001 A.8.13, AS9100D 8.5.4, ISO 13485 4.2.5 |
| **Current State** | Git provides repository-level backup. No explicit backup procedure or verification. |
| **Action Required** | 1. Define backup frequency and retention for `.agile-v/` contents. 2. Implement automated backup verification (test restore quarterly). 3. Define disaster recovery procedure and RTO/RPO. |
| **Owner** | IT / DevOps |

---

### P3 -- Enhancement Gaps

#### GAP-009: Organizational QMS KPIs
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 9001 4.4, 9.1 |
| **Action Required** | Define QMS-level KPIs (cross-project defect density, first-pass yield trends, average cycle time). Aggregate per-project metrics from compliance-auditor output. |

#### GAP-010: Audit Program
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 9001 9.2 |
| **Action Required** | Define audit schedule (e.g., quarterly process audits, annual QMS audit). Assign auditors with documented independence. Track corrective actions from audits. |

#### GAP-011: Configuration Management Plan
| Attribute | Detail |
|-----------|--------|
| **Standards** | AS9100D 8.1.2 |
| **Action Required** | Create CM plan template that references `.agile-v/` structure, defines configuration baselines at Gate 2, and specifies configuration audit procedure. |

#### GAP-012: Security Test Type in Test Designer
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 27001 A.8.29 |
| **Action Required** | Add `security` as a test type in the Test Designer taxonomy. Integrate SAST/DAST tools into CI pipeline. Include security test results in Verification Summary. |

#### GAP-013: Document Register and Distribution Control
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 13485 4.2.4, ISO 9001 7.5 |
| **Action Required** | Create master document register for `.agile-v/` controlled documents. Define distribution lists. Implement obsolescence marking for superseded documents. |

#### GAP-019: Training / Role Qualification
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 9001 7.1.2, ISO 13485 6.2, GxP / GAMP 5 |
| **Current State** | **NORMATIVE CONTRACT (draft).** Role-qualification expectations are expressed in `agile-v-gxp-qualification`; competency/training records remain an organizational (external) responsibility. |
| **Action Required** | Define role-to-competency mapping for accountable humans operating gates and validation; retain training/qualification records in the organizational QMS. |
| **Owner** | Quality / People |

#### GAP-020: Requalification on Trigger Events
| Attribute | Detail |
|-----------|--------|
| **Standards** | GxP / GAMP 5, ISO 13485 4.1.6 |
| **Current State** | **SCHEMA-BACKED (draft).** `REQUALIFICATION_ASSESSMENT` schema + example template link revalidation triggers (model/runtime/skill change, accumulated CRs, interval) to a documented reassessment. |
| **Action Required** | On each trigger, instantiate `REQUALIFICATION_ASSESSMENT`, determine which qualification stages must be re-executed, and record the disposition. Draft contract requires local baselining. |
| **Owner** | Quality / Engineering |

#### GAP-014: Formal Risk Methodology (FMEA/FTA)
| Attribute | Detail |
|-----------|--------|
| **Standards** | AS9100D 8.1.1, ISO 13485 7.1 |
| **Action Required** | For hardware/safety-critical projects, conduct product-level FMEA or FTA. Feed results into REQUIREMENTS.md as constraints and into RISK_REGISTER.md. |

---

### P4 -- Advisory Gaps

#### GAP-015: Agent Sandboxing and Access Control Enforcement
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 27001 A.8.3 |
| **Action Required** | Explore runtime-level agent isolation (restricted file access per agent role). Currently protocol-based only. |

#### GAP-016: Lessons Learned Mechanism
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 9001 10.2 |
| **Action Required** | Conduct retrospectives at cycle boundaries. Record lessons learned in Decision Log with a `LESSON` tag. |

#### GAP-017: API Key Management for LLM Providers
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 27001 A.8.5 |
| **Action Required** | Implement API key rotation schedule, scoped tokens, secure storage (vault/keychain). Document in security policy. |

#### GAP-018: Design Transfer Procedures
| Attribute | Detail |
|-----------|--------|
| **Standards** | ISO 13485 7.3.8 |
| **Action Required** | For products moving to manufacturing, create design transfer procedures linking Agile V outputs (Build Manifest, verified artifacts) to manufacturing specifications. |

---

## 4. Roadmap Visualization

```mermaid
gantt
    title Compliance Gap Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %b %Y
    section P1 Blocking
        GAP-001 E-Signatures           :crit, g1, 2026-03-01, 60d
        GAP-002 IQ/OQ/PQ Evidence     :crit, g2, 2026-03-01, 45d
        GAP-003 Supplier Qualification  :crit, g3, 2026-03-15, 30d
    section P2 Significant
        GAP-004 Audit Trail Integrity   :g4, 2026-04-01, 30d
        GAP-005 Validation Plan         :g5, 2026-03-15, 21d
        GAP-006 Design Validation       :g6, 2026-04-01, 21d
        GAP-007 Customer Processes      :g7, 2026-04-15, 30d
        GAP-008 Backup/DR              :g8, 2026-03-15, 21d
    section P3 Enhancement
        GAP-009 Org KPIs               :g9, 2026-05-01, 30d
        GAP-010 Audit Program          :g10, 2026-05-01, 21d
        GAP-011 CM Plan                :g11, 2026-05-15, 14d
        GAP-012 Security Tests         :g12, 2026-05-15, 14d
        GAP-013 Doc Register           :g13, 2026-06-01, 14d
        GAP-014 FMEA/FTA              :g14, 2026-06-01, 30d
    section P4 Advisory
        GAP-015 Agent Sandboxing       :g15, 2026-07-01, 30d
        GAP-016 Lessons Learned        :g16, 2026-07-01, 7d
        GAP-017 API Key Management     :g17, 2026-07-01, 14d
        GAP-018 Design Transfer        :g18, 2026-07-15, 21d
```

## 5. How to Use This Roadmap

1. **Identify your regulatory context.** Not all gaps apply to all projects. A non-regulated web app needs none of these. A medical device needs P1 and P2. An aerospace system needs P1 + P2 + GAP-011 + GAP-014.
2. **Assign owners.** Each gap has a suggested owner role. Map to your team members.
3. **Track in your QMS.** These gaps should be entered as actions in your organizational QMS or project management system.
4. **Verify closure.** Each gap includes verification criteria. Confirm closure before claiming compliance.
5. **Re-audit periodically.** When skills are updated or your regulatory context changes, re-run the compliance audit. The documentation-agent can regenerate this documentation.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: GxP / GAMP 5 Matrix](06_GXP_GAMP5_MATRIX.md)
