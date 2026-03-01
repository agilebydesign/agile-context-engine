# Agile Context Engine

Engine for building and running skills in their entirety. Defines skill structure, config, and conventions.

## Structure

- **src/** — Engine code (scaffold_skill, build_skill)
- **skills/** — Registered ace-skills (ace-build, ace-shaping, etc.)
- **conf/** — Engine config (ace-config.json)

## Quick Start

```bash
# Scaffold a new skill
python skills/ace-build/scripts/scaffold.py --name ace-foo

# Build AGENTS.md for a skill
cd skills/ace-foo
python scripts/build.py
```

## Install

```bash
pip install -e .
```
