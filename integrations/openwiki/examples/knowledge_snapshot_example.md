# Example: `knowledge_snapshot` in an evidence bundle

## Passing, fully fresh

```json
{
  "task_id": "AAV-0001",
  "title": "Integrate OpenWiki as repository knowledge layer",
  "task_type": "feature",
  "risk_level": "L2",
  "requirement_ids": ["REQ-0001", "REQ-0005"],
  "changed_files": ["src/agilev/wiki/cli.py"],
  "tests": [{"name": "wiki unit tests", "command": "pytest tests/unit/wiki", "result": "pass"}],
  "checks": [{"name": "lint", "command": "ruff check src/agilev/wiki", "result": "pass"}],
  "knowledge_snapshot": {
    "wiki_dir": "openwiki",
    "manifest_path": ".agile-v/wiki/manifest.json",
    "manifest_generated_at": "2026-07-07T18:45:04.579068+00:00",
    "page_count": 6,
    "pages": [
      "ARCHITECTURE.md",
      "ONBOARDING.md",
      "README.md",
      "ci-and-release.md",
      "domains/pcb.md",
      "domains/software.md"
    ],
    "required_pages": [
      "README.md",
      "ARCHITECTURE.md",
      "ONBOARDING.md",
      "domains/software.md",
      "ci-and-release.md",
      "domains/pcb.md"
    ],
    "validation_passed": true,
    "validation_errors": [],
    "validation_warnings": [],
    "stale_pages": [],
    "captured_at": "2026-07-07T18:45:10.612224+00:00"
  }
}
```

## Structural failure (do not trust for this task)

```json
{
  "knowledge_snapshot": {
    "wiki_dir": "openwiki",
    "manifest_path": ".agile-v/wiki/manifest.json",
    "manifest_generated_at": null,
    "page_count": 0,
    "pages": [],
    "required_pages": ["README.md", "ARCHITECTURE.md", "ONBOARDING.md", "domains/software.md", "ci-and-release.md"],
    "validation_passed": false,
    "validation_errors": [
      "openwiki/ does not exist. Run 'agilev wiki init' to scaffold it."
    ],
    "validation_warnings": [],
    "stale_pages": [],
    "captured_at": "2026-07-07T19:00:00+00:00"
  }
}
```

An agent seeing `validation_passed: false` should not cite `openwiki/`
pages as authoritative for this task, and should recommend
`agilev wiki init` as a follow-up rather than treating it as blocking.
