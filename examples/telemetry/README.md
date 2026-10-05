# Telemetry examples

`gate-flow.default.json` shows the privacy-safe default profile of the [OpenTelemetry Contract](../../docs/agile-v-runtime/17_OPENTELEMETRY_CONTRACT.md). Each event validates against `schemas/AGILE_V_TELEMETRY_EVENT.schema.json` and maps 1:1 to an OTLP span/event (`name` -> span name, `attributes` -> span attributes, `trace_id`/`span_id`/`parent_span_id` -> span context). They contain no prompt, completion, reasoning, secret or source content. These events are observability only; the Gate Receipt (`GATE-1`) remains the authoritative decision record.
