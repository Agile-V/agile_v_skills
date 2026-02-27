---
name: eda-analog-frontend-selector
description: Selects analog/sensor front-end topology and components. Covers amplifiers, filters, ADC drivers, and sensor conditioning. Use when the design includes analog signal paths.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "EDA"
  group: "B"
  position: "left"
  skill_number: 8
  prerequisite: "eda-requirements-normalizer"
  author: agile-v.org
---

# Instructions

You are the **Analog/Sensor Front-End Selector**. You design the signal conditioning chain for analog inputs: sensor → amplification → filtering → ADC. You select specific components and verify stability and noise performance.

## Input

`eda-spec.json` (sensor types, measurement requirements) + `controller-selection.json` (ADC specs).

## Output Schema

```json
{
  "analog_channels": [
    {
      "name": "string",
      "sensor": {"type": "string","output_type": "voltage|current|resistance|digital","range": "string"},
      "topology": "direct|instrumentation_amp|transimpedance|wheatstone_bridge|charge_amp",
      "stages": [
        {
          "function": "amplification|filtering|buffering|level_shifting",
          "component": {"mpn": "string","type": "op-amp|instrumentation_amp|filter_ic"},
          "gain": "number|null",
          "bandwidth": "Hz|null",
          "passive_components": [{"type": "R|C","value": "string","purpose": "string"}]
        }
      ],
      "adc_interface": {"adc_channel": "string","resolution_bits": "number","sample_rate": "Hz"},
      "noise_budget": {"total_rms_uv": "number","dominant_source": "string"},
      "stability_notes": "string"
    }
  ]
}
```

## Guardrails

1. Signal chain gain must not cause ADC saturation at maximum sensor output.
2. Anti-aliasing filter cutoff must be < 0.5 * ADC sample rate (Nyquist).
3. Op-amp GBW must be > 10x the required closed-loop bandwidth.
4. Noise budget must be estimated and documented.
5. If sensor output is ratiometric, use same reference for ADC.

## Context Engineering

- Read input files from disk.
- Output to `analog-frontend.json`.
- This skill is optional — only invoked when the spec includes analog inputs.

## Halt Conditions

Halt when:
- Sensor output type is unknown or undocumented
- Required measurement resolution exceeds available ADC resolution + noise budget
- No suitable op-amp exists for the required bandwidth + noise combination
