# Core Definitions

## Ace-Skill

An ace-skill is a structured skill with:
- **content/** — Markdown: core-definitions, intro, output-structure, shaping-process, validation
- **rules/** — DO/DO NOT rules, scanners (JSON)
- **scripts/** — Build script (and scaffold for ace-build)
- **AGENTS.md** — Assembled output (built from content)

## Build-ACE (ace-build)

The skill that creates other ace-skills. Provides scaffold and build scripts that delegate to the engine.

---

# Ace-Build

Build new ace-skills. Use when the user wants to create a skill with the standard ace-skill structure.

## Process

1. **Scaffold** — Run `scaffold.py --name ace-<name>` to create the directory.
2. **Fill content** — AI or user fills core-definitions, intro, output-structure, shaping-process, validation from markdown/prompts/text.
3. **Complete gaps** — If pieces are missing, user completes them.
4. **Build** — Run `build.py` to assemble AGENTS.md.

---

# Output Structure

After build, the skill contains:

- **AGENTS.md** — Merged content for agent consumption
- **metadata.json** — Skill metadata
- **SKILL.md** — Skill descriptor
- **README.md** — Usage instructions

Content merge order: core-definitions → intro → output-structure → shaping-process → validation.

---

# Shaping Process

When creating an ace-skill:

1. User provides markdown, prompts, or text describing the skill.
2. AI uses Build-ACE to scaffold (if new) or identifies target skill.
3. AI fills content pieces from input. If insufficient, report gaps.
4. User completes missing pieces.
5. AI reruns build when all pieces are complete.

---

# Validation

Before considering the skill complete:

- [ ] All content pieces filled (core-definitions, intro, output-structure, shaping-process, validation)
- [ ] build.py runs without error
- [ ] AGENTS.md produced and non-empty
- [ ] metadata.json has name and version

---

# Script Invocation

AI guidance for calling ace-build scripts. Run from `agile-context-engine` root.

## scaffold.py

Creates a new ace-skill directory with content/, rules/, scripts/.

**When to call:** When the user wants to create a new ace-skill.

**Usage:**
```bash
python skills/ace-build/scripts/scaffold.py --name ace-<name> [--path skills/ace-<name>]
```

**Parameters:**
- `--name` (required): Skill name, e.g. `ace-foo`, `ace-shaping`
- `--path` (optional): Output path. Default: `skills/<name>` relative to engine root.

**Example:**
```bash
python skills/ace-build/scripts/scaffold.py --name ace-foo
```

**Output:** Creates `skills/ace-foo/` with content/, rules/, scripts/, and standard files.

---

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage (from ace-build itself):**
```bash
cd skills/ace-build
python scripts/build.py
```

**Usage (from any scaffolded skill):**
```bash
cd skills/ace-<name>
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: core-definitions, intro, output-structure, shaping-process, validation.

**Sequencing:** Run scaffold first → fill content → run build when complete.

---
