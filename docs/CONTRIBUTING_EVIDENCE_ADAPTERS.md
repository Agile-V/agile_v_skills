# Contributing Evidence Adapters

Evidence adapters are **policy-side capability profiles** in the [Evidence Adapter Registry](agile-v-runtime/15_EVIDENCE_ADAPTER_REGISTRY.md). They state what a tool's evidence may and may not establish. They do not rate tool quality.

## Required contribution evidence

A new adapter PR MUST include:

1. Authoritative tool documentation (link in `references`).
2. The exact evidence format and a redacted sample (`tests/fixtures/evidence-adapters/<slug>/`).
3. Supported tool/version scope (`source_version_scope`).
4. `may_establish`.
5. `may_not_establish` (including the five authority/validation properties).
6. Known limitations (true, specific statements).
7. At least one positive fixture: a bundle the profile admits.
8. At least three negative/overclaim fixtures: e.g. claiming a `may_not_establish` property, wrong `evidence_type`, missing locator, unsupported version.
9. Owner (`Agile-V` maintainers by default).
10. Freshness/revalidation assumptions (`freshness.invalidated_by`).

Start from [`templates/evidence-source-profile.yaml`](../templates/evidence-source-profile.yaml) and [`templates/evidence-property-profile.yaml`](../templates/evidence-property-profile.yaml), then run:

```bash
python tools/build_evidence_adapter_catalog.py
python tools/build_release_manifest.py
python -m pytest tests -q
```

## Review rule

A vendor's own contribution is not trusted because the vendor authored it. Repository maintainers (CODEOWNERS for `/profiles/`) approve the Agile-V capability profile. A contributor cannot self-authorize: the builder rejects contradictory capability sets, every profile must deny authority/validation properties, and admission never reads a profile from evidence.

## Status model

| Status | Meaning | Resolvable for current decisions |
|---|---|---|
| `experimental` | New or unreviewed against real output | No |
| `candidate` | Maintainer-reviewed with positive and overclaim fixtures | Yes |
| `stable` | Candidate plus independent review against real tool output and one release without changes | Yes |
| `deprecated` | Superseded; kept for historical resolution by digest | No (historical only) |

Promotion follows the same evidence-based philosophy as the [Skill Graduation Policy](agile-v-runtime/13_SKILL_GRADUATION_POLICY.md).

## Review checklist

- [ ] `may_establish` and `may_not_establish` are disjoint and justified by the format
- [ ] No property implies human authority, independence, intended-use validation or compliance
- [ ] Locators are sufficient to retrieve and re-verify the evidence
- [ ] Version scope is as narrow as the evidence supports
- [ ] Positive and >= 3 negative fixtures pass through `evaluate_evidence_bundle_against_registry`
- [ ] Catalog and release digests regenerated
