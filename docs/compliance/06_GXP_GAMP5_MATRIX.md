# GxP / GAMP 5 Compliance Matrix

> **Document ID**: COMP-006
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 27001 Matrix](05_ISO_27001_MATRIX.md) | [Next: Gap Roadmap →](07_GAP_ROADMAP.md)

---

## Scope

GxP (Good Practice) regulations and GAMP 5 (Good Automated Manufacturing Practice) apply to computerized systems in pharmaceutical and life sciences industries. This matrix assesses Agile V's readiness for building and validating such systems, including 21 CFR Part 11 and Annex 11 requirements for electronic records and signatures.

> **Non-certification statement:** This Agile V profile supports structured qualification and validation evidence. It does not determine legal applicability, replace controlled procedures, provide technical Part 11 controls, or establish regulatory compliance.

> **Sources:** Regulatory/guidance anchors (Annex 15, Annex 11, 21 CFR Part 11, FDA CSA, GAMP 5 2nd Ed., ICH Q9(R1)/Q10, ALCOA+) with public URLs and status are in the [standards source register](../standards/SOURCE_REGISTER.md) (`SRC-GXP-01`..`SRC-GXP-07`). Verify current editions before use.

## Two Distinct Qualification Scopes

Qualification evidence in this matrix falls into two separate scopes that must not be conflated:

| Scope | What is qualified | Owner |
|---|---|---|
| **Target-system qualification** | The computerized system built/validated *using* Agile V (the regulated product) | Project / Quality |
| **Assurance-toolchain qualification** | The Agile V skills + runtime + model configuration used to produce evidence | Quality / Engineering (organizational responsibility) |

DQ/IQ/OQ/PQ apply to each scope independently. A qualified assurance toolchain does not qualify the target system, and vice versa.

## Coverage Labels (Legend)

Replaces the prior binary COMPLIANT/PARTIAL grading. A Markdown skill or JSON schema is, by itself, at most a **NORMATIVE CONTRACT** or **SCHEMA-BACKED** — it is not proof of operational compliance or certification.

| Label | Meaning |
|---|---|
| **NOT ADDRESSED** | No contract, schema, or control exists |
| **NORMATIVE CONTRACT** | A skill defines required behavior in prose (contract only) |
| **SCHEMA-BACKED** | A machine-checkable schema/template defines the evidence structure |
| **RUNTIME-ENFORCED** | The runtime mechanically enforces the control |
| **OPERATIONALLY EVIDENCED** | Executed on a real project with retained evidence |
| **EXTERNALLY ASSESSED** | Independently audited/certified by a qualified external party |

## Qualification Stages Are Evidence Stages, Not Agents

DQ/IQ/OQ/PQ are **evidence stages** coordinated by the `agile-v-gxp-qualification` profile — they are **not** agent names. Agents **contribute evidence** to stages; no single agent "is" a stage. The evidence-based model:

| Stage / Activity | Contributing role | Evidence produced |
|---|---|---|
| User requirements | requirement-architect | URS |
| Requirement-quality review (independent; *not* DQ) | logic-gatekeeper | requirement-quality findings |
| **DQ** — design qualification | independent DQ review | design evaluation vs. URS |
| Installation inputs (*not* IQ by itself) | build-agent | installable/configurable outputs |
| **OQ** — test design | test-designer | OQ test specifications |
| **OQ** — execution/challenge (*not* PQ) | red-team-verifier | OQ execution + independent challenge |
| **PQ** — intended-use validation | validation-agent | PQ / intended-use validation evidence |
| Qualification summary | compliance-auditor | QUALIFICATION_SUMMARY |
| Release after stage decisions | release-manager | release record |

Schemas backing these stages (SCHEMA-BACKED): `QUALIFICATION_PLAN`, `SYSTEM_DESCRIPTION`, `SYSTEM_BASELINE`, `QUALIFICATION_PROTOCOL`, `QUALIFICATION_EXECUTION`, `QUALIFICATION_DEVIATION`, `QUALIFICATION_SUMMARY`, `REQUALIFICATION_ASSESSMENT`, each with a matching `templates/agile-v/*.example.yaml`.

## Compliance Matrix

| Requirement | Status | Evidence (Skill) | Gap / User Action Required |
|-------------|--------|-------------------|---------------------------|
| **V-Model Lifecycle** | **NORMATIVE CONTRACT** | Left Side (Requirements → Validation) → Apex (Synthesis) → Right Side (Verification → Acceptance). Pipeline stages map to V-Model phases. Traceability REQ → ART → TC → VER. | DQ/IQ/OQ/PQ are **evidence stages**, not agent names. Agents **contribute evidence** to stages coordinated by the `agile-v-gxp-qualification` profile — do NOT map an agent one-to-one to a stage. Use the evidence-based model above (URS → requirement-quality review → DQ → installation inputs → OQ design → OQ execution/challenge → PQ/intended-use validation → summary → release). |
| **Computer System Validation (CSV)** | **SCHEMA-BACKED** | Requirements documentation (REQUIREMENTS.md). Design traceability (Build Manifest). Verification protocols (Test Specification, VER records). Human Gates as approval checkpoints. `validation-agent` now provides validation planning, protocol, report, and deviation behavior (VALIDATION_PLAN/PROTOCOL/REPORT). `agile-v-gxp-qualification` adds QUALIFICATION_PLAN and SYSTEM_DESCRIPTION contracts. | Verification and validation are **separate** and no longer conflated: `red-team-verifier` verifies specified outputs; `validation-agent` assesses intended use. **User must:** instantiate QUALIFICATION_PLAN + SYSTEM_DESCRIPTION before Stage 1; these are draft contracts requiring local baselining. |
| **Installation / Configuration Qualification (IQ)** | **SCHEMA-BACKED** | `build-agent` produces installable/configurable outputs. `SYSTEM_BASELINE` schema captures installed skill/schema versions, model config, and runtime identity. | No IQ execution evidence yet. **Proposed solution:** capture installation/configuration evidence via `SYSTEM_BASELINE` plus an IQ protocol instance (`QUALIFICATION_PROTOCOL` → `QUALIFICATION_EXECUTION`) confirming components are installed, version-matched, and configured as specified. |
| **21 CFR Part 11 -- Electronic Records** | **NORMATIVE CONTRACT** | Decision Log with timestamps, agent IDs, audit rationale. Append-only design. Git commit hashes for integrity. VER records with concise rationale, evidence paths, reproducible commands, and decision records. Cycle archives frozen. | No technical enforcement of append-only (file system allows modification). No checksums on individual log entries. No closed-system controls. **User must:** Implement technical controls: write-protect archived files, compute and verify checksums, restrict file system access. |
| **21 CFR Part 11 -- Electronic Signatures** | **NOT ADDRESSED** *(external control)* | APPROVALS.md captures approver name, role, timestamp, signature method. Minimum requirements table by regulatory context. | **External-control gap — preserved:** skills cannot provide authenticated identity, non-repudiable e-signatures, or secure audit-trail infrastructure by themselves. Git signed commits are not 21 CFR Part 11 compliant without additional infrastructure. **User must:** Implement PKI-based digital signatures bound to approved documents with intent declaration and a signature-meaning table. |
| **Annex 11 -- Operational Controls** | **PARTIAL** | HITL alerts for critical findings. Halt conditions prevent unauthorized progression. Checkpoint types gate critical decisions. | No batch record concept. No periodic integrity checks during operation. **User must:** Implement automated integrity checks during long-running sessions. |
| **ALCOA+ Data Integrity** | | | |
| - Attributable | **PARTIAL** | Decision Log includes AGENT_ID. APPROVALS.md includes approver name. | Human approver identity depends on APPROVALS.md being filled correctly -- no enforcement. **User must:** Integrate with organizational identity management; enforce approver authentication. |
| - Legible | **COMPLIANT** | All formats are plain text/markdown, human-readable. Structured tables with clear columns. | -- |
| - Contemporaneous | **COMPLIANT** | Timestamps required on all log entries. Write-through persistence. VER records created at verification time. | -- |
| - Original | **PARTIAL** | Append-only design preserves originals. VER re-runs reference originals. Git provides commit-level immutability. | No technical enforcement of append-only at file level. Pre-commit modifications possible. **User must:** Implement file-level write protection after each log entry; consider database-backed logging. |
| - Accurate | **PARTIAL** | Red Team Protocol prevents self-verification. Logic Gatekeeper validates quantitative metrics. | No checksum/hash per log entry. Corrupted entries undetectable. **User must:** Implement per-entry hashing or use a tamper-evident logging system. |
| - Complete | **PARTIAL** | ATM flags dangling artifacts. Non-conformance alerting. | Completeness depends on agent compliance -- if an agent skips logging, the gap is invisible. **User must:** Implement health checks that verify log completeness (e.g., every VER must have a Decision Log entry). |
| - Consistent | **COMPLIANT** | Standardized ID formats across all agents. Cycle-tagged records. | -- |
| - Enduring | **PARTIAL** | Git repository for long-term storage. Cycle archives. | No retention policy. No media migration plan. **User must:** Define retention periods; implement backup verification. |
| - Available | **COMPLIANT** | Files in accessible locations. Structured for human and machine parsing. | -- |
| **Risk-Based Validation** | **COMPLIANT** | Logic Gatekeeper constraint checks. Risk Register with severity matrix. Red Team Verifier severity classification. CRITICAL blocks release. HITL alerts for safety-critical gaps. | -- |
| **Traceability Matrix** | **COMPLIANT** | ATM: REQ → ART → VER with status. Cycle-aware partitioning. CR chain validation. Dangling artifact detection. | -- |
| **Change Control** | **COMPLIANT** | CR-XXXX protocol with rationale, impact analysis, Human approval. Requirement status tags. Cycle-tagged changes. | -- |
| **Periodic Review** | **COMPLIANT** | REVALIDATION_LOG.md with 5 defined triggers (model change, runtime change, skill change, accumulated CRs, 12-month interval). Model version tracking in config.json. | -- |
| **Intended-Use Validation (PQ)** | **NORMATIVE CONTRACT** | `validation-agent` provides validation planning, protocol, report, and deviation behavior (VALIDATION_PLAN/PROTOCOL/REPORT). Distinct from `red-team-verifier` verification. | Draft contract; requires local baselining. **User must:** run validation in representative conditions and retain VALIDATION_REPORT. |
| **Qualification Plan** | **SCHEMA-BACKED** | `QUALIFICATION_PLAN` schema + `templates/agile-v/QUALIFICATION_PLAN.example.yaml` via `agile-v-gxp-qualification` (draft). | Instantiate and baseline per project scope. |
| **System Description** | **SCHEMA-BACKED** | `SYSTEM_DESCRIPTION` schema + example template (draft). | Instantiate before Stage 1 (system boundaries, data flows, roles, interfaces). |
| **Protocol Integrity** | **SCHEMA-BACKED** | `QUALIFICATION_PROTOCOL` + `QUALIFICATION_EXECUTION` + `QUALIFICATION_DEVIATION` schemas separate pre-approved protocol from execution results and deviations (draft). | No runtime enforcement of pre-approval; procedural control required. |
| **Supplier Suitability** | **NORMATIVE CONTRACT** | Supplier/LLM-provider suitability addressed as contract guidance; see GAP-003. | **User must:** evaluate providers against defined criteria; document in supplier register (external activity). |
| **Training / Role Qualification** | **NORMATIVE CONTRACT** | Role-qualification expectations expressed as draft contract in `agile-v-gxp-qualification`. | Competency/training records are an organizational responsibility (external evidence). |
| **Requalification** | **SCHEMA-BACKED** | `REQUALIFICATION_ASSESSMENT` schema + example template (draft) links revalidation triggers to a documented reassessment. | Instantiate on trigger events; requires local baselining. |

## Summary

Coverage is now reported with precise labels (see legend) rather than a binary COMPLIANT/PARTIAL count. Skill/schema wording alone is at most **NORMATIVE CONTRACT** or **SCHEMA-BACKED**; it is not proof of operational compliance or certification.

**Key message for pharma/life sciences teams:** Agile V provides strong traceability, risk-based validation, change control, periodic review, and — now — separate intended-use **validation** (`validation-agent`) and a **qualification-evidence** profile (`agile-v-gxp-qualification`, draft) with schema-backed contracts for plan, system description/baseline, protocol integrity, summary, and requalification. Verification and validation are no longer conflated. The **critical external-control gap remains 21 CFR Part 11 electronic signatures** — authenticated identity, non-repudiable e-signatures, and secure audit-trail infrastructure require organizational controls a skill set cannot provide. IQ/configuration evidence is proposed via `SYSTEM_BASELINE` + an IQ protocol instance. Draft contracts require local baselining before operational use.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 27001 Matrix](05_ISO_27001_MATRIX.md) | [Next: Gap Roadmap →](07_GAP_ROADMAP.md)
