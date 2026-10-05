"""Convert Agile-V telemetry events to OTLP/JSON (ExportTraceServiceRequest).

Usage: python tools/telemetry_to_otlp.py examples/telemetry/gate-flow.default.json > otlp.json
The output can be POSTed to any OTLP/HTTP collector at /v1/traces
(Content-Type: application/json). No proprietary collector is required.
"""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import sys


def _nanos(value: str) -> str:
    return str(int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1_000_000_000))


def _value(value):
    if isinstance(value, bool):
        return {"boolValue": value}
    if isinstance(value, int):
        return {"intValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, list):
        return {"arrayValue": {"values": [_value(v) for v in value]}}
    return {"stringValue": str(value)}


def to_otlp(events: list[dict], service_name: str = "agile-v") -> dict:
    spans = []
    for event in events:
        attributes = dict(event["attributes"])
        service_name = attributes.pop("service.name", service_name)
        span = {
            "traceId": event["trace_id"], "spanId": event["span_id"], "name": event["name"],
            "kind": 1,  # SPAN_KIND_INTERNAL
            "startTimeUnixNano": _nanos(event["time"]),
            "endTimeUnixNano": _nanos(event.get("end_time", event["time"])),
            "attributes": [{"key": k, "value": _value(v)} for k, v in sorted(attributes.items())],
            "status": {"code": {"UNSET": 0, "OK": 1, "ERROR": 2}[event.get("status", "UNSET")]},
        }
        if "parent_span_id" in event:
            span["parentSpanId"] = event["parent_span_id"]
        spans.append(span)
    return {"resourceSpans": [{
        "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": service_name}}]},
        "scopeSpans": [{"scope": {"name": "org.agile-v", "version": "1.0"}, "spans": spans}]}]}


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    data = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    print(json.dumps(to_otlp(data["events"]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
