# ACE Architecture Pattern

**Purpose:** Specific architecture, file layout, and implementation conventions for the Agile Context Engine. Constrain Epics and / or stories to one or more architecture ptterns


## Base Engine

**Applies to:** All Epics and stories tha rely on the Agile Context Engine, eg: Use Shape Skill). Base engine is foundational.

The Agile Context Engine is the core — the engine for building and running skills in their entirety. It defines structure, config, and conventions. all AceSkills are built on top of it.

### Decisions

**Module/class mapping** 
 One file per module, one class per concept  `skills/ace-shaping/scripts/engine.py` → `class AgileContextEngine`; `skills/ace-shaping/scripts/ace_skill.py` → `class AceSkill`. 

**Type safety** 
Yes — pydantic.  Use pydantic for config, strategy, and DTOs. Typed function signatures. Catches config/schema errors early. 

**Persistence**
**JSON  for Relationships, connections, configurations** 
Use JSON for structured data only: relationships (e.g. connections between nodes in story-map), traversal slices (order, status), skill config (e.g. templates to render output), scanner associated with a rule, engine state.

**Markdown for Long-form text, qualitative content** 
Use Markdown for all prose: instructions, guidance, rules, process. Content of each epic and/or story goes in separate `.md` files. Assembled agent output is Markdown.

### Path (Cross-cutting)

**Applies to:** All epics (file paths used throughout).

**All file-returning properties return Path objects, not strings.**

The Path object represents the file or directory at that path. Use Path for:

- **OS separators** — Different operating systems use different separators; Path handles this.
- **Centralized path logic** — Dispersing path logic across the codebase is error-prone; a single Path abstraction keeps it in one place.
- **Resolution, joining, existence checks** — Path provides resolve(), join, exists(), read_text(), etc.


---

### Engine vs Skill Scripts: Code Sharing and Responsibility

**Principle:** Ace-shaping hosts the base engine. Other skills (e.g. coding) extend the engine with domain-specific logic. Skills have robust logic; they are not thin wrappers.


| Location | Responsibility |
|----------|----------------|
| `skills/ace-shaping/scripts/` | Hosts the engine. Defines what an ace-skill is: directory layout, content pieces, rules structure, scripts folder, output paths. Engine owns the schema. |
| `skills/ace-shaping/scripts/ace_skill.py` | `AceSkill` — skill structure, rule set, content assembly. |
| `skills/ace-shaping/scripts/engine.py` | `AgileContextEngine` — `scaffold_skill(name, path)`, `build_skill(path)`, `get_skill_scaffold_spec()`. Creates scaffold on disk. |

The engine is the **single source of truth** for:
- What a skill directory contains
- What gets saved where
- Content piece names (core-definitions, intro, output-structure, shaping-process, validation, script-invocation)
- Output conventions

```
┌─────────────────────────────────────────────────────────────┐
│  ace-shaping (Engine + Shaping — same skill)                  │
│  Bolt 1 — Engine: structure, paths, scaffold_skill,          │
│           build_skill, get_skill_scaffold_spec()              │
│  Bolt 2 — Shaping: domain logic for shaping                  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ imports, extends
                              │
┌─────────────────────────────────────────────────────────────┐
│  Other skills (ace-coding, ace-context-to-memory, etc.)       │
│  - Add ace-shaping/scripts to sys.path; import engine         │
│  - Implement domain logic (e.g. code gen, render, convert)     │
│  - Robust skill-specific behavior; not thin wrappers          │
└─────────────────────────────────────────────────────────────┘
```

### Script Invocation Markdown (AI Guidance)

**File:** `script-invocation.md` — path: `skills/ace-<name>/content/script-invocation.md` (e.g. `skills/ace-shaping/content/script-invocation.md`).

Each skill includes this **Markdown that instructs the AI on how to call the Python scripts**. The AI reads it to know:

- Which script to run (e.g. `scripts/scaffold.py`, `scripts/build.py`)
- What parameters to pass (e.g. `--name`, `--path`, `--skill-space`)
- When to call (e.g. after content is complete, before strategy creation)
- What to expect (success output, error handling, next steps)

| Location | Purpose |
|----------|---------|
| `skills/ace-shaping/content/script-invocation.md` | How to invoke build.py; params, examples, sequencing. |
| `skills/ace-<name>/content/script-invocation.md` | Per-skill script usage when the skill has scripts. Optional if skill has no scripts. |

This Markdown is part of the skill content. The AI reads it before invoking Python and follows it when orchestrating the workflow (e.g. Create Ace-Skill, Gather Context).


### Engine File Structure

**Two views, same per-skill layout:**

| View | Root | Notes |
|------|------|-------|
| **Engine** | `agile-context-engine/` | Full repo: conf/, skills/, pyproject.toml. ace-shaping hosts engine code (engine.py, ace_skill.py, etc.). |
| **Deployment** | `.agents/skills/` | Consuming project (e.g. agile_bots, mm3e-experiment). Same layout per skill; no engine code. |

```
agile-context-engine/
├── conf/                   # Engine config (outside any skill space)
│   └── ace-config.json
├── skills/                 # Registered ace-skills
│   ├── ace-shaping/        # Shaping skill — also hosts the engine
│   │   ├── content/        # Markdown: core definitions, process, validation
│   │   │   ├── core-definitions.md   # Core domain concepts (Interaction, State Concept)
│   │   │   ├── intro.md             # Intro to the skill; framing and context
│   │   │   ├── output-structure.md  # Output format (Interaction Tree, State Model)
│   │   │   ├── shaping-process.md   # Process overview; when to do what
│   │   │   ├── validation.md        # Validation checklist; DO/DON'T rules
│   │   │   └── script-invocation.md # AI guidance: how to call scripts (params, when, what to expect)
│   │   ├── rules/          # DO/DO NOT rules, scanners
│   │   │   ├── scanners.json
│   │   │   └── *.md
│   │   ├── scripts/        # Engine + build (ace-shaping only: engine.py, ace_skill.py, etc.)
│   │   │   ├── engine.py   # AgileContextEngine
│   │   │   ├── ace_skill.py
│   │   │   ├── config.py
│   │   │   ├── rule_set.py
│   │   │   ├── build.py   # Assembles content → AGENTS.md
│   │   │   └── ...
│   │   ├── AGENTS.md       # Assembled output (built from content)
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── metadata.json
│   └── ace-context-to-memory/   # Other skills: content/, rules/, scripts/ (build.py only), same layout
├── pyproject.toml
├── requirements.txt
└── README.md
```

**Per-skill template** (Create Skill output): `skills/ace-<name>/` or `.agents/skills/ace-<name>/` — content, rules, scripts (build.py + domain scripts), AGENTS.md, SKILL.md, README.md, metadata.json. Only ace-shaping has engine.py, ace_skill.py, etc.


### 1.4 Config Format

**File:** `conf/ace-config.json`


---


### Loading registered skills and rule sets

| Concept / Behavior | Implementation |
|--------------------|----------------|
| **Skills list** | Discover by convention: scan `skills/` or `.agents/skills/` for `ace-*` dirs. Config optional (e.g. for engine root or overrides). |
| **Per-skill load** | For each discovered path, instantiate `AceSkill` at `.agents/skills/<path>/` |
| **Rule set load** | Per skill: `rules/*.md` (Markdown), `rules/scanners.json` (JSON). Merge into unified `RuleSet` per skill. |
| **Output folders** | Create `<skill_space>/<output-folder>/` for each skill; output folder = skill name with `ace-` stripped (e.g. ace-shaping → shaping, ace-context-to-memory → context-to-memory) |
| **Engine API** | `Engine.load()` — reads config, loads skills, derives skill space, creates output dirs |
| **Failure** | Malformed JSON; missing skill path; invalid rule path → report and fail |

---

## 2. Ace Skills

**Applies to:** Epic: Create Ace-Skill;

Ace-skills are built on top of the base engine. They use engine APIs for scaffold, build, and structure.

Some skills will inherit from the base ace_skills when they need to do common things (e.g. create strategy, apply rules, inject content).

### 2.1 Concept Implementation (Create Ace-Skill)

Domain concepts for Create Ace-Skill, mapped to implementation: exact file path, format. Parameterization where needed (e.g. `<name>`).

#### AceSkill

**Object model:** AceSkill receives `Engine` injected at construction. Uses engine for context (workspace, strategy_path, etc.). No context parameters on instruction assembly — pulls from engine.

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Class | `skills/ace-shaping/scripts/ace_skill.py` → `class AceSkill` |
| `AceSkill.engine` | Injected at construction. Used for context (workspace, strategy_path, slice_index). |
| `AceSkill.path` | `skills/ace-<name>/` |
| `AceSkill.rule_set` | `skills/ace-<name>/rules/` (dir); `rules/scanners.json` (JSON); `rules/*.md` (Markdown) |
| `AceSkill.scripts` | `skills/ace-<name>/scripts/` (dir); each script `scripts/<script>.py` |
| `AceSkill.core_definition`, `intro`, `output_structure`, `shape`, `validation` | `skills/ace-<name>/content/*.md` |
| `AceSkill.operation_sections` | Map: operation → section IDs to inject (create_strategy, generate_slice, improve_strategy, improve_skill) |
| `AceSkill.instructions` | Property. Assembles from `operation_sections` and engine context. No context parameter. |
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

#### Build (ace-shaping hosts engine)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Engine location | `skills/ace-shaping/scripts/` — engine.py, ace_skill.py, config.py, rule_set.py, etc. |
| Build script | `skills/ace-shaping/scripts/build.py` — assembles content → AGENTS.md |
| Script invocation guidance | `skills/ace-shaping/content/script-invocation.md` (Markdown) — AI reads to know how to call build.py |

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



## 3. Instruction Injection

**Applies to:** Epic **Use Shape Skill** (Create Shaping Strategy, Generate Slices, Improve Strategy); Epic **Initialize Agile Context Engine** (Load registered skills and rule sets — AceSkill must support `operation_sections` and `instructions`); and **running any ace-skill** (ace-shaping, ace-coding, ace-context-to-memory, etc.) — the same injection pattern applies across all skills.

Instructions are assembled and **injected** into the AI prompt. The AI doesn't "go read" the rules — they're given. While the AI could read the words because they live in the skill, we enhance this by having the caller assemble and inject the relevant instructions into the prompt for each operation, so the AI has exactly what it needs in context without fetching files. The caller (MCP, CLI, panel, etc.) asks the skill for instructions before the AI runs an operation and injects the assembled markdown into the prompt.

### 3.1 Operations → Stories

| Story | Operation | What it does |
|-------|-----------|--------------|
| Create Shaping Strategy | `create_strategy` | Analyze source; propose epic breakdown, slice order, assumptions; save strategy doc |
| Generate Shaping Slices | `generate_slice` | Load strategy; produce 4–7 stories; output Interaction Tree + State Model |
| Improve Strategy | `improve_strategy` | Add DO/DO NOT to strategy doc; re-run slice until approved |
| Improve Skill (post-shaping) | `improve_skill` | Take accumulated corrections; update base skill content/rules |

**Improve strategy** = corrections go into the strategy document. **Improve skill** = strategy doc improvements are applied to the skill's content and rules.

### 3.2 Skill Markdown Decomposition (Section IDs)

**Applies to:** Epic **Initialize Agile Context Engine** (Load registered skills — skills expose sectioned content); Epic **Use <Skill> Skill** (all operations — caller assembles per operation).

**Alignment convention:** Section IDs mirror domain. `<skill>.X.Y` → content in file matching X (e.g. `<skill>-strategy.md` for `<skill>.strategy.*`). **section-led** layout: one file per section.

| File | Section IDs | Content |
|------|-------------|---------|
| **<skill>-process.md** | `<skill>.process.intro`, `<skill>.process.post_shaping.review` | Process overview; post-shaping review |
| **<skill>-strategy.md** | `<skill>.strategy.phase`, `<skill>.strategy.criteria`, `<skill>.strategy.slices.running`, `<skill>.strategy.corrections` | Strategy phase, criteria, running slices, DO/DO NOT |
| **<skill>-output.md** | `<skill>.output.interaction_tree`, `<skill>.output.state_model` | Interaction Tree and State Model format |
| **<skill>-validation.md** | `<skill>.validation.checklist`, `<skill>.validation.rules` | Validation checklist; DO/DON'T rules |
| **<skill>-core.md** | `<skill>.core.interaction`, `<skill>.core.state_concept` | Interaction and State Concept definitions |
| **rules/** (markdown + JSON) | `<skill>.validation.rules` | DO/DON'T rules, scanner configs; merged into RuleSet |

### 3.3 What to Inject and When

**Applies to:** Epic **Use Shape Skill** — Stories: Create Shaping Strategy, Generate Slices, Improve Strategy.

| Operation | Inject | Story |
|-----------|--------|-------|
| **create_strategy** | `shaping.process.intro`, `shaping.strategy.phase`, `shaping.strategy.criteria`, `shaping.core.interaction`, `shaping.core.state_concept` | Create Shaping Strategy |
| **generate_slice** | `shaping.process.intro`, `shaping.strategy.slices.running`, `shaping.strategy.corrections`, `shaping.output.*`, `shaping.validation.checklist`, `shaping.validation.rules`, `shaping.core.*`, **strategy doc** (from path) | Generate Shaping Slices |
| **improve_strategy** | `shaping.strategy.corrections`, `shaping.validation.checklist` (correction format only) | Improve Strategy |
| **improve_skill** | `shaping.process.post_shaping.review`, `shaping.strategy.corrections`, **strategy doc** (from path) | Improve Skill |

**Corrections in generate_slice:** When user feedback implies a reusable rule, AI adds DO/DO NOT during the slice flow; no separate `improve_strategy` call needed.

**Validation:** No separate validate operation. `generate_slice` injects both checklist and rules. AI validates against checklist before presenting; reports status (✓ pass or ⚠ needs attention) in response.

**Scanners:** Programmatic validators live in `rules/` as config. Flow: (1) Generate output. (2) Run scanners. (3) Determine false positives. (4) Inject problems, fixes, and report location into the next prompt. AI addresses real issues in the next iteration.

**Context (always available):** Context source paths, workspace path, strategy path (when exists). Caller provides these; not "injected" as instruction content.

### 3.4 Injection Flow and Object Model

**Applies to:** Epic **Use Shape Skill** (Create Shaping Strategy, Generate Slices, Improve Strategy); Epic **Initialize Agile Context Engine** (Load skills — inject Engine into each AceSkill); Epic **Create Ace-Skill** (AceSkill structure).

**Flow:**

| Step | Caller | Engine / Skill |
|------|--------|----------------|
| 1 | User requests operation (e.g. create strategy, generate slice 1) | — |
| 2 | Asks skill for instructions: `skill.instructions.display_content("create_strategy")` | Skill assembles from `operation_sections` + engine context |
| 3 | Injects assembled markdown + context paths into AI prompt | — |
| 4 | AI runs operation; instructions already in prompt | — |

**When:** Before the AI runs the operation. Caller injects; AI receives — doesn't have to "load" guidelines.

**Object model:**

| Concept | Implementation |
|---------|----------------|
| **Engine injection** | AceSkill receives `Engine` at construction. Uses engine for workspace, strategy_path, slice_index. |
| **operation_sections** | Map: operation → section IDs. Keys: `create_strategy`, `generate_slice`, `improve_strategy`, `improve_skill`. From skill config. |
| **instructions** | Property. Assembles from `operation_sections` and engine context. No context parameter — pulls from engine. |
| **display_content(operation)** | Returns markdown for that operation. Caller injects into prompt. |

