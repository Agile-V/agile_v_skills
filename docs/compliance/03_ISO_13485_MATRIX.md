# ISO 13485:2016 Compliance Matrix

> **Document ID**: COMP-003
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 9001 Matrix](02_ISO_9001_MATRIX.md) | [Next: AS9100D Matrix →](04_AS9100D_MATRIX.md)

---

## Scope

ISO 13485 is a quality management system standard for medical devices. Agile V covers the **design and development controls** (Clause 7.3) and supporting traceability, document control, and CAPA clauses. Production, service provision, and post-market clauses are out of scope.

## Compliance Matrix

| Clause | Title | Status | Evidence (Skill) | Gap / User Action Required |
|--------|-------|--------|-------------------|---------------------------|
| 4.1.6 | Validation of QMS software | **NOT COVERED** | -- | The AI agent platform (LLMs, runtime) must be validated as a computerized system. **User must:** Conduct IQ/OQ/PQ for the AQMS platform. Define acceptance criteria. Document in validation plan. |
| 4.2.4 | Control of documents | **PARTIAL** | Revision headers, cycle archival, write-through persistence (`agile-v-core`). APPROVALS.md records approval. | No master document register. No distribution control. No obsolescence marking on superseded files. **User must:** Maintain a document register; implement distribution and obsolescence procedures. |
| 4.2.5 | Control of records | **PARTIAL** | Append-only Decision Log and Change Log. Cycle archives frozen/read-only. Timestamps on all entries. | No defined retention period. No integrity protection beyond git. No backup procedure. **User must:** Define retention periods per record type; implement backup and integrity verification. |
| 7.1 | Planning of product realization | **PARTIAL** | Orchestration pipeline defines process. Pre-execution validation. Risk Register. | No explicit quality objectives per product. No resource or environment planning. **User must:** Define product-specific quality objectives in REQUIREMENTS.md. |
| 7.2 | Customer-related processes | **NOT COVERED** | -- | No customer communication. No regulatory requirement determination. No contract review. **User must:** Implement customer requirements process; determine applicable medical device regulations (MDR/FDA) before entering Agile V pipeline. |
| 7.3.1 | Design planning | **PARTIAL** | Pipeline stages, phase directories, wave execution. | No design and development plan document template. No responsibility assignment to named personnel. **User must:** Create a design plan referencing Agile V pipeline stages with named reviewers. |
| 7.3.2 | Design inputs | **COMPLIANT** | Requirement Architect: REQ-XXXX with constraints, verification criteria, done criteria. Logic Gatekeeper validates. | -- |
| 7.3.3 | Design outputs | **PARTIAL** | Build Manifest traces ART to REQ. Per-artifact headers. | No specification of acceptance criteria in output format. No explicit reference to essential performance or safety characteristics. **User must:** Include essential performance requirements as REQ-XXXX with safety flags. |
| 7.3.4 | Design review | **COMPLIANT** | Human Gate 1 (Blueprint). Evidence Summary format. Decision Log. APPROVALS.md. | -- |
| 7.3.5 | Design verification | **COMPLIANT** | Red Team Protocol. Independent test design from requirements. VER records with chain-of-thought. Stub detection. | -- |
| 7.3.6 | Design validation | **PARTIAL** | Human Gate 2 serves as acceptance. | Verification and validation are conflated. No user-environment validation distinct from requirements verification. **User must:** Conduct separate validation in intended-use conditions (simulated or clinical). Add validation protocol to REQUIREMENTS.md. |
| 7.3.7 | Design changes | **COMPLIANT** | CR-XXXX protocol. Impact analysis. Re-validation. Artifact versioning (ART-XXXX.N). Human Gate approval of CRs. | -- |
| 7.3.8 | Design transfer | **NOT COVERED** | -- | No manufacturing specification, process validation, or production documentation. **User must:** Create design transfer procedures linking Agile V outputs to manufacturing inputs. |
| 7.5.1 | Production control | **NOT COVERED** | -- | Skills are design-phase only. **User must:** Implement production controls independently. |
| 7.5.3 | Traceability | **COMPLIANT** | REQ → ART → TC → VER full chain. ATM with gap detection. Dangling artifact alerts. Cycle-aware partitioning. | -- |
| 7.5.8 | Unique Device Identification | **NOT COVERED** | -- | ID schemes (REQ-XXXX, ART-XXXX) are for design artifacts, not manufactured devices. **User must:** Implement UDI system per MDR/FDA requirements. |
| 8.2.4 | Product monitoring and measurement | **PARTIAL** | VER records with PASS/FAIL/FLAG. Severity classification. Coverage tracking. | No measurement equipment calibration. No field monitoring. **User must:** Validate test tools; implement post-market surveillance. |
| 8.3 | Nonconforming product | **PARTIAL** | NC disposition (rework, accept-as-is, reject, defer). Severity classification. CAPA trigger. | No formal NCR lifecycle document. No authority matrix for disposition decisions. **User must:** Define disposition authority matrix; implement NCR document template. |
| 8.5 | CAPA | **COMPLIANT** | CAPA_LOG.md with root cause analysis, corrective action, preventive action, effectiveness verification. Compliance Auditor tracks open CAPAs. | -- |

## Summary

| Status | Count |
|--------|-------|
| COMPLIANT | 6 |
| PARTIAL | 7 |
| NOT COVERED | 5 |

**Key message for medical device teams:** Agile V provides strong design controls (7.3.2-7.3.7), traceability (7.5.3), and CAPA (8.5). You must supplement it with: IQ/OQ/PQ for the platform, design validation in intended-use conditions, design transfer procedures, production controls, UDI, and post-market surveillance.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 9001 Matrix](02_ISO_9001_MATRIX.md) | [Next: AS9100D Matrix →](04_AS9100D_MATRIX.md)
