# Risk Assessment v2

> **Normative.** This contract adds explicit, dimension-based rationale to the `L0`–`L4` classification in `docs/agile-v-runtime/04_RISK_CLASSIFICATION.md`. It does not replace `L0`–`L4`; it makes the reasoning behind a selected level auditable and prevents a level from being silently lowered below a deterministic floor.

## 1. Why

`L0`–`L4` levels are useful workflow profiles, but recording only the final level loses the reasoning. Two tasks at the same level can have very different risk shapes (e.g. high reversibility/low data-sensitivity vs. low reversibility/high data-sensitivity), and a level can be quietly lowered by omitting the dimension that would have raised it.

## 2. Dimensions

| Dimension | Question |
|---|---|
| `impact` | How severe is the consequence if this is wrong? |
| `reversibility` | How hard is it to undo? |
| `external_side_effect` | Does this affect systems/data/parties outside the immediate task? |
| `privilege` | What access/authority does executing this require? |
| `data_sensitivity` | Does this touch privacy-sensitive, secret, or regulated data? |
| `safety_relevance` | Could this affect physical or operational safety? |
| `regulatory_relevance` | Is this in a regulated scope (GxP, safety case, financial, privacy law)? |
| `deployment_scope` | How broadly does this take effect (one user, all users, production-wide)? |
| `uncertainty` | How novel or poorly understood is this change? |
| `dependency_supply_chain_change` | Does this change a dependency, vendor, or supply-chain input? |
| `verification_difficulty` | How hard is it to independently verify this claim? |
| `recovery_difficulty` | How hard is recovery if this fails after release? |

Score each applicable dimension (e.g. 1–4) with a short rationale; omit dimensions that are genuinely not applicable rather than scoring them arbitrarily.

## 3. Risk floors

A **floor** is a deterministic minimum level triggered by a specific condition, independent of the scored dimensions:

```yaml
floors:
  - reason: production_release
    minimum_level: L2
  - reason: regulated_scope
    minimum_level: L3
```

**Rule:** the dimension-based score MAY raise the selected level above the highest applicable floor. It MUST NOT be used to select a level below the highest applicable floor. Lowering below a floor requires an explicit, authorized `EXCEPTION_DECISION` (`docs/agile-v-runtime/09_EXCEPTION_AND_WAIVER_CONTRACT.md`) — never a bare judgment call in the assessment itself.

## 4. Structure

See `schemas/RISK_ASSESSMENT.schema.json`. Required: `dimensions` (at least one scored), `floors` (may be empty), `selected_level`, `rationale`. If `floors` is non-empty, `selected_level` must be at least as high as the highest `minimum_level` among the floors, unless an `exception_ref` is present.

## 5. Relationship to `04_RISK_CLASSIFICATION.md`

`RISK_ASSESSMENT` is the structured rationale that justifies the `RISK_REGISTER` entry's level. It does not change the `L0`–`L4` evidence obligations table; it makes the classification decision itself reviewable and prevents silent downgrades.
