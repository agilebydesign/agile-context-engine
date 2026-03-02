# Script Invocation

Run from workspace root. Set `CONTENT_MEMORY_ROOT` if workspace root differs from current directory.

**Dependencies**: `pip install "markitdown[all]"` (convert); `pip install pandas openpyxl` (organize)

## convert_to_markdown.py

Converts source files to markdown. Creates `memory/<name>/*/converted/`.

**Single file (when user asks for one file):**
```bash
python scripts/convert_to_markdown.py --file <file_path>
```

**Folder (when user explicitly wants folder processed):**
```bash
python scripts/convert_to_markdown.py --memory <source_path>
```

- `--file`: Process ONLY the specified file. Use when user says "one file", "this file", "just X.pdf". Output: `memory/<filename_stem>/` — subfolder named after the file; all chunks in one place.
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
