# Safety Assurance Profiles

> **Status:** Informational public-scope profiles
> **Checked:** 2026-07-30
> **Sources:** [SRC-SAF-01 to SRC-SAF-07](SOURCE_REGISTER.md)

## Boundary

Safety work requires competent, domain-authorized personnel and the applicable controlled/licensed text. These profiles are not safety cases, hazard analyses, independence plans, tool qualification evidence, certification evidence, or permission to deploy. Agile-V supports traceability and review mechanics; it does not determine safety integrity/classification, make a product safe, or grant regulatory/product approval.

## Profiles

| Domain / source | Profile trigger and focus | Agile-V artifacts | Mandatory project decision point |
|---|---|---|---|
| Automotive: ISO 26262:2018 | Item definition, HARA, safety concepts, ASIL allocation, confirmation | Item/hazard analysis; safety requirements; allocation/traceability; verification and confirmation evidence | Functional-safety authority approves item, HARA, ASIL and safety concept before implementation |
| Generic functional safety: IEC 61508:2010 | Safety functions, SIL lifecycle, independence, validation, modification | Safety plan; hazard/risk records; safety requirements; validation and modification impact records | Safety authority selects SIL and independence/validation approach; unresolved hazards block release |
| Medical software: IEC 62304:2006+A1:2015 | Software safety class, SOUP, problem resolution, maintenance, medical-risk links | Classification rationale; SOUP inventory; risk-control traceability; problem-resolution and maintenance records | Qualified medical-device/QMS reviewer approves classification, risk controls, and release evidence |
| Aviation: DO-178C / DO-330 | Plans, lifecycle data, independence, coverage, configuration index, tool qualification | Certification plans/data index; requirement/design/code/test traceability; review independence; tool evidence | Certification authority/applicant process governs level, plans, coverage and tool-qualification decisions |
| Railway: EN 50716:2023 | Railway software lifecycle and assurance; legacy EN 50128/50657 only when contractually invoked | Safety plan; software requirements/design/test/configuration records; hazard interfaces | Railway safety/assurance authority confirms applicable standard, national adoption, and contract basis |
| Automotive process: Automotive SPICE 4.0 | Process outcomes and evidence indicators; distinct from safety compliance | Process assessment plan; work-product/evidence index; improvement actions | Qualified assessor selects scope and rating method; do not present assessment as safety certification |
| US medical QMS: FDA QMSR / CSA | QMS and risk-based assurance of production/QMS software; not a shortcut for product software | QMS applicability record; software-assurance rationale; validation evidence | Qualified regulatory/QMS reviewer confirms scope, effective dates, and product-software obligations |

## Common Safety Gate Pattern

| Point | Required outcome |
|---|---|
| Before Gate 1 | Named safety authority; approved scope, hazard source, classification method, and applicable profile |
| Before implementation | Approved safety requirements, risk controls, independence plan, and traceability baseline |
| Before Gate 2 / release | Independent verification, unresolved-anomaly disposition, residual-risk decision, configuration/evidence baseline |
| After change | Impact analysis; retest/revalidation scope; safety authority decision before reuse or release |

Use `RISK_REGISTER.md`, `DECISION_LOG.md`, `REVALIDATION_LOG.md`, `TEST_SPEC.md`, `EVAL_RESULTS.md`, and an independent verifier as supporting records. Keep safety risk, cybersecurity, privacy, supplier, tool, and AI risks distinct but linked. A risk acceptance is a documented accountable decision, not an automated gate result.
