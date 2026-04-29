# Context Manifest

Last updated: {{DATE}}

This file tells humans and models how to read this workspace.

## Canonical memory rule

The canonical project memory lives in normal repository markdown files.
Tool-specific memory features may help execution, but they are not the sole source of truth.

If the repository also uses `AGENTS.md`, `CLAUDE.md`, or similar files, those files should point to this manifest and the canonical docs instead of duplicating long-lived memory.

## Language policy

- User-facing communication may follow the user's language.
- Canonical docs and file names should stay in the repository's chosen documentation language unless explicitly changed.
- If chat language and doc language differ, explain in the chat language without silently translating canonical docs.
- If the documentation language is unclear or mixed, confirm it once and record the decision here.

## Read first

This is a priority order for orientation, not a checklist.
Read only the files needed to understand and route the current work safely.

1. `RECOVERY_NOTES.md` — latest resume checkpoint
2. `HUMAN_BRIEF.md` — human-facing project orientation
3. `CURRENT_STATE.md` — current truth
4. `ROADMAP.md` — planned work
5. `DECISION_LOG.md` — rationale and decision history
6. `RESEARCH_LOG.md` — evidence, experiments, observations
7. `HYPOTHESIS_LAB.md` — raw sparks and working hypotheses
8. `DOCS_GUIDE.md` — routing rules
9. `GLOSSARY.md` — terminology

## Canonical sources

| Question | Trust this first |
| --- | --- |
| What is true now? | `CURRENT_STATE.md` |
| What should happen next? | `ROADMAP.md` and latest `RECOVERY_NOTES.md` |
| Why was this choice made? | `DECISION_LOG.md` |
| What evidence or experiment supports this? | `RESEARCH_LOG.md` |
| What is speculative? | `HYPOTHESIS_LAB.md` |
| What should a human read quickly? | `HUMAN_BRIEF.md` |
| Where should new information be written? | `DOCS_GUIDE.md` |

## Conflict handling

If files disagree:

1. Prefer `CURRENT_STATE.md` for current truth.
2. Prefer the latest relevant dated `DECISION_LOG.md` entry for rationale.
3. Prefer the latest relevant dated `RESEARCH_LOG.md` entry for evidence.
4. Treat `ROADMAP.md` as intent, not proof.
5. Treat `HYPOTHESIS_LAB.md` as unverified by default.
6. Treat `RECOVERY_NOTES.md` as the resume pointer, not the full source of truth.
7. Report the conflict before merging claims.

## Ignore unless specifically requested

Use `.contextignore` when present. At minimum, ignore:

```text
.git/
.cache/
cache/
tmp/
.tmp/
__pycache__/
logs/
*.log
*.jsonl
node_modules/
dist/
build/
target/
private/
secrets/
.env
*.key
*.pem
```

## Privacy boundaries

Do not copy secrets, credentials, private source text, sensitive personal information, or restricted data into public/canonical docs.

If private material matters, summarize it and link to the private location only when appropriate.

## Update policy

Project memory is routed by responsibility.
Update only the canonical files whose responsibility changed.
Most sessions should update 1-3 files, not the whole memory set.

Before editing memory files, produce a short update plan listing the files to update, why they need updates, and relevant files that will not be touched.

Update this file when:

- the canonical file set changes
- the read order changes
- a new ignore pattern matters
- privacy boundaries change
- a project-specific source of truth is added

## Workspace profile

Profile: research

Change to `light`, `standard`, or `research` as needed.
