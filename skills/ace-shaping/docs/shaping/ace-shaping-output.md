# Interaction Tree and State Model — Agile Bots (Slice 1)

**Source:** `agile_bots` — bots/, src/, docs/story/story-graph.json; `ace-shaping` skill (currently `solution-shaping`) — AGENTS.md, content/*.md  
**Methodology:** ace-shaping skill (`skills/ace-shaping/` or `skills/solution-shaping/`)  
**Domain:** Agile Bots — workflow orchestration for AI agents and developers  
**Slice:** 1 — Shaping skill + Python/JSON hybrid  
**Assumption:** Developer initiates; Agile Context Engine responds. AI Agent may invoke via MCP tools.

---

## A) Interaction Tree (Slice 1)

```
Epic: Create Ace-Skill
     Actor: Developer
     Supporting: AI Agent, Build-ACE skill
     Required State: User has one or more markdown files (or prompts, text) describing how the skill will work
     State Concepts: AceSkill, AssembledAgent, BuildScript, BuildAceSkill
     Initiation: User initiates build ace-skill through AI
     Response: AI uses Build-ACE skill; skill invokes script with params to create scaffolding; AI follows skill guidance to fill content pieces from markdown/prompts/text; if pieces missing/incomplete, AI tells user and user completes; AI reruns build script when all pieces done
     Resulting State: Ace-skill created; ready to register
│
├─ Story: Create scaffolding via script
│    Required State: Build-ACE skill available; user has provided skill name and params
│    State Concepts: AceSkill, BuildScript, BuildAceSkill
│    Initiation: AI invokes Build-ACE skill with params (skill name, etc.)
│    Response: Skill runs script with params; creates ace-skill directory; content/ with core-definitions, intro, output-structure, shaping-process, validation; scripts/ folder; build script
│    Resulting State: Ace-skill scaffold created; ready for content fill
│    Failure Modes: Template missing; path conflict; invalid ace-skill name; script fails
│
├─ Story: AI fills content pieces from input
│    Required State: Scaffold created
│    State Concepts: AceSkill
│    Initiation: AI follows Build-ACE skill guidance
│    Response: AI takes markdown file(s), prompts, text passed in; fills core_definition, intro, output_structure, shape, validation per skill guidance
│    Resulting State: Content pieces filled (or gaps identified)
│    Failure Modes: Input insufficient; skill guidance unclear
│
├─ Story: User completes missing pieces
│    Required State: AI has identified missing/incomplete pieces
│    State Concepts: AceSkill
│    Initiation: AI tells user which pieces are missing or incomplete
│    Response: User completes those pieces; repeats until all pieces done
│    Resulting State: All content pieces complete
│    Failure Modes: User does not complete; invalid content format
│
└─ Story: AI reruns build script
     Required State: All content pieces complete
     State Concepts: AceSkill, AssembledAgent
     Initiation: AI reruns build script (when necessary)
     Response: Build script assembles core_definition, intro, output_structure, shape, validation into single agent file; produces rules, readme, metadata, skills file
     Resulting State: Assembled agent file ready; ace-skill usable
     Failure Modes: Build script fails; content merge conflict

Epic: Initialize Agile Context Engine
     Actor: Developer
     Supporting: Agile Context Engine
     Required State: At least one skill created (e.g. ace-shaping)
     State Concepts: AgileContextEngine, AceSkill, RuleSet
     Initiation: Developer starts engine (CLI or chat)
     Response: Engine loads registered skills from JSON; each skill provides rule set (markdown + JSON for scanners)
     Resulting State: Engine initialized; skills loaded; rule sets available
│
├─ Story: Load registered skills and rule sets
│    Required State: Shaping skill installed (ace-shaping)
│    State Concepts: AgileContextEngine, AceSkill, RuleSet
│    Initiation: Developer starts engine
│    Response: Engine loads skills list from JSON; for each skill path, loads rule set (markdown from content/, JSON for scanners); merges into unified rule set per skill
│    Resulting State: Skills loaded; rule sets available for instruction assembly
│    Failure Modes: Malformed JSON config; missing skill path; invalid rule path
│
├─ Story: Set workspace
│    Required State: Skills loaded
│    State Concepts: AgileContextEngine, Workspace
│    Initiation: Developer specifies workspace (path)
│    Response: Engine writes workspace_path to engine config JSON (e.g. .ace-skills/conf/ace-config.json); creates <workspace>/ace-output/<skill>/ for every registered skill
│    Resulting State: Workspace set; engine knows current workspace; skill output folders created
│    Failure Modes: Workspace path invalid; JSON write fails
│
│
├─ Epic: Gather Context
│    Actor: Developer
│    Supporting: Agile Context Engine, ace-context-to-memory skill
│    Required State: Engine initialized; workspace set; content sources available
│    State Concepts: ContextSources, Memories, Memory, Chunk, Workspace, Strategy, RuleSet
│    Initiation: Developer requests context for shaping
│    Response: Engine populates memory (convert, chunk, sync via ace-context-to-memory); workspace has reference to memories; assembles with workspace, strategy (when exists), and skill rule set per shaping process needs
│    Resulting State: Memories populated; context assembled; available for shaping
│    │
│    └─ Story: Gather context for shaping run
│         Required State: Engine initialized; workspace set; content sources available
│         State Concepts: ContextSources, Memories, Memory, Chunk, Workspace, Strategy, RuleSet
│         Initiation: Developer requests context for shaping run (strategy phase or slice run)
│         Response: Engine populates memory (convert, chunk, sync to <workspace>/ace-output/.../memory/); refers to memories for chunks; assembles with workspace; adds strategy (for slice run); merges with ace-skill rule set; workspace scopes output path
│         Resulting State: Memories populated; context assembled; ready for strategy creation or slice production
│         Failure Modes: Workspace missing; no content to convert; strategy missing (when required for slice); rule set load fails
│
└─ Epic: Use Shape Skill
     Actor: Developer
     Supporting: Agile Context Engine
     Required State: Engine initialized; context gathered; strategy approved (for slices)
     State Concepts: Strategy, Slice, InteractionTree, StateModel
     Initiation: Developer invokes shaping (create strategy, generate slice, improve skill)
     Response: Engine loads shaping instructions; assembles with context; produces or updates strategy/slice output
     Resulting State: Strategy created or updated; slice output produced; skill improved
     │
     ├─ Story: Create Shaping Strategy
     │    Required State: Context gathered (from memories)
     │    State Concepts: Strategy, SourceAnalysis
     │    Initiation: Developer requests strategy creation
     │    Response: Engine loads shaping instructions; injects context from memories; produces strategy doc (complexity analysis, epic breakdown, slice order, assumptions); saves to <workspace>/ace-output/ace-shaping/story/<name>-shaping-strategy.md
     │    Resulting State: Strategy saved; ready for approval
     │    Failure Modes: Memories empty; strategy validation fails; save path invalid
     │
     ├─ Story: Generate Shaping Slices
     │    Required State: Strategy approved; slice order defined
     │    State Concepts: Slice, InteractionTree, StateModel
     │    Initiation: Developer requests slice (e.g. Slice 1)
     │    Response: Engine loads strategy; produces 4–7 stories for the slice; derives concepts; builds State Model; outputs Interaction Tree + State Model
     │    Resulting State: Slice output produced; available for review
     │    Failure Modes: Strategy not approved; slice index invalid; output validation fails
     │
     └─ Story: Improve Shaping Skill
          Required State: Slice produced; user has corrections
          State Concepts: Strategy, Slice
          Initiation: Developer provides corrections (DO/DO NOT rules)
          Response: Engine updates strategy with new rules; re-runs slice until approved
          Resulting State: Strategy updated; corrections applied; slice ready for approval or next slice
          Failure Modes: Correction format invalid; rule conflicts with existing
```

---

## B) State Model (Slice 1)

Concepts scoped to the smallest subtree where they are used.

### Path (Cross-cutting)

**All file-returning properties return Path objects, not strings.**

The Path object represents the file or directory at that path. Use Path for:

- **OS separators** — Different operating systems use different separators; Path handles this.
- **Centralized path logic** — Dispersing path logic across the codebase is error-prone; a single Path abstraction keeps it in one place.
- **Resolution, joining, existence checks** — Path provides resolve(), join, exists(), read_text(), etc.

**Implementation:** Reuse `agile_bots/src/bot_path` (BotPath, StoryGraphPaths) in its entirety. Do not reimplement. The engine and ace-skills should depend on that module or a shared copy of it.

| Property / Operation | Returns | Notes |
|----------------------|---------|-------|
| Any property that points to a file or directory | `Path` | Never `String` for file paths |
| Path.join(...) | `Path` | Use Path for joining |
| Path.resolve() | `Path` | Absolute, normalized |

### AgileContextEngine, AceSkill, RuleSet, Workspace, ArchitectureConstraint (Epic: Initialize Agile Context Engine)

```
AgileContextEngine
- Path engine_path
      Path to the engine itself
      invariant: agile-context-engine/
      Other paths to things like skills, rules, etc. should be under this.
- Path config_path
     Path to engine config 
     invariant:(e.g. conf/ace-config.json)
     invariant: engine knows this path; config lives outside any workspace
- AceSkill[] skills
     List of registered ace-skills (path in JSON)
- Workspace workspace
     Current workspace (when set)
     invariant: workspace_path in engine config JSON; engine reads on load

- AgileContextEngine load(): AgileContextEngine
     uses Path engine_path to locate
     loads JSON config
     Loads skills from skills folder
     orders using skills_config 
     each skill loads its rule set based on rules folder and rules config
- Context context
     Reference to context object below

Workspace
- Path path
     Folder path (root of project/IDE or subfolder)
     invariant: outputs of engine for skill work here; returns Path, not String
- String name
     Workspace identifier (for output paths)
     invariant: derived from path

AceSkill
- Path path
     Path to skill directory
     invariant: skills/ace-<skill_name>/
- RuleSet rule_set
     RuleSet (markdown + JSON)
     invariant: skills/ace-<skill_name>/rules
- Script[] scripts
     Scripts collection
     invariant: skills/ace-<skill_name>/scripts/
- String core_definition
     Content from core-definitions.md
     invariant: from skills/ace-<skill_name>/content/core-definitions.md
- String intro
     Content from intro.md
     invariant: from skills/ace-<skill_name>/content/intro.md
- String output_structure
     Content from output-structure.md
     invariant: from skills/ace-<skill_name>/content/output-structure.md
- String shape
     Content from shaping-process.md
     invariant: from skills/ace-<skill_name>/content/shaping-process.md
- String validation
     Content from validation.md
     invariant: from skills/ace-<skill_name>/content/validation.md
- AssembledAgent assembled_agent
     All pieces assembled into single agent file
     invariant: output of build() — core_definition + intro + output_structure + shape + validation
- AceSkill build(path_to_markdown): AceSkill  
     Build script
     Assembles pieces; produces assembled agent file
     creates Json config scaffold for rules and ace-skill / engine


RuleSet
- Path[] markdown_paths
     Path to each content file
     invariant: Path objects for core-definitions.md, intro.md, output-structure.md, shaping-process.md, validation.md
     Specific markdown file eg
     - Object scanner_rules
          JSON for scanners
          invariant: from skills/ace-<skill_name>/rules
- String merged_content
     Unified content for instruction assembly
     invariant: markdown from all markdown_paths concatenated with scanner_rules
- RuleSet load(path): RuleSet
     AceSkill path
     Reads markdown from content/; loads JSON from rules

ArchitectureConstraint
- String pattern
     e.g. "must use X", "must run in Y time"
- String scope
     Scope of constraint
     invariant: Epic, Story, or global
```

### AssembledAgent, BuildScript (Epic: Create Ace-Skill)

*AceSkill is defined above (Initialize). Create Skill adds:*

```
AssembledAgent
- Path path
     Path to assembled output
     invariant: skills/ace-<skill_name>/AGENTS.md (or assembled agent file under skill); returns Path, not String
- String content
     Merged content for agent consumption
     invariant: core_definition + intro + output_structure + shape + validation assembled in order

BuildScript
- Path path
     Path to build script
     invariant: skills/ace-<skill_name>/scripts/build.py; returns Path, not String
- BuildScript run(): AssembledAgent
     AceSkill path
     Assembles content files; writes assembled agent file
```

### ContextSources, Memories, Memory, Workspace, Strategy, Slice (Epic: Gather Context, Use Shape Skill)

**ace-context-to-memory skill** defines what our context sources are, converts them to markdown, chunks them, and puts them in memories so we can refer to them later. Shaping gets context from those memories — not from raw paths.

```
ContextSources

- Memories memories
     Populated by ace-context-to-memory (defines context sources → convert → markdown → chunk → memories)
     invariant: each folder in memory/ = one Memory; each Memory = chunked markdown for one file; points to original artifact and markdown converted artifact (alongside original); memories nested
- Workspace workspace
     Folder containing project; all skill operations happen in this context
     invariant: likely at root of project/IDE; can be subfolder; everything packed into workspace
- Strategy strategy
     When we have one (for slice runs)
     invariant: required for Generate Slice; optional for Create Strategy
- RuleSet rule_set
     From ace-skill (shaping instructions)
- ContextSources gather(content_sources, workspace, strategy): ContextSources
     ContentSources, Workspace, Strategy
     Populates memory (convert, chunk, sync via ace-context-to-memory); refers to memories for chunks; assembles with workspace, strategy, rule_set per shaping phase (strategy vs slice)

Workspace
- Path path
     Folder path (root of project/IDE or subfolder)
     invariant: everything gets packed into this workspace; returns Path, not String
- String name
     Workspace identifier (for output paths)
     invariant: derived from path

Memories
- Path root_path
     <workspace>/ace-output/<skill>/memory/ subfolder
     invariant: under workspace; returns Path, not String
- Memory[] memories
     All memory folders (nested)
     invariant: each folder = one Memory
- Chunk[] refer(): Chunk[]
     Chunks available for shaping to use

Memory
- Path path
     Folder in <workspace>/ace-output/<skill>/memory/
     invariant: one folder = one memory; returns Path, not String
- Chunk[] chunks
     Chunked markdown for one specific file
     invariant: all chunks from same original artifact
- String artifact_ref
     Original artifact (source file: PDF, PPTX, DOCX, etc.)
     invariant: path or file://url to the file that was added
- String markdown_ref
     Markdown converted artifact (full file, alongside original)
     invariant: original converted in entirety to markdown; stored alongside original
- Memory[] children
     Nested memories
     invariant: memories are nested (folder hierarchy)

Chunk
- String content
     Chunk content (markdown)
- String source_ref
     Original source path and location
     invariant: <!-- Source: path | file://url --> for attribution

Strategy
- Path path
     Path to strategy document
     invariant: <workspace>/ace-output/ace-shaping/story/<name>-shaping-strategy.md; returns Path, not String
- SourceAnalysis source_analysis
     SourceAnalysis
- Epic[] epic_breakdown
     Epic
- Slice[] slice_order
     Slice
- String[] assumptions
- Strategy save(path): Strategy
     File
     Persists to path
- Strategy load(path): Strategy
     File
     Loads from path
- Strategy update(rules): Strategy
     DO/DO NOT rules
     Appends rules; re-validates

Slice
- Number index
     Slice order (1, 2, 3, …)
     invariant: positive integer
- String theme
     Slice theme (e.g. de-risk foundation, structure decision)
- Story[] stories
     Story
     invariant: 4–7 stories per slice
- Slice produce(strategy): InteractionTree, StateModel
     Strategy
     Produces 4–7 stories; derives concepts; outputs tree + model
```

---

## C) Inline Concepts (Epic: Use Shape Skill)

**Use Shape Skill** — Concepts used across Gather Context, Create Strategy, Generate Slices, Improve Skill:

| Concept | Properties | Operations |
|---------|------------|------------|
| **Path** | — | Represents file/dir; all path properties return Path, not String. Reuse agile_bots bot_path. |
| **Workspace** | path (Path), name | — |
| **Strategy** | path (Path), source_analysis, epic_breakdown, slice_order, assumptions | save(), load(), update(rules) |
| **Slice** | index, theme, stories | produce(Strategy): InteractionTree, StateModel |
| **InteractionTree** | Epic[] hierarchy | validate(): boolean |
| **StateModel** | Concept[] concepts | validate(): boolean |

---

## D) ace-context-to-memory (Embedded)

**Source:** `ace-context-to-memory` skill — SKILL.md, scripts  
**Methodology:** ace-shaping skill  
**Domain:** ace-context-to-memory — content sources → markdown → chunks → refer for future use  
**Assumption:** Developer initiates; ace-context-to-memory responds. Integration (e.g. Vesta 7) is separate.

### D.1) Interaction Tree (ace-context-to-memory)

```
Epic: Add Context to Memory
     Actor: Developer
     Supporting: ace-context-to-memory
     Required State: Workspace with content sources
     State Concepts: ContentSource, Markdown, Chunk, Memory, Memories, Workspace
     Initiation: Developer requests add to memory (convert and chunk, ingest, refresh)
     Response: Skill converts each original artifact in full to markdown (alongside original, within workspace); chunks markdown into memory; each file → one memory; memories nested; each memory points to original artifact and markdown converted artifact
     Resulting State: Memories available for future reference
│
├─ Story: Convert content sources to markdown
│    Required State: Content sources available (PDF, PPTX, DOCX, etc.)
│    State Concepts: ContentSource, Markdown
│    Initiation: Developer requests conversion (or step 1 of pipeline)
│    Response: Skill converts original artifact in its entirety to markdown; markdown stored alongside original (same folder)
│    Resulting State: Markdown converted artifact available alongside original artifact
│    Failure Modes: Unsupported format; conversion fails; path invalid
│
├─ Story: Chunk markdown
│    Required State: Markdown available
│    State Concepts: Markdown, Chunk
│    Initiation: Developer requests chunking (or step 2 of pipeline)
│    Response: Skill splits markdown by slide, heading, or whole file; writes chunks with source attribution
│    Resulting State: Chunks produced; available for reference
│    Failure Modes: No markdown found; chunk strategy fails
│
└─ Story: Sync workspace to memory (convert + copy + chunk)
     Required State: Workspace with content
     State Concepts: ContentSource, Markdown, Chunk, Memory, Memories, Workspace
     Initiation: Developer requests sync workspace to memory
     Response: Skill converts each original to markdown in full (alongside original); copies chunks to <workspace>/ace-output/ace-context-to-memory/memory/; each file → one memory; memories nested; each memory points to original artifact and markdown converted artifact
     Resulting State: Memories populated; available for reference
     Failure Modes: Workspace missing; copy fails; chunk fails
```

### D.2) State Model (ace-context-to-memory)

```
ContentSource
- String path
     Path to source file or folder
     invariant: supported format (PDF, PPTX, DOCX, XLSX, HTML, etc.)
- String format
     File extension / type
- Markdown convert(): Markdown
     ContentSource
     Converts to markdown in place

Markdown
- String path
     Path to .md file
     invariant: alongside original artifact (same folder as source)
- String content
     Full content converted to markdown
     invariant: includes <!-- Source: path | file://url --> when converted
- String artifact_ref
     Original artifact this markdown was converted from
     invariant: path to PDF, PPTX, DOCX, etc.
- Chunk[] chunk(): Chunk[]
     Markdown
     Splits by slide, heading, or whole file

Chunk
- String path
     Path to chunk file
     invariant: <workspace>/ace-output/ace-context-to-memory/memory/<folder>/<stem>__<label>.md
- String content
     Chunk content
     invariant: includes <!-- Source: path | file://url --> for attribution
- String source_ref
     Original source path and location (slide/section)
     invariant: <!-- Source: path, location | url -->

Memory
- String path
     Folder in <workspace>/ace-output/ace-context-to-memory/memory/
     invariant: each folder = one memory
- Chunk[] chunks
     Chunked markdown for one specific file
     invariant: all chunks from same original artifact
- String artifact_ref
     Original artifact (source file: PDF, PPTX, DOCX, etc.)
     invariant: path or file://url to the file that was added
- String markdown_ref
     Markdown converted artifact (full file, alongside original)
     invariant: same folder as original; entire content converted to markdown
- Memory[] children
     Nested memories
     invariant: memories are nested (folder hierarchy)

Memories
- String root_path
     <workspace>/ace-output/ace-context-to-memory/memory/ subfolder
     invariant: under workspace
- Memory[] memories
     All memory folders (nested)
- Chunk[] refer(): Chunk[]
     Chunks available for agents/context to find

Workspace
- String path
     Folder (root of project/IDE or subfolder)
     invariant: everything gets packed into this workspace
- String name
     Workspace identifier
     invariant: derived from path
```

### D.3) Inline Concepts (ace-context-to-memory)

| Concept | Properties | Operations |
|---------|------------|------------|
| **ContentSource** | path, format | convert(): Markdown |
| **Markdown** | path, content | chunk(): Chunk[] |
| **Chunk** | path, content, source_ref | — |
| **Memory** | path, chunks, artifact_ref, markdown_ref, children | — |
| **Memories** | root_path, memories | refer(): Chunk[] |
| **Workspace** | path, name | — |

### D.4) Notes (ace-context-to-memory)

- **Very specific skill:** ace-context-to-memory does one thing: take content → convert → chunk → memories. Does not need to change as we create new skills.
- **Memories structure:** Each folder in the memory subfolder = one Memory. A Memory = chunked markdown for one specific file. Memories are nested. Each memory points to (1) original artifact and (2) markdown converted artifact.
- **Conversion in place:** The original artifact is converted in its entirety to markdown; the markdown file is stored alongside the original (same folder). Chunks are derived from that markdown and stored in memory.
- **Triad:** Memory ↔ Original Artifact ↔ Markdown Converted Artifact. Each memory links to both: the source file (artifact_ref) and the full markdown version (markdown_ref, alongside original).
- **Chunking strategy:** Slide decks → one chunk per slide; docs >200 lines → split at # or ##; small files → single chunk.
- **Source attribution:** Each chunk includes `<!-- Source: path | file://url -->` for traceability.
- **Integration:** How chunks are added to context (e.g. Vesta 7) is separate; this skill produces referable chunks.
- **Workspace:** All skill operations happen in the context of a workspace — a folder (likely at root of project/IDE, or a subfolder). Everything gets packed into this workspace. Workspace path in engine config (engine knows where to find it).
- **Skill outputs:** Always at <workspace>/ace-output/<skill>/. This skill's memory: <workspace>/ace-output/ace-context-to-memory/memory/.

---

## Notes (Slice 1)

- **Object-oriented model:** AgileContextEngine → AceSkill[] (not EngineConfig). Each ace-skill has path, RuleSet (markdown + JSON), hard-coded properties (core_definition, intro, output_structure, shape, validation), assembled agent file, build method.
- **Ace-skill:** Shaping skill is `ace-shaping` (currently `solution-shaping`). Every ace-skill has the same five content pieces: core-definitions, intro, output-structure, shaping-process, validation.
- **Rule dual representation:** Ace-skill–rule relationship lives in (1) markdown (content files) and (2) JSON (for scanners).
- **Create Skill:** User creates markdown(s) describing intent; initiates build ace-skill through AI. AI uses Build-ACE skill; skill runs script with params to create scaffolding; AI fills content pieces from markdown/prompts/text; if incomplete, user completes; AI reruns build script when done.
- **Python/JSON hybrid:** Config lists skill paths in JSON; Python (or CLI) loads skills and assembles; instruction injection uses merged content.
- **Architecture-pattern constraints:** Constraints (must use X, must run in Y time) are stored in config and applied when validating shaping output.
- **Workspace:** All skill operations happen in the context of a workspace — a folder (likely at root of project/IDE, or a subfolder). Everything gets packed into that workspace. Current workspace saved in engine config JSON. Example config path: `.cursor/agile-context-engine.json`. Example format: `{ "workspace_path": "/abs/path/to/workspace", "skills": ["skills/ace-shaping"], "constraints": [] }`. Config lives outside workspace so engine can find it on load.
- **Skill outputs:** Always at <workspace>/ace-output/<skill>/. Fixed convention; never changes.
- **Context from memories, not raw paths:** Gather Context populates memory (convert, chunk, sync via ace-context-to-memory) and then refers to it. Context comes from Memories (memory/ subfolder under workspace). Each folder = one Memory = chunked markdown for one file. Each memory points to (1) original artifact and (2) markdown converted artifact (full conversion, alongside original). Memories are nested. Shaping refers to memories for context — not to raw file paths. Full ace-context-to-memory detail embedded below.
- **Subsequent slices:** Slice 2+ will add one-skill-vs-many, slice-as-run semantics, instruction injection, CLI, hierarchy scoping, panel, impacts.
- **Path concept:** All file-returning properties return Path objects (not strings). Path handles OS separators and centralizes path logic. Reuse `agile_bots/src/bot_path` (BotPath, StoryGraphPaths) in its entirety — do not reimplement.
