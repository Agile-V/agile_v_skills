# PCB Schematic Placement & Routing Guidelines

> Reference document for EDA agents generating KiCad `.kicad_sch` files programmatically.

---

## Schematic vs PCB: Two Different Placements

* **Schematic placement** = where symbols go on the page + where **wires** (not PCB traces) run.
* **PCB placement/routing** = where footprints go on the board + where copper **tracks** run.

For generating a **`.kicad_sch`**, you only need **symbol placement + wire routing**. KiCad's schematic format is S-expression based, with coordinates stored at high resolution (schematic/symbol files have 0.0001 mm precision internally).

---

## 1. Layout Pipeline: Graph → Placement → Wire Routing → Emit `.kicad_sch`

### Step A — Build a Connectivity Graph

Represent the schematic as a graph:

* **Nodes**: component instances (symbol units), connectors, power symbols, sheet ports
* **Ports**: pins (with direction/type and preferred side if you know it)
* **Edges**: nets between pins

This graph is your "truth." Everything else (XY + wire segments) is derived.

### Step B — Block-Aware Grouping (Critical for Readability)

Before any auto-layout, cluster nodes into blocks:

* Power in / regulation / rails
* MCU + clock/reset/programming
* Each interface (USB, I2C, CAN, etc.)
* Sensors / analog

This is *the* trick that keeps auto-placement from producing spaghetti.

### Step C — Place Blocks, Then Place Parts Inside Each Block

Two-level placement is far more stable than "layout everything at once."

Heuristics that work well:

* **Connectors at sheet edges** (left for inputs, right for outputs, bottom for "external")
* **Power left/top**, ground bottom
* **Signal flow left→right**
* **MCU central**, interfaces radiating out
* Keep each block inside a bounding box, leave whitespace "channels" for wires

### Step D — Run an Auto-Layout Engine That Understands Ports

For deterministic web-style layouts, use a graph layout engine like **ELK Layered** (available as `elkjs` in JS). It supports **orthogonal routing** and **port constraints**, which maps nicely to "schematic-ish" diagrams.

You feed ELK:

* node sizes (symbol bounding boxes)
* port positions (pin anchors on the symbol boundary)
* edges (nets)

You get back:

* **node x/y**
* optional **edge routes** (polyline segments)

You then map those coordinates onto the KiCad schematic grid.

### Step E — Manhattan Wire Routing with Obstacle Avoidance

Even with ELK, you usually want a "schematic wire router":

* route wires orthogonally (Manhattan)
* avoid symbol bounding boxes
* prefer short runs; avoid crossing
* where nets are busy, prefer **labels** over long wires

`kicad-sch-api` explicitly advertises **component bounding boxes** and **Manhattan-style orthogonal routing with basic obstacle avoidance**, which is exactly what you need for schematic wire placement.

### Step F — Emit `.kicad_sch` via a Writer API (Don't Hand-Serialize)

To reliably generate valid schematics, use a library that writes KiCad schematics correctly (and preserves format). `kicad-sch-api` is built for generating `.kicad_sch` that open in KiCad 7/8 and includes objects for components/wires/labels.

Alternative for patching existing files: `kicad-skip`.

---

## 2. Placement Data Required for Correct Rendering

### For Each Symbol Instance

* `at (x y rot)` (position + rotation)
* unit selection (for multi-unit symbols)
* fields (Ref, Value, Footprint, MPN...)
* UUIDs (writer libs typically handle this)

### For Wires

* polyline points (orthogonal segments)
* junctions
* labels (local/global/hierarchical)
* sheet pins if hierarchical

**Important:** for a generator, you'll get much nicer results if you treat labels as a *routing primitive*:

* If a net touches >N pins or crosses blocks → use a **net label bus** or distributed labels
* Keep wires mostly local inside a block

---

## 3. Practical "Good Enough" Placement Strategy

If you want something deterministic without heavy layout math:

1. **Define a grid** (e.g., 2.54 mm or 1.27 mm step; snap everything)
2. **Place blocks in rows** (Power row, Digital row, Interfaces row)
3. **Inside each block**:
   * place ICs centrally
   * place passives close (decoupling under/near IC symbol)
   * place connectors at block boundary
4. **Route within the block** with Manhattan wires
5. **Between blocks**: prefer labels (short "stubs" + labels) over long wires

This avoids 80% of "auto-schematic ugliness."

---

## 4. Validation: Verify Placement Didn't Break the File

After generating, do an authoritative check by making KiCad parse it:

* **Export PDF** (parse + render): `kicad-cli sch export pdf`
* **Run ERC**: `kicad-cli sch erc`

That's the most reliable "not corrupted" smoke test for generated schematics.

---

## 5. PCB Footprint Placement + Copper Routing (Separate Pipeline)

If the project extends to `.kicad_pcb`, you'd need:

* footprint placement constraints
* board outline
* design rules
* interactive router or autorouter
* differential pair/impedance constraints, etc.

This is handled by the **layout-handoff-exporter** skill, which generates the netlist and critical placement notes for downstream PCB layout work.

---

## Tool Stack Recommendation

| Tool | Language | Purpose |
|------|----------|---------|
| **ELK / elkjs** | TypeScript/JS | Initial block/node placement with port constraints + orthogonal routing |
| **kicad-sch-api** | Python | Bounding boxes, Manhattan wire routing, `.kicad_sch` emission |
| **kicad-skip** | Python | Patch/modify existing `.kicad_sch` files (S-expression manipulation) |
| **KiCad CLI** | Shell | Authoritative validation: `sch export pdf`, `sch erc` |

## References

* [KiCad S-Expression Format](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html)
* [KiCad Schematic File Format](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/)
* [ELK Layered Algorithm](https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-layered.html)
* [kicad-sch-api on PyPI](https://pypi.org/project/kicad-sch-api/)
* [kicad-skip on GitHub](https://github.com/psychogenic/kicad-skip)
