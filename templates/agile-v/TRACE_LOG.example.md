# TRACE_LOG.md — append-only (Phase 1)

Format: `TRACE-ID | ISO8601_UTC | agent_id | span_name | parent_TRACE-ID | event_type | REQ-IDs | ref_path_or_uri | notes`

```text
TR-0001 | 2026-04-26T10:00:00Z | build-agent | build_start | — | start | REQ-0001,REQ-0002 | .agile-v/BUILD_MANIFEST.md | cycle C1
TR-0002 | 2026-04-26T10:05:00Z | build-agent | tool:Write | TR-0001 | tool | REQ-0001 | src/foo.ts | —
```

See [01_SCHEMAS.md](../../docs/agile-v-runtime/01_SCHEMAS.md#1-trace-trace_logmd).
