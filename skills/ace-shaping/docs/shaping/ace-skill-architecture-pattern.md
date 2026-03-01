# ACE Skill Architecture & Implementation Pattern

**Purpose:** Specific architecture, file layout, and implementation conventions for the Agile Context Engine and ace-skills. Story-by-story and epic-by-epic.

**Scope:** This document currently focuses on **Create Ace-Skill** (fixing and creating the skill). We will go into more detail on that first. Everything after the dividing line below is tentative and will be detailed later.

---

## 1. Base Engine

The Agile Context Engine is the core — the engine for building and running skills in their entirety. It defines structure, config, and conventions. Ace-skills are built on top of it.

### 1.1 Global Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Root** | `agile-context-engine/` | Engine folder is the root of the skill space. All engine code, config, and skills live under this. Location: `C:\dev\agile-context-engine`. |
| **Code location** | `src/` | Python source under root. |
| **Module/class mapping** | One file per module, one class per concept | `src/skill_space.py` → `class SkillSpace`; `src/ace_skill.py` → `class AceSkill`. |
| **Type safety** | **Yes — pydantic** | Use pydantic for config, strategy, and DTOs. Typed function signatures. Catches config/schema errors early. |
| **Structured data** | **JSON** | Config, strategy metadata, scanner rules, engine state. |
| **Text / instructions / rules** | **Markdown** | Content files, rules, instructions, assembled agent output. |

---

### 1.2 Engine vs Skill Scripts: Code Sharing and Responsibility

**Principle:** All structural logic lives in the engine. Skill scripts are thin entry points that call engine APIs.

### Centralized Code (Engine)

| Location | Responsibility |
|----------|----------------|
| `src/` | Defines what an ace-skill is: directory layout, content pieces, rules structure, scripts folder, output paths. Engine owns the schema. |
| `src/ace_skill.py` | `AceSkill.scaffold_spec()` or `Engine.get_skill_scaffold_spec()` — returns the canonical structure (paths, file names, templates). |
| `src/engine.py` | `Engine.scaffold_skill(name, path)` — creates the scaffold on disk using the spec. Engine does the actual file/dir creation. |

The engine is the **single source of truth** for:
- What a skill directory contains
- What gets saved where
- Content piece names (core-definitions, intro, output-structure, shaping-process, validation, script-invocation)
- Output conventions

### Skill Scripts

| Location | Responsibility |
|----------|----------------|
| `skills/ace-build/scripts/scaffold.py` | Parses CLI args (e.g. `--name`, `--path`); calls `Engine.scaffold_skill(name, path)`. Does **not** define structure. |
| `skills/ace-build/scripts/build.py` | Invokes engine build API (or shared build logic). Assembles content per engine conventions. |
| `skills/ace-<name>/scripts/*.py` | Any skill script: parses params, delegates to engine. No structural logic. |

### Script Invocation Markdown (AI Guidance)

Each skill includes **Markdown that instructs the AI on how to call the Python scripts**. The AI reads this to know:

- Which script to run (e.g. `scripts/scaffold.py`, `scripts/build.py`)
- What parameters to pass (e.g. `--name`, `--path`, `--skill-space`)
- When to call (e.g. after content is complete, before strategy creation)
- What to expect (success output, error handling, next steps)

| Location | Purpose |
|----------|---------|
| `skills/ace-build/content/script-invocation.md` (or `scripts/README.md`) | How to invoke scaffold.py, build.py; params, examples, sequencing. |
| `skills/ace-<name>/content/script-invocation.md` | Per-skill script usage when the skill has scripts. Optional if skill has no scripts. |

This Markdown is part of the skill content. The AI reads it before invoking Python and follows it when orchestrating the workflow (e.g. Create Ace-Skill, Gather Context).

### Relationship

```
┌─────────────────────────────────────────────────────────────┐
│  Engine (src/)                                               │
│  - Defines skill structure, paths, conventions               │
│  - scaffold_skill(name, path)                                │
│  - get_skill_scaffold_spec() → { dirs, files, templates }    │
│  - build_skill(skill_path)                                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ calls
                              │
┌─────────────────────────────────────────────────────────────┐
│  Skill Scripts (skills/ace-*/scripts/*.py)                    │
│  - Parse CLI/params                                          │
│  - Call engine.scaffold_skill(...) or engine.build_skill()   │
│  - No structural logic; no duplicate path/file definitions   │
└─────────────────────────────────────────────────────────────┘
```

### Rules

1. **Common structure for skills is centralized.** Skills do not define the basic structure of a skill, the standard files in a skill, or where the standard things go. They ask the engine. **Skill-specific logic is decentralized** — each skill owns its own domain logic. 
2. **Engine exposes APIs.** `scaffold_skill()`, `build_skill()`, `get_skill_scaffold_spec()`, etc. Scripts call these.
3. **Scripts are entry points.** They adapt CLI/env/params into engine calls. They can be run standalone (e.g. `python scripts/scaffold.py --name ace-foo`) or invoked by AI/tooling.
4. **Shared package.** Engine is installable (e.g. `pip install -e .` from engine root). Skill scripts run with engine on `PYTHONPATH` or installed, and call `from agile_context_engine.engine import AgileContextEngine` (or `engine.scaffold_skill`). Scripts never duplicate engine logic.

---

### 1.3 Root Structure (Engine)

```
agile-context-engine/
├── src/                    # Python code
│   ├── __init__.py
│   ├── engine.py           # AgileContextEngine
│   ├── skill_space.py       # SkillSpace
│   ├── ace_skill.py        # AceSkill
│   ├── rule_set.py         # RuleSet
│   ├── context_sources.py  # ContextSources
│   ├── memories.py         # Memories, Memory, Chunk
│   ├── strategy.py         # Strategy
│   ├── slice.py            # Slice
│   └── ...
├── conf/                   # Engine config (outside any skill space)
│   └── ace-config.json
├── skills/                 # Registered ace-skills
│   ├── ace-shaping/        # Example: one skill expanded
│   │   ├── content/        # Markdown: core definitions, process, validation
│   │   │   ├── core-definitions.md
│   │   │   ├── intro.md
│   │   │   ├── output-structure.md
│   │   │   ├── shaping-process.md
│   │   │   └── validation.md
│   │   ├── rules/          # DO/DO NOT rules, scanners
│   │   │   ├── scanners.json
│   │   │   └── *.md
│   │   ├── scripts/        # Build, scaffold, etc.
│   │   │   └── build.py    # Assembles content → AGENTS.md
│   │   ├── AGENTS.md       # Assembled output (built from content)
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── metadata.json
│   ├── ace-context-to-memory/
│   └── ace-build/          # Build-ACE skill
├── pyproject.toml
├── requirements.txt
└── README.md
```

**Config path:** `agile-context-engine/conf/ace-config.json` (relative to engine root). Engine resolves via `engine_path` so config is always found.

---

### 1.4 Config Format

**File:** `conf/ace-config.json`

```json
{
  "skill_space_path": "/abs/path/to/skill-space",
  "skills": ["skills/ace-shaping", "skills/ace-context-to-memory", "skills/ace-build"],
  "skills_config": {
    "order": ["ace-context-to-memory", "ace-shaping"]
  },
  "constraints": []
}
```

- `skill_space_path`: Current skill space; written when user sets skill space.
- `skills`: List of skill paths (relative to engine root).
- `skills_config.order`: Optional load/run order.
- `constraints`: Architecture-pattern constraints (e.g. `{"pattern": "must use X", "scope": "Epic"}`).

---

## 2. Ace-Skill

Ace-skills are built on top of the base engine. They use engine APIs for scaffold, build, and structure.

Some skills will inherit from the base ace_skills when they need to do common things around strategy (e.g. create strategy, load/save strategy, apply rules).

### 2.1 Concept Implementation (Create Ace-Skill)

Domain concepts for Create Ace-Skill, mapped to implementation: exact file path, format. Parameterization where needed (e.g. `<name>`).

#### AceSkill

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Class | `src/ace_skill.py` → `class AceSkill` |
| `AceSkill.path` | `skills/ace-<name>/` |
| `AceSkill.rule_set` | `skills/ace-<name>/rules/` (dir); `rules/scanners.json` (JSON); `rules/*.md` (Markdown) |
| `AceSkill.scripts` | `skills/ace-<name>/scripts/` (dir); each script `scripts/<script>.py` |
| `AceSkill.core_definition` | `skills/ace-<name>/content/core-definitions.md` (Markdown) |
| `AceSkill.intro` | `skills/ace-<name>/content/intro.md` (Markdown) |
| `AceSkill.output_structure` | `skills/ace-<name>/content/output-structure.md` (Markdown) |
| `AceSkill.shape` | `skills/ace-<name>/content/shaping-process.md` (Markdown) |
| `AceSkill.validation` | `skills/ace-<name>/content/validation.md` (Markdown) |
| `AceSkill.assembled_agent` | See AssembledAgent |
| `AceSkill.build()` | Invokes `Engine.build_skill(path)`; see BuildScript |

#### BuildScript

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `BuildScript.path` | `skills/ace-<name>/scripts/build.py` |
| `BuildScript.run()` | Calls `Engine.build_skill(skill_path)`; engine reads content/*.md, assembles, writes AGENTS.md |

#### AssembledAgent

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `AssembledAgent.path` | `skills/ace-<name>/AGENTS.md` |
| `AssembledAgent.content` | Merged Markdown: core-definitions + intro + output-structure + shaping-process + validation (in order) |

#### BuildAceSkill (ace-build)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Skill root | `skills/ace-build/` |
| Scaffold script | `skills/ace-build/scripts/scaffold.py` |
| Build script (for ace-build itself) | `skills/ace-build/scripts/build.py` |
| Script invocation guidance | `skills/ace-build/content/script-invocation.md` (Markdown) — AI reads to know how to call scaffold.py, build.py |

#### Scaffold spec (engine)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `Engine.get_skill_scaffold_spec()` | Returns structure; no file — in-memory spec. |
| `Engine.scaffold_skill(name, path)` | Creates `skills/ace-<name>/` with: `content/*.md`, `rules/`, `scripts/`, `metadata.json`, `SKILL.md`, `README.md` |
| Content files (scaffold) | `content/core-definitions.md`, `intro.md`, `output-structure.md`, `shaping-process.md`, `validation.md`, `script-invocation.md` — empty or template Markdown |
| Metadata | `metadata.json` (JSON) |
| Skill descriptor | `SKILL.md` (Markdown) |

#### Per-skill outputs (created by scaffold or build)

| Artifact | Path | Format |
|----------|------|--------|
| Assembled agent | `skills/ace-<name>/AGENTS.md` | Markdown |
| Metadata | `skills/ace-<name>/metadata.json` | JSON |
| Scanner rules | `skills/ace-<name>/rules/scanners.json` | JSON |
| Rule markdown | `skills/ace-<name>/rules/*.md` | Markdown |

---

### 2.2 Epic: Create Ace-Skill

#### Story: Create scaffolding via script

| Aspect | Implementation |
|--------|----------------|
| **Skill** | `skills/ace-build/` (Build-ACE skill) |
| **Script** | `skills/ace-build/scripts/scaffold.py` — thin entry point |
| **Script behavior** | Parses `--name`, `--path`; calls `engine.scaffold_skill(name, path)`. Does **not** define structure. |
| **Engine** | `Engine.scaffold_skill(name, path)` — uses `get_skill_scaffold_spec()` from engine; creates dirs and files. All logic centralized. |
| **Output structure** | Defined by engine (see §2.1 Concept Implementation). Directory, content (including script-invocation.md for skills with scripts), rules, scripts, metadata all come from engine spec. |
| **Invocation** | `python scripts/scaffold.py --name ace-foo --path skills/ace-foo` (from engine root or `skills/ace-build/`) |

#### Story: AI fills content pieces from input

| Aspect | Implementation |
|--------|----------------|
| **Input** | Markdown path(s), prompts, or raw text passed to Build-ACE skill. |
| **Target files** | `skills/ace-<name>/content/*.md` (core-definitions, intro, output-structure, shaping-process, validation) |
| **Format** | Markdown. AI writes/overwrites these files per skill guidance. |
| **Script invocation** | Build-ACE skill has `content/script-invocation.md` that tells the AI how to call scaffold.py and build.py (params, when, sequencing). AI reads this before invoking Python. |

#### Story: User completes missing pieces

| Aspect | Implementation |
|--------|----------------|
| **Gap reporting** | AI returns list of missing/incomplete pieces (e.g. `["core-definitions", "validation"]`). |
| **User edit** | User edits `skills/ace-<name>/content/<piece>.md` directly. |
| **Re-check** | AI re-reads files and re-validates. |

### Story: AI reruns build script

| Aspect | Implementation |
|--------|----------------|
| **Script** | `skills/ace-<name>/scripts/build.py` — thin entry point; calls `engine.build_skill(skill_path)` or equivalent. |
| **Engine** | `Engine.build_skill(path)` — assembles content per engine conventions; writes AGENTS.md, rules, etc. |
| **Output** | `skills/ace-<name>/AGENTS.md` (assembled agent file) |
| **Other outputs** | `rules/*.md`, `rules/*.json`, `README.md`, `metadata.json`, `SKILL.md` per engine conventions |

### Ace-Skill Directory Layout (output of Create Skill)

```
skills/ace-<name>/
├── content/
│   ├── core-definitions.md
│   ├── intro.md
│   ├── output-structure.md
│   ├── shaping-process.md
│   ├── validation.md
│   └── script-invocation.md    # AI guidance: how to call scripts (params, when, what to expect)
├── rules/
│   ├── scanners.json          # or per-scanner JSON
│   └── *.md                   # rule markdown if any
├── scripts/
│   ├── build.py
│   ├── scaffold.py            # (ace-build only)
│   └── ...                    # other scripts
├── AGENTS.md                  # assembled agent file (output of build)
├── SKILL.md                   # skill descriptor
├── README.md
└── metadata.json
```

---

---

**══════════════════════════════════════════════════════════════**  
**TENTATIVE — To Be Detailed Later**  
**══════════════════════════════════════════════════════════════**

Everything below is placeholder. We will go into more detail on Create Ace-Skill first.

---

## 7. Epic: Initialize Agile Context Engine

### Story: Load registered skills and rule sets

| Aspect | Implementation |
|--------|----------------|
| **Config** | `conf/ace-config.json` → `skills` array |
| **Skill load** | For each path in `skills`, instantiate `AceSkill(path)`. |
| **AceSkill** | `src/ace_skill.py` — `class AceSkill` with `path`, `rule_set`, content strings. |
| **RuleSet** | `src/rule_set.py` — `class RuleSet` loads markdown from `content/`, JSON from `rules/`. |
| **Markdown paths** | `content/core-definitions.md`, `intro.md`, `output-structure.md`, `shaping-process.md`, `validation.md` |
| **Scanner rules** | `rules/scanners.json` or per-scanner JSON in `rules/` |

### Story: Set skill space

| Aspect | Implementation |
|--------|----------------|
| **Persist** | Write `skill_space_path` to `conf/ace-config.json`. |
| **Create output dirs** | For each registered skill: `<skill_space_path>/ace-output/<skill_name>/` |
| **Example** | Skill space `/home/user/proj` → `/home/user/proj/ace-output/ace-shaping/`, `/home/user/proj/ace-output/ace-context-to-memory/` |

---

## 8. Epic: Gather Context

### Story: Gather context for shaping run

| Aspect | Implementation |
|--------|----------------|
| **Populate memory** | Invoke ace-context-to-memory: convert → chunk → sync to `<workspace>/ace-output/ace-context-to-memory/memory/`. |
| **Memory layout** | Each source file → one folder under `memory/`; folder = one `Memory`; chunks as `.md` files with `<!-- Source: path -->`. |
| **ContextSources** | `src/context_sources.py` — `class ContextSources` with `gather(content_sources, workspace, strategy)`. |
| **Memories** | `src/memories.py` — `Memories`, `Memory`, `Chunk`. |
| **Refer** | `Memories.refer()` returns `Chunk[]` for shaping. |

**Memory path:** `<skill_space>/ace-output/ace-context-to-memory/memory/<artifact_id>/`  
**Chunk files:** `chunk_001.md`, `chunk_002.md`, … with source attribution in each.

---

## 9. Epic: Use Shape Skill

### Story: Create Shaping Strategy

| Aspect | Implementation |
|--------|----------------|
| **Output path** | `<skill_space>/ace-output/ace-shaping/story/<name>-shaping-strategy.md` |
| **Format** | Markdown. Structure: source analysis, epic breakdown, slice order, assumptions. |
| **Strategy** | `src/strategy.py` — `class Strategy` with `save(path)`, `load(path)`, `update(rules)`. |
| **Metadata (optional)** | `<skill_space>/ace-output/ace-shaping/story/<name>-shaping-strategy.json` for structured parts (epics, slices) if needed. |

### Story: Generate Shaping Slices

| Aspect | Implementation |
|--------|----------------|
| **Output** | Interaction Tree + State Model. |
| **Paths** | `<skill_space>/ace-output/ace-shaping/slice-<n>/interaction-tree.md`, `slice-<n>/state-model.md` (or `.json` for structured). |
| **Slice** | `src/slice.py` — `class Slice` with `produce(strategy): (InteractionTree, StateModel)`. |

### Story: Improve Shaping Skill

| Aspect | Implementation |
|--------|----------------|
| **Update** | `Strategy.update(rules)` appends DO/DO NOT rules; persists to same strategy path. |
| **Re-run** | Regenerate slice with updated strategy. |

---

## 10. Skill Space Output Layout (Tentative)

```
<skill_space>/
├── ace-output/
│   ├── ace-context-to-memory/
│   │   └── memory/
│   │       ├── <artifact_id_1>/
│   │       │   ├── chunk_001.md
│   │       │   └── ...
│   │       └── <artifact_id_2>/
│   │           └── ...
│   └── ace-shaping/
│       ├── story/
│       │   └── <name>-shaping-strategy.md
│       └── slice-1/
│           ├── interaction-tree.md
│           └── state-model.md
└── ...                        # user's project files
```

---

## 11. Python Module → Concept Mapping (Tentative)

| Concept | Module | Class |
|---------|--------|-------|
| AgileContextEngine | `src/engine.py` | `AgileContextEngine` |
| SkillSpace | `src/skill_space.py` | `SkillSpace` |
| AceSkill | `src/ace_skill.py` | `AceSkill` |
| RuleSet | `src/rule_set.py` | `RuleSet` |
| ContextSources | `src/context_sources.py` | `ContextSources` |
| Memories | `src/memories.py` | `Memories` |
| Memory | `src/memories.py` | `Memory` |
| Chunk | `src/memories.py` | `Chunk` |
| Strategy | `src/strategy.py` | `Strategy` |
| Slice | `src/slice.py` | `Slice` |
| BuildScript | `src/build_script.py` | `BuildScript` |
| AssembledAgent | `src/assembled_agent.py` | `AssembledAgent` |

---

## 12. Pydantic Models (Tentative)

```python
# conf/ace_config.py or src/config.py
from pydantic import BaseModel
from pathlib import Path

class AceConfig(BaseModel):
    skill_space_path: str | None = None
    skills: list[str]
    skills_config: dict | None = None
    constraints: list[dict] = []

    class Config:
        extra = "forbid"  # strict schema
```

---

## 13. Summary Table (Tentative)

| Artifact | Format | Location |
|----------|--------|----------|
| Engine config | JSON | `agile-context-engine/conf/ace-config.json` |
| Skill content | Markdown | `skills/ace-<name>/content/*.md` (includes script-invocation.md for AI) |
| Scanner rules | JSON | `skills/ace-<name>/rules/*.json` |
| Assembled agent | Markdown | `skills/ace-<name>/AGENTS.md` |
| Strategy | Markdown | `<skill_space>/ace-output/ace-shaping/story/<name>-shaping-strategy.md` |
| Memory chunks | Markdown | `<skill_space>/ace-output/ace-context-to-memory/memory/<id>/*.md` |
| Slice output | Markdown / JSON | `<skill_space>/ace-output/ace-shaping/slice-<n>/*.md` |
