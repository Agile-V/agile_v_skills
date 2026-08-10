# Agile V Outreach Kit

Reusable, factual copy for maintainers and contributors. Adapt each template to the venue and disclose your affiliation. This kit does not record or imply that any external submission has occurred.

## Repository Descriptions

### One-Line

Agile V is an open Agent Skills library for traceable requirements, independent verification, human approval gates, and auditable AI-assisted engineering evidence.

### Short

Agile V is a CC BY-SA 4.0 library of AgentSkills.io-compatible instructions for human-governed AI-assisted engineering. It connects baselined requirements to implementation, tests, independent verification, and release evidence, with profiles for common and regulated workflows.

### Long

Agile V is an open library of 45 Agent Skills for teams that want more structure around AI-assisted engineering. Its lifecycle persists and reviews requirements before build work, freezes approved baselines, separates implementation from test design and verification, records typed traceability, and stops for human approval at critical gates. The repository includes installation profiles, reusable evidence templates, JSON Schemas and validation fixtures, language-specific build skills, risk-scaled controls, intended-use validation, safety, security, release, and observability guidance. Some business, C-Suite, and AI provenance skills are explicitly marked draft and require local review. The materials can support quality and compliance processes but do not establish certification, regulatory approval, or organizational conformity.

## Release Announcement

```text
Agile V [VERSION] is available: [RELEASE URL]

This release [one sentence describing the user-visible change].

Highlights:
- [specific change with link]
- [specific change with link]
- [migration, compatibility, or draft-status note]

Agile V is an open Agent Skills library for traceable requirements, independent verification, human gates, and auditable engineering evidence. Start with the installation profiles: https://github.com/Agile-V/agile_v_skills/blob/main/docs/INSTALL_PROFILES.md

Feedback and reproducible issue reports are welcome: https://github.com/Agile-V/agile_v_skills/issues
```

Before publishing, replace every bracketed field, link to the exact release or tag, and state breaking changes and limitations plainly.

## Tutorial Announcements

Replace `[TUTORIAL TITLE]`, `[TUTORIAL URL]`, and `[specific outcome]`. Post only where the topic is relevant and follow each community's self-promotion rules.

### Hacker News

```text
Title: [TUTORIAL TITLE]: a traceable workflow for AI-assisted engineering

I maintain Agile V, an open library of Agent Skills for requirements, independent verification, and human approval gates. This tutorial walks through [specific outcome] and shows the evidence produced at each stage: [TUTORIAL URL]

I would value feedback on the workflow, especially where the controls feel incomplete or unnecessarily heavy.
```

### Reddit

```text
Title: Tutorial: [specific outcome] with traceable AI-agent evidence

Disclosure: I maintain Agile V. I wrote a practical walkthrough of [specific outcome], including baselined requirements, independent test design and verification, and the human approval points: [TUTORIAL URL]

The project is open under CC BY-SA 4.0. This is not a certification framework, and several preview skills are clearly marked draft. I am interested in concrete feedback from teams using coding agents in real repositories.
```

### LinkedIn

```text
AI-assisted engineering needs more than a successful generation step. It needs a record of what was requested, what changed, how it was checked, and who approved it.

This tutorial demonstrates [specific outcome] using Agile V's baselined requirements, typed traceability, independent verification, and human gates:
[TUTORIAL URL]

I maintain the project. It is open under CC BY-SA 4.0, and feedback on the workflow and evidence model is welcome.
```

### DEV Community

```text
Title: [TUTORIAL TITLE]

In this tutorial, we will [specific outcome] while preserving a reviewable chain from requirements through implementation, tests, and independent verification.

You will see:
- how to persist and approve a requirement baseline;
- how implementation and test design remain independent;
- which evidence supports the final human release decision.

Tutorial: [TUTORIAL URL]
Repository: https://github.com/Agile-V/agile_v_skills

Disclosure: I maintain Agile V. The materials support engineering governance; they do not establish compliance or certification.
```

## Directory or Awesome-List Submission

```text
Project: Agile V Agent Skills Library
Repository: https://github.com/Agile-V/agile_v_skills
Website: https://agile-v.org/
License: CC BY-SA 4.0
Category: Agent skills / AI-assisted software engineering / engineering governance

Suggested entry:
Agile V - AgentSkills.io-compatible skills for baselined requirements, typed traceability, independent verification, human approval gates, and auditable AI-assisted engineering evidence.

Why it fits this directory:
[One venue-specific sentence tied to the directory's inclusion criteria.]

Maintenance and scope:
The repository publishes releases and documentation, includes schemas and validation fixtures, and labels preview contracts with `metadata.status: draft`. It supports engineering and compliance processes but does not claim certification or regulatory approval.

Affiliation disclosure:
[State your relationship to the project.]
```

## Key Links

| Resource | URL |
|---|---|
| Repository | https://github.com/Agile-V/agile_v_skills |
| Website | https://agile-v.org/ |
| Releases | https://github.com/Agile-V/agile_v_skills/releases |
| Issues | https://github.com/Agile-V/agile_v_skills/issues |
| Documentation hub | https://github.com/Agile-V/agile_v_skills/blob/main/docs/README.md |
| Installation profiles | https://github.com/Agile-V/agile_v_skills/blob/main/docs/INSTALL_PROFILES.md |
| Golden Journey | https://github.com/Agile-V/agile_v_skills/blob/main/docs/GOLDEN_JOURNEY.md |
| Skill Routing Guide | https://github.com/Agile-V/agile_v_skills/blob/main/SKILL_ROUTING_GUIDE.md |
| Performance measurement | https://github.com/Agile-V/agile_v_skills/blob/main/PERFORMANCE.md |
| License | https://github.com/Agile-V/agile_v_skills/blob/main/LICENSE |

## Truthful Proof Points

Use only proof points that remain true at the linked revision.

| Proof point | Evidence |
|---|---|
| The v3.9.x catalog contains 45 skills. | [Skill Routing Guide](../SKILL_ROUTING_GUIDE.md) |
| Skills use AgentSkills.io-compatible Markdown and YAML frontmatter. | Individual `SKILL.md` files and the [AgentSkills.io specification](https://agentskills.io/specification) |
| Five documented installation profiles cover minimal, verified-build, existing-repository, regulated, and business-preview use. | [Installation Profiles](INSTALL_PROFILES.md) |
| The canonical lifecycle separates baselining, build, test design, independent verification, intended-use validation when applicable, and human release approval. | [Golden Journey](GOLDEN_JOURNEY.md) |
| Structured evidence contracts include JSON Schemas and valid/invalid test fixtures. | [`schemas/`](../schemas/) and [`tests/fixtures/schemas/`](../tests/fixtures/schemas/) |
| Domain build skills cover Python, JavaScript/TypeScript, NestJS, Dart/Flutter, and embedded C/C++. | [`domains/`](../domains/) |
| The project is licensed under CC BY-SA 4.0. | [License](../LICENSE) |
| Draft status is explicit in current frontmatter; draft skills are preview contracts requiring local review. | Each applicable `SKILL.md` and the [Skill Routing Guide](../SKILL_ROUTING_GUIDE.md) |
| Compliance materials describe support and gaps; they do not establish certification, approval, or organizational conformity. | [Documentation hub](README.md) and [`docs/compliance/`](compliance/) |
| Performance claims require identified inputs and reproducible methods. | [Performance Measurement](../PERFORMANCE.md) |

Do not convert these into claims of guaranteed quality, eliminated hallucinations, regulatory compliance, certification, production suitability, universal performance gains, or adoption by organizations unless separate current evidence supports the claim.

## Manual External Submission Checklist

This is a planning checklist, not a submission log. An unchecked or checked item must not be interpreted as evidence that a submission was accepted or even sent; record actual activity separately with URL and date.

### Preparation

- [ ] Confirm the target accepts maintainer submissions and projects under CC BY-SA 4.0.
- [ ] Read current submission, self-promotion, formatting, and disclosure rules.
- [ ] Verify the repository description, version, skill count, draft status, and links against the current revision.
- [ ] Select one venue-specific description rather than posting identical copy everywhere.
- [ ] Disclose maintainer or contributor affiliation.
- [ ] Check that the target category is relevant to agent skills, AI engineering, verification, or governance.
- [ ] Avoid tracking parameters unless the venue permits them and measurement requires them.

### AgentSkills Directories

- [ ] Identify active directories that explicitly accept AgentSkills.io-compatible skills.
- [ ] Check whether the directory lists repositories, individual skills, or both.
- [ ] Submit only the fields requested, using the directory template above.
- [ ] Distinguish current skills from draft preview skills.
- [ ] Record the submission URL and date only after a maintainer actually submits it.

### Awesome Lists

- [ ] Search existing agent-skills, AI agents, AI engineering, software quality, and developer-tools lists for duplicates.
- [ ] Verify the list's contribution policy and alphabetical or category ordering.
- [ ] Explain fit in one factual sentence; do not cite stars as a quality proxy.
- [ ] Open a focused pull request only when maintainer submissions are allowed.
- [ ] Record the pull request and outcome separately; do not imply inclusion while pending.

### Relevant Communities

- [ ] Confirm the tutorial or release directly answers the community's subject matter.
- [ ] Prefer a useful walkthrough, release detail, or technical discussion over a generic project link.
- [ ] Use the HN, Reddit, LinkedIn, or DEV variant as a starting point and adapt it to local norms.
- [ ] Do not cross-post repeatedly, manufacture engagement, or ask for votes, stars, or endorsements.
- [ ] Answer questions candidly, including limitations and draft status.
- [ ] Record where and when a post was actually published; do not claim publication beforehand.

### Follow-Up

- [ ] Respond to substantive feedback without pressuring users to adopt the project.
- [ ] Convert reproducible defects or documentation gaps into repository issues when appropriate.
- [ ] Remove or correct stale claims in future announcements.
- [ ] Review traffic in aggregate using [Growth Metrics](GROWTH_METRICS.md), without identifying or profiling visitors.
