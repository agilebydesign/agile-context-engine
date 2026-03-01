# Core Definitions

## Ace-Skill

An ace-skill is a structured skill with:
- **content/** — Markdown: core-definitions, intro, output-structure, shaping-process, validation
- **rules/** — DO/DO NOT rules, scanners (JSON)
- **scripts/** — Build script (and scaffold for ace-build)
- **AGENTS.md** — Assembled output (built from content)

## Build-ACE (ace-build)

The skill that creates other ace-skills. Provides scaffold and build scripts that delegate to the engine.
