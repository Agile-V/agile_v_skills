---
name: openwiki-agent
description: Uses the Agile-V OpenWiki knowledge layer (agilev wiki) before making changes to an existing repository, and keeps it current after changes. Wraps the external langchain-ai/openwiki CLI with Agile-V validation, freshness tracking, and evidence bundle integration.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  compliance: "Repository knowledge layer (informational; not a Human Gate)"
  author: agile-v.org
  companion_repo: agentic_agile_v
  companion_package: "src/agilev/wiki/"
  companion_docs: "docs/integrations/openwiki.md"
---

# Skill: openwiki-agent

## Purpose

Treat the repository's `openwiki/` documentation
(generated and maintained by [OpenWiki](https://github.com/langchain-ai/openwiki))
as a first-class, validated knowledge layer — not optional background reading.
This skill tells an agent when to consult it, when to trust it, when to flag
it as stale, and how to record that it was checked as part of the evidence
trail.

This is a **companion skill** to the `agilev wiki` CLI implemented in the
`agentic_agile_v` repository (`src/agilev/wiki/`). This skill does not
reimplement that logic; it tells the agent how and when to invoke it.

---

## Trigger conditions

Use this skill:

- At the start of any session that will change an **existing** repository
  (alongside/before `system-understanding-agent` if Understand Anything is
  also integrated).
- Before writing a task brief or impact analysis, to ground both in
  documented architecture rather than re-derived guesses.
- Whenever a repository contains an `openwiki/` directory or an
  `.agile-v/wiki/manifest.json` file.
- When a user asks "what does this repo's knowledge base say about X?",
  "is the wiki up to date?", or "check the docs before you touch this."
- Before closing out a task, to record a `knowledge_snapshot` in the
  evidence bundle.

Do **not** use this skill to generate `openwiki/` content itself — that is
the job of the real `openwiki` CLI (`openwiki --update`, run by a human or
by the scheduled `openwiki-update.yml` CI workflow). This skill governs how
an Agile-V agent *consults* and *proves the state of* that knowledge layer.

---

## Inputs

```text
- openwiki/**                              optional (repo may not have it yet)
- .agile-v/wiki/manifest.json               optional
- .agile-v/wiki/validation.json             optional
- .agentic-agile-v/tasks/<task_id>/         required for snapshot step
```

## Outputs

This skill does not produce new Markdown artifacts of its own. Its effect
is procedural:

- A recorded decision about whether the knowledge layer was consulted and
  trusted (in the agent's evidence summary / handoff notes).
- A `knowledge_snapshot` entry in the task's evidence bundle (via
  `agilev wiki snapshot --task <id>`).

---

## Required behavior

### Step 1: Check whether the knowledge layer exists

Run (or ask the user/CI to confirm):

```bash
agilev wiki status --json
```

- If `initialized` is `false` (no `openwiki/`): note this in the evidence
  summary as "no knowledge layer present" and proceed using normal
  repository exploration. Do not block on this — recommend
  `agilev wiki init` as a follow-up, but this skill's absence is never a
  Halt Condition on its own.
- If `initialized` is `true`: continue to Step 2.

### Step 2: Validate before trusting

```bash
agilev wiki validate --json
```

- `validation_passed: false` (structural failure — a required page is
  missing, or the manifest is out of sync with `openwiki/`): treat the
  knowledge layer as **unreliable**. Do not cite specific pages as
  authoritative until a human runs `agilev wiki update` (or fixes the
  missing page). Say so explicitly in your summary.
- `validation_passed: true` with `stale_pages` non-empty: the structure is
  sound, but specific pages may be out of date relative to code that
  changed since the manifest was recorded. Treat those specific pages'
  claims about the stale source paths with reduced confidence; other pages
  remain trustworthy.
- `validation_passed: true` with no stale pages: treat `openwiki/` as
  current and authoritative background context.

### Step 3: Read the relevant pages

Start with `openwiki/README.md` (index), then follow to the page(s)
relevant to the task:

| Task touches... | Read |
|---|---|
| CLI, state kernel, OpenHands integration | `openwiki/domains/software.md` |
| PCB design/circuit IR | `openwiki/domains/pcb.md` |
| Firmware build backend | `openwiki/domains/firmware.md` |
| Embedded/RTOS targets | `openwiki/domains/embedded.md` |
| Anything touching two or more hardware-adjacent domains | `openwiki/co-verification.md` |
| CI, evidence bundles, release gates | `openwiki/ci-and-release.md` |
| First session in this repo | `openwiki/ONBOARDING.md`, then `openwiki/ARCHITECTURE.md` |

Do not read pages unrelated to the current task just because they exist —
this skill exists to make context retrieval targeted, not exhaustive.

### Step 4: Record that the knowledge layer was checked

In your evidence summary or handoff notes, state:

- Whether `openwiki/` existed and was validated.
- Which pages you relied on.
- Any pages you explicitly distrusted due to staleness or validation
  failure, and why.

### Step 5: Snapshot at task close (if a task ID exists)

```bash
agilev wiki snapshot --task <task_id>
```

This writes a `knowledge_snapshot` object into the task's evidence file
(`evidence.json` or `evidence_bundle.json`), so a reviewer can see, after
the fact, whether the knowledge layer was valid and current when the agent
relied on it.

---

## Anti-patterns to avoid

- Do not treat `openwiki/` content as ground truth without checking
  `agilev wiki validate` first — a stale or structurally broken wiki is
  worse than no wiki if trusted blindly.
- Do not block or fail a task solely because `openwiki/` is missing or
  stale; this is an informational/supporting skill, not a Human Gate.
- Do not attempt to hand-edit `openwiki/` pages to "fix" staleness —
  content generation is the real `openwiki` CLI's job
  (`openwiki --update`), not this skill's.
- Do not run `openwiki --init`/`--update` (the real, LLM-backed CLI)
  automatically mid-session without explicit user request; it requires an
  API key and produces real content changes. `agilev wiki init/update`
  (Agile-V's own scaffolding/manifest recompute, no LLM call) are safe to
  run freely.
- Do not skip recording the `knowledge_snapshot` for L2+ tasks — reviewers
  use it to judge whether the agent had accurate context.

---

## Compatible tools

Claude Code, Cursor, Copilot, Codex, Gemini CLI, OpenCode, Cline.

## See also

- `../../integrations/openwiki/README.md` — CLI command reference and
  evidence mapping
- `agentic_agile_v` repo: `src/agilev/wiki/`, `docs/integrations/openwiki.md`
