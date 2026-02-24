# AS9100D Compliance Matrix

> **Document ID**: COMP-004
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 13485 Matrix](03_ISO_13485_MATRIX.md) | [Next: ISO 27001 Matrix →](05_ISO_27001_MATRIX.md)

---

## Scope

AS9100D extends ISO 9001 for the aerospace industry, adding operational risk management, configuration management, and heightened control requirements. This matrix covers the AS9100D-specific clauses beyond what ISO 9001 requires.

## Compliance Matrix

| Clause | Title | Status | Evidence (Skill) | Gap / User Action Required |
|--------|-------|--------|-------------------|---------------------------|
| 8.1.1 | Operational risk management | **PARTIAL** | Risk Register (`RISK_REGISTER.md`) with severity matrix, 4 risk categories, assessment rules per pipeline stage. Logic Gatekeeper constraint checks. | No formal risk management methodology (e.g., FMEA, FTA). Risk checks are per-requirement, not product-level. **User must:** Conduct product-level risk assessment (FMEA or equivalent); feed results into REQUIREMENTS.md as constraints. |
| 8.1.2 | Configuration management | **PARTIAL** | `.agile-v/` state directory. Build Manifest identifies configuration items. ATM provides configuration status accounting. Cycle archival provides baselines. | No formal CM plan. No configuration audit procedure. No interface control between configuration items. **User must:** Create CM plan referencing Agile V artifacts; define configuration baselines at Gate 2; implement configuration audits. |
| 8.3.4 | Design controls (V&V) | **COMPLIANT** | Red Team Protocol (independent verification). Requirement-only test design. Positive/negative/boundary/edge tests. Stub detection. Severity classification. 3-attempt fix limit. Hallucination hunting. | -- |
| 8.4 | External providers | **NOT COVERED** | LLM provider documentation in `config.json` (data residency, retention, certification). | Documentation only -- no supplier evaluation, selection, monitoring, or audit procedure. **User must:** Qualify LLM providers as suppliers; conduct periodic supplier assessments; flow down requirements (data handling, availability SLAs). |
| 8.5.2 | Identification and traceability | **COMPLIANT** | REQ → ART → TC → VER chain. ATM. Cycle-aware partitioning. Dangling artifact detection. | -- |
| 8.5.4 | Preservation | **PARTIAL** | Cycle archival (`.agile-v/cycles/CN/`). Append-only logs. Write-through persistence. Git provides integrity. | No backup procedure. No media migration plan. No integrity verification (checksums). **User must:** Implement backup and disaster recovery; add hash verification to archival process. |
| 8.7 | Nonconforming outputs | **PARTIAL** | Severity classification. NC disposition categories. CAPA trigger. | Same as ISO 9001: no consolidated NC register. **User must:** Aggregate NC data across projects for trending. |
| 9.1.1 | Monitoring and KPIs | **COMPLIANT** | 7 defined KPIs. Cycle-over-cycle trend analysis. Metrics in Validation Summary. | -- |

## Summary

| Status | Count |
|--------|-------|
| COMPLIANT | 3 |
| PARTIAL | 4 |
| NOT COVERED | 1 |

**Key message for aerospace teams:** Agile V provides strong design verification controls (8.3.4), traceability (8.5.2), and KPIs (9.1.1). You must supplement it with: formal risk methodology (FMEA), CM plan with configuration audits, supplier qualification for LLM providers, and preservation/backup procedures.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: ISO 13485 Matrix](03_ISO_13485_MATRIX.md) | [Next: ISO 27001 Matrix →](05_ISO_27001_MATRIX.md)
