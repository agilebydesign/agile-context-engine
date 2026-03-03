# Script Invocation

Run from workspace root (abd_content or agile-context-engine). Set `CONTENT_MEMORY_ROOT` if workspace differs from cwd.

## setup_response.py

Creates response folder and symlink for proposal response workflow.

**When to call:** Before creating strategy; when starting a new proposal response.

**Usage:**
```bash
python .agents/skills/ace-proposal-respond/scripts/setup_response.py --proposal <proposal_folder> [--project <project_root>]
```

**Parameters:**
- `--proposal` (required): Folder containing proposal material (e.g. `workspace/jbom response`)
- `--project` (optional): Project root for symlink (default: CONTENT_MEMORY_ROOT or cwd)

**Example:**
```bash
python .agents/skills/ace-proposal-respond/scripts/setup_response.py --proposal "workspace/jbom response"
```

**Output:** Creates `<proposal_folder>/response/` and symlink `<project_root>/response` → response folder.

---

## ace-context-to-memory (dependency)

Convert proposal material to memory and index for RAG. Run before answering questions.

**link_workspace_source.py** — Link proposal folder to source (if not already):
```bash
python .agents/skills/ace-context-to-memory/scripts/link_workspace_source.py --path "workspace/jbom response" --name "JBOM"
```

**index_memory.py** — Full pipeline (convert → chunk → embed):
```bash
python .agents/skills/ace-context-to-memory/scripts/index_memory.py --path "source/JBOM"
```

**search_memory.py** — Semantic search when answering questions:
```bash
python .agents/skills/ace-context-to-memory/scripts/search_memory.py "<query>" --k 5
```

---

## build.py

Assembles content into AGENTS.md.

**Usage:**
```bash
cd skills/ace-proposal-respond
python scripts/build.py
```
