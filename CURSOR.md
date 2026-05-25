# Using Agile V with Cursor

This project includes **Cursor project rules** so Agile V framework applies automatically when you work here.

## In this repository

1. Open the folder in Cursor.
2. The rule [`.cursor/rules/agile-v-core.mdc`](.cursor/rules/agile-v-core.mdc) is committed with `alwaysApply: true`, so you do not need extra installation steps.
3. In Cursor, confirm it under **Settings → Rules** (or the project rules UI), where `agile-v-core` should appear.

## Use Agile V in another project

### Option 1: Cursor Project Rules (Recommended)

Copy `.cursor/rules/agile-v-core.mdc` into that project's `.cursor/rules/` directory (create the folders if needed). 

**For additional skills:**
```bash
# Copy specific skill rules as needed
cp .cursor/rules/build-agent.mdc /path/to/your/project/.cursor/rules/
cp .cursor/rules/red-team-verifier.mdc /path/to/your/project/.cursor/rules/
```

Adjust or merge with existing rules as you like.

### Option 2: Root Instruction File

If your stack only supports a root instruction file, copy [`CLAUDE.md`](CLAUDE.md) into your project root (or merge its contents into your existing instructions).

### Option 3: Personal Agent Skills

If you want Agile V as reusable skills under `~/.cursor/skills`, copy or symlink individual skill directories:

```bash
# Copy all Agile V skills to personal skills directory
cp -r agile-v-core ~/.cursor/skills/
cp -r build-agent ~/.cursor/skills/
cp -r requirement-architect ~/.cursor/skills/
cp -r red-team-verifier ~/.cursor/skills/
# ... etc
```

Use whatever layout you use for other skills.

## Available Cursor Rules

This repository provides the following pre-configured Cursor rules:

- **agile-v-core.mdc** — Foundation (traceability, verification, compliance)
- Build Agent rules (coming soon)
- Red Team Verifier rules (coming soon)
- Additional skill rules (coming soon)

## Claude Code vs Cursor

- **Claude Code:** Install via the plugin marketplace (see [`README.md`](README.md) instructions); the plugin exposes skills from this repo. Per-project use can also rely on `CLAUDE.md`.
- **Cursor:** Use the committed `.cursor/rules/` files as described above. Cursor does not read `.claude-plugin/` or `CLAUDE.md` by default.

## How to Know It's Working

After enabling Agile V in Cursor, you should see:

✅ **Agents halt when requirements are unclear:**
```
⚠️ HALT CONDITION: No requirement specification found for "login feature"
Invoking: requirement-architect
```

✅ **Code includes traceability comments:**
```python
# ART-0001: User authentication
# Implements: REQ-0001
```

✅ **Independent verification:**
```
Build Agent: Implementation complete ✓
Red Team Verifier: Testing independently...
```

✅ **Evidence summaries before deployments:**
```
=== EVIDENCE SUMMARY ===
Scope: Deploy API v2.1.0
Traceability: REQ-0101 to REQ-0115 ✓
Status: AWAITING HUMAN APPROVAL
```

## Quick Start Example

1. **Start a new project in Cursor**
2. **Copy Agile V rules:**
   ```bash
   mkdir -p .cursor/rules
   cp /path/to/agile_v_skills/.cursor/rules/agile-v-core.mdc .cursor/rules/
   ```

3. **Test with a vague request:**
   ```
   You: "Add user authentication"
   
   Agent: ⚠️ HALT CONDITION: No requirement specification
   Invoking: requirement-architect to formalize REQ-XXXX
   ```

4. **Work with Requirement Architect:**
   ```
   Agent: Before implementing, I need to clarify:
   1. Authentication method? (username/password, OAuth, SSO?)
   2. Password requirements? (complexity, length?)
   3. Session management? (JWT, cookies, Redis?)
   4. Compliance requirements? (ISO 27001, GDPR?)
   ```

5. **Watch traceability in action:**
   ```python
   # After requirements are formalized
   # app/auth.py
   # ART-0001: Authentication handler
   # Implements: REQ-0001
   ```

## Advanced: Multi-Skill Projects

For complex projects, use multiple Agile V skills:

```bash
# Copy relevant skills for your project type
.cursor/rules/
  agile-v-core.mdc          # Always include (foundation)
  build-agent-python.mdc    # If building Python apps
  test-designer.mdc         # For test-driven development
  compliance-auditor.mdc    # For regulated environments
```

Each skill includes specific instructions for its role in the V-shaped workflow.

## For contributors

When you change Agile V skills, keep these in sync:
- **Individual skill SKILL.md** files (e.g., `agile-v-core/SKILL.md`)
- **[`CLAUDE.md`](CLAUDE.md)** (minimal guidelines)
- **[`.cursor/rules/*.mdc`](.cursor/rules/)** (Cursor project rules)

## More Information

- **Full Documentation:** [README.md](README.md)
- **Concrete Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Skill Routing Guide:** [SKILL_ROUTING_GUIDE.md](SKILL_ROUTING_GUIDE.md)
- **Homepage:** https://github.com/Agile-V/agile_v_skills

---

**License:** CC-BY-SA-4.0 | **Author:** Agile V™
