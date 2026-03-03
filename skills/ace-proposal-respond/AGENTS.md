# Core Definitions

<!-- section: proposal.core.definitions -->
## State Concepts (Proposal Response)

- **ProposalSource** — Client RFP, Q&A, requirements, or other proposal materials (PDF, PPTX, DOCX, XLSX, etc.)
- **Memory** — Converted and chunked content from proposal sources; searchable via RAG
- **ResponseFolder** — Output area where response artifacts live; created alongside proposal material; symlinked from project
- **Strategy** — Response plan: question coverage, priorities, assumptions, slice order
- **Workspace** — Root path containing proposal sources and response output

## Epic: Respond to Client Proposal

- **Actor**: Proposal author
- **Supporting**: ace-proposal-respond, ace-context-to-memory
- **Required State**: Workspace with proposal sources (RFP, Q&A, requirements)
- **Initiation**: Author requests proposal response (convert to memory, create strategy, answer questions)
- **Response**: Skill converts sources to memory; creates response folder; proposes strategy; answers questions using RAG; iterates on strategy
- **Resulting State**: Strategy approved; answers drafted; response artifacts in response folder

## Dependency: ace-context-to-memory

This skill depends on ace-context-to-memory for:
- Converting proposal documents to markdown and chunks
- Indexing chunks for semantic search (RAG)
- Running `search_memory "<query>"` when answering questions

Run `index_memory.py --path <proposal_source>` or `--memory <name>` before answering questions. Use `search_memory.py "<query>"` to retrieve relevant chunks.

---

# Process Overview

<!-- section: proposal.process.intro -->
Your task is to **respond to a client proposal** — RFP, Q&A, requirements — by converting materials to memory, creating a response strategy, and answering questions iteratively. Work in small batches: strategy first, then answer a few questions, then iterate.

**You MUST follow this process before producing any output.**

1. **Setup** — Convert proposal material to memory (ace-context-to-memory); create response folder; symlink to project.
2. **Strategy Phase first** — Analyze all documents; propose response plan (question coverage, priorities, assumptions, slice order). Save strategy. Do not answer questions until strategy is approved.
3. **Answer a few questions ONLY** — Use memory RAG to answer 3–5 questions per batch. Get user approval.
4. **Iterate** — Corrections → add DO/DO NOT to strategy; proceed to next batch or expand scope.

### When the user says

- "Create strategy," "propose response plan," "analyze and plan" → Run **create_strategy**
- "Answer questions," "answer a few," "next batch" → Run **answer_questions** (few questions only)
- "Correct," "fix that," "wrong" → Run **improve_strategy** (add DO/DO NOT to strategy; re-run)
- "Proceed," "expand," "next slice" → Run **proceed_slice** (expand scope or next batch)

### Output Paths

- **Strategy:** `<workspace>/response/strategy.md` or `<proposal_folder>/response/strategy.md`
- **Response artifacts:** `<proposal_folder>/response/` (symlinked to project)
- **Memory:** Via ace-context-to-memory (chunks, index)

### Before You Produce Output

**STOP.** Before answering any questions, you MUST:

1. [ ] Convert proposal material to memory (index_memory or convert + chunk)
2. [ ] Create response folder and symlink
3. [ ] Complete Strategy Phase (analyze, propose plan, save strategy)
4. [ ] Get user approval of the strategy
5. [ ] Answer only 3–5 questions per batch; get approval before continuing

<!-- section: proposal.process.post_strategy.review -->
## Post-Strategy Review

When user says "correct" or provides feedback that implies a reusable rule: add a **DO** or **DO NOT** to the strategy document with wrong/correct examples. Re-run the current batch until approved. Do not proceed until user approves.

---

# Strategy Phase

<!-- section: proposal.strategy.phase -->
1. **Analyze the proposal sources** to determine question coverage, dependencies, and complexity.
2. **Present the strategy** to the user. Include: question/requirement breakdown, proposed response order, assumptions, priorities, **proposed slice order** (which questions to answer first).
3. **Validate until reasonable** — User reviews; refine until approved. Do not answer questions until then.
4. **Save the strategy** to `<response_folder>/strategy.md`.

<!-- section: proposal.strategy.criteria -->
## Strategy Criteria

### 1 - Question Coverage

Map each client question or requirement to:
- Source document and section
- Dependencies (e.g. Supplier Q&A answers needed before certain sections)
- Priority (high/medium/low)
- Assumptions when information is missing

### 2 - Slice Order

Answer questions in batches of 3–5. Proposed order:
- **Dependency-first** — Questions that unblock others first
- **High-priority** — Client-critical sections
- **Value slice** — Sections that demonstrate capability early
- **Risk slice** — Sections with most uncertainty or assumptions

State your slice order and reasoning so the user can adjust.

### 3 - Depth

Decide per batch:
- **Full answer** — Complete response with citations
- **Draft** — Outline or bullet points for review
- **Placeholder** — "To be completed after Q&A" or similar

Document in the strategy what is in scope per slice.

<!-- section: proposal.strategy.slices.running -->
## Running Slices

1. **Run the first batch** — Answer 3–5 questions for Batch 1. User reviews and corrects.
2. **Corrections → strategy** — When a mistake is found, add a **DO** or **DO NOT** to the strategy document. Each correction must include:
   - The **DO** or **DO NOT** rule
   - **Example (wrong):** What was done incorrectly
   - **Example (correct):** What it should be after the fix
   - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
   - Re-run the batch until the user approves
3. **Next batch** — Proceed to the next batch. Repeat for each batch.
4. **Expand scope** — At any point, user may expand (more questions) or narrow (fewer). Update strategy and continue.
5. **Correct** — "Correct" means correct the strategy (add DO/DO NOT); do not just fix the answer in place.

<!-- section: proposal.strategy.corrections -->
## Corrections Format

When adding corrections to the strategy document, each **DO** or **DO NOT** must include:
- The **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix
- If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block

Re-run the batch until the user approves.

When answering questions, **use memory RAG** — run `search_memory "<query>"` and cite retrieved chunks. Do not answer from general knowledge when proposal content exists in memory.

---

# Output Structure

## Response Folder

- **Location:** `<proposal_folder>/response/` (e.g. `workspace/jbom response/response/`)
- **Symlink:** Project folder has symlink/junction to response folder (e.g. `response` → `workspace/jbom response/response`)
- **Contents:**
  - `strategy.md` — Response plan, assumptions, slice order, DO/DO NOT corrections
  - `batch-N/` — Per-batch answers (optional; or single `answers.md`)

## Strategy Document Format

```markdown
# Response Strategy: [Proposal Name]

## Question Coverage
| # | Question/Requirement | Source | Priority | Assumptions |
|---|----------------------|--------|----------|-------------|

## Slice Order
1. Batch 1: [questions]
2. Batch 2: [questions]
...

## DO / DO NOT (from corrections)
- **DO** — [rule]
  - Example (wrong): ...
  - Example (correct): ...
```

<!-- section: proposal.output.answer_format -->
## Answer Format

Each answer should:
- Cite source (document, section, slide/page) from memory
- Use `search_memory "<query>"` to retrieve relevant chunks before drafting
- Follow Content Voice rules (Agile by Design perspective) when applicable

---

# Validation

## Pre-Strategy Checklist

- [ ] Proposal material converted to memory (chunks + index)
- [ ] Response folder created
- [ ] Symlink from project to response folder exists
- [ ] Strategy saved to `response/strategy.md`

<!-- section: proposal.validation.pre_answer -->
## Pre-Answer Checklist

- [ ] Strategy approved by user
- [ ] Batch size is 3–5 questions only
- [ ] `search_memory` used for each question before drafting
- [ ] Sources cited (path, slide/page)

<!-- section: proposal.validation.correction -->
## Correction Checklist

When user says "correct":
- [ ] DO or DO NOT added to strategy with wrong/correct examples
- [ ] Batch re-run with corrected guidance
- [ ] User approval before proceeding

---

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

---
