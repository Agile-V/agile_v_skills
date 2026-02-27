# KiCad API & Tooling Reference

> Reference for Python and TypeScript tools used by EDA domain skills.

## Python: kicad-sch-api

**Purpose:** Generate `.kicad_sch` files with proper component placement and wire routing.

**Install:** `pip install kicad-sch-api`

**Key capabilities:**
- Component bounding box calculation
- Manhattan-style orthogonal wire routing with obstacle avoidance
- Symbol placement with rotation and field management
- Wire, junction, and label generation
- KiCad 7/8 compatible output

**Typical usage pattern:**
```python
from kicad_sch_api import Schematic, Symbol, Wire, Label

# Create schematic
sch = Schematic()

# Add symbol instance
sym = Symbol(
    lib_id="Device:R",
    at=(25.4, 50.8, 0),  # x, y, rotation
    reference="R1",
    value="10k",
    footprint="Resistor_SMD:R_0402_1005Metric"
)
sch.add(sym)

# Add wire
wire = Wire(
    points=[(25.4, 45.72), (25.4, 40.64), (38.1, 40.64)]
)
sch.add(wire)

# Add net label
label = Label(
    text="VCC",
    at=(38.1, 40.64, 0)
)
sch.add(label)

# Write to file
sch.save("output.kicad_sch")
```

## Python: kicad-skip

**Purpose:** Read, modify, and write existing KiCad files using S-expression parsing.

**Install:** `pip install kicad-skip`

**Best for:** Patching existing schematics rather than generating from scratch.

```python
from kicad_skip import Schematic

sch = Schematic("existing.kicad_sch")
for symbol in sch.symbols:
    if symbol.reference.startswith("C"):
        # Modify capacitor values
        symbol.value = "100nF"
sch.save("modified.kicad_sch")
```

## TypeScript: elkjs (ELK Layered)

**Purpose:** Graph layout engine for initial block/node placement with port constraints.

**Install:** `npm install elkjs`

**Key capabilities:**
- Layered graph layout (ideal for signal-flow schematics)
- Port constraints (pin positions on symbol boundaries)
- Orthogonal edge routing
- Hierarchical graph support (multi-sheet)

**Typical usage pattern:**
```typescript
import ELK from 'elkjs';

const elk = new ELK();

const graph = {
  id: "root",
  layoutOptions: {
    "elk.algorithm": "layered",
    "elk.direction": "RIGHT",
    "elk.layered.spacing.nodeNodeBetweenLayers": "50",
    "elk.spacing.nodeNode": "30",
    "elk.edgeRouting": "ORTHOGONAL"
  },
  children: [
    {
      id: "U1",
      width: 80,
      height: 120,
      ports: [
        { id: "U1_VCC", properties: { "port.side": "NORTH" } },
        { id: "U1_GND", properties: { "port.side": "SOUTH" } },
        { id: "U1_PA0", properties: { "port.side": "EAST" } },
        { id: "U1_PB0", properties: { "port.side": "WEST" } }
      ]
    },
    {
      id: "R1",
      width: 20,
      height: 10,
      ports: [
        { id: "R1_1", properties: { "port.side": "WEST" } },
        { id: "R1_2", properties: { "port.side": "EAST" } }
      ]
    }
  ],
  edges: [
    { id: "net1", sources: ["U1_PA0"], targets: ["R1_1"] }
  ]
};

const layout = await elk.layout(graph);
// layout.children[i].x, .y → symbol positions
// layout.edges[i].sections → wire routing points
```

## KiCad CLI Reference

**Schematic export:**
```bash
# PDF export
kicad-cli sch export pdf -o output.pdf project.kicad_sch

# SVG export
kicad-cli sch export svg -o output_dir/ project.kicad_sch

# Netlist export
kicad-cli sch export netlist -o netlist.xml project.kicad_sch

# BOM export
kicad-cli sch export python-bom -o bom.xml project.kicad_sch
```

**Electrical Rules Check:**
```bash
kicad-cli sch erc -o erc_report.json --format json project.kicad_sch
```

**Symbol library operations:**
```bash
# Export symbol to SVG
kicad-cli sym export svg -o output_dir/ library.kicad_sym
```

## Coordinate System Notes

- KiCad schematic coordinates: origin at top-left, Y increases downward
- Default grid: 2.54 mm (100 mil) — snap all placements to this grid
- Fine grid: 1.27 mm (50 mil) — for dense layouts
- Symbol fields use separate coordinate offsets relative to symbol origin
- Wire coordinates must exactly match pin positions for connectivity

## S-Expression Format Quick Reference

```lisp
(kicad_sch
  (version 20231120)
  (generator "eda-agent")
  (uuid "...")
  (paper "A4")

  (lib_symbols
    (symbol "Device:R" ...))

  (symbol
    (lib_id "Device:R")
    (at 25.4 50.8 0)
    (uuid "...")
    (property "Reference" "R1" (at 25.4 48.26 0))
    (property "Value" "10k" (at 25.4 53.34 0))
    (property "Footprint" "Resistor_SMD:R_0402_1005Metric" ...)
    (pin "1" (uuid "..."))
    (pin "2" (uuid "...")))

  (wire
    (pts (xy 25.4 45.72) (xy 25.4 40.64))
    (uuid "..."))

  (label "VCC"
    (at 38.1 40.64 0)
    (uuid "...")))
```
