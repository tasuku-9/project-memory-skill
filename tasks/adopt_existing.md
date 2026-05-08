# Adopt Existing Project Task

Use this when introducing project-memory into a project that already has code, documents, history, or accumulated context, but no structured memory workspace yet.

## Detecting adopt state

A project is in adopt state when:

- The project directory contains code, docs, or other working files
- No `CONTEXT_MANIFEST.md` exists
- No `CURRENT_STATE.md` exists (or it is an empty template)
- Context lives in one or more of: an overloaded README, scattered notes, chat history, git log, the user's head

## Process

### Phase 1: Inventory existing context

1. Read `README.md` if present. Note what it contains: setup instructions, current state, decisions, plans, hypotheses. Most READMEs mix all of these.
2. Check for existing documentation: `docs/`, `notes/`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`, `ADR/` (architecture decision records), or similar.
3. Check for path collisions with project-memory template names, especially `README.md`, `ROADMAP.md`, `DECISION_LOG.md`, `AGENTS.md`, and `CLAUDE.md`. Treat existing same-name files as user-owned.
4. Detect the dominant repository language from the README, docs, and existing file names. If the documentation language is unclear or mixed, plan to confirm it once before writing canonical docs.
5. Scan recent git log if available: `git log --oneline -30`. Look for decision points, direction changes, and major milestones.
6. Recommend a profile and capture trigger strength based on the project shape:
   - `light`: small personal project, short-lived work, or minimal continuity
   - `standard`: normal coding, writing, or product work with decisions and next actions
   - `research`: experiments, evidence, hypotheses, repeated investigation, or debugging loops
   - `academic`: literature, figures, tables, thesis, paper, or publication workflow
7. Ask the user:
   - **What is this project and where is it now?**
   - **Is there anything not in the files that I should know?** Decisions made in chat, rejected approaches, unwritten rules.
   - **What is the immediate goal?**
   - **Does the recommended profile and capture trigger strength fit?** If not, adjust them.
   - **Only if language is unclear or mixed:** Which language should canonical docs use?

### Phase 2: Classify and route

Map existing information into canonical files. Use this classification:

| Found in existing docs | Route to |
| --- | --- |
| "We are using X", "The system does Y", current architecture | `CURRENT_STATE.md` |
| "We chose X over Y because Z", ADRs, rejected approaches | `DECISION_LOG.md` |
| "We tested X and found Y", benchmarks, experiments | `RESEARCH_LOG.md` when present; otherwise `DECISION_LOG.md` if it changed direction |
| "We should try X", "maybe X would work", open questions | `HYPOTHESIS_LAB.md` |
| Planned features, milestones, TODO lists, backlog | `ROADMAP.md` |
| Blockers, risks, current priority | `HUMAN_BRIEF.md` |
| Project-specific jargon, abbreviations, internal names | `GLOSSARY.md` |
| Setup instructions, "how to run this" | Keep in `README.md` |

Preserve the repository's established documentation language for canonical files unless the user explicitly wants to change it.

### Phase 3: Write canonical files

Never overwrite existing project files without explicit user approval.
If a project-memory template path collides with an existing file, choose a non-conflicting location such as `memory/` or `project-memory/`, or keep the existing file as the canonical source if it already serves that role.
Record the chosen canonical locations in `CONTEXT_MANIFEST.md`.
The init script can do this safely with `--memory-dir memory`; when it detects same-name files and no explicit memory directory is given, it writes the generated memory workspace under `memory/` by default.

Write these roles in this order, using the chosen canonical locations and only when the selected profile includes the file:

1. `CURRENT_STATE.md` - extract confirmed truths from README and existing docs
2. `DECISION_LOG.md` - extract past decisions with rationale. If rationale is missing, record the decision and mark rationale as `unknown - predates project-memory`
3. `ROADMAP.md` - extract plans, TODOs, and known blockers
4. `RESEARCH_LOG.md` - extract any documented experiments or test results when present
5. `HYPOTHESIS_LAB.md` - extract unverified ideas and open questions
6. `HUMAN_BRIEF.md` - write a fresh summary based on what was classified
7. `RECOVERY_NOTES.md` - first checkpoint
8. `CONTEXT_MANIFEST.md` - set profile, read order, and documentation language if it was confirmed
9. `GLOSSARY.md` - extract terminology if any was found

### Phase 4: Handle README safely

Existing `README.md` is user-owned.
Do not overwrite, delete, or aggressively slim it down without explicit user approval.

After routing content to canonical files, propose README changes rather than applying them automatically:

- Keep project name, one-paragraph description, and setup/install instructions.
- Optionally move current-state descriptions, decision history, plans, or TODOs into canonical docs.
- Optionally add a pointer at the top or bottom of README:

```md
## Project memory

This project uses [project-memory](<REPO_URL>) for structured context management. See `CONTEXT_MANIFEST.md` for the read order and canonical file roles.
```

If the memory workspace lives under `memory/`, point to `memory/CONTEXT_MANIFEST.md` instead.

### Phase 5: Handle AGENTS.md / CLAUDE.md

If the project already uses `AGENTS.md`, `CLAUDE.md`, or similar tool-facing files:

- Do not delete them
- Add a line pointing to `CONTEXT_MANIFEST.md` as the read-first document
- Move any project memory content from these files into the canonical docs
- Keep these files short and focused on tool-specific configuration only

## Response structure

```md
## Adoption Summary

### Sources inventoried

| Source | Content found |
| --- | --- |
| `README.md` | ... |
| `docs/` | ... |
| git log | ... |
| User input | ... |

### Classification result

| Canonical file | Entries written | Source |
| --- | --- | --- |
| `CURRENT_STATE.md` | ... | README, user |
| `DECISION_LOG.md` | ... | README, git log |
| `ROADMAP.md` | ... | README |
| `RESEARCH_LOG.md` | ... | docs/ when present |
| `HYPOTHESIS_LAB.md` | ... | user |
| `HUMAN_BRIEF.md` | ... | synthesized |

### README changes

- Proposed: ...
- Applied only with user approval: ...

### Collision handling

- Existing same-name files: ...
- Canonical locations chosen: ...

### Gaps

- Decisions without rationale: ...
- Areas with no documentation: ...

### Recommended next action

...
```

## Common mistakes

- Copying README content into canonical files without classifying it. Each piece of information should be routed to exactly one file based on its type.
- Overwriting or deleting existing same-name project files. Existing files are user-owned unless the user explicitly says otherwise.
- Defaulting to the largest profile or strongest capture trigger just to be safe.
- Inventing rationale for old decisions. If the reason is unknown, write `unknown - predates project-memory`. Do not guess.
- Trying to capture everything at once. Focus on what matters now. Old history can be backfilled later if needed.
- Duplicating content across canonical files and `AGENTS.md` / `CLAUDE.md`. The canonical docs are the source of truth; tool files just point to them.
