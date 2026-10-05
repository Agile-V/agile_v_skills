# agile-v-aibom known limitations

1. `verified` confidence cannot currently be established: `evaluate_ai_run_manifest` accepts `verified` only from a registry source that may establish `verified_<kind>_identity`, and no registry v1 profile does. Every `verified` entry is rejected (fail closed).
2. Observed AI-context sources (`EAD-agent-session-metadata-v1`, `EAD-otel-genai-trace-v1`, `EAD-k8s-aibom-v1`) are `experimental`; they cannot admit evidence for current decisions.
3. Hidden-reasoning and secret detection are pattern-based heuristics over manifest strings; they reduce, not eliminate, the risk of capture.
4. `ai_bom_diff` maps skill changes to the `tool` revalidation kind and runtime changes to `environment`; finer-grained dependency matching is not defined.
5. The CycloneDX export is a view; it is not validated against the CycloneDX 1.6 JSON schema in this repository.
6. No external reviewer or independent user feedback has been recorded (required for `stable`).
