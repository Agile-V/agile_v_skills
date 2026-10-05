# AgileV-Bench v0.1

A public, reproducible adversarial corpus for assurance decisions in AI-assisted engineering: **108 cases** across state binding, policy binding, evidence capability, contradiction, approvals, independence, exceptions, revalidation, delegation, context trust, AI provenance and cross-domain (software, firmware, PCB) transitions.

## Three different things -- do not conflate

| Result kind | Meaning |
|---|---|
| Unit test | A repository test passed. |
| **Reference semantic result** | `contracts.semantics` (this repository's reference evaluator) reproduces the declared expectation. This is what `tools/run_agilev_bench.py` produces. |
| Live runtime / platform benchmark | A released runtime or agent platform was run against the corpus and scored. **None is published for v0.1.** |

A reference result says nothing about how any runtime or agent platform behaves.

## Layout

| Path | Content |
|---|---|
| `VERSION` | Corpus version |
| `cases/<category>/AVB-*.json` | Self-contained cases (candidate `input`, `trusted` provider data, `expected`) |
| `manifests/v0.1.json` | Case list with per-case SHA-256 and the immutable `corpus_digest` |
| `benchmark.schema.json` / `result.schema.json` | Case and per-case result schemas |

Cases are generated from repository fixtures by declared mutations (`tools/build_agilev_bench.py`). Expected outcomes are declared by the generator, not computed by the reference evaluator; CI checks that the reference evaluator reproduces them and that the committed corpus matches its manifest.

## Expected outcomes

`expected.status` is `admitted`, `rejected` or `proposed`. For `rejected` cases, `expected.reason_codes` is the **minimum** set of reason codes a conforming evaluator must report (it may report more). Admitted/proposed cases expect no reason codes.

## Running

```bash
python tools/build_agilev_bench.py --check                # corpus matches generator + manifest
python tools/run_agilev_bench.py --results ref.jsonl       # reference semantics + metrics
python tools/run_agilev_bench.py --score my-runtime.jsonl  # score an external runtime's results
```

An external runtime reads each case file, evaluates `input` using only `trusted` as its trusted-provider data (operation semantics: `docs/agile-v-runtime/`), and writes one `result.schema.json` object per line. Missing cases count as not executed, never as passes.

## Metrics

`false_authorize_rate` (expected reject, actually admitted/proposed), `false_reject_rate`, `status_agreement`, `reason_code_agreement`, `tamper_detection_rate` (cases tagged `tamper`), `revalidation_precision`, `case_coverage`. Optional live metrics: latency, token cost, human review time.

## Versioning

The corpus digest in `manifests/v0.1.json` is immutable for v0.1. Any case change produces a new corpus version.
