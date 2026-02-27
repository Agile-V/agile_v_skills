---
name: eda
description: Electronic Design Automation domain for PCB schematic generation, component research, KiCad library creation, and validated `.kicad_sch` output. Covers the full pipeline from requirements normalization through BOM handoff.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  author: agile-v.org
  skills_count: 26
  groups: 6
---

# EDA Domain

Complete pipeline for generating validated PCB schematics from requirements. 26 skills organized into 6 functional groups covering spec → component research → library build → schematic generation → validation → handoff.

## Tool Stack

| Tool | Language | Purpose |
|------|----------|---------|
| **ELK / elkjs** | TypeScript | Graph layout with port constraints + orthogonal routing |
| **kicad-sch-api** | Python | Bounding boxes, Manhattan wire routing, `.kicad_sch` emission |
| **kicad-skip** | Python | Patch/modify existing KiCad files (S-expression manipulation) |
| **KiCad CLI** | Shell | Authoritative validation: `sch export pdf`, `sch erc` |

## Skill Groups

### Group A — Spec & Architecture (3 skills)

| # | Skill | Input | Output |
|---|-------|-------|--------|
| 1 | `requirements-normalizer` | Free text, interface list, constraints | Structured spec (rails, interfaces, environmental, cost/size) |
| 2 | `schematic-sheet-plan` | Structured spec | Sheet hierarchy, per-sheet responsibilities, naming conventions |
| 3 | `power-tree-plan` | Loads + input sources | Rails, max currents, sequencing/enable strategy, measurement points |

### Group B — Component Research & Selection (6 skills)

| # | Skill | Output |
|---|-------|--------|
| 4 | `power-path-selector` | Regulator/protection candidates + derating notes + alternates |
| 5 | `controller-selector` | MCU/SoC + reset/boot/clock/programming circuits + pin strategy |
| 6 | `interface-selector` | Per-interface canonical circuits (connectors, terminations, level shifting) |
| 7 | `protection-emc-selector` | Per-port ESD/TVS, fusing, reverse polarity, filtering plan + placement notes |
| 8 | `analog-frontend-selector` | Topology + stability/noise notes + candidate parts |
| 9 | `bom-risk-check` | Single-source risk, lifecycle flags, alternates/AVL recommendations |

### Group C — Library Build (4 skills)

| # | Skill | Output |
|---|-------|--------|
| 10 | `symbol-builder` | `.kicad_sym` with correct pin numbers/names/types, units, power pins |
| 11 | `footprint-builder` | `.kicad_mod` with pads, courtyard, mask/paste, polarity, fab layers |
| 12 | `symbol-footprint-mapper` | Symbol-footprint mapping + metadata (MPN, value, tolerance, voltage) |
| 13 | `library-qa` | Pass/fail report: pin/pad match, polarity, courtyard, multi-unit consistency |

### Group D — Schematic Generation (5 skills)

| # | Skill | Output |
|---|-------|--------|
| 14 | `template-instantiator` | New project with baseline `.kicad_sch` scaffold from company template |
| 15 | `placement-engine` | Deterministic XY placement on grid with consistent rotations |
| 16 | `connectivity-synthesizer` | Wires, junctions, labels (local/global/hierarchical), sheet pins |
| 17 | `support-passives` | Completed schematic with decoupling caps, pull-ups/downs, boot straps, RC filters |
| 18 | `net-naming-hygiene` | Normalized net labels, diff pairs, buses, power nets + naming report |

### Group E — Validation (5 skills)

| # | Skill | Output |
|---|-------|--------|
| 19 | `file-integrity-check` | Quick integrity verdict: UTF-8, balanced S-expr, required root nodes |
| 20 | `kicad-render-test` | PDF/SVG export via `kicad-cli` (authoritative parse check) |
| 21 | `kicad-erc-gate` | ERC report, categorized (fatal vs warning), allowed exceptions |
| 22 | `protocol-rule-checks` | Pass/fail per interface (USB-C CC, I2C pullups, CAN termination, etc.) |
| 23 | `library-resolution-check` | Actionable list of missing symbols/footprints + resolution steps |

### Group F — Release & Downstream Handoff (3 skills)

| # | Skill | Output |
|---|-------|--------|
| 24 | `bom-generator` | Normalized BOM + alternates/AVL + DNP handling |
| 25 | `documentation-packager` | Schematic PDF(s), design notes, bring-up checklist, known risks |
| 26 | `layout-handoff-exporter` | Netlist, critical placement notes, testpoint list |

---

## V-Model Integration

```
DRAFT
  └→ DEFINITION
       ├─ requirements-normalizer
       ├─ schematic-sheet-plan
       └─ power-tree-plan
  └→ GATE_1 (approve architecture + component selection)
       ├─ power-path-selector ─┐
       ├─ controller-selector  ├─ (parallel)
       ├─ interface-selector   │
       ├─ protection-emc-selector
       ├─ analog-frontend-selector
       └─ bom-risk-check
  └→ SYNTHESIS
       ├─ symbol-builder ──────┐
       ├─ footprint-builder    ├─ (parallel)
       ├─ symbol-footprint-mapper
       ├─ library-qa
       ├─ template-instantiator
       ├─ placement-engine
       ├─ connectivity-synthesizer
       ├─ support-passives
       └─ net-naming-hygiene
  └→ VERIFICATION
       ├─ file-integrity-check
       ├─ kicad-render-test
       ├─ kicad-erc-gate
       ├─ protocol-rule-checks
       └─ library-resolution-check
  └→ GATE_2 (approve validated schematic)
  └→ COMPLETED
       ├─ bom-generator ───────┐
       ├─ documentation-packager ├─ (parallel)
       └─ layout-handoff-exporter
```

## Fast Path (13 Skills)

Minimal viable pipeline that still covers the critical path:

1. `requirements-normalizer`
2. `schematic-sheet-plan`
4. `power-path-selector`
6. `interface-selector`
10. `symbol-builder`
11. `footprint-builder`
12. `symbol-footprint-mapper`
14. `template-instantiator`
15. `placement-engine`
16. `connectivity-synthesizer`
20. `kicad-render-test`
21. `kicad-erc-gate`
24. `bom-generator`

## Full Path (26 Skills)

All skills in sequence with parallel execution where marked above. Use for production-quality schematics where component lifecycle, EMC, and protocol correctness matter.

## Parallel Execution Opportunities

| Group | Can Run in Parallel |
|-------|-------------------|
| B (Component Research) | Skills 4-8 can all run in parallel after Group A completes |
| C (Library Build) | Skills 10-11 can run in parallel; 12-13 sequential after |
| F (Handoff) | Skills 24-26 can all run in parallel after GATE_2 |

## Example Workflows

### Simple USB-C Power Board (Single Sheet)
1. requirements-normalizer → "5V/3A USB-C PD source"
2. schematic-sheet-plan → single sheet
3. power-path-selector → USB-C PD controller + buck converter
4. symbol-builder + footprint-builder → library entries
5. template-instantiator → blank project
6. placement-engine + connectivity-synthesizer → wired schematic
7. kicad-render-test + kicad-erc-gate → validated
8. bom-generator → BOM

### MCU + Sensors + Connectivity (Hierarchical)
1. requirements-normalizer → STM32 + I2C sensors + BLE + USB
2. schematic-sheet-plan → 4 sheets (power, MCU, sensors, connectivity)
3. Full component research (skills 4-9)
4. Full library build (skills 10-13)
5. template-instantiator → hierarchical project
6. Per-sheet: placement-engine + connectivity-synthesizer
7. support-passives + net-naming-hygiene
8. Full validation (skills 19-23)
9. Full handoff (skills 24-26)

## Documentation

See `docs/` for detailed guides:
- `pcb_guidelines.md` — Schematic placement & routing methodology
- `validation_checklist.md` — KiCad CLI validation procedures
- `kicad_api_reference.md` — Python/TypeScript tooling reference

## Golden Rule

**Generation targets `.kicad_sch` + `.kicad_sym` together**, and validation must include:
* **KiCad CLI export** (parse/render) and
* **KiCad CLI ERC** (semantic correctness).

Never ship a schematic that hasn't been parsed by KiCad itself.
