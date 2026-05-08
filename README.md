# project-memory

Japanese overview: [README.ja.md](README.ja.md)

Durable project memory across chat loss, model switches, and multi-session research.

Hypotheses don't silently become facts. Decisions record why, not just what. Recovery takes seconds, not hours of re-explanation.

Designed for Claude Code and Codex CLI. Expected to work with Gemini CLI, Cursor, and other agents supporting the Agent Skills standard.

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
| `LITERATURE_NOTES.md` | Prior work and its relevance (academic profile) |
| `FIGURES_LOG.md` | Figures and tables linked to data and methods (academic profile) |
| `GLOSSARY.md` | Project-specific terminology |

The AI agent maintains these files during the session. The human usually doesn't write them directly.

project-memory is not a checklist of files to update every time.
It is a routed memory system: agents update only the canonical files whose responsibility changed.
Most sessions update 1-3 files, not the whole memory set.

project-memory is a skeleton, not a fixed operating system.
Choose the smallest sufficient profile and customize capture triggers, review cadence, archive policy, and tool-facing instructions to fit the project.
When adopting an existing project, do not overwrite existing same-name files; place memory files in non-conflicting locations and record them in `CONTEXT_MANIFEST.md`.

## What makes this different

**Promotion rules** — A hypothesis cannot be promoted to `CURRENT_STATE.md` without evidence in `RESEARCH_LOG.md` or an explicit decision in `DECISION_LOG.md`. This prevents unverified ideas from silently becoming project assumptions.

**Conflict resolution** — When files disagree, the skill defines a clear priority order for resolving contradictions instead of silently merging them.

**Model-independent** — The memory lives in plain markdown files, not in any tool's hidden state. Switch from Claude to GPT to Gemini — hand over the folder, and the new model picks up where the last one left off.

**Tracked threads** — `HUMAN_BRIEF.md` maintains a thread table so parallel workstreams are visible at a glance, solving the problem of time-series logs being hard for humans to scan.

## Which profile should I use?

| Situation | Use |
| --- | --- |
| Small personal project or minimal continuity | `light` |
| Long-running product, coding, writing, or planning | `standard` |
| Debugging, experiments, product discovery, or repeated investigation | `research` |
| Paper, thesis, literature review, figures, or publication workflow | `academic` |

## Quick start

Preview before writing:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile standard --dry-run
```

Create a new memory workspace:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile standard
```

For research-heavy work:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile research
```

Adopt an existing project without overwriting same-name files:

```bash
python scripts/init_memory_workspace.py /path/to/project --profile standard --memory-dir memory
```

Audit an existing workspace:

```bash
python scripts/audit_memory_workspace.py /path/to/project --profile standard
```

Generate a handoff brief from existing docs:

```bash
python scripts/make_handoff_brief.py /path/to/project
```

Handoff briefs redact likely secrets by default. Use `--fail-on-secret` when automation should stop if secret-like material is detected.

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

```text
Log this paper in LITERATURE_NOTES.md and connect it to our current hypotheses.
```

```text
この実験結果をRESEARCH_LOGに記録して、関連する仮説のステータスを更新して。
図表が出たらFIGURES_LOGにも追加して。
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

### Academic

For managing a research paper, thesis, or publication. Includes everything in Research plus:

- `LITERATURE_NOTES.md` — prior work and its relevance to your research
- `FIGURES_LOG.md` — every figure and table linked to its data source and generation method

The academic profile connects literature to hypotheses, tracks which findings support or challenge your claims, and ensures every figure is reproducible. The promotion rules enforce that only evidence-backed claims enter your results.

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

**Human-reviewed cleanup.** AI agents may propose cleanup candidates for `HYPOTHESIS_LAB.md`, grouped as merge, promote, link to evidence, mark as dropped, or delete. They should not remove hypotheses or raw sparks without human approval.

**Update with discipline.** `HUMAN_BRIEF.md` is reviewed when decisions, risks, blockers, or tracked threads change — and updated only when the human-facing picture actually changed.

## Package layout

```text
.github/                       # CI and issue templates
SKILL.md                       # Instructions for the AI agent
README.md                      # This file — guide for humans
manifest.txt                   # File manifest
templates/                     # Copyable memory workspace templates
profiles/                      # Profile file lists (light/standard/research/academic)
scripts/                       # Helper scripts (init, audit, handoff)
examples/                      # Sample log entries and handoff briefs
tasks/                         # Task-specific guidance docs
```

## Feedback wanted

This project is still early.

If you try it, I would especially appreciate feedback on:

- whether the file structure feels too heavy or too light
- whether the promotion rules are clear
- whether the research / academic profile is useful
- whether this works naturally with Claude Code, Codex, Gemini CLI, or Cursor

If it seems useful, a star also helps others find it.

## Feedback and issues

If something is confusing or broken, please open a GitHub issue.

- Use the bug report form for broken scripts, incorrect file routing, missing templates, or behavior that contradicts the documented rules.
- Use the improvement form for new profile ideas, workflow pain points, agent compatibility gaps, or onboarding/doc quality feedback.
- Include the tool or agent you used, the profile (`light`, `standard`, `research`, or `academic`), and a small prompt or reproduction example when possible.

## License

MIT
