# AI-BOM Revalidation Triggers

## Overview

A task must be marked for revalidation when any of the following AI components change after verification. This rule applies regardless of whether the artifact code itself changed.

## Trigger List

| Trigger | Description |
|---------|-------------|
| `model_provider_changed` | The organization or API serving the model changed |
| `model_id_changed` | The model name or identifier changed |
| `model_version_changed` | A new model version or deployment was used |
| `inference_runtime_changed` | The runtime serving inference (vLLM, TGI, etc.) changed |
| `agent_framework_changed` | The agent execution framework (OpenHands, LangChain, etc.) changed |
| `agile_v_skill_changed` | A loaded Agile-V skill version changed |
| `tool_access_changed` | Available tools or connectors were added, removed, or modified |
| `rag_source_changed` | A RAG document corpus or retrieval source changed |
| `vector_store_changed` | The vector store or collection was updated |
| `embedding_model_changed` | The embedding model used for RAG changed |
| `sandbox_image_changed` | The sandbox container image or digest changed |
| `system_prompt_or_policy_changed` | System instructions or policy-as-code changed |
| `unresolved_runtime_attribute_in_l2_plus` | An L2+ task has unresolved critical AI fields |

## Revalidation Severity by Risk Level

| Risk Level | Revalidation Scope |
|------------|-------------------|
| Documentation/L0 | Review AI influence summary and refresh docs if needed |
| L1 | Rerun tests affected by generated artifacts |
| L2 | Rerun full verification for changed artifacts |
| L3 | Rerun independent verifier and require human review |
| L4 | Treat as controlled change request with formal approval |

## Policy Configuration

Revalidation triggers are configured in `templates/AI_BOM_POLICY.yaml` under `revalidation_triggers`. Projects may add custom triggers but must not remove core triggers for L2+ tasks.

## Detecting Changes

Use `AI_BOM_DIFF_REPORT.md` to compare the current manifest against the baseline manifest. The diff report identifies:

- Changed components and their field-level deltas
- Confidence level changes
- Which triggers are activated
- Recommended revalidation scope

## Integration with agile-v-compliance

Revalidation triggers from AI-BOM changes feed into the Agile-V revalidation log (`.agile-v/REVALIDATION_LOG.md`). Log entries should include:

- Trigger type
- Affected AI component
- Task ID and run ID
- Revalidation scope
- Completion status
- Human approval reference (L3/L4)
