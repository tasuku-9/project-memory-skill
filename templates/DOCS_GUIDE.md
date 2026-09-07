# Docs Guide

This file explains where information belongs.

The goal is to prevent a single file, chat transcript, or README from becoming overloaded.

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
Most sessions should update 1-3 files, not the whole memory set.

Before editing memory files, produce a short update plan covering:

- which files will be updated
- why each file needs an update
- which relevant files will not be touched

For small, obvious one-file updates, a one-sentence plan is enough.

If information seems to belong in multiple files, choose the most canonical file using this guide and `CONTEXT_MANIFEST.md`.
Other files may reference the canonical entry, but should not duplicate the full details.

## Conversation capture

First apply the capture strength in `CONTEXT_MANIFEST.md` to decide what is eligible. File routing below does not override that scope or the timing rule.

Keep candidates silently while the discussion develops. Automatic writes happen at a topic change, conclusion, or genuine stopping point, not at the first appearance of an idea or merely because it sounds clear. An explicit request to record something can override the wait.

At that boundary, write only the latest outcome that changes project memory. Do not preserve superseded drafts or withdrawn proposals as current decisions. Still-useful unresolved ideas may be recorded as unverified when the selected capture strength includes them.

Use the update plan above for necessary edits, then briefly report actual writes. A boundary does not require an edit: skip unchanged entries and checkpoints. Do not announce that candidates are being held or that nothing was written during ordinary conversation.

This skill cannot recover session-local candidates lost before a write. Copying accessible transient attachments to durable storage can happen immediately; their interpretation and canonical log entries still follow this capture policy.

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
{{DOCS_GUIDE_ROUTING_ROWS}}

## Update triggers

### Update `CURRENT_STATE.md` when

- confirmed behavior, constraints, or facts change
- a previous truth is retired
- the project’s current status changes
- a current operating rule becomes worth trusting as a stable working assumption

Avoid:

- raw ideas
- “we might” statements
- experiments without interpretation
- direct promotion from `HYPOTHESIS_LAB.md`

### Update `ROADMAP.md` when

- planned work changes
- priorities change
- blockers change
- a hypothesis becomes planned work

Avoid:

- treating planned work as completed work
- burying rationale that belongs in `DECISION_LOG.md`

### Update `DECISION_LOG.md` when

- a meaningful decision is made
- an option is rejected
- a workaround or rule is introduced
- a finding changes direction

Avoid:

- routine edits
- entries without rationale

{{DOCS_GUIDE_RESEARCH_TRIGGER}}

### Update `HYPOTHESIS_LAB.md` when

- an idea is worth preserving but not yet accepted
- a possible explanation appears
- an experiment idea appears
- the user expresses a new idea, discomfort, possibility, or half-formed thought

Use `Raw sparks` for low-commitment captures and `Working hypotheses` for structured, recurring, or next-step-ready ideas.

Avoid:

- silently promoting ideas into current truth
- requiring the human to explicitly ask for logging

### Update or review `HUMAN_BRIEF.md` when

- the current goal, main blocker, main risk, or next decision changes
- a decision changes project direction, priority, risk, tracked threads, or required human decisions
{{DOCS_GUIDE_HUMAN_BRIEF_EVIDENCE_TRIGGER}}
- a hypothesis is promoted into `CURRENT_STATE.md`
- a tracked thread starts, pauses, resumes, closes, or becomes blocked
- a recovery checkpoint changes what a human should do next

Do not update it for routine progress notes unless the human-facing picture changed.

Keep it short. It is for human judgment, not proof, history, or detailed methods.

### Update `RECOVERY_NOTES.md` when

- a session ends
- work is interrupted
- the next step should be recoverable in under a minute

Avoid:

- making this the full history
- copying long research detail

## Common workflows

### New idea appears

Apply Conversation capture first; the following steps are conditional routes, not a checklist.

1. At a capture boundary, add an eligible, still-useful idea to `HYPOTHESIS_LAB.md`, usually under `Raw sparks`.
2. If it becomes structured or recurring, move or summarize it under `Working hypotheses`.
3. If it becomes planned work, add it to `ROADMAP.md`.
{{DOCS_GUIDE_NEW_IDEA_TEST_STEP}}
5. If it drives a choice, record the choice in `DECISION_LOG.md`.
6. If it becomes true now, update `CURRENT_STATE.md`.
7. If the session reaches a stopping point and the resume pointer changed, update `RECOVERY_NOTES.md`.

{{DOCS_GUIDE_EVIDENCE_WORKFLOW}}

### Project direction changes

1. Add a decision entry in `DECISION_LOG.md`.
2. Update `ROADMAP.md`.
3. Update `CURRENT_STATE.md` if current truths changed.
4. Update `HUMAN_BRIEF.md` if the human-facing picture changed.
5. Add a checkpoint in `RECOVERY_NOTES.md`.

### Handoff to another model

1. Read `CONTEXT_MANIFEST.md`.
2. Read latest `RECOVERY_NOTES.md`.
3. Read `HUMAN_BRIEF.md` and `CURRENT_STATE.md`.
4. Pull only relevant decisions, research entries, and hypotheses.
5. State ignore rules and privacy boundaries.

## Anti-patterns

- Putting everything in `README.md`.
- Treating `ROADMAP.md` as proof something is done.
- Treating `HYPOTHESIS_LAB.md` as truth.
- Recording decisions without alternatives or rationale.
{{DOCS_GUIDE_RESEARCH_ANTI_PATTERN}}
- Letting recovery notes become a long hidden history.
- Copying private data into canonical docs.
- Letting `AGENTS.md` or `CLAUDE.md` become a second hidden source of truth.
