# Process Overview

<!-- section: proposal.process.intro -->
Respond to a client proposal by converting materials to memory, creating a strategy, and answering questions. Work in small batches. **Correct** means add DO/DO NOT to the strategy—do not just fix the answer.

1. **Setup** — Convert to memory; create response folder; symlink.
2. **Strategy first** — Analyze documents; propose response plan; save to `response/strategy.md`. Get approval.
3. **Answer a few questions** — Use memory RAG. 3–5 per batch. Get approval.
4. **Iterate** — Corrections → add DO/DO NOT to strategy; re-run or proceed.

### When the user says

- "Create strategy," "propose plan" → **create_strategy**
- "Answer questions," "next batch" → **answer_questions**
- "Correct," "fix that," "wrong" → **improve_strategy** (add DO/DO NOT to strategy; re-run)
- "Proceed," "expand" → **proceed_slice**

### Output Paths

- **Strategy:** `response/strategy.md`
- **Response artifacts:** `response/` (symlinked)

<!-- section: proposal.process.post_strategy.review -->
## Corrections

When user says "correct" or feedback implies a reusable rule: add **DO** or **DO NOT** to the strategy with wrong/correct examples. Re-run until approved.
