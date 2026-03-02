# Ace-Build

Build new ace-skills with the standard structure. Delegates to the Agile Context Engine.

## Scaffold

From `agile-context-engine` root:

```bash
python skills/ace-build/scripts/scaffold.py --name ace-foo
```

Creates `skills/ace-foo/` with content/, rules/, scripts/.

## Build

```bash
cd skills/ace-build
python scripts/build.py
```

Assembles content/*.md into AGENTS.md.

## Process

1. Scaffold (or use existing skill)
2. Fill content pieces from markdown/prompts
3. Run build when complete
