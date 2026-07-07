# Expected Artifacts: openwiki-agent

This skill does not produce its own Markdown deliverables; it governs
procedure and evidence. Verify these artifacts/effects instead:

| Artifact / effect | Location | Required when |
|---|---|---|
| `knowledge_snapshot` object | `.agentic-agile-v/tasks/<id>/evidence.json` or `evidence_bundle.json` | Task has a task ID and reaches evidence-collection stage, and `openwiki/` exists |
| Evidence summary mentions whether the wiki was consulted/trusted | Agent's final summary / handoff notes | Every session where `openwiki/` or `.agile-v/wiki/` is present |
| No unsolicited edits to `openwiki/**` | Diff / changed files list | Always (unless the user explicitly asked the agent to run `openwiki --update`) |

## Example `knowledge_snapshot` (for reference)

```json
{
  "knowledge_snapshot": {
    "wiki_dir": "openwiki",
    "manifest_generated_at": "2026-07-07T18:45:04.579068+00:00",
    "page_count": 6,
    "pages": ["ARCHITECTURE.md", "ONBOARDING.md", "README.md", "ci-and-release.md", "domains/pcb.md", "domains/software.md"],
    "required_pages": ["README.md", "ARCHITECTURE.md", "ONBOARDING.md", "domains/software.md", "ci-and-release.md", "domains/pcb.md"],
    "validation_passed": true,
    "validation_errors": [],
    "validation_warnings": [],
    "stale_pages": [],
    "captured_at": "2026-07-07T18:45:10.612224+00:00"
  }
}
```

See `../../../integrations/openwiki/examples/knowledge_snapshot_example.md`
for a fuller worked example including a stale/failed case.
