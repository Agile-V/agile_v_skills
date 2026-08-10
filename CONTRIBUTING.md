# Contributing

Thank you for improving the Agile V Agent Skills Library. Contributions are licensed under [CC BY-SA 4.0](LICENSE).

## Before You Start

- Search existing issues and pull requests. Use the skill proposal form for a new skill.
- Keep changes concise, stage-focused, and consistent with `AGENTS.md`.
- Do not describe a draft skill as stable. A skill is draft only when its frontmatter contains `metadata.status: draft`.
- Do not claim certification, conformity, or guaranteed compliance. Describe evidence or alignment precisely.

## Skill Requirements

Each skill belongs in a matching kebab-case directory with one `SKILL.md`. It must contain YAML frontmatter with `name`, `description`, `license: CC-BY-SA-4.0`, and quoted `metadata.version`, plus `metadata.standard` and `metadata.author`. The first heading must be `# Instructions`.

Use the repository ID conventions (`REQ-XXXX`, `ART-XXXX`, `TC-XXXX`), typed lineage, halt-on-ambiguity behavior, independent verification, human gates, and decision rationale. Prefer cross-references over duplicated contracts. Add `adapted_from` attribution when applicable.

If a skill contract changes, update that skill's `metadata.version`. Do not edit the repository version in `package.json`; release automation owns it.

## Submit a Change

1. Create a focused branch and make the smallest complete change.
2. Run `python -m pytest tests -q` when Python and the dependencies in `requirements-test.txt` are available. Otherwise, state the manual validation performed.
3. Validate changed YAML frontmatter, templates, schemas, links, and examples.
4. When AI materially influences an artifact, create or update `AI_RUN_MANIFEST.yaml` using `templates/AI_RUN_MANIFEST.yaml`, link it to the evidence bundle, and exclude hidden reasoning, secrets, keys, and unredacted proprietary prompts.
5. Use a [Conventional Commit](https://www.conventionalcommits.org/) title, such as `feat(skills): add rust build agent` or `fix(compliance): correct gate wording`.
6. Complete the pull request template and identify draft contracts, tests, evidence, attribution, and unresolved risks.

Maintainers may request changes or decline proposals that duplicate existing skills, lack traceability, weaken role separation, or make unsupported assurance claims.
