# Capability Composition Metadata

**Contract version: 1.0.** Registry key `capability_composition`.

> **Normative for packaging.** Extends `catalog/skills.json` with optional `capabilities` per skill so that distribution profiles can be checked for composition errors. Capability metadata helps package composition; it does **not** prove that a runtime implements the behavior correctly. Runtime conformance remains separate ([runtime status](../../conformance/RUNTIME_STATUS.md)).

## Fields

```json
"capabilities": {
  "provides":   ["org.agile-v.verification.independent"],
  "requires":   ["org.agile-v.testing.design"],
  "conflicts":  [],
  "supersedes": [],
  "exclusive":  []
}
```

| Field | Rule |
|---|---|
| `provides` | Stable reverse-domain names (`org.agile-v.<area>.<name>`). Every released skill provides at least one; a name has exactly one provider in the catalog. |
| `requires` | Every `routing.prerequisites` entry is represented by requiring one of that prerequisite's provided capabilities. |
| `conflicts` | Capabilities that must not be present in the same package. |
| `supersedes` | Capabilities this skill replaces; a package must not contain both. |
| `exclusive` | Provided capabilities that at most one skill in a package may provide. |

## Build-time rejections (`tools/build_agent_plugins.py`)

Missing required capability; duplicate exclusive capability; direct conflict; stable profile depending on a capability provided only by draft skills; superseded capability present alongside its successor; unknown skill; unsatisfied prerequisite.

## Examples of capability names

`org.agile-v.requirements.baseline`, `org.agile-v.verification.independent`, `org.agile-v.validation.intended-use`, `org.agile-v.risk.classification`, `org.agile-v.evidence.admission`, `org.agile-v.ai-influence.inventory`, `org.agile-v.hardware.schematic`.

Manual skill installation remains supported; capability metadata is advisory for manual installs.
