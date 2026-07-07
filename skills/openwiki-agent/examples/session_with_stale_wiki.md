# Example: Session with a stale/partially-invalid knowledge layer

## Scenario

The agent is asked to add a new endpoint to `src/agilev/pcb/`. The
repository has an `openwiki/` directory from a previous OpenWiki run.

## Step 1 — Check status

```bash
$ agilev wiki status --json
{
  "wiki_dir": "openwiki",
  "initialized": true,
  "page_count": 6,
  "manifest_generated_at": "2026-06-01T00:00:00+00:00",
  "fresh": false,
  "stale_pages": ["domains/pcb.md"],
  "validation_passed": true,
  "validation_errors": [],
  "validation_warnings": [
    "Pages may be stale relative to their declared sources (run 'agilev wiki update' to refresh): domains/pcb.md"
  ]
}
```

## Step 2 — Interpret

- Structural validation passed (no missing pages, manifest matches disk) —
  the knowledge layer as a whole is trustworthy.
- `domains/pcb.md` specifically is stale: `src/agilev/pcb/` changed after
  the manifest was last recorded. The agent treats claims in that one page
  with reduced confidence and instead inspects `src/agilev/pcb/` directly
  for current behavior, rather than relying solely on the page's narrative.
- Other pages (`README.md`, `ARCHITECTURE.md`, `ci-and-release.md`, etc.)
  remain trusted as-is.

## Step 3 — Agent's evidence summary (excerpt)

```text
Knowledge layer: openwiki/ present, structurally valid (agilev wiki
validate: PASS). domains/pcb.md flagged stale relative to src/agilev/pcb/
(changed after last 'agilev wiki update') — read the page for background
but verified current PCB module behavior directly from source rather than
trusting the page's specifics. Other wiki pages used as-is.
```

## Step 4 — Snapshot at task close

```bash
$ agilev wiki snapshot --task AAV-0042
✅ Knowledge snapshot written to .agentic-agile-v/tasks/AAV-0042/evidence.json
   Pages: 6
   Validation passed: True
   Stale pages: domains/pcb.md
```

The recorded `knowledge_snapshot` lets a reviewer see, after the fact,
that the agent had a valid but partially-stale knowledge layer, and which
specific page it discounted.
