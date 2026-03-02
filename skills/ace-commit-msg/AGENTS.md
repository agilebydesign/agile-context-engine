# Core Definitions

## CommitScope

The unit of work a commit describes. **No story_graph** — scope is inferred from conversation, changed files, and persisted state.

**Scope sources (priority order):**
1. **last_commit_scope.json** — Persisted scope from last meaningful commit or user override
2. **scope.json** — Current working scope (if non-empty)
3. **Conversation** — What the user asked to do; features, areas, artifacts discussed
4. **Changed files** — Paths, directory structure, file names, document content

**Scope granularity (most specific wins):**
- Feature/area name (e.g. "bot panel", "scope enrichment")
- Document type (e.g. "prioritization", "story map increments")
- Path-derived (e.g. "Invoke Bot" from `test/invoke_bot/`)
- Generic ("project artifacts") when nothing specific found

## Behavior

What kind of work the commit represents. Inferred from **changed files** first; fallback to `behavior_action_state.json` if present.

| Changed content | Behavior |
|-----------------|----------|
| Application/source code | `code` |
| Test files | `tests` |
| Story structure (epics, sub-epics, stories) | `shape` |
| Increments | `prioritization` |
| Acceptance criteria | `exploration` |
| Scenarios / BDD steps | `scenarios` |
| CRC / domain concepts | `domain` |
| CRC design | `design` |
| Walkthrough | `walkthrough` |

## Action

The operation performed. From `current_action` (e.g. `render`, `build`, `validate`) or inferred (`build` for code/tests, `fix` for corrections).

## CommitMessage

The generated message. Format: `{behavior}.{action}: {meaningful description based on scope}`

- Present tense verbs
- Under 80 characters when possible
- Describe WHAT changed in relation to scope

---

# Process

## When to Run

- User types `/commit` or requests a commit
- After completing a meaningful change (auto-commit when configured)
- **CRITICAL:** Do NOT commit before completing the user's primary instructions. If the user's message contains scope, behavior instructions, validation steps, build process, or workflow steps AND "commit", complete those first. The commit rule must not shortcut the actual workflow.

## Process Steps

1. **Read context files** (workspace root):
   - `last_commit_scope.json` — Preferred scope source
   - `scope.json` — Fallback scope
   - `behavior_action_state.json` — Current behavior/action (optional; override from changed files)

2. **Update last scope** (if scope.json changed):
   - If `scope.json` has non-empty `value`, save to `last_commit_scope.json` with timestamp
   - User overrides: "scope is [name]" or "scope is all" → save immediately

3. **Infer behavior from changed files**:
   - Run `git status` and `git diff`
   - Match changed content to behavior (code, tests, shape, prioritization, exploration, scenarios, domain, design)
   - Use `behavior_action_state.json` only if changed files don't clearly match

4. **Infer scope** (when both scope files empty):
   - **First:** Conversation — what did the user ask? What features, areas, artifacts were discussed?
   - **Then:** Changed files — paths, directory names, document types, file names
   - Save inferred scope to `last_commit_scope.json`
   - Last resort: `{behavior}.{action}: Update project artifacts`

5. **Generate commit message**:
   - Format: `{behavior}.{action}: {meaningful description based on scope}`
   - Use present tense; keep concise; reference scope when relevant

6. **Execute**:
   - `git add -A`
   - `git commit -m "message"`
   - **Never** add Co-authored-by trailers

## Scope Inference (No story_graph)

**From conversation:** Epic, sub-epic, story, feature area, document type — whatever the user discussed. Use chat history.

**From changed files:**
- `test/invoke_bot/...` → "Invoke Bot" or "perform action"
- `docs/story/prioritization/*` → "story map increments" or "prioritization"
- `src/panel/*.js` → "bot panel" or "UI components"
- `story-graph.json` diff → parse for epic/story names if present (optional; not required)
- `docs/crc/*` → "CRC documentation"
- Test file name `test_render_drawio_diagrams.py` → "Synchronized Graph" or "DrawIO diagrams"

**Scope is "all":** Use generic description.

---

# Strategy

No separate strategy phase. Scope and behavior inference (see Process) replaces story-graph-based scope. The "strategy" is: infer from conversation first, then changed files; persist to last_commit_scope.json.

---

# Output Structure

## Commit Message Format

```
{behavior}.{action}: {meaningful description based on scope}
```

**Examples:**
- `prioritization.render: Update story map increments for Invoke Bot`
- `code.build: Fix scope in instructions and validation context`
- `tests.build: Fix EnrichScopeWithLinks scenario test links`
- `shape.build: Add story structure for user management`
- `exploration.build: Add acceptance criteria for user management stories`
- `design.render: Update CRC documentation`

## Scope Output

When scope is inferred or updated, persist to `last_commit_scope.json`:

```json
{
  "value": ["Scope Name 1", "Scope Name 2"],
  "timestamp": "2026-03-01T12:00:00"
}
```

- `value`: Array of scope identifiers (feature area, epic name, document type, etc.)
- `timestamp`: When scope was set or inferred

## Behavior → Action Mapping

| Behavior | Typical actions |
|----------|-----------------|
| code | build, fix |
| tests | build, fix |
| shape | build |
| prioritization | render |
| exploration | build |
| scenarios | build |
| domain | build |
| design | render, refine |
| walkthrough | build |

---

# Validation

## Commit Message Checklist

Before executing the commit, verify:

- [ ] **Format:** `{behavior}.{action}: {description}`
- [ ] **Behavior** inferred from changed files (or behavior_action_state.json)
- [ ] **Scope** from last_commit_scope.json, scope.json, or inferred from conversation/changed files
- [ ] **Description** uses present tense; describes WHAT changed; references scope when relevant
- [ ] **Length** under 80 characters when possible
- [ ] **No Co-authored-by** trailers

## Scope Inference Checklist

When inferring scope (both files empty):

- [ ] **Conversation first** — What did the user ask? What features, areas, artifacts were discussed?
- [ ] **Changed files second** — Paths, directory names, document types
- [ ] **Persist** inferred scope to last_commit_scope.json
- [ ] **Confirm** to user: "Inferred scope as [name] from conversation" or "from changed files"

---

# Script Invocation

No scripts. Use as Cursor rule (`.cursor/rules/`) or inject AGENTS.md into the AI prompt when user requests a commit. The skill produces instructions only; the AI executes `git add` and `git commit`.

---
