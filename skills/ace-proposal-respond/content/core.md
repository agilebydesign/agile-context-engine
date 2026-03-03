# Core Definitions

<!-- section: proposal.core.definitions -->
## Concepts

- **ProposalSource** — Client RFP, Q&A, requirements (PDF, PPTX, DOCX, XLSX, etc.)
- **Memory** — Converted and chunked content; searchable via RAG (ace-context-to-memory)
- **ResponseFolder** — Output area for response artifacts; created alongside proposal material; symlinked from project
- **Strategy** — Response plan: which questions, in what order, format guidance, DO/DO NOT corrections

## What This Skill Does

- Convert proposal material to memory (via ace-context-to-memory)
- Create response folder and symlink
- Propose a strategy (question coverage, order, format)
- Answer questions using memory RAG
- **Correct** — When user says "correct," add DO/DO NOT to the strategy document; re-run

## Pattern from Shaping (what we reuse)

- **Inject prompt** — Instructions are assembled per operation and injected into the AI prompt
- **Strategy** — A strategy document (`response/strategy.md`) holds the plan and accumulated corrections
- **Correct** — Corrections go into the strategy (DO/DO NOT with wrong/correct examples); do not just fix the answer in place

## Dependency: ace-context-to-memory

- Convert documents to markdown and chunks
- Index for semantic search
- Run `search_memory "<query>"` when answering questions
