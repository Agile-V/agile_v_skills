# EDA Validation Checklist

> Procedures for verifying generated KiCad schematics are correct and uncorrupted.

## Level 1: File Integrity (Skill #19)

Quick checks before invoking KiCad:

- [ ] File is valid UTF-8 text
- [ ] S-expression parentheses are balanced
- [ ] Root node is `(kicad_sch (version ...) (generator ...) ...)`
- [ ] All required top-level nodes present: `lib_symbols`, `wire`, `symbol`
- [ ] No truncation (file doesn't end mid-expression)
- [ ] UUIDs are present and unique

```bash
# Quick balance check
python3 -c "
text = open('project.kicad_sch').read()
assert text.count('(') == text.count(')'), 'Unbalanced parens'
print('S-expression balance: OK')
"
```

## Level 2: KiCad CLI Render Test (Skill #20)

The authoritative "not corrupted" check. If KiCad can parse and render it, it's structurally valid.

```bash
# Export schematic to PDF
kicad-cli sch export pdf \
  --output output.pdf \
  project.kicad_sch

# Export to SVG (per-page)
kicad-cli sch export svg \
  --output output_dir/ \
  project.kicad_sch

# Check exit code
echo "Exit code: $?"  # 0 = success
```

**Pass criteria:** Exit code 0 + non-empty PDF/SVG output.

**Common failures:**
- Missing symbol libraries → see Level 5
- Malformed S-expressions → see Level 1
- Invalid field references → check symbol metadata

## Level 3: Electrical Rules Check (Skill #21)

Semantic correctness validation.

```bash
# Run ERC
kicad-cli sch erc \
  --output erc_report.json \
  --format json \
  --severity-all \
  project.kicad_sch
```

**Error categories:**

| Severity | Action | Examples |
|----------|--------|----------|
| **Error** | Must fix | Unconnected power pins, conflicting pin types, missing net connections |
| **Warning** | Review | Unconnected input pins, bidirectional pin conflicts |
| **Exclusion** | Document | Known acceptable conditions (add to exceptions list) |

**Allowed exceptions format:**
```json
{
  "exceptions": [
    {
      "rule": "pin_not_connected",
      "component": "U1",
      "pin": "NC",
      "rationale": "No-connect pin per datasheet"
    }
  ]
}
```

## Level 4: Protocol Rule Checks (Skill #22)

Domain-specific electrical correctness.

### USB-C
- [ ] CC1/CC2 have 5.1k pulldowns (UFP) or Rp (DFP)
- [ ] VBUS has appropriate capacitance
- [ ] D+/D- have series resistors if needed
- [ ] Shield connected to chassis ground via RC

### I2C
- [ ] SDA/SCL have pullup resistors (typ 4.7k for 100kHz, 2.2k for 400kHz)
- [ ] Pullups connected to correct voltage rail
- [ ] Address conflicts checked across all devices

### SPI
- [ ] CS lines are unique per device
- [ ] MISO has pullup/pulldown when multiple devices share bus
- [ ] Clock polarity documented

### CAN
- [ ] 120 ohm termination at both ends of bus
- [ ] Transceiver CANH/CANL properly connected
- [ ] Slope control / silent mode pin handling documented

### UART
- [ ] TX→RX crossover correct
- [ ] Level shifting present if voltage domains differ
- [ ] Flow control (RTS/CTS) connected if required

### Reset / Boot
- [ ] Reset has RC filter (typ 100nF + 10k)
- [ ] Boot pins have correct pullup/pulldown for desired boot mode
- [ ] Watchdog connections verified

### Power
- [ ] Each IC has decoupling capacitors (100nF minimum per VDD pin)
- [ ] Bulk capacitance on each rail
- [ ] Power-on sequencing constraints met
- [ ] Measurement/test points on each rail

## Level 5: Library Resolution Check (Skill #23)

Ensures all referenced symbols and footprints exist.

```bash
# Check for missing symbols
kicad-cli sch export netlist \
  --output netlist.xml \
  project.kicad_sch 2>&1 | grep -i "missing\|not found\|error"
```

**Common causes of "missing symbol" errors:**
1. Symbol not in project-local library
2. Library table (`sym-lib-table`) doesn't include the library path
3. Symbol name changed between KiCad versions
4. Custom library not installed

**Resolution steps:**
1. Check `sym-lib-table` and `fp-lib-table` in project directory
2. Verify `.kicad_sym` files exist at referenced paths
3. Ensure footprint libraries (`.kicad_mod` files) are in place
4. Run `symbol-footprint-mapper` to regenerate mappings

## Docker Setup for KiCad CLI

For CI/CD or agent execution environments without KiCad installed:

```dockerfile
FROM kicad/kicad:8.0
WORKDIR /workspace
COPY . .
RUN kicad-cli sch export pdf --output /output/schematic.pdf project.kicad_sch
RUN kicad-cli sch erc --output /output/erc.json --format json project.kicad_sch
```

## Validation Pipeline Summary

```
Generated .kicad_sch
  │
  ├─ Level 1: File integrity (fast, no KiCad needed)
  │   └─ FAIL → fix S-expression issues
  │
  ├─ Level 2: KiCad render test (authoritative parse check)
  │   └─ FAIL → fix structural issues or missing libraries
  │
  ├─ Level 3: ERC gate (semantic correctness)
  │   └─ ERROR → fix electrical issues
  │   └─ WARNING → review + document exceptions
  │
  ├─ Level 4: Protocol rule checks (domain-specific)
  │   └─ FAIL → fix interface-specific issues
  │
  └─ Level 5: Library resolution (missing symbols/footprints)
      └─ FAIL → rebuild libraries or fix references
```
