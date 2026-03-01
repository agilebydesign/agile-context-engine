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
