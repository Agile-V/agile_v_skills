# agile-v-aibom graduation evidence (draft -> candidate)

Per [Skill Graduation Policy](../../../docs/agile-v-runtime/13_SKILL_GRADUATION_POLICY.md) a skill graduates only when the evidence exists **and an authorized reviewer records the decision**. This directory assembles the evidence. **The skill remains `draft`.** No `stable` claim is made.

| Candidate requirement | Status | Evidence |
|---|---|---|
| Contract review completed | **Pending** -- requires authorized reviewer | `REVIEW_RECORD.yaml` (`decision: pending`) |
| Negative test suite exists | Present | `tests/test_aibom_graduation.py` (declared-as-verified, unresolved L3 identity, missing influence diff, confidence flip, hidden CoT, secrets, CycloneDX translation) |
| Two end-to-end scenarios (recommended) | Present (reference semantics) | `test_e2e_scenario_1_*` (model A->B, exact affected evidence), `test_e2e_scenario_2_*` (declared vs observed k8s-aibom) |
| Documented failure modes and limitations | Present | `KNOWN_LIMITATIONS.md` |
| Owner declared | Present | `agile-v.org` (skill frontmatter) |
| Gate Receipt compatibility (recommended) | Partial | Telemetry/evidence correlation only; no gate-level AI-BOM claim type yet |
| Compatibility statement | Present | `COMPATIBILITY.md` |
| Source profiles | Present (experimental) | `EAD-agent-session-metadata-v1`, `EAD-otel-genai-trace-v1`, `EAD-k8s-aibom-v1` (experimental); `EAD-container-image-digest-v1`, `EAD-git-commit-v1`, `EAD-agent-plugin-package-v1` (candidate) |

Reproduce: `python -m pytest tests/test_aibom_graduation.py -q`. Results are reference-semantics results; they do not show that any runtime captures AI-BOMs correctly.
