# Core Definitions

## State Concepts (Add Context to Memory)

- **ContentSource** — Original artifact (PDF, PPTX, DOCX, XLSX, etc.) in supported format
- **Markdown** — Converted artifact; full fidelity; stored alongside original
- **Chunk** — Split unit of markdown for retrieval; by slide, heading, or whole file
- **Memory** — Single memory entry; one per file; points to original and markdown
- **Memories** — Collection of memories; nested by source structure
- **Workspace** — Root path containing content sources and memory output

## Epic: Add Context to Memory

- **Actor**: Developer
- **Supporting**: ace-context-to-memory
- **Required State**: Workspace with content sources
- **Initiation**: Developer requests add to memory (convert and chunk, ingest, refresh)
- **Response**: Skill converts each original to markdown; chunks markdown into memory; each file → one memory; memories nested; each memory points to original and markdown
- **Resulting State**: Memories available for future reference

**CRITICAL — Respect user scope**: If user specifies ONE file (e.g. "this file", "just X.pdf", "one file"), use `convert_to_markdown.py --file <path>` and process ONLY that file. Do NOT use `--memory` on a folder when user asked for a single file.

---

# Pipeline Process

## Step 1: Convert to Markdown

**Story: Convert content sources to markdown**

- **Required State**: Content in supported formats (PDF, PPTX, DOCX, XLSX, etc.)
- **Response**: Skill converts original artifact in its entirety to markdown; markdown stored alongside original (same folder)
- **Resulting State**: Markdown converted artifact available alongside original
- **Failure Modes**: Unsupported format; conversion fails; path invalid

**Supported formats**: `.pdf`, `.pptx`, `.docx`, `.xlsx`, `.xls`, `.html`, `.htm`, `.txt`, `.csv`, `.json`, `.xml`

## Step 2: Chunk Markdown

**Story: Chunk markdown**

- **Required State**: Markdown available
- **Response**: Skill splits markdown by slide, heading, or whole file; writes chunks with source attribution
- **Resulting State**: Chunks produced; available for reference
- **Failure Modes**: No markdown found; chunk strategy fails

**Chunking strategy**:
- Slide decks (`<!-- Slide number: N -->`): One chunk per slide
- Other docs (>200 lines): Split at `#` or `##` boundaries
- Small files (<200 lines): Kept as single chunk

## Step 2b: Organize Excel Story Maps (optional)

- Parses: Category (Epic) → Capability → System → Notes
- Outputs: One markdown file per Epic with `##` Capability, `###` System, `-` notes
- Writes to: `memory/<name>/chunked/`

## Step 3: Sync Workspace to Memory (full pipeline)

**Story: Sync workspace to memory (convert + copy + chunk)**

- **Required State**: —
- **Response**: Skill converts each original to markdown; copies chunks to `<workspace>/ace-output/ace-context-to-memory/memory/`; each file → one memory; memories nested; each memory points to original and markdown
- **Resulting State**: Memories populated
- **Failure Modes**: Workspace missing; copy fails; chunk fails

---

# Output Structure

## Memory Mode

- **Convert**: `memory/<name>/<rel>/converted/` (markdown + images)
- **Chunk**: `memory/<name>/<rel>/chunked/` (chunked markdown)
- **Single-file** (`--file`): `memory/<filename_stem>/` — subfolder named after the file; all chunks in one place
- **Organize**: `memory/<name>/chunked/` (hierarchical markdown for Excel story maps)

## Pipeline Mode (single-folder)

- **Convert**: `pipeline/converted/`
- **Chunk**: `pipeline/chunked/`

## Chunk Source Reference

Each chunk includes: `<!-- Source: path | file://url -->` for navigation.

---

# Script Invocation

Run from workspace root. Set `CONTENT_MEMORY_ROOT` if workspace root differs from current directory.

**Dependencies**: `pip install "markitdown[all]"` (convert); `pip install pandas openpyxl` (organize)

## convert_to_markdown.py

Converts source files to markdown. Creates `memory/<name>/*/converted/`.

**Single file (use when user asks for one file):**
```bash
python scripts/convert_to_markdown.py --file <file_path>
```

**Folder (use only when user explicitly wants a folder processed):**
```bash
python scripts/convert_to_markdown.py --memory <source_path>
```

- `--file`: Process ONLY the specified file. Use when user says "one file", "this file", "just X.pdf".
- `--memory`: Process all supported files in folder. Tries under `Assets/` first, then workspace root.

## chunk_markdown.py

Chunks converted markdown. Reads from `memory/<name>/*/converted/`, writes to `memory/<name>/*/chunked/`.

**Usage:**
```bash
python scripts/chunk_markdown.py --memory <memory_name>
```

- `<memory_name>`: Name of folder under `memory/` (e.g. `CBE`)
- Run convert first

## organize_story_map_hierarchy.py

Reorganizes Excel story map into hierarchical markdown (Epic → Capability → System → Notes).

**Usage:**
```bash
python scripts/organize_story_map_hierarchy.py --memory <memory_name> [--source <xlsx_path>]
```

- If `--source` omitted, looks for `global-sco/<memory_name>/*.xlsx` or first matching xlsx
- Writes to `memory/<name>/chunked/`

## Key Behaviors

1. **Run convert before chunk** — Chunk reads from converted output.
2. **Handle errors gracefully** — Some files may fail. Log and continue.
3. **Long-running** — Large folders (100+ files) take time.

---
