---
name: ace-context-to-memory
description: >-
  Converts documents (PDF, PPTX, DOCX, XLSX, etc.) to markdown and chunks them
  for agent memory. Use when the user wants to "add to memory", "convert and
  chunk", "ingest content for agent", "refresh memory", or process a folder of
  documents for AI agent context.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Ace-Context-to-Memory

Converts source documents to markdown and chunks them for agent memory. Pipeline: **convert** (documents → markdown + images) → **chunk** (markdown → smaller files for retrieval). Optional: **organize** (Excel story maps → hierarchical markdown).

## When to Activate

- User asks to "add content to memory" or "refresh memory"
- Wants to convert a folder of documents (PPTX, PDF, DOCX, XLSX) for agent context
- Mentions "convert and chunk", "ingest for agent", or "memory pipeline"
- Has added new files and wants them processed

## CRITICAL: Respect User Scope

- **One file**: When user says "one file", "this file", "just X.pdf", or names a specific file → use `--file <path>`. Process ONLY that file.
- **Folder**: When user says "folder", "all", "everything in X", or explicitly requests a folder → use `--memory <path>`.
- **Do NOT** process entire folders when the user asked for a single file.

## Pipeline Overview

1. **Convert**: Use `markitdown` to convert supported files to markdown. Images extracted and referenced.
2. **Chunk**: Split large markdown by slides (decks) or headings (docs). Small files stay as single chunks.
3. **Organize** (optional): For Excel story maps, output Epic → Capability → System → Notes hierarchy.

## Scripts

Run from workspace root. Scripts in `skills/ace-context-to-memory/scripts/`.

- `convert_to_markdown.py --file <file_path>` — **single file only** (use when user asks for one file); creates `memory/<filename_stem>/` so all chunks stay in one place
- `convert_to_markdown.py --memory <source_path>` — folder (all supported files)
- `chunk_markdown.py --memory <memory_name>`
- `organize_story_map_hierarchy.py --memory <memory_name> [--source <xlsx_path>]`

See `content/script-invocation.md` for full usage.

## Build

```bash
cd skills/ace-context-to-memory
python scripts/build.py
```
