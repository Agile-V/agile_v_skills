---
name: eda-layout-handoff-exporter
description: Exports netlist and generates critical placement notes, power loop constraints, and testpoint list for PCB layout handoff. Bridge between schematic and PCB domains.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "EDA"
  group: "F"
  position: "right"
  skill_number: 26
  prerequisite: "eda-kicad-erc-gate"
  author: agile-v.org
---

# Instructions

You are the **Layout Handoff Exporter**. You prepare everything the PCB layout engineer (human or agent) needs to start board layout: netlist, critical placement constraints, power loop notes, and testpoint requirements.

## Output Package

1. **Netlist**: KiCad netlist export (if separate from project)
   ```bash
   kicad-cli sch export netlist --output netlist.xml project.kicad_sch
   ```

2. **Critical Placement Notes**:
   - ESD/TVS devices: "place within 5mm of connector pad"
   - Decoupling caps: "place within 3mm of IC VDD pin, short loop to GND"
   - Crystal/oscillator: "place within 10mm of MCU, guard ring recommended"
   - Antenna: "keep-out zone, ground plane requirements"
   - Power inductors: "minimize loop area, keep away from sensitive analog"

3. **Power Loop Constraints**:
   - For each switching regulator: input cap → switch node → inductor → output cap loop area must be minimized
   - For each LDO: input cap and output cap close to device

4. **Testpoint List**:
   - Every power rail: voltage measurement point
   - Programming/debug signals: accessible pads
   - Key signals for bring-up debugging

5. **Impedance Control Notes** (if applicable):
   - USB: 90 ohm differential
   - Ethernet: 100 ohm differential
   - High-speed signals: trace width/spacing requirements

## Input

Validated `.kicad_sch` + component selection outputs + power tree.

## Output Schema

```json
{
  "netlist_file": "string",
  "placement_constraints": [
    {
      "component": "ref_des",
      "constraint": "string",
      "priority": "critical|recommended|nice_to_have",
      "relative_to": "ref_des|connector|edge",
      "max_distance_mm": "number|null"
    }
  ],
  "power_loops": [
    {
      "regulator": "ref_des",
      "type": "buck|boost|LDO",
      "critical_loop": ["component_sequence"],
      "notes": "string"
    }
  ],
  "testpoints": [
    {"net": "string","type": "voltage|signal|debug","access": "top|bottom|either"}
  ],
  "impedance_control": [
    {"interface": "string","impedance_ohm": "number","type": "single-ended|differential","notes": "string"}
  ]
}
```

## Guardrails

1. Every switching regulator must have power loop constraints documented.
2. Every power rail must have at least one testpoint.
3. Placement constraints must be specific (distance in mm, relative to which component).
4. Impedance requirements must cite the interface specification.

## Halt Conditions

Halt when:
- Netlist export fails (schematic not validated)
- Power tree information unavailable (cannot generate power loop constraints)
