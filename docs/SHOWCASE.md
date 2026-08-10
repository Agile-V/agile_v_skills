# Agile V Showcase Submissions

Case studies help others understand how Agile V was tailored and what evidence supported the reported result. A showcase is not an endorsement, certification, regulatory approval, or proof that the same outcome will occur elsewhere.

## How to Submit

Propose a repository contribution through the project's normal issue or pull-request workflow. Before publishing, confirm that your organization and relevant data owners authorize disclosure. Maintainers may request clarification, narrower claims, more evidence, or further redaction.

Use this structure:

```markdown
# Case Study: [descriptive title]
## Context and intended use
## Scope, baseline, and Agile V version
## Risk classification and rationale
## Tailoring and roles
## Workflow and human gates
## Verification evidence
## Intended-use validation, if performed
## AI influence and runtime provenance
## Results and measurement method
## Limitations, deviations, and open risks
## Evidence index and redaction statement
```

## Required Evidence

| Claim area | Minimum support |
|---|---|
| Scope and requirements | Baseline identifier, relevant `REQ-XXXX` revisions, configuration, and exclusions |
| Risk and decisions | `L0`-`L4` rationale, controls, decision owners, and residual-risk disposition |
| Verification | Independent role, `VER-XXXX` summary, procedure or command, expected/actual results, and evidence locators |
| Intended-use validation | Representative users/environment/data, protocol, limitations, and `VALIDATION_REPORT.md`; omit the claim if not performed |
| AI influence | Redacted manifest fields, model/runtime/tool/skill versions, affected artifacts, and evidence-fragment locator when material |
| Outcomes | Defined metric, baseline/comparator, collection period, sample size where relevant, and reproducible calculation method |

Label `agile-v-aibom` as **draft/preview** if it was used. Keep `.agile-v/VERIFICATION_SUMMARY.md` distinct from `VALIDATION_REPORT.md`, and state the applicable risk level rather than implying uniform rigor across all work.

## Redaction and Safety

Remove secrets, API keys, credentials, personal or patient data, customer-confidential content, proprietary prompts, hidden chain-of-thought, exploitable security details, and data you lack permission to publish. Replace content with stable markers such as `[REDACTED: credential]`, retain enough metadata to understand the evidence type, and state who performed the redaction and why.

Do not fabricate hashes, approvals, test results, runtime observations, independence, or missing evidence. If evidence cannot be shared, describe its type, custodian, review status, and access limitation; maintainers and readers may treat the claim as unverified.

Use bounded language such as "the recorded tests passed for configuration X on date Y." Do not claim certification, universal safety, compliance, productivity gains, or quality improvements without the authority and reproducible evidence needed for that claim.

See [Tutorials](tutorials/README.md) for canonical workflow examples and [Comparisons](COMPARISONS.md) for positioning guidance.
