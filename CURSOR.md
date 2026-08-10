# Agile V for Cursor

Agile V works best in Cursor as Agent Skills. The individual `SKILL.md` files are authoritative; Cursor project rules are only a lightweight foundation.

## Bundled Rule

This repository bundles exactly one Cursor rule: [`.cursor/rules/agile-v-core.mdc`](.cursor/rules/agile-v-core.mdc). It has `alwaysApply: true` when this repository is opened in Cursor. No build-agent, verifier, domain, or other `.mdc` rule files are bundled.

## Install Agent Skills

Choose the smallest complete [installation profile](docs/INSTALL_PROFILES.md), then copy its listed skill directories into a Cursor-supported skill-discovery location such as project-local `.cursor/skills/` or the corresponding user-level directory.

For example, install `core-minimal` from a checkout:

```bash
mkdir -p .cursor/skills
cp -R agile-v-core requirement-architect logic-gatekeeper .cursor/skills/
```

For implementation, prefer `verified-build` or `existing-repo` and add one domain directory such as `domains/build-agent-python`. Copy nested existing-repository skills from `skills/` as individual directories. Do not invent `.cursor/rules/*.mdc` equivalents; copy the Agent Skills directories containing their authoritative `SKILL.md` contracts.

Available profiles:

| Profile | Use |
|---|---|
| `core-minimal` | Requirements and review |
| `verified-build` | Baselined build and independent verification |
| `existing-repo` | Understanding, impact, regression, and diff evidence |
| `regulated` | Risk-scaled assurance and release evidence |
| `business-preview` | Locally reviewed draft business contracts |

See [Installation Profiles](docs/INSTALL_PROFILES.md) for exact directory sets and [Skill Routing](SKILL_ROUTING_GUIDE.md) for stage-specific selection. Load `agile-v-core` first.

## Optional Project Rule

To apply the lightweight core rule in another repository, copy only [`.cursor/rules/agile-v-core.mdc`](.cursor/rules/agile-v-core.mdc) into that repository's `.cursor/rules/`. This does not install the full skill contracts.

## Verify

Ask Cursor to list or load `agile-v-core`, then request an ambiguous implementation such as “add login.” A working installation should halt, ask for missing scope and acceptance criteria, and persist requirements before creating implementation artifacts.

Continue with the [Golden Journey](docs/GOLDEN_JOURNEY.md), [examples](EXAMPLES.md), or [tutorials](docs/tutorials/README.md).

**License:** CC-BY-SA-4.0 | **Author:** Agile V™
