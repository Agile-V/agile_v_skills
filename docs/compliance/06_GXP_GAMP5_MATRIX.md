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

## Compliance Matrix

| Requirement | Status | Evidence (Skill) | Gap / User Action Required |
|-------------|--------|-------------------|---------------------------|
| **V-Model Lifecycle** | **COMPLIANT** | Left Side (Requirements → Validation) → Apex (Synthesis) → Right Side (Verification → Acceptance). Pipeline stages map to V-Model phases. Traceability REQ → ART → TC → VER. | V-Model phases not explicitly mapped to IQ/OQ/PQ terminology. **User should:** Create mapping document: Logic Gatekeeper = DQ, Build Agent = IQ, Test Designer = OQ, Red Team Verifier = PQ. |
| **Computer System Validation (CSV)** | **PARTIAL** | Requirements documentation (REQUIREMENTS.md). Design traceability (Build Manifest). Verification protocols (Test Specification, VER records). VSR (Validation Summary Report). Human Gates as approval checkpoints. | No Validation Plan (VP) document. No System Description document. No Validation Protocol templates for IQ/OQ/PQ. **User must:** Create VP before starting Agile V pipeline; include system description, validation approach, responsibilities, acceptance criteria. |
| **21 CFR Part 11 -- Electronic Records** | **PARTIAL** | Decision Log with timestamps, agent IDs, rationale. Append-only design. Git commit hashes for integrity. VER records with chain-of-thought. Cycle archives frozen. | No technical enforcement of append-only (file system allows modification). No checksums on individual log entries. No closed-system controls. **User must:** Implement technical controls: write-protect archived files, compute and verify checksums, restrict file system access. |
| **21 CFR Part 11 -- Electronic Signatures** | **NOT COVERED** | APPROVALS.md captures approver name, role, timestamp, signature method. Minimum requirements table by regulatory context. | No actual electronic signature mechanism. Git signed commits are available but not 21 CFR Part 11 compliant without additional infrastructure. **User must:** Implement PKI-based digital signatures for Gate approvals; bind signatures to approved documents with intent declaration ("I approve this for release"); implement signature meaning table. |
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

## Summary

| Status | Count |
|--------|-------|
| COMPLIANT | 8 |
| PARTIAL | 7 |
| NOT COVERED | 1 |

**Key message for pharma/life sciences teams:** Agile V provides strong traceability, risk-based validation, change control, and periodic review. The critical gap is **21 CFR Part 11 electronic signatures** -- this requires organizational PKI infrastructure that a skill set cannot provide. You must also implement: Validation Plan, closed-system controls, technical enforcement of append-only logs, and per-entry integrity hashing.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 27001 Matrix](05_ISO_27001_MATRIX.md) | [Next: Gap Roadmap →](07_GAP_ROADMAP.md)
