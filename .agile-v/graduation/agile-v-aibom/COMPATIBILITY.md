# agile-v-aibom compatibility statement

| Interface | Compatibility |
|---|---|
| `schemas/AI_RUN_MANIFEST.schema.json` (`aibom_schema_version: "0.2"`) | Additive optional `context_profile_ref` on named-evidence entries (Context Trust Contract). Existing manifests remain valid. |
| Change-Aware Revalidation | `ai_bom_diff` output is a list of `changed_refs` entries usable in `REVALIDATION_ASSESSMENT`; `evaluate_revalidation_reuse` decides reuse. |
| Evidence Adapter Registry | AI provenance sources are registry profiles; none may establish human authority, verification or compliance. |
| OpenTelemetry Contract | `agilev.agent_run.id` correlates telemetry with `identity.run_id`. |
| CycloneDX ML-BOM | Export/view only (`tools/aibom_to_cyclonedx.py`); not the normative internal contract. |
| Agent Plugins | Shipped only in the `agile-v-regulated-preview` package (preview channel). |
