# Tutorial — GxP Qualification Pilot

> **Status:** Draft guidance for the `agile-v-gxp-qualification` skill.
> This Agile V profile supports structured qualification and validation evidence. It does not determine legal applicability, replace controlled procedures, provide technical Part 11 controls, or establish regulatory compliance.

This pilot walks a controlled qualification through DQ → IQ → OQ → PQ for a representative regulated system, and separately for the Agile V assurance toolchain. It uses no proprietary or personal data.

## 0. Decide applicability

Applicability is decided by the **local quality profile**, not by Agile V delivery level. Confirm with quality/CSV personnel whether GxP qualification applies. L0-L4 only scale rigor once applicability is established.

## 1. Plan and tailor

1. Load `agile-v-core`, then `agile-v-gxp-qualification`, `agile-v-control-matrix`, and `agile-v-compliance`.
2. Choose an install profile: `gxp-lean-csa`, `gxp-standard`, or `gxp-high-assurance` (see `docs/INSTALL_PROFILES.md`).
3. Author a `QUALIFICATION_PLAN` identifying the **subject** (`target_system` vs `assurance_toolchain` — keep these separate), required stages, and rationale for any omitted stage. **Approve the plan before executing controlled protocols.**
4. Capture a `SYSTEM_DESCRIPTION` distinguishing standard / configured / custom / external-service / manual functionality.

## 2. DQ — independent design review

An independent reviewer (not the builder) evaluates the design against the approved URS and constraints, producing a `DQ_REPORT.md`. A DQ PASS means only that the reviewed design is acceptable against the stated scope — it does not qualify installation or operation.

## 3. IQ — installation and configuration

1. Capture a controlled `SYSTEM_BASELINE` (hashes/identifiers only — **never secret values**).
2. Execute IQ checks against that named baseline. Unsupported platforms or unresolved critical patch status block release unless a documented, authorized risk decision exists.

## 4. OQ — requirement-derived operation

`test-designer` designs OQ tests from approved baselined requirements (tag `qualification_stage: OQ`, `gxp_critical`). `red-team-verifier` verifies IQ preconditions, executes/challenges the approved protocol, and preserves failures. OQ verifies operation against specification — **it does not establish PQ**.

## 5. PQ — representative intended-use validation

`validation-agent` defines representative users, workflow, environment, configuration, production-like data (or a qualified-substitute rationale), and operating range. Conclusions are bounded to tested conditions. An AI agent MUST NOT self-authorize residual-risk acceptance.

## 6. Summary and release

`compliance-auditor` produces the `QUALIFICATION_SUMMARY`, leading with unexpected changes, failures/inconclusive results, open deviations, evidence gaps, residual risks, and recovery limitations *before* passing coverage. It distinguishes PASSING TESTS vs STAGE ACCEPTANCE vs INTENDED-USE ACCEPTANCE vs REGULATORY/QUALITY RELEASE AUTHORITY. `release-manager` blocks release when required stages are incomplete or conditionally accepted without satisfied conditions.

## 7. Toolchain pilot (seeded conditions)

Separately qualify the Agile V toolchain configuration. Run a production-representative pilot seeded with: an ambiguous requirement, a missing critical requirement, an incorrect implementation, a builder-written inadequate test, a correlated verifier error, scope expansion, forged provenance, a failed rollback prerequisite, unrepresentative PQ data, and an unauthorized approval. Record whether the controlled configuration halts, blocks, or flags each. Keep conclusions bounded to the tested model/runtime versions and task classes.

## 8. Requalification

On any change trigger (patch, configuration, supplier, interface, intended-use, model/runtime/skill change, periodic interval), create a `REQUALIFICATION_ASSESSMENT` selecting one outcome from document review through full DQ/IQ/OQ/PQ or retirement.
