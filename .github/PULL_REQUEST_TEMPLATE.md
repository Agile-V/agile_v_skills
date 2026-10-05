## Summary

Describe the problem and the smallest complete change.

## Validation

- [ ] Ran `python -m pytest tests -q`, or documented why it was unavailable and the manual checks performed
- [ ] Validated changed YAML/frontmatter, schemas, fixtures, links, and examples as applicable
- [ ] Kept the repository version in `package.json` unchanged

## Skill Contract Checks

- [ ] New or changed skills follow the required frontmatter and `# Instructions` structure
- [ ] Changed skill contracts have an appropriate `metadata.version` update
- [ ] Draft skills retain `metadata.status: draft` and are not presented as stable
- [ ] Traceability, independent verification, human gates, halt conditions, and rationale are preserved where applicable
- [ ] Adapted material includes complete source and license attribution
- [ ] No unsupported certification, conformity, performance, or compliance claims are introduced

## AI Influence

- [ ] No material AI influence, or an `AI_RUN_MANIFEST.yaml` was created/updated and linked to the evidence bundle without secrets or hidden reasoning

## Evidence and Risk

List test output, evidence locators, affected draft contracts, and unresolved risks. Write `None` where applicable.

## Normative Change (contracts, schemas, profiles, runtime docs, benchmark)

Answer or write `N/A`:

- What behavior changes?
- Is the change backward compatible?
- Which schema/contract version changes (`contracts/versions.yaml`)?
- Which positive test proves intended behavior?
- Which negative tests prove failure behavior?
- Does the conformance corpus / AgileV-Bench change (regenerate with `tools/build_agilev_bench.py`)?
- Does a runtime implementation need an update?
- Does an evidence profile need revalidation?
- [ ] Regenerated derived files: `tools/build_evidence_adapter_catalog.py`, `tools/build_agilev_bench.py`, `tools/build_release_manifest.py`
