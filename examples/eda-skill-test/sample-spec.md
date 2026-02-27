# Sample Hardware Spec: EnvSense USB-C Sensor Board

This is a realistic free-text hardware project description intended to be fed
through the full 26-skill EDA pipeline as a worked example.

---

## Project Brief

**Product Name:** EnvSense v1.0
**Purpose:** Indoor environmental monitoring module for smart building HVAC systems.
**Form Factor:** 50mm x 35mm, single-sided placement preferred, 4-layer stackup.

## Power

- **Input:** USB-C (5V only, no PD negotiation needed), max 500mA draw
- **Rails needed:**
  - 3.3V for MCU + digital peripherals (expect ~120mA peak)
  - 1.8V for VOC sensor analog supply (expect ~30mA)
  - 5V passthrough for fan header (100mA max)
- **Battery:** None. Bus-powered only.
- **Protection:** Reverse polarity on USB-C VBUS, ESD on data lines

## Controller

- STM32L4 series preferred (low power, Cortex-M4F, built-in ADC)
- Need: I2C x2, SPI x1, UART x1, ADC x2 channels, GPIO x4 minimum
- 8MHz HSE crystal, 32.768kHz LSE crystal for RTC
- SWD programming header (Tag-Connect TC2030 footprint)

## Interfaces & Sensors

| Interface | Device / Purpose | Protocol | Notes |
|-----------|-----------------|----------|-------|
| I2C #1 | SHT40 — Temperature + Humidity | I2C, 400kHz | 3.3V, address 0x44 |
| I2C #1 | BMP390 — Barometric Pressure | I2C, 400kHz | 3.3V, address 0x77 |
| I2C #2 | SGP41 — VOC/NOx Index | I2C, 400kHz | 1.8V supply, 3.3V I2C (level shift needed) |
| SPI | W25Q32 — 4MB NOR Flash | SPI, 50MHz | Data logging buffer, 3.3V |
| UART | Debug/CLI console | 115200 baud | 3.3V TTL, exposed on test pads |
| ADC Ch0 | NTC thermistor (board temp) | Analog | 10k @ 25C, voltage divider to 3.3V |
| ADC Ch1 | Light sensor (TEMT6000) | Analog | Phototransistor, 3.3V bias |
| GPIO | Status LED (green) | Digital out | 3.3V, 20mA max via current-limiting resistor |
| GPIO | User button | Digital in | Active-low with debounce RC, pulled high |
| GPIO | Fan enable | Digital out | N-FET switching 5V fan header, flyback diode |

## Connectivity

- **No wireless.** Upstream data via USB CDC (virtual COM port over USB-C data lines).
- USB 2.0 Full Speed (12 Mbps). STM32L4 has built-in USB peripheral.

## Environmental & Compliance

- Operating temperature: -10C to +60C (industrial indoor)
- Humidity: 0-95% RH non-condensing
- ESD: IEC 61000-4-2, Contact ±4kV, Air ±8kV on USB-C connector
- EMC: CE Class B target (no formal cert for v1.0, but design for it)

## Mechanical Constraints

- 4x M2.5 mounting holes at corners, 3mm from board edge
- USB-C connector at board edge (mid-point of 50mm side)
- Fan header (JST-XH 2-pin) at opposite edge
- All sensors within 10mm of board center (thermal coupling)
- SWD header near MCU (within 15mm)
- Status LED visible from top, near USB-C connector

## Cost & Volume

- Target BOM cost: <$15 USD at 500 units
- Single source acceptable for v1.0 prototyping, but flag single-source parts
- Prefer JLCPCB/LCSC basic parts where possible

## Deliverables Expected

1. Validated `.kicad_sch` (passes KiCad ERC with zero errors)
2. Complete `.kicad_sym` + `.kicad_mod` project library
3. BOM (CSV) with MPN, manufacturer, quantity, alternates
4. Schematic PDF for review
5. Layout handoff package (netlist + placement constraints + testpoints)
