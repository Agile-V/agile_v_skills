# CycloneDX ML-BOM Export

## Overview

[CycloneDX](https://cyclonedx.org/capabilities/mlbom/) supports Machine Learning Bill of Materials use cases for transparency around AI/ML systems, including models, datasets, configurations, frameworks, and risk-relevant metadata.

Agile-V uses CycloneDX as the primary external export format. The internal `AI_RUN_MANIFEST.yaml` is the Agile-V source of truth; CycloneDX is the interoperability format.

## Why CycloneDX

- Supports multiple BOM families (SBOM + ML-BOM)
- Allows AI/ML inventory to be linked with broader supply-chain inventory
- Useful for security, compliance, transparency, and audit workflows
- Stable format suitable for diffing and round-trip validation

## Field Mapping

| AI_RUN_MANIFEST Field | CycloneDX Target |
|----------------------|-----------------|
| `identity.task_id` | `metadata.properties["agile-v:task_id"]` |
| `identity.run_id` | `serialNumber` or `metadata.properties["agile-v:run_id"]` |
| `models[].name`, `model_id` | `components[].name`, `type: machine-learning-model` |
| `models[].inference_runtime` | `components[]` or `services[]` |
| `agent_runtime.agent_framework` | `components[]` or `services[]` |
| `rag_and_context.sources[]` | `components[]` or `services[]` (data reference where applicable) |
| `tools[]` | `components[]` or `services[]` |
| `models[].confidence` | `components[].properties["agile-v:confidence"]` |
| `models[].evidence_locator` | `externalReferences[]` |
| `evidence_links.sbom` | `externalReferences[]` or BOM-Link |

## Export Requirements

The export must be:

- Valid JSON conforming to CycloneDX 1.6 schema
- Clearly marked as generated from Agile-V (`tools[].vendor = "agile-v.org"`)
- Traceable to the internal manifest (manifest path and hash in `externalReferences`)
- Stable enough for diffing between runs
- Preserving confidence and evidence locator metadata in `properties`

## Template

See `templates/CYCLONEDX_AGENT_RUN_BOM.cdx.json` for a minimal example.

## Phase Roadmap

```
Phase 1: Agile-V internal AI_RUN_MANIFEST + CycloneDX export (current)
Phase 2: SPDX 3.0 AI export adapter
Phase 3: BOM diffing and round-trip validation across formats
```

## SPDX Note

SPDX 3.0.1 includes an AI profile for documenting AI systems and model artifacts. Agile-V is intentionally not locked to one external format. Phase 2 will add SPDX export support.

Reference: https://spdx.github.io/spdx-spec/v3.0.1/model/AI/AI/
