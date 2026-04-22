# project-memory

Durable project memory across chat loss, model switches, and multi-session research.

Hypotheses don't silently become facts. Decisions record why, not just what. Recovery takes seconds, not hours of re-explanation.

Works with Claude Code, Codex CLI, Gemini CLI, Cursor, and any agent that supports the Agent Skills standard.

## The problem

You're deep into a project with an AI agent. Then:

- The chat disappears. Context is gone.
- You switch models. The new one knows nothing.
- A teammate joins. There's no onboarding doc.
- Six months later, nobody remembers why that decision was made.
- An insight from last week's experiment never connects to today's decision.
- You can't tell which hypotheses you've already tested and ruled out.

Every long-running project hits this. Most people work around it by re-explaining everything from scratch. This skill solves it structurally — not just as a backup, but as a structured knowledge base that accumulates and becomes analysable over time.

## How it works

The skill separates project knowledge into canonical markdown files, each with a clear role:

| File | What it holds |
| --- | --- |
| `CURRENT_STATE.md` | What is true right now |
| `ROADMAP.md` | What is planned |
| `DECISION_LOG.md` | What was decided and why |
| `RESEARCH_LOG.md` | What was tested, observed, or investigated |
| `HYPOTHESIS_LAB.md` | What is still unverified |
| `HUMAN_BRIEF.md` | What a human should read first |
| `RECOVERY_NOTES.md` | How to resume after interruption |
| `CONTEXT_MANIFEST.md` | Read order, canonical sources, ignore rules |
| `DOCS_GUIDE.md` | Rules for where to write information |
| `GLOSSARY.md` | Project-specific terminology |

The AI agent maintains these files during the session. The human usually doesn't write them directly.

## What makes this different

**Promotion rules** — A hypothesis cannot be promoted to `CURRENT_STATE.md` without evidence in `RESEARCH_LOG.md` or an explicit decision in `DECISION_LOG.md`. This prevents unverified ideas from silently becoming project assumptions.

**Conflict resolution** — When files disagree, the skill defines a clear priority order for resolving contradictions instead of silently merging them.

**Model-independent** — The memory lives in plain markdown files, not in any tool's hidden state. Switch from Claude to GPT to Gemini — hand over the folder, and the new model picks up where the last one left off.

**Tracked threads** — `HUMAN_BRIEF.md` maintains a thread table so parallel workstreams are visible at a glance, solving the problem of time-series logs being hard for humans to scan.

## Quick start

Create a new memory workspace:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile research
```

For a smaller project:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile standard
```

Preview without writing:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile research --dry-run
```

Audit an existing workspace:

```bash
python scripts/audit_memory_workspace.py /path/to/project --profile research
```

Generate a handoff brief from existing docs:

```bash
python scripts/make_handoff_brief.py /path/to/project
```

## Example prompts

```text
Resume this project. Read CONTEXT_MANIFEST.md and RECOVERY_NOTES.md first, then tell me what to do next.
```

```text
Classify this conversation into the continuity docs. Output patch-ready sections for each file that should change.
```

```text
Create a handoff brief for another model. Keep hypotheses, facts, decisions, and open questions strictly separated.
```

```text
Log what we just discovered in RESEARCH_LOG.md format with methods, results, confidence, and limitations.
```

```text
このプロジェクトを再開したい。CONTEXT_MANIFEST.md と RECOVERY_NOTES.md から読んで、次に何をすべきか出して。
```

```text
この会話内容を continuity docs に分類して、更新すべきファイルごとに patch-ready で出して。
```

```text
別モデルに渡すための handoff brief を作って。仮説・事実・決定・未解決点を混ぜないで。
```

## Profiles

### Light

For very small projects or personal notes.

Files: `README.md`, `CURRENT_STATE.md`, `RECOVERY_NOTES.md`, `LOGBOOK.md`, `DOCS_GUIDE.md`, `CONTEXT_MANIFEST.md`

### Standard

For general long-running work, product development, and writing projects.

Files: `README.md`, `CURRENT_STATE.md`, `ROADMAP.md`, `DECISION_LOG.md`, `HYPOTHESIS_LAB.md`, `HUMAN_BRIEF.md`, `RECOVERY_NOTES.md`, `DOCS_GUIDE.md`, `CONTEXT_MANIFEST.md`, `GLOSSARY.md`

### Research

For research, experiments, literature review, product discovery, or exploratory engineering. Includes everything in Standard plus:

- `RESEARCH_LOG.md`
- Stronger promotion rules from hypothesis to confirmed truth
- Evidence and confidence fields

## Agent integration

If your repository uses `AGENTS.md`, `CLAUDE.md`, or similar tool-facing files:

- Keep them short
- Point them to `CONTEXT_MANIFEST.md` and `CURRENT_STATE.md`
- Have the agent write updates back into the canonical markdown docs
- Do not duplicate project memory inside tool-specific files

This keeps Codex, Claude Code, Gemini CLI, and other agents aligned on a single source of truth.

## Key idea

The AI agent updates these files. The human reads them when needed.

This only works if the memory lives in normal files in the repository — not in a tool's hidden state, not in chat history, not in a vendor-specific memory feature. Plain markdown in the repo is the canonical memory layer.

## Design notes

**README stays the entrance, not the dump.** `CURRENT_STATE.md` holds the canonical truth. This prevents setup instructions, decisions, hypotheses, and recovery notes from collapsing into one overloaded file.

**Capture broadly, promote narrowly.** `HYPOTHESIS_LAB.md` should capture more than you think you need. The cost of over-capturing is lower than losing a useful idea.

**Update with discipline.** `HUMAN_BRIEF.md` is reviewed when decisions, risks, blockers, or tracked threads change — and updated only when the human-facing picture actually changed.

## Package layout

```text
SKILL.md                       # Instructions for the AI agent
README.md                      # This file — guide for humans
manifest.txt                   # File manifest
templates/                     # Copyable memory workspace templates
profiles/                      # Profile file lists (light/standard/research)
scripts/                       # Helper scripts (init, audit, handoff)
examples/                      # Sample log entries and handoff briefs
tasks/                         # Task-specific guidance docs
```

## License

MIT
