# Skill Preview/Draft Graduation Policy

> **Normative.** A skill is preview/draft only when its frontmatter `metadata.status` is `draft` (see AGENTS.md). This document defines the objective lifecycle a draft skill moves through and the minimum evidence required at each stage. Graduating a skill is a decision, not a schedule — do not graduate merely because time has passed or the schema is stable.

## 1. States

```text
experimental -> draft -> candidate -> stable -> deprecated -> retired
```

| State | Meaning |
|---|---|
| `experimental` | Exploratory; contract may change incompatibly at any time; not distributed via the plugin catalog. |
| `draft` | Contract is proposed and reasonably stable; requires local review before operational use (this repository's current usage of `metadata.status: draft`). |
| `candidate` | Contract review complete, negative test suite exists, and at least the minimum evidence below is present; still not distributed as `released` in the plugin catalog pending a final compatibility check. |
| `stable` | Meets all "stable" requirements below; distributed as `released`. |
| `deprecated` | Superseded or no longer recommended; still present for compatibility; consumers should migrate. |
| `retired` | Removed from distribution; historical reference only. |

## 2. Minimum requirements per state

| Requirement | `candidate` | `stable` |
|---|---|---|
| Contract review completed | Required | Required |
| Negative test suite exists | Required | Required |
| At least two end-to-end scenarios exercised | Recommended | Required |
| Forged-authorship / self-approval / scope-expansion tests (where the skill touches Human Gates or approvals) | Recommended | Required |
| Recovery-evidence test (where the skill claims recovery/oversight properties) | Recommended | Required |
| External reviewer or independent user feedback | Not required | Required |
| Compatibility with Gate Receipt (`schemas/GATE_RECEIPT.schema.json`) where the skill participates in a gate decision | Recommended | Required |
| Documented failure modes and limitations | Required | Required |
| Owner declared | Required | Required |
| Changelog entry on contract change | Not required | Required |

A skill does not graduate `draft -> candidate -> stable` by asserting these; it graduates when the evidence exists and an authorized reviewer records the decision (this is a `GOVERNANCE_CONVERSION`-style decision for the skill's own contract, not a self-declaration).

## 3. Required frontmatter fields for any `draft`/`experimental`/`candidate` skill

```yaml
metadata:
  status: draft
  preview:
    owner: agile-v.org
    graduation_target: candidate | stable
    graduation_criteria_ref: "docs/agile-v-runtime/13_SKILL_GRADUATION_POLICY.md#2-minimum-requirements-per-state"
    compatibility_declaration: "<what this skill requires/is compatible with, or 'none beyond metadata.requires'>"
    known_limitations:
      - "<at least one true, specific statement of what is not yet established>"
```

See `schemas/SKILL_STATUS.schema.json` for the structured form. `known_limitations` MUST be true statements about the current skill, not boilerplate reassurance; "not yet evaluated against the graduation criteria in this document" is an acceptable and honest limitation when no more specific gap analysis has been performed yet — it is not acceptable to omit the field or state "none."

## 4. Rules

1. Do not present a `draft`/`experimental`/`candidate` skill as a stable operational contract (see AGENTS.md "What NOT to Do").
2. Do not graduate a skill merely because its schema validates or its frontmatter is well-formed; graduation requires the evidence in section 2.
3. A skill's own agent instructions may not assert its own graduation; only an external record (changelog entry + authorized review) constitutes graduation.
4. `catalog/skills.json` and `SKILL_ROUTING_GUIDE.md` must mark `draft` skills as Draft/Preview and must never present them as `released`/`official` (existing rule, unchanged; see `tests/test_behavioral_contracts.py::test_draft_skills_do_not_leak_as_released`).
