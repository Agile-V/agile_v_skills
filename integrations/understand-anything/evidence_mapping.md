# Evidence Mapping: Understand Anything → Agile V Evidence Bundle

## Overview

When a knowledge graph is used, Agile V adds a new first section to the evidence bundle:

```text
evidence_bundle/
  00_understanding/    ← NEW
  01_impact/           ← NEW
  02_requirements/
  03_design/
  04_build/
  05_tests/
  06_red_team/
  07_traceability/     ← EXTENDED
  08_validation/
  09_release/
```

---

## Section 00_understanding

| Artifact | Source skill | Required? | Notes |
|---|---|---|---|
| `knowledge_graph_hash.txt` | `system-understanding-agent` | Required if graph used | Hash for reproducibility |
| `normalized_graph.json` | `system-understanding-agent` | Required if graph used | Agile V normalized format |
| `system_overview.md` | `system-understanding-agent` | Required | Plain-English system summary |
| `architecture_map.md` | `system-understanding-agent` | Required | Layers and key components |
| `domain_flow_summary.md` | `system-understanding-agent` | Optional | Business/domain flows |
| `knowledge_graph_summary.md` | `system-understanding-agent` | Optional | Graph statistics and key nodes |
| `system_understanding_confidence.md` | `system-understanding-agent` | Required | Confidence level and rationale |
| `known_constraints.md` | `system-understanding-agent` | Optional | Technical constraints identified |
| `understanding_gate_decision.md` | Gate 0 | Required | Gate 0 pass/fail record |

The original `knowledge_graph.json` is **optional** in the evidence bundle. In regulated or
proprietary environments, include only the hash and the normalized summary. Set
`--redact-source` on the evidence export command to exclude it.

---

## Section 01_impact

| Artifact | Source skill | Required? | Notes |
|---|---|---|---|
| `impact_map.md` | `impact-analysis-agent` | Required for change tasks | Predicted affected components |
| `affected_components.json` | `impact-analysis-agent` | Required for change tasks | Machine-readable impact list |
| `required_regression_tests.md` | `regression-selection-agent` | Required for change tasks | Regression test candidates |
| `change_risk_assessment.md` | `impact-analysis-agent` | Required for change tasks | Risk register pre-change |
| `impact_confidence.md` | `impact-analysis-agent` | Required | Confidence level and assumptions |

---

## Section 07_traceability (extended)

The existing traceability section is extended with graph-level links.

| Artifact | Source skill | Required? | Notes |
|---|---|---|---|
| `graph_traceability_matrix.md` | `graph-traceability-agent` | Required if graph used | REQ → graph node → file → test |
| `req_to_component_links.json` | `graph-traceability-agent` | Required if graph used | Machine-readable links |
| `component_to_test_links.json` | `graph-traceability-agent` | Required if graph used | Machine-readable links |
| `traceability_gaps.md` | `graph-traceability-agent` | Required if gaps found | Orphan requirements/changes |
| `diff_impact_report.md` | `diff-evidence-agent` | Required for change tasks | Predicted vs actual impact |
| `risk_delta.md` | `diff-evidence-agent` | Required if risks changed | Updated risk status post-build |

---

## Evidence manifest extension

When the understanding integration is active, the evidence manifest includes:

```json
{
  "schema_version": "1.1.0",
  "bundle_id": "EVB-2026-0001",
  "includes_understanding": true,
  "understanding": {
    "source": "understand-anything",
    "source_graph_path": ".understand-anything/knowledge-graph.json",
    "source_graph_hash": "sha256:...",
    "normalized_graph_path": "00_understanding/normalized_graph.json",
    "impact_map_path": "01_impact/impact_map.md",
    "graph_traceability_path": "07_traceability/graph_traceability_matrix.md"
  }
}
```

---

## Audit chain

The evidence bundle supports the following auditable chain:

```text
Change request
  → system graph context (00_understanding/system_overview.md)
  → impacted components   (01_impact/affected_components.json)
  → generated requirements (02_requirements/requirements.md)
  → implementation changes  (04_build/diff.patch)
  → selected tests          (05_tests/test_plan.md)
  → executed test results   (05_tests/results.json)
  → graph traceability      (07_traceability/graph_traceability_matrix.md)
  → validation decision     (08_validation/validation_summary.md)
```

This chain is the core audit differentiator of the integration.

---

## What to include in external audits

For external audits (customers, regulators, third parties), include:

```text
00_understanding/knowledge_graph_hash.txt
00_understanding/system_overview.md
00_understanding/architecture_map.md
00_understanding/understanding_gate_decision.md
01_impact/impact_map.md
01_impact/required_regression_tests.md
07_traceability/graph_traceability_matrix.md
08_validation/validation_summary.md
```

Exclude raw source files and the full `knowledge_graph.json` unless explicitly required.
Use `agilev evidence export --external-audit-safe` to generate a redacted bundle.

---

## Standalone mode (no graph available)

When no knowledge graph is available, all sections from `00_understanding/` and `01_impact/`
are omitted. The evidence bundle falls back to the standard Agile V format starting at
`02_requirements/`.

Gate 0 records the absence of a graph as `graph_available: false` in
`understanding_gate_decision.md` and proceeds.
