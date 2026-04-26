# Init Session Task

Use this when the memory workspace has just been created and all canonical files are empty templates. This is the first session with project-memory on a new project.

## Detecting init state

A workspace is in init state when all of the following are true:

- `CURRENT_STATE.md` contains only the template placeholders (no project-specific content)
- `RECOVERY_NOTES.md` has no dated entries
- `HUMAN_BRIEF.md` has no one-paragraph summary

If any of these files contain real content, this is not an init session. Use `resume_work.md` instead.

## Process

1. Confirm that the workspace is in init state.
2. Ask the user four things:
   - **What is this project?** One-sentence purpose.
   - **Where are you now?** Current stage, maturity, or progress.
   - **What is the immediate goal?** What should happen next.
   - **What constraints or decisions already exist?** Known rules, chosen tools, rejected approaches, or anything the agent should not re-evaluate.
3. Do not ask more than these four unless the canonical documentation language is unclear. In that case, ask one extra confirmation and record the answer in `CONTEXT_MANIFEST.md` or `DOCS_GUIDE.md`. Start with minimal viable memory and let it grow through use.
4. Write the answers into canonical files in this order:
   - `CURRENT_STATE.md` - project purpose, current stage, known constraints
   - `ROADMAP.md` - immediate goal as the first NOW item, any mentioned future work as NEXT or LATER
   - `DECISION_LOG.md` - any decisions or rejected alternatives the user mentioned
   - `HUMAN_BRIEF.md` - one-paragraph summary, current goal, main blocker if known
   - `RECOVERY_NOTES.md` - first checkpoint with today's date
   - `CONTEXT_MANIFEST.md` - update the profile, last-updated date, and documentation language if it was confirmed
5. Leave `RESEARCH_LOG.md`, `HYPOTHESIS_LAB.md`, and `GLOSSARY.md` empty until content naturally arises. Do not fill them with placeholders.
6. Return a summary of what was written and where.

## Response structure

```md
## Init Summary

### Project

...

### Written to

| File | What was written |
| --- | --- |
| `CURRENT_STATE.md` | ... |
| `ROADMAP.md` | ... |
| `DECISION_LOG.md` | ... |
| `HUMAN_BRIEF.md` | ... |
| `RECOVERY_NOTES.md` | ... |

### Left empty (will populate during work)

- `RESEARCH_LOG.md`
- `HYPOTHESIS_LAB.md`
- `GLOSSARY.md`

### Recommended next action

...
```

## Common mistakes

- Asking too many questions upfront. Four is enough to start. Memory grows through use, not through interviews.
- Filling every file with placeholder content. Empty files are better than fake entries.
- Running Resume mode on an empty workspace. It produces a meaningless summary.
- Not writing `RECOVERY_NOTES.md` at init. The next session needs a checkpoint even if nothing was done yet.
