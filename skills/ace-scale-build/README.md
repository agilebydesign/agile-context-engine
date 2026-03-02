# Ace Scale Build

Create and scale ace-skills with the standard structure. Delegates to the Agile Context Engine.

## Scaffold

From `agile-context-engine` root:

```bash
python skills/ace-scale-build/scripts/scaffold.py --name ace-foo
```

Creates `skills/ace-foo/` with content/, rules/, scripts/.

## Build

```bash
cd skills/ace-scale-build
python scripts/build.py
```

Assembles content/*.md into AGENTS.md.

## Process

1. Scaffold (or use existing skill)
2. Fill content pieces from markdown/prompts
3. Run build when complete
