# Evidence Adapter Registry

**Contract version: 1.0.** Registry key `evidence_adapter_registry` in [`contracts/versions.yaml`](../../contracts/versions.yaml).

> **Normative.** Defines the reviewed, digest-pinned registry of evidence-source and evidence-property profiles for real engineering tools. Refines the [Evidence Admission Contract](07_EVIDENCE_ADMISSION_CONTRACT.md) §5.1 and the [Trusted Admission Context](14_TRUSTED_ADMISSION_CONTEXT.md). Adapters describe **what a tool's evidence is capable of establishing**, not the quality of the tool.

## 1. Layout

| Path | Content | Owner |
|---|---|---|
| `profiles/evidence-sources/<slug>.yaml` | Active source profile (`EVIDENCE_SOURCE_PROFILE` envelope) | Assurance maintainers |
| `profiles/evidence-sources/history/` | Superseded snapshots, byte-identical, resolvable by digest only | Assurance maintainers |
| `profiles/evidence-properties/<slug>.yaml` | Property profile (`EVIDENCE_PROPERTY_PROFILE` envelope) | Assurance maintainers |
| `profiles/evidence-*-registry-entry.schema.json` | Registry overlay schemas (stricter than storage schemas) | Assurance maintainers |
| `catalog/evidence-adapters.json` | Generated catalog: id, path, digest, status, owner | Generated (`tools/build_evidence_adapter_catalog.py`) |

Storage schemas (`schemas/EVIDENCE_SOURCE_PROFILE.schema.json`, `schemas/EVIDENCE_PROPERTY_PROFILE.schema.json`) are unchanged; registry entries must satisfy both the storage schema and the overlay.

## 2. Profile fields

| Field | Rule |
|---|---|
| `adapter_id` | `EAD-<slug>-v<N>`; equals file name. A content change that alters meaning gets a new major `vN`. |
| Digest | `contracts.semantics.profile_digest(envelope)`; never embedded in the profile itself. Pinned in the catalog. |
| `owner` / `fixture_owner` | Accountable maintainer group. A tool vendor is never the owner by virtue of authorship. |
| `status` | `experimental`, `candidate`, `stable`, `deprecated`. Only `candidate`/`stable` resolve for current decisions. |
| `source_version_scope` | Tool, evidence format and `supported_versions` (`*` or `>=a,<b` clauses). Outside scope rejects. |
| `evidence_type` | Must equal the evidence item's `evidence_type`. |
| `may_establish` / `may_not_establish` | Disjoint. Every profile lists `human_authority`, `organizational_independence`, `independent_verification`, `intended_use_validation`, `regulatory_compliance` under `may_not_establish`. |
| `minimum_evidence_locators` | Keys that `evidence_source.locators` must carry with non-empty values. |
| `freshness` | `invalidated_by` dependency kinds (aligned with [Change-Aware Revalidation](10_CHANGE_AWARE_REVALIDATION.md)); optional `max_age_days`. |
| `known_limitations` | True, specific statements. Required. |
| `supersedes` / `superseded_by` | Digest links. History files keep their original bytes. |

## 3. Governance rule

Profiles are **policy-side artifacts**. An evidence producer MUST NOT be able to edit, select or supply the profile that defines what its evidence may establish during the same task. Concretely:

1. Admission resolves profiles only from the trusted registry (`EvidenceAdapterRegistry`), never from the evidence item.
2. An evidence item carrying a profile-like object (`profile`, `adapter_profile`, `source_profile`, `may_establish`) in `evidence_source` is rejected with `EVIDENCE_SOURCE_SELF_SUPPLIED_PROFILE`.
3. Registry files that do not match their catalog digest make the registry unloadable (`RegistryIntegrityError`) -- fail closed, never "use what is on disk".
4. Changes to `profiles/` require CODEOWNER review (`.github/CODEOWNERS`).

## 4. Evaluation

`evaluate_evidence_bundle_against_registry(bundle, registry, historical=False)` runs the canonical `evaluate_evidence_bundle` with the registry's resolvers and adds:

| Code | Trigger |
|---|---|
| `EVIDENCE_SOURCE_SUPERSEDED` | Item bound to a historical/deprecated snapshot in a current-decision evaluation. |
| `EVIDENCE_SOURCE_TOOL_VERSION_UNKNOWN` | Scope is not `*` and `evidence_source.tool_version` is absent. |
| `EVIDENCE_SOURCE_TOOL_VERSION_UNSUPPORTED` | `tool_version` unparseable or outside `supported_versions`. |
| `EVIDENCE_LOCATOR_MISSING` | A `minimum_evidence_locators` key is absent or empty. |
| `EVIDENCE_SOURCE_SELF_SUPPLIED_PROFILE` | See §3 rule 2. |

Inherited codes (`EVIDENCE_SOURCE_UNRESOLVED`, `EVIDENCE_SOURCE_DIGEST_MISMATCH`, `EVIDENCE_SOURCE_IDENTITY_MISMATCH`, `EVIDENCE_PROPERTY_OVERCLAIM`, `EVIDENCE_ADMISSION_INCONSISTENT`, ...) keep their [aggregate-semantics](14_TRUSTED_ADMISSION_CONTEXT.md) meaning.

## 5. Property profiles

`resolve_property_profile(claim_type, risk_level)` selects exactly one non-deprecated profile; the builder rejects ambiguity. Registry v1 ships `requirement_satisfaction` L0-L4, `static_security_analysis` L2, `hardware_electrical_rule_check` L3 and `firmware_hil` L4. `requirement_satisfaction` L4 and `firmware_hil` L4 require properties (`independent_verification`, `hil_execution`, `physical_measurement`) that **no v1 tool adapter can establish**; such claims fail closed until a reviewed source exists.

## 6. Supersession and historical resolution

1. Move the old file unchanged to `history/<slug>@<digest-prefix>.yaml`.
2. Write the new active profile with `supersedes: <old digest>`.
3. Regenerate the catalog; the history entry has `historical: true`.
4. `historical=True` evaluation resolves each `adapter_ref` to the snapshot whose digest the evidence is bound to (`historical_adapter_resolver`). Conflicting or unregistered digests resolve to nothing.

Historical validity is not current reuse eligibility; reuse remains governed by Change-Aware Revalidation.

## 7. Contribution

Third-party adapters follow [`docs/CONTRIBUTING_EVIDENCE_ADAPTERS.md`](../CONTRIBUTING_EVIDENCE_ADAPTERS.md). New profiles start as `experimental`; promotion to `candidate`/`stable` is a maintainer decision with positive and overclaim fixtures. All v1 profiles are `candidate` or `experimental`: none is `stable` until reviewed against real tool output by an independent maintainer.

## 8. Non-claims

Registry membership does not certify a tool, does not establish runtime enforcement by any agent platform, and does not make tool output admissible without the aggregate checks above.
