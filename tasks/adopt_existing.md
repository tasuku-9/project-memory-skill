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
3. Detect the dominant repository language from the README, docs, and existing file names. If the documentation language is unclear or mixed, plan to confirm it once before writing canonical docs.
4. Scan recent git log if available: `git log --oneline -30`. Look for decision points, direction changes, and major milestones.
5. Ask the user:
   - **What is this project and where is it now?**
   - **Is there anything not in the files that I should know?** Decisions made in chat, rejected approaches, unwritten rules.
   - **What is the immediate goal?**
   - **Only if language is unclear or mixed:** Which language should canonical docs use?

### Phase 2: Classify and route

Map existing information into canonical files. Use this classification:

| Found in existing docs | Route to |
| --- | --- |
| "We are using X", "The system does Y", current architecture | `CURRENT_STATE.md` |
| "We chose X over Y because Z", ADRs, rejected approaches | `DECISION_LOG.md` |
| "We tested X and found Y", benchmarks, experiments | `RESEARCH_LOG.md` |
| "We should try X", "maybe X would work", open questions | `HYPOTHESIS_LAB.md` |
| Planned features, milestones, TODO lists, backlog | `ROADMAP.md` |
| Blockers, risks, current priority | `HUMAN_BRIEF.md` |
| Project-specific jargon, abbreviations, internal names | `GLOSSARY.md` |
| Setup instructions, "how to run this" | Keep in `README.md` |

Preserve the repository's established documentation language for canonical files unless the user explicitly wants to change it.

### Phase 3: Write canonical files

Write in this order:

1. `CURRENT_STATE.md` - extract confirmed truths from README and existing docs
2. `DECISION_LOG.md` - extract past decisions with rationale. If rationale is missing, record the decision and mark rationale as `unknown - predates project-memory`
3. `ROADMAP.md` - extract plans, TODOs, and known blockers
4. `RESEARCH_LOG.md` - extract any documented experiments or test results
5. `HYPOTHESIS_LAB.md` - extract unverified ideas and open questions
6. `HUMAN_BRIEF.md` - write a fresh summary based on what was classified
7. `RECOVERY_NOTES.md` - first checkpoint
8. `CONTEXT_MANIFEST.md` - set profile, read order, and documentation language if it was confirmed
9. `GLOSSARY.md` - extract terminology if any was found

### Phase 4: Slim down the README

After routing content to canonical files:

- Remove current-state descriptions from README (now in `CURRENT_STATE.md`)
- Remove decision history from README (now in `DECISION_LOG.md`)
- Remove plans and TODOs from README (now in `ROADMAP.md`)
- Keep: project name, one-paragraph description, setup/install instructions, link to `CONTEXT_MANIFEST.md` for full project context

Add a pointer at the top or bottom of README:

```md
## Project memory

This project uses [project-memory](<REPO_URL>) for structured context management. See `CONTEXT_MANIFEST.md` for the read order and canonical file roles.
```

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
| `RESEARCH_LOG.md` | ... | docs/ |
| `HYPOTHESIS_LAB.md` | ... | user |
| `HUMAN_BRIEF.md` | ... | synthesized |

### README changes

- Removed: ...
- Kept: ...
- Added: project-memory pointer

### Gaps

- Decisions without rationale: ...
- Areas with no documentation: ...

### Recommended next action

...
```

## Common mistakes

- Copying README content into canonical files without classifying it. Each piece of information should be routed to exactly one file based on its type.
- Deleting the README. README stays as the entry point with setup instructions.
- Inventing rationale for old decisions. If the reason is unknown, write `unknown - predates project-memory`. Do not guess.
- Trying to capture everything at once. Focus on what matters now. Old history can be backfilled later if needed.
- Duplicating content across canonical files and `AGENTS.md` / `CLAUDE.md`. The canonical docs are the source of truth; tool files just point to them.
