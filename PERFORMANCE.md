# Agile V Skills 3.8.x Measurement Guide

This repository does not publish universal token, latency, quality-zone, throughput, or efficiency guarantees. Those values depend on the exact revision, selected files, tokenizer, model, agent runtime, tool behavior, context policy, project evidence, and cache state.

## What Can Be Measured Reproducibly

| Measure | Definition | Required report fields |
|---|---|---|
| Bytes | Raw UTF-8 byte count of each loaded file | commit/tag, path, byte count |
| Lines | Physical line count using one stated tool | commit/tag, path, tool/version, line count |
| Tokens | Tokens produced by a named tokenizer over exact file bytes | commit/tag, paths, tokenizer/model/version, per-file and total counts |
| Load set | Exact skill and supporting files supplied to an agent for one stage | profile, paths, inclusion order, full vs selected sections |
| Runtime | Wall-clock duration for a defined scenario | hardware, runtime/model, cache state, repetitions, raw samples |
| Outcome | Pass/fail against a versioned evaluation suite | suite revision, policy thresholds, results, failures, waivers |

File size is not model quality, execution speed, or task cost. A `sections_index` is navigation metadata; it does not prove that a host loads only selected sections. Referencing an artifact by path defers content loading but does not make project-scale context cost constant.

## Reproducible Procedure

1. Check out a clean, identified commit or tag and record `git rev-parse HEAD`.
2. Declare the profile and exact paths under measurement. Include supporting files such as C-Suite primitives if the runtime loads them.
3. Hash each input file and preserve the ordered path list.
4. Measure bytes and lines with stated tool versions.
5. For token counts, use the production model's documented tokenizer when available. Record tokenizer package, version, encoding, normalization, and special-token settings. If unavailable, label any estimate as an estimate and state the formula.
6. For runtime or quality comparisons, define a fixed task corpus, hardware/runtime, model parameters, tool permissions, cache state, and policy. Run enough repetitions to report raw samples plus median and spread.
7. Store commands, environment metadata, raw output, exclusions, and date with the report so another person can repeat it.

Example inventory commands on macOS/Linux:

```bash
git rev-parse HEAD
wc -c -l agile-v-core/SKILL.md requirement-architect/SKILL.md logic-gatekeeper/SKILL.md
shasum -a 256 agile-v-core/SKILL.md requirement-architect/SKILL.md logic-gatekeeper/SKILL.md
```

Tokenizer commands are intentionally not prescribed because this repository has no tokenizer dependency and model tokenization differs. Do not use a generic bytes-to-tokens ratio as measured data.

## Comparison Rules

- Compare identical task corpora and evidence obligations; do not compare a compact skill to an unspecified body of “equivalent documentation.”
- Separate prompt/input tokens, generated/output tokens, tool-return tokens, and persisted artifacts where the runtime exposes them.
- Report cold and warm cache runs separately.
- Treat parallel execution as a scheduling strategy, not an automatic speedup; dependencies, contention, edits, and rate limits can reduce or reverse gains.
- Publish negative and failed runs. Do not infer “zero information loss,” “peak quality,” or scalability from file compression alone.
- Re-run measurements after skill, profile, runtime, model, tokenizer, or evaluation-suite changes.

## Current Guidance

Load only the stage-relevant profile from [Installation Profiles](docs/INSTALL_PROFILES.md), pass durable evidence by path, and use fresh independent contexts where the lifecycle requires independence. These are context-management practices, not quantified performance claims.
