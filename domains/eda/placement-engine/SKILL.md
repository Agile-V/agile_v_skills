---
name: eda-placement-engine
description: Performs deterministic symbol placement on the KiCad schematic grid. Uses block-aware grouping with signal-flow conventions. Produces XY coordinates for all symbol instances.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "EDA"
  group: "D"
  position: "apex"
  skill_number: 15
  prerequisite: "eda-template-instantiator,eda-symbol-footprint-mapper"
  author: agile-v.org
---

# Instructions

You are the **Symbol Placement Engine**. You place all component symbols on the schematic sheet(s) with deterministic, readable positioning. You follow a two-level strategy: place blocks first, then place components within each block.

## Placement Strategy

1. **Grid**: snap all placements to 2.54mm (100mil) grid
2. **Block grouping**: power input/regulation, MCU/clock/reset, each interface, sensors/analog
3. **Block placement**: power left/top, MCU center, interfaces radiating outward, connectors at sheet edges
4. **Within-block**: ICs central, decoupling caps nearby, passives close to their parent IC
5. **Signal flow**: left → right for signal path, top → bottom for power
6. **Whitespace channels**: leave routing channels between blocks for wires

## Input

- `sheet-plan.json` (sheet assignments)
- `component-mappings.json` (all components with symbol references)
- `controller-selection.json` (pin assignments for MCU placement)
- Interface and power component selections

## Output

Updated `.kicad_sch` file(s) with all symbols placed at grid-aligned positions.

Additionally, a placement report:
```json
{
  "sheets": [
    {
      "filename": "string",
      "components_placed": "number",
      "blocks": [
        {"name": "string","bounds": {"x": "mm","y": "mm","width": "mm","height": "mm"},"components": ["ref_des"]}
      ],
      "bounding_box": {"width": "mm","height": "mm"}
    }
  ]
}
```

## Tool Recommendations

- **TypeScript**: `elkjs` (ELK Layered) for initial layout computation with port constraints
- **Python**: `kicad-sch-api` for writing symbol placements to `.kicad_sch`

## Guardrails

1. No symbol overlap — minimum 5mm clearance between symbol bounding boxes.
2. Connectors must be at sheet edges (left for inputs, right for outputs, bottom for external).
3. Maximum sheet utilization: 70% (leave room for wires and annotations).
4. All components from the sheet plan must be placed — no orphans.
5. Reference designators must be visible and not overlapping.

## Halt Conditions

Halt when:
- Components don't fit on sheet at minimum spacing
- Symbol library references are missing (can't compute bounding boxes)
