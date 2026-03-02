# Script Invocation

AI guidance for calling ace-shaping scripts.

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage:**
```bash
cd skills/ace-shaping
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: shaping-core, shaping-process, shaping-strategy, shaping-output, shaping-validation.
