# Attribution and Source Index

This index identifies material external sources and distinguishes adapted content from inspiration, interoperability references, and public standards sources. It is not a complete license analysis.

## Authoritative Attribution Records

- For adapted skill content, the authoritative record is the skill's YAML `metadata.adapted_from` entry, including source, license, copyright, and adapted sections.
- For the NestJS upstream material, see `domains/build-agent-nestjs/NOTICE.md` and the skill's `metadata.upstream` entry.
- For standards, regulations, editions, source status, and public publisher or regulator links, see `docs/standards/SOURCE_REGISTER.md`.
- The repository license is `CC-BY-SA-4.0`; see `LICENSE` and the [license deed](https://creativecommons.org/licenses/by-sa/4.0/) or [legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en).
- Source-specific notices and upstream license terms continue to apply to included or adapted third-party material.

## Adapted Content

The following sources contributed content or patterns that were adapted. Consult the named skill metadata and notices for the precise scope rather than treating this summary as the attribution record.

| Source | License / notice | Adaptation record |
|---|---|---|
| [Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done), Lex Christopherson | MIT; Copyright (c) 2025 Lex Christopherson | `metadata.adapted_from` in the skills that adapt GSD context-engineering, orchestration, state, or verification patterns |
| [Karpathy Skills](https://github.com/forrestchang/andrej-karpathy-skills) | MIT | `agile-v-behavioral/SKILL.md` `metadata.adapted_from` |
| [Kadajett/agent-nestjs-skills](https://github.com/Kadajett/agent-nestjs-skills), Kadajett | MIT; Copyright (c) 2024 Kadajett | `domains/build-agent-nestjs/NOTICE.md` and `metadata.upstream` |

MIT copyright and permission notices must be retained where the MIT license requires them. The repository's `CC-BY-SA-4.0` license does not replace applicable upstream notices.

## Reference and Interoperability

These sources are referenced for formats, compatibility, tooling, or external outputs. A reference or integration does not by itself mean source content was adapted or redistributed.

| Source | Role |
|---|---|
| [Understand Anything](https://github.com/Lum1104/Understand-Anything) | MIT-licensed external codebase-understanding tool; Agile V documentation describes consuming its generated graph outputs without vendoring its source |
| [AgentSkills.io specification](https://agentskills.io/specification) | Skill format and metadata reference |
| [JSON Schema Draft 7](https://json-schema.org/draft-07/schema) and [2020-12](https://json-schema.org/draft/2020-12/schema) | Schema vocabulary references |
| [Semantic Versioning](https://semver.org/) | Versioning convention reference |
| [Conventional Commits](https://www.conventionalcommits.org/) | Commit-format convention reference |
| [Cursor Skills](https://cursor.com/docs/context/skills), [Claude Code Skills](https://code.claude.com/docs/en/skills), [VS Code agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), and [GitHub Copilot agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | Platform compatibility references |

## Inspiration and Research

- [pcbGPT: Automatic PCB Schematic Synthesis from Natural Language Requirements](https://arxiv.org/pdf/2606.01188) informed consideration of natural-language-assisted PCB schematic workflows. It is cited as research inspiration, not identified here as adapted or redistributed content.

## Standards and Public Sources

Standards and regulatory references provide design, risk, quality, security, safety, or lifecycle context. Citation does not claim compliance, certification, endorsement, or permission to redistribute standards text.

- Authoritative public links, editions, and usage cautions are maintained in `docs/standards/SOURCE_REGISTER.md`.
- Publisher and framework entry points include [ISO](https://www.iso.org/standards.html), [IEC](https://webstore.iec.ch/), [RTCA](https://www.rtca.org/), [FDA](https://www.fda.gov/), [EUR-Lex](https://eur-lex.europa.eu/), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [OWASP GenAI Security Project](https://genai.owasp.org/), [MITRE ATLAS](https://atlas.mitre.org/), and [Automotive SPICE](https://vda-qmc.de/en/automotive-spice/).
- Referenced families include ISO 9001, ISO 13485, ISO/IEC 27001, ISO/IEC 42001, ISO 26262, IEC 61508, IEC 62304, ISO/IEC/IEEE 12207, ISO/IEC/IEEE 15288, ISO/IEC/IEEE 29148, ISO/IEC 25010, ISO/IEC/IEEE 29119, AS9100D, DO-178C/DO-330, GxP/GAMP 5, 21 CFR Part 11, EU Annex 11, the EU AI Act, MISRA C, and AUTOSAR.
- Many standards are copyrighted and available only under publisher license. This repository references public catalog, regulator, or framework pages and does not purport to reproduce or grant rights in standards text.
- Before relying on a reference, verify the applicable edition, amendments, jurisdiction, adoption, and licensed text with qualified reviewers.

## Attribution Use

When reusing material from this repository:

- comply with `LICENSE` and identify changes where required;
- retain applicable upstream copyright, license, and notice text;
- preserve source attribution recorded in `metadata.adapted_from`, `metadata.upstream`, and `NOTICE.md` files; and
- do not describe inspiration or interoperability references as adapted content without evidence of adaptation.
