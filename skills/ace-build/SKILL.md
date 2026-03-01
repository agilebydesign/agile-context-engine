---
name: ace-build
description: Build new ace-skills. Scaffold and assemble content into AGENTS.md. Use when creating a skill with the standard ace-skill structure.
license: MIT
metadata:
  author: agilebydesign
  version: "0.1.0"
---

# Ace-Build

Build new ace-skills. Scaffold creates the directory; build assembles content into AGENTS.md.

## When to Use

- User wants to create a new ace-skill
- User has markdown/prompts describing the skill
- Regenerating AGENTS.md after content changes

## Scripts

- **scaffold.py** — `--name ace-<name>` creates the skill directory
- **build.py** — Assembles content → AGENTS.md

See `content/script-invocation.md` for params and sequencing.
