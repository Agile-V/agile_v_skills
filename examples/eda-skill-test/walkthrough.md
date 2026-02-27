# End-to-End EDA Pipeline Walkthrough: EnvSense USB-C Sensor Board

This document demonstrates the expected output of each of the 26 EDA skills
in sequence, using the `sample-spec.md` (EnvSense v1.0) as input.

---

## Pipeline Overview

```
sample-spec.md (free text)
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ GROUP A — Spec & Architecture                                   │
│  #1 requirements-normalizer → eda-spec.json                     │
│  #2 schematic-sheet-plan   → sheet-plan.json                    │
│  #3 power-tree-plan        → power-tree.json                    │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼  GATE 1 — Approve architecture + component selection
┌─────────────────────────────────────────────────────────────────┐
│ GROUP B — Component Research (parallelizable: #4-#8)            │
│  #4 power-path-selector    → power-components.json              │
│  #5 controller-selector    → controller-selection.json          │
│  #6 interface-selector     → interface-circuits.json            │
│  #7 protection-emc-selector→ protection-plan.json               │
│  #8 analog-frontend-selector→ analog-frontend.json              │
│  #9 bom-risk-check         → bom-risk-report.json              │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ GROUP C — Library Build                                         │
│  #10 symbol-builder         → project.kicad_sym                 │
│  #11 footprint-builder      → *.kicad_mod                       │
│  #12 symbol-footprint-mapper→ component-mappings.json           │
│  #13 library-qa             → library-qa-report.json            │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ GROUP D — Schematic Generation                                  │
│  #14 template-instantiator  → EnvSense.kicad_pro + .kicad_sch  │
│  #15 placement-engine       → placed .kicad_sch                 │
│  #16 connectivity-synthesizer→ wired .kicad_sch                 │
│  #17 support-passives       → completed .kicad_sch              │
│  #18 net-naming-hygiene     → finalized .kicad_sch              │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ GROUP E — Validation                                            │
│  #19 file-integrity-check   → integrity-report.json             │
│  #20 kicad-render-test      → EnvSense.pdf + render-report.json │
│  #21 kicad-erc-gate         → erc-report.json                   │
│  #22 protocol-rule-checks   → protocol-report.json              │
│  #23 library-resolution-check→ resolution-report.json           │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼  GATE 2 — Approve validated schematic
┌─────────────────────────────────────────────────────────────────┐
│ GROUP F — Release & Handoff (parallelizable: #24-#26)           │
│  #24 bom-generator          → bom.csv + bom.json               │
│  #25 documentation-packager → docs/ package                     │
│  #26 layout-handoff-exporter→ handoff-package.json              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skill #1: requirements-normalizer

**Input:** `sample-spec.md` (free text hardware description)

**Expected Output:** `eda-spec.json`

```json
{
  "project": {
    "name": "EnvSense",
    "version": "1.0",
    "form_factor": {
      "width_mm": 50,
      "height_mm": 35,
      "layers": 4,
      "placement": "single-sided preferred"
    }
  },
  "power": {
    "input_sources": [
      {
        "name": "USB-C VBUS",
        "voltage": 5.0,
        "max_current_ma": 500,
        "connector": "USB-C",
        "pd_negotiation": false
      }
    ],
    "rails": [
      {
        "name": "VDD_3V3",
        "voltage": 3.3,
        "max_current_ma": 120,
        "loads": ["MCU", "SHT40", "BMP390", "W25Q32", "I2C_bus", "LED", "NTC", "TEMT6000"]
      },
      {
        "name": "VDD_1V8",
        "voltage": 1.8,
        "max_current_ma": 30,
        "loads": ["SGP41"]
      },
      {
        "name": "VBUS_5V",
        "voltage": 5.0,
        "max_current_ma": 100,
        "loads": ["fan_header"],
        "note": "passthrough from USB-C VBUS"
      }
    ],
    "battery": null
  },
  "interfaces": [
    {
      "name": "I2C_1",
      "protocol": "I2C",
      "speed_khz": 400,
      "voltage": 3.3,
      "devices": [
        {"part": "SHT40", "address": "0x44", "function": "temperature + humidity"},
        {"part": "BMP390", "address": "0x77", "function": "barometric pressure"}
      ]
    },
    {
      "name": "I2C_2",
      "protocol": "I2C",
      "speed_khz": 400,
      "voltage": 3.3,
      "devices": [
        {"part": "SGP41", "address": "auto", "function": "VOC/NOx", "note": "1.8V supply, needs level shifter"}
      ]
    },
    {
      "name": "SPI_FLASH",
      "protocol": "SPI",
      "speed_mhz": 50,
      "voltage": 3.3,
      "devices": [
        {"part": "W25Q32", "function": "4MB NOR flash data logging"}
      ]
    },
    {
      "name": "UART_DEBUG",
      "protocol": "UART",
      "baud": 115200,
      "voltage": 3.3,
      "note": "exposed on test pads"
    },
    {
      "name": "USB_FS",
      "protocol": "USB",
      "speed": "Full Speed (12 Mbps)",
      "class": "CDC",
      "note": "built-in STM32L4 USB peripheral"
    },
    {
      "name": "ADC_NTC",
      "protocol": "analog",
      "channel": 0,
      "sensor": "NTC 10k@25C",
      "conditioning": "voltage divider to 3.3V"
    },
    {
      "name": "ADC_LIGHT",
      "protocol": "analog",
      "channel": 1,
      "sensor": "TEMT6000",
      "conditioning": "phototransistor bias"
    }
  ],
  "gpios": [
    {"name": "LED_STATUS", "direction": "output", "function": "green status LED", "current_ma": 20},
    {"name": "BTN_USER", "direction": "input", "function": "user button", "active": "low", "debounce": true},
    {"name": "FAN_EN", "direction": "output", "function": "5V fan enable via N-FET"}
  ],
  "controller": {
    "family": "STM32L4",
    "core": "Cortex-M4F",
    "peripherals_required": ["I2C x2", "SPI x1", "UART x1", "ADC x2ch", "USB FS", "GPIO x4+"],
    "clocks": {"hse_mhz": 8, "lse_khz": 32.768},
    "programming": "SWD via TC2030"
  },
  "environmental": {
    "temperature_min_c": -10,
    "temperature_max_c": 60,
    "humidity_max_pct": 95,
    "esd_contact_kv": 4,
    "esd_air_kv": 8,
    "emc_target": "CE Class B"
  },
  "mechanical": {
    "mounting_holes": {"type": "M2.5", "count": 4, "edge_clearance_mm": 3},
    "usb_c_position": "center of 50mm edge",
    "fan_header": "opposite edge, JST-XH 2-pin",
    "sensor_zone": "within 10mm of board center",
    "swd_constraint": "within 15mm of MCU",
    "led_position": "near USB-C, visible from top"
  },
  "cost": {
    "target_bom_usd": 15.0,
    "volume": 500,
    "single_source_ok": true,
    "preferred_suppliers": ["JLCPCB", "LCSC"]
  },
  "assumptions": [
    "USB-C CC resistors for UFP (5.1k to GND) — no PD IC needed",
    "All I2C buses use 4.7k pull-ups unless sensor datasheet specifies otherwise",
    "Fan header is a simple 2-wire (5V + GND), no tach/PWM"
  ],
  "unresolved": [
    "Exact STM32L4 part number — depends on pin count vs package trade-off",
    "Whether SGP41 needs separate VDDIO or can tolerate 3.3V on IO pins"
  ]
}
```

---

## Skill #2: schematic-sheet-plan

**Input:** `eda-spec.json`

**Expected Output:** `sheet-plan.json`

```json
{
  "hierarchy": "flat",
  "sheets": [
    {
      "name": "EnvSense",
      "filename": "EnvSense.kicad_sch",
      "is_root": true,
      "responsibilities": [
        "Power input (USB-C + protection)",
        "Voltage regulators (3.3V, 1.8V)",
        "MCU (STM32L4) + crystals + SWD",
        "I2C sensors (SHT40, BMP390, SGP41 + level shifter)",
        "SPI flash (W25Q32)",
        "Analog inputs (NTC, TEMT6000)",
        "GPIO peripherals (LED, button, fan FET)",
        "USB data path"
      ],
      "estimated_components": 65,
      "blocks": [
        {"name": "PWR_INPUT", "position": "top-left", "components": ["USB-C", "ESD", "fuse", "CC resistors"]},
        {"name": "PWR_REG", "position": "top-center", "components": ["3.3V LDO", "1.8V LDO", "decoupling"]},
        {"name": "MCU", "position": "center", "components": ["STM32L4", "HSE", "LSE", "decoupling", "reset", "boot"]},
        {"name": "SWD", "position": "center-right", "components": ["TC2030 header"]},
        {"name": "SENSORS_I2C", "position": "bottom-left", "components": ["SHT40", "BMP390", "SGP41", "level shifter", "pull-ups"]},
        {"name": "FLASH_SPI", "position": "bottom-center", "components": ["W25Q32", "decoupling"]},
        {"name": "ANALOG", "position": "bottom-right", "components": ["NTC divider", "TEMT6000 bias"]},
        {"name": "PERIPHERALS", "position": "right", "components": ["LED + resistor", "button + RC", "FAN FET + flyback"]},
        {"name": "USB_DATA", "position": "top-right", "components": ["USB D+/D- ESD", "series resistors"]}
      ]
    }
  ],
  "naming_conventions": {
    "power_nets": "VDD_{voltage} or VBUS_{voltage}",
    "signal_nets": "{INTERFACE}_{SIGNAL} (e.g., I2C1_SDA, SPI_MOSI)",
    "gpio_nets": "{FUNCTION} (e.g., LED_STATUS, BTN_USER, FAN_EN)"
  },
  "rationale": "Single sheet chosen: ~65 components fits comfortably on A3. No hierarchical complexity warranted for this design."
}
```

---

## Skill #3: power-tree-plan

**Input:** `eda-spec.json` + load estimates from sheet plan

**Expected Output:** `power-tree.json`

```json
{
  "input_sources": [
    {
      "name": "USB_VBUS",
      "voltage": 5.0,
      "max_current_ma": 500,
      "protection": ["reverse polarity (ideal diode or P-FET)", "500mA resettable fuse"]
    }
  ],
  "rails": [
    {
      "name": "VDD_3V3",
      "voltage": 3.3,
      "source": "USB_VBUS",
      "regulation_type": "LDO",
      "max_current_ma": 200,
      "typical_current_ma": 120,
      "loads": [
        {"name": "STM32L4", "typical_ma": 40, "peak_ma": 80},
        {"name": "SHT40", "typical_ma": 0.4},
        {"name": "BMP390", "typical_ma": 0.7},
        {"name": "W25Q32", "typical_ma": 15, "peak_ma": 25},
        {"name": "I2C pull-ups", "typical_ma": 2},
        {"name": "LED", "max_ma": 20},
        {"name": "NTC divider", "typical_ma": 0.3},
        {"name": "TEMT6000", "typical_ma": 0.5},
        {"name": "Level shifter", "typical_ma": 0.1}
      ],
      "decoupling": "10uF bulk + 100nF per IC",
      "sequencing": "first (MCU needs 3.3V before 1.8V)",
      "measurement_point": "TP_3V3"
    },
    {
      "name": "VDD_1V8",
      "voltage": 1.8,
      "source": "VDD_3V3",
      "regulation_type": "LDO",
      "max_current_ma": 50,
      "typical_current_ma": 30,
      "loads": [
        {"name": "SGP41", "typical_ma": 25, "peak_ma": 48}
      ],
      "decoupling": "10uF bulk + 100nF",
      "sequencing": "after VDD_3V3 stable",
      "enable": "tied to VDD_3V3 via RC delay (optional) or always-on",
      "measurement_point": "TP_1V8"
    },
    {
      "name": "VBUS_5V",
      "voltage": 5.0,
      "source": "USB_VBUS",
      "regulation_type": "passthrough",
      "max_current_ma": 100,
      "loads": [
        {"name": "fan_header", "max_ma": 100}
      ],
      "note": "switched via N-FET (FAN_EN GPIO)",
      "measurement_point": "TP_5V"
    }
  ],
  "total_power_budget": {
    "max_input_current_ma": 500,
    "worst_case_total_ma": 380,
    "margin_pct": 24,
    "thermal_note": "LDO 5V→3.3V: (5-3.3)*0.2 = 340mW. SOT-223 or SOT-23-5 adequate."
  },
  "measurement_points": ["TP_VBUS", "TP_3V3", "TP_1V8", "TP_5V", "TP_GND"]
}
```

---

## Skill #4: power-path-selector

**Input:** `power-tree.json`

**Expected Output:** `power-components.json`

```json
{
  "components": [
    {
      "rail": "VDD_3V3",
      "type": "LDO",
      "primary": {
        "mpn": "AMS1117-3.3",
        "manufacturer": "Advanced Monolithic Systems",
        "package": "SOT-223",
        "vin_max": 15,
        "vout": 3.3,
        "iout_max_ma": 1000,
        "dropout_mv": 1100,
        "quiescent_ua": 5000
      },
      "alternate": {
        "mpn": "AP2112K-3.3TRG1",
        "manufacturer": "Diodes Inc",
        "package": "SOT-23-5",
        "iout_max_ma": 600,
        "dropout_mv": 250,
        "quiescent_ua": 55,
        "note": "lower dropout, lower Iq, smaller package — preferred for new designs"
      },
      "external_components": [
        {"type": "capacitor", "value": "10uF", "package": "0805", "position": "input"},
        {"type": "capacitor", "value": "22uF", "package": "0805", "position": "output"},
        {"type": "capacitor", "value": "100nF", "package": "0402", "position": "output"}
      ],
      "derating": "At 200mA, Pdiss = (5-3.3)*0.2 = 340mW. SOT-223 Rth ~60C/W → 20C rise. OK to +60C ambient."
    },
    {
      "rail": "VDD_1V8",
      "type": "LDO",
      "primary": {
        "mpn": "AP2112K-1.8TRG1",
        "manufacturer": "Diodes Inc",
        "package": "SOT-23-5",
        "vin_max": 6,
        "vout": 1.8,
        "iout_max_ma": 600,
        "dropout_mv": 250,
        "quiescent_ua": 55
      },
      "alternate": {
        "mpn": "MIC5504-1.8YM5-TR",
        "manufacturer": "Microchip",
        "package": "SOT-23-5"
      },
      "external_components": [
        {"type": "capacitor", "value": "1uF", "package": "0402", "position": "input"},
        {"type": "capacitor", "value": "10uF", "package": "0805", "position": "output"}
      ],
      "derating": "At 50mA from 3.3V: Pdiss = (3.3-1.8)*0.05 = 75mW. Negligible."
    }
  ],
  "input_protection": {
    "fuse": {
      "mpn": "0603L050YR",
      "type": "PTC resettable",
      "trip_current_ma": 500,
      "package": "0603"
    },
    "reverse_polarity": "USB-C CC resistors enforce correct orientation; no additional protection needed for USB-C"
  }
}
```

---

## Skill #5: controller-selector

**Input:** `eda-spec.json` + `power-tree.json`

**Expected Output:** `controller-selection.json`

```json
{
  "selected": {
    "mpn": "STM32L431CBT6",
    "manufacturer": "STMicroelectronics",
    "core": "Cortex-M4F",
    "flash_kb": 128,
    "ram_kb": 64,
    "package": "LQFP-48",
    "vdd_range": "1.71-3.6V",
    "max_freq_mhz": 80,
    "usb": "USB 2.0 FS device"
  },
  "alternate": {
    "mpn": "STM32L432KCU6",
    "package": "UFQFPN-32",
    "note": "smaller package, fewer GPIOs — viable if pin budget is tight"
  },
  "pin_assignment": {
    "I2C1_SCL": "PB6",
    "I2C1_SDA": "PB7",
    "I2C2_SCL": "PB10",
    "I2C2_SDA": "PB11",
    "SPI1_SCK": "PA5",
    "SPI1_MISO": "PA6",
    "SPI1_MOSI": "PA7",
    "SPI1_CS_FLASH": "PA4",
    "USART1_TX": "PA9",
    "USART1_RX": "PA10",
    "USB_DM": "PA11",
    "USB_DP": "PA12",
    "ADC1_IN5": "PA0",
    "ADC1_IN6": "PA1",
    "LED_STATUS": "PB0",
    "BTN_USER": "PB1",
    "FAN_EN": "PB2",
    "HSE_IN": "PH0",
    "HSE_OUT": "PH1",
    "NRST": "NRST",
    "BOOT0": "BOOT0",
    "SWDIO": "PA13",
    "SWCLK": "PA14"
  },
  "pin_budget": {
    "total_io": 37,
    "used": 23,
    "available": 14,
    "margin_pct": 38
  },
  "support_circuits": {
    "reset": {
      "components": ["100nF cap to GND", "10k pull-up to VDD_3V3"],
      "note": "Internal pull-up exists but external recommended for noise immunity"
    },
    "boot": {
      "components": ["10k pull-down to GND on BOOT0"],
      "note": "Ensures boot from flash by default"
    },
    "hse": {
      "crystal": "8MHz HC49 or 3215 package",
      "load_caps": "2x 20pF (calculate from crystal datasheet CL)"
    },
    "lse": {
      "crystal": "32.768kHz",
      "load_caps": "2x 6.8pF"
    },
    "decoupling": {
      "vdd_pins": ["100nF each on pins 1, 17, 32, 48", "4.7uF bulk near pin 48"],
      "vdda": "1uF + 100nF + ferrite bead from VDD_3V3"
    }
  }
}
```

---

## Skill #6: interface-selector

**Input:** `eda-spec.json` + `controller-selection.json`

**Expected Output:** `interface-circuits.json` (abbreviated — one entry shown)

```json
{
  "interfaces": [
    {
      "name": "I2C_1",
      "devices": ["SHT40", "BMP390"],
      "voltage": 3.3,
      "pull_ups": {"value": "4.7k", "package": "0402", "rail": "VDD_3V3"},
      "esd": {"mpn": "PRTR5V0U2X", "note": "shared TVS on SDA/SCL"},
      "routing_notes": "Keep traces <50mm total, avoid parallel to noisy signals"
    },
    {
      "name": "I2C_2_with_level_shift",
      "devices": ["SGP41"],
      "mcu_side_voltage": 3.3,
      "device_side_voltage": 1.8,
      "level_shifter": {
        "mpn": "TXS0102DCT",
        "manufacturer": "Texas Instruments",
        "channels": 2,
        "note": "Bidirectional, auto direction sensing, suitable for I2C"
      },
      "pull_ups_device_side": {"value": "10k", "package": "0402", "rail": "VDD_1V8"},
      "pull_ups_mcu_side": {"value": "4.7k", "package": "0402", "rail": "VDD_3V3"}
    },
    {
      "name": "SPI_FLASH",
      "device": "W25Q32",
      "signals": ["SCK", "MOSI", "MISO", "CS"],
      "cs_pull_up": {"value": "10k", "package": "0402", "rail": "VDD_3V3", "note": "hold CS high during reset"},
      "decoupling": "100nF on W25Q32 VCC"
    },
    {
      "name": "USB_FS",
      "connector": {
        "mpn": "USB4110-GF-A",
        "type": "USB-C 2.0 receptacle",
        "manufacturer": "GCT"
      },
      "cc_resistors": {"value": "5.1k", "count": 2, "to": "GND", "note": "UFP identification"},
      "data_esd": {"mpn": "PRTR5V0U2X", "note": "on D+/D-"},
      "series_resistors": {"value": "27R", "package": "0402", "note": "optional per STM32 reference design"}
    },
    {
      "name": "UART_DEBUG",
      "signals": ["TX", "RX"],
      "exposure": "test pads (no connector populated)",
      "series_resistors": {"value": "100R", "package": "0402", "note": "protect MCU pins on test pads"}
    }
  ]
}
```

---

## Skills #7-9: (protection-emc-selector, analog-frontend-selector, bom-risk-check)

**#7 protection-emc-selector** outputs `protection-plan.json` with per-port ESD devices (PRTR5V0U2X on USB, TVS on I2C), a PTC fuse on VBUS, and EMC filtering notes (ferrite bead on VDDA, common-mode choke option for USB if CE Class B fails).

**#8 analog-frontend-selector** outputs `analog-frontend.json` — straightforward for this design: NTC voltage divider (10k NTC + 10k fixed → ADC), TEMT6000 with 10k load resistor → ADC. Both with 100nF low-pass filter caps. No amplification needed.

**#9 bom-risk-check** outputs `bom-risk-report.json`:
- STM32L431CBT6: **MEDIUM** risk (lead times historically variable, but widely available)
- SGP41: **MEDIUM** risk (single source — Sensirion only)
- All passives: **LOW** risk (0402/0805 commodity parts)
- USB4110-GF-A: **LOW** risk (multiple USB-C receptacle alternates available)
- Recommendation: Pre-order SGP41 and STM32L4 for 500-unit production

---

## Skills #10-13: Library Build

**#10 symbol-builder** generates `.kicad_sym` entries for all unique components (~15 symbols: STM32L431, AMS1117-3.3, AP2112K-1.8, SHT40, BMP390, SGP41, W25Q32, TXS0102, PRTR5V0U2X, USB4110-GF-A, 0603L050YR, TEMT6000, generic passives use KiCad built-in).

**#11 footprint-builder** generates `.kicad_mod` for any non-standard footprints (USB4110-GF-A, TC2030-IDC, JST-XH-2P). Standard packages (LQFP-48, SOT-223, SOT-23-5, 0402, 0805) use KiCad standard library.

**#12 symbol-footprint-mapper** outputs `component-mappings.json`:
```json
{
  "mappings": [
    {
      "symbol": "EnvSense:STM32L431CBT6",
      "footprint": "Package_QFP:LQFP-48_7x7mm_P0.5mm",
      "fields": {"MPN": "STM32L431CBT6", "Manufacturer": "STMicroelectronics", "LCSC": "C94784"}
    },
    {
      "symbol": "EnvSense:AMS1117-3.3",
      "footprint": "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
      "fields": {"MPN": "AMS1117-3.3", "Value": "3.3V LDO"}
    }
  ]
}
```

**#13 library-qa** outputs `library-qa-report.json`:
```json
{
  "verdict": "PASS",
  "components_checked": 15,
  "checks": {
    "pin_pad_match": "PASS — all symbols have matching footprint pad counts",
    "polarity_marks": "PASS — all polarized components have pin 1 indicators",
    "courtyard": "PASS — all footprints have courtyard on F.CrtYd",
    "fields": "PASS — all have MPN, Manufacturer, Footprint fields",
    "multi_unit": "N/A — no multi-unit symbols in this design"
  }
}
```

---

## Skills #14-18: Schematic Generation

**#14 template-instantiator** creates:
```
EnvSense/
├── EnvSense.kicad_pro
├── EnvSense.kicad_sch        (root, single sheet with title block)
├── sym-lib-table              (points to project library)
├── fp-lib-table               (points to project + KiCad standard)
└── EnvSense.kicad_sym         (project-specific symbols)
```

**#15 placement-engine** places ~65 components on the single sheet in functional blocks:
- PWR_INPUT block (top-left): USB-C connector, CC resistors, fuse, VBUS ESD
- PWR_REG block (top-center): 3.3V LDO, 1.8V LDO, bulk caps
- MCU block (center): STM32L431 + decoupling caps + crystals + reset/boot
- SENSORS block (bottom-left): SHT40, BMP390, SGP41, level shifter, pull-ups
- FLASH block (bottom-center): W25Q32 + decoupling
- ANALOG block (bottom-right): NTC divider, TEMT6000 circuit
- PERIPHERALS block (right): LED, button, fan FET
- USB_DATA block (top-right): USB data ESD, series resistors
- SWD block (center-right): TC2030 header

**#16 connectivity-synthesizer** wires everything with:
- Power nets: `VDD_3V3`, `VDD_1V8`, `VBUS_5V`, `GND` (global labels)
- Signal nets: `I2C1_SDA`, `I2C1_SCL`, `SPI_MOSI`, etc. (local labels within sheet)
- ~120 wire segments, ~30 junctions, ~45 net labels

**#17 support-passives** adds:
- 4x 100nF decoupling on STM32 VDD pins
- 1x 4.7uF bulk cap near MCU
- 1x ferrite bead + 1uF + 100nF on VDDA
- 100nF on each sensor VDD pin
- Pull-up/down resistors already placed by interface-selector
- Total added: ~12 components

**#18 net-naming-hygiene** normalizes:
- All power nets to `VDD_*` / `GND` convention
- USB signals to `USB_DP` / `USB_DM`
- Renames any auto-generated `Net-(...)` labels to meaningful names
- Outputs naming report with 0 violations

---

## Skills #19-23: Validation

**#19 file-integrity-check:**
```json
{
  "files_checked": 3,
  "results": [
    {"file": "EnvSense.kicad_sch", "utf8": "PASS", "sexpr_balance": "PASS", "root_node": "PASS", "truncation": "PASS"},
    {"file": "EnvSense.kicad_sym", "utf8": "PASS", "sexpr_balance": "PASS", "root_node": "PASS", "truncation": "PASS"},
    {"file": "EnvSense.kicad_pro", "utf8": "PASS", "sexpr_balance": "PASS", "root_node": "PASS", "truncation": "PASS"}
  ],
  "verdict": "PASS"
}
```

**#20 kicad-render-test:**
```json
{
  "command": "kicad-cli sch export pdf EnvSense.kicad_sch -o EnvSense.pdf",
  "exit_code": 0,
  "output_file": "EnvSense.pdf",
  "file_size_bytes": 245000,
  "warnings": [],
  "verdict": "PASS"
}
```

**#21 kicad-erc-gate:**
```json
{
  "command": "kicad-cli sch erc EnvSense.kicad_sch -o erc-report.json --format json",
  "errors": 0,
  "warnings": 2,
  "warning_details": [
    "Pin unconnected: U1 pin 35 (PA8) — unused GPIO, acceptable",
    "Pin unconnected: U1 pin 36 (PA15) — unused GPIO, acceptable"
  ],
  "exceptions_applied": 2,
  "verdict": "PASS (0 errors, 2 excluded warnings — unused GPIOs)"
}
```

**#22 protocol-rule-checks:**
```json
{
  "checks": [
    {"protocol": "USB-C", "rule": "CC1/CC2 have 5.1k to GND", "result": "PASS"},
    {"protocol": "USB-C", "rule": "VBUS decoupling present", "result": "PASS"},
    {"protocol": "I2C", "rule": "Pull-ups present on SDA/SCL", "result": "PASS", "bus": "I2C_1", "value": "4.7k"},
    {"protocol": "I2C", "rule": "Pull-ups present on SDA/SCL", "result": "PASS", "bus": "I2C_2", "value": "4.7k+10k"},
    {"protocol": "SPI", "rule": "CS has pull-up for reset safety", "result": "PASS"},
    {"protocol": "MCU", "rule": "BOOT0 pulled to known state", "result": "PASS"},
    {"protocol": "MCU", "rule": "NRST has cap + pull-up", "result": "PASS"},
    {"protocol": "Power", "rule": "All VDD pins decoupled", "result": "PASS"},
    {"protocol": "Power", "rule": "VDDA has ferrite + cap", "result": "PASS"}
  ],
  "verdict": "PASS (9/9 rules passed)"
}
```

**#23 library-resolution-check:**
```json
{
  "symbols_referenced": 15,
  "symbols_resolved": 15,
  "footprints_referenced": 18,
  "footprints_resolved": 18,
  "missing": [],
  "verdict": "PASS"
}
```

---

## GATE 2: Human Approval

At this point, the schematic is validated. A human reviewer would:
1. Review `EnvSense.pdf` for correctness
2. Approve the ERC report (2 excluded warnings are acceptable)
3. Sign off on the BOM risk assessment

---

## Skills #24-26: Release & Handoff (parallel)

**#24 bom-generator** outputs `bom.csv`:

```
Item,Qty,Reference,Value,MPN,Manufacturer,Footprint,DNP,Alternate MPN
1,1,U1,STM32L431CBT6,STM32L431CBT6,STMicroelectronics,LQFP-48,,STM32L432KCU6
2,1,U2,AMS1117-3.3,AMS1117-3.3,AMS,SOT-223,,AP2112K-3.3TRG1
3,1,U3,AP2112K-1.8,AP2112K-1.8TRG1,Diodes Inc,SOT-23-5,,MIC5504-1.8YM5-TR
4,1,U4,SHT40,SHT40-AD1B-R3,Sensirion,DFN-4,,
5,1,U5,BMP390,BMP390-SENR,Bosch,LGA-10,,
6,1,U6,SGP41,SGP41-D-R4,Sensirion,DFN-6,,
7,1,U7,W25Q32,W25Q32JVSSIQ,Winbond,SOIC-8,,W25Q32JVZPIQ
8,1,U8,TXS0102,TXS0102DCT,Texas Instruments,SSOP-8,,
9,2,D1 D2,PRTR5V0U2X,PRTR5V0U2X,Nexperia,SOT-143B,,
10,1,J1,USB-C,USB4110-GF-A,GCT,USB-C-16P,,
11,1,J2,JST-XH-2P,B2B-XH-A,JST,XH-2P,,
12,1,J3,TC2030,TC2030-IDC,Tag-Connect,TC2030,,
13,12,C1-C12,100nF,GRM155R71C104KA88J,Murata,0402,,
14,3,C13-C15,10uF,GRM21BR61A106ME51L,Murata,0805,,
15,2,C16-C17,22uF,GRM21BR61A226ME51L,Murata,0805,,
16,2,C18-C19,1uF,GRM155R61A105KE01D,Murata,0402,,
17,4,C20-C23,20pF,GRM1555C1H200GA01D,Murata,0402,,
18,2,C24-C25,6.8pF,GRM1555C1H6R8BA01D,Murata,0402,,
19,4,R1-R4,4.7k,RC0402FR-074K7L,Yageo,0402,,
20,3,R5-R7,10k,RC0402FR-0710KL,Yageo,0402,,
21,2,R8-R9,5.1k,RC0402FR-075K1L,Yageo,0402,,
22,1,R10,100R,RC0402FR-07100RL,Yageo,0402,,
23,1,R11,220R,RC0402FR-07220RL,Yageo,0402,,
24,1,F1,500mA PTC,0603L050YR,Littelfuse,0603,,
25,1,Q1,N-FET,2N7002,ON Semi,SOT-23,,
26,1,D3,Schottky,BAT54S,Nexperia,SOT-23,,
27,1,LED1,Green,19-217/GHC-YR1S2/3T,Everlight,0603,,
28,1,Y1,8MHz,ABLS-8.000MHZ-B4-T,Abracon,HC49,,
29,1,Y2,32.768kHz,ABS07-32.768KHZ-T,Abracon,3215,,
30,1,FB1,Ferrite 600R@100MHz,BLM15PX601SN1D,Murata,0402,,
```

**Total: ~65 components, 30 unique line items, est. BOM cost ~$11.50 @ 500 units**

**#25 documentation-packager** outputs:
- `EnvSense.pdf` — schematic PDF (from render-test)
- `design-notes.md` — architecture decisions, power tree rationale, component selection justification
- `bringup-checklist.md` — step-by-step power-on procedure (check VBUS → 3.3V → 1.8V → MCU boots → USB enumerates → sensors respond)
- `known-risks.md` — SGP41 single-source, STM32L4 lead time, first-run thermal verification needed

**#26 layout-handoff-exporter** outputs `handoff-package.json`:
```json
{
  "netlist": "EnvSense.net",
  "placement_constraints": [
    {"ref": "J1", "constraint": "board edge, center of 50mm side", "priority": "mandatory"},
    {"ref": "J2", "constraint": "opposite edge from J1", "priority": "mandatory"},
    {"ref": "U4 U5 U6", "constraint": "within 10mm of board center", "priority": "high"},
    {"ref": "J3", "constraint": "within 15mm of U1", "priority": "high"},
    {"ref": "C1-C4", "constraint": "within 2mm of U1 VDD pins", "priority": "critical"}
  ],
  "power_loop_constraints": [
    {"rail": "VDD_3V3", "regulator": "U2", "note": "Minimize input cap → VIN → VOUT → output cap loop area"},
    {"rail": "VDD_1V8", "regulator": "U3", "note": "Place close to SGP41"}
  ],
  "testpoints": ["TP_VBUS", "TP_3V3", "TP_1V8", "TP_5V", "TP_GND", "TP_SWD_TX", "TP_SWD_RX"],
  "impedance_control": "None required (no high-speed differential pairs — USB FS is 12Mbps, standard 90R diff okay)",
  "mounting_holes": [
    {"id": "H1", "x_mm": 3, "y_mm": 3, "drill_mm": 2.7},
    {"id": "H2", "x_mm": 47, "y_mm": 3, "drill_mm": 2.7},
    {"id": "H3", "x_mm": 3, "y_mm": 32, "drill_mm": 2.7},
    {"id": "H4", "x_mm": 47, "y_mm": 32, "drill_mm": 2.7}
  ]
}
```

---

## Pipeline Complete

Final deliverables:
1. `EnvSense.kicad_sch` — validated schematic (0 ERC errors)
2. `EnvSense.kicad_sym` + standard library footprints — complete library
3. `bom.csv` — 30 line items, ~$11.50 BOM cost at 500 units
4. `EnvSense.pdf` — schematic PDF for review
5. `handoff-package.json` — netlist + placement constraints + testpoints

All 26 skills executed. Both gates passed. Ready for PCB layout.
