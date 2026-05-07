# Docs Guide

This file explains where information belongs in the Light profile.

The goal is to keep continuity useful without creating a heavy multi-file memory system.

## Operating assumption

The human usually does not write these files directly.
The AI agent should update them during the chat or coding session.

Treat repository markdown files as the durable shared memory layer.
Do not treat tool-internal memory as the canonical source of truth.

## Routed memory rule

Project memory is not a full-file synchronization system.
Do not read or update every project-memory file on every run.

Information should be routed to its canonical home.
Update only the files whose responsibility changed.
Most sessions should update 1-2 files in the Light profile.

Before editing memory files, produce a short update plan covering:

- which files will be updated
- why each file needs an update
- which relevant files will not be touched

For small, obvious one-file updates, a one-sentence plan is enough.

## Conversation capture

Do not wait for the human to explicitly ask for logging.

Do not write to canonical memory files at the first appearance of an idea.
Treat new hypotheses, decisions, observations, blockers, risks, and next actions as capture candidates until they stabilize.
Keep capture candidates silently during the current session.
Do not announce every candidate or repeatedly say that it is being held for later.

Write capture candidates to memory when the topic changes, the discussion reaches a conclusion, the session is ending or may be interrupted, the human explicitly asks to record something, or a decision, result, blocker, or next action becomes clear enough to preserve.
After writing, briefly report what was recorded and where.

Capture only material that changes project memory.
Do not summarize routine conversation, temporary phrasing, or early ideas that are still being refined.

Use `RECOVERY_NOTES.md` only as a short resume pointer.
Do not make it the source of truth.

## Language policy

- Communicate with the human in their preferred language when practical.
- Keep structured memory docs in the repository's dominant language unless the human explicitly asks to change it.
- If chat language and doc language differ, explain in the chat language and keep the canonical docs and file names in the chosen documentation language.
- If the documentation language is unclear or mixed, confirm it once before writing or translating structured memory files.

## One-line routing

| File | Write this here |
| --- | --- |
| `README.md` | Entry point, purpose, orientation, how to read the workspace |
| `CURRENT_STATE.md` | What is true now |
| `LOGBOOK.md` | Lightweight decisions, observations, hypotheses, notes, and supporting history |
| `RECOVERY_NOTES.md` | How to resume quickly after interruption |
| `CONTEXT_MANIFEST.md` | What to read first, what to trust, what to ignore |
| `DOCS_GUIDE.md` | Rules for where to write information |

## Update triggers

### Update `CURRENT_STATE.md` when

- confirmed behavior, constraints, or facts change
- a previous truth is retired
- the project current status changes
- a current operating rule becomes worth trusting as a stable working assumption

Avoid:

- raw ideas
- maybe statements
- observations without interpretation

### Update `LOGBOOK.md` when

- a meaningful decision is made
- an option is rejected
- an observation, test, or failed attempt teaches something
- a hypothesis, hunch, or question is worth revisiting
- a blocker, risk, or next action affects continuation

Use the `type` field to distinguish decision, research, hypothesis, and note entries.

### Update `RECOVERY_NOTES.md` when

- a session ends
- work is interrupted
- the next step should be recoverable in under a minute

Avoid:

- making this the full history
- copying long detail that belongs in `LOGBOOK.md`

## Common workflows

### New idea appears

1. Hold it as a silent capture candidate until it stabilizes.
2. If it remains worth preserving, add it to `LOGBOOK.md` with `type: hypothesis` or `type: note`.
3. If it becomes true now, update `CURRENT_STATE.md`.
4. If the session may stop, update `RECOVERY_NOTES.md`.

### Observation or result appears

1. Record the observation, method, result, confidence, and limitation in `LOGBOOK.md`.
2. If the result changes current truth, update `CURRENT_STATE.md`.
3. If it changes the next step, update `RECOVERY_NOTES.md`.

### Project direction changes

1. Add a decision entry in `LOGBOOK.md`.
2. Update `CURRENT_STATE.md` if current truths changed.
3. Add a checkpoint in `RECOVERY_NOTES.md`.

## Anti-patterns

- Putting everything in `README.md`.
- Treating `LOGBOOK.md` as current truth.
- Recording decisions without context.
- Recording observations without confidence or limitation.
- Letting recovery notes become a long hidden history.
- Copying private data into canonical docs.
