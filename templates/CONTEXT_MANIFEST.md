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
Do not preemptively read the full memory set.
For non-trivial work, briefly state which memory files will be read and which relevant files will not be read.

{{READ_FIRST}}

## Canonical sources

{{CANONICAL_SOURCES}}

## Canonical locations

Memory root: `{{MEMORY_ROOT}}`

{{CANONICAL_LOCATIONS}}

## Conflict handling

If files disagree:

{{CONFLICT_HANDLING}}

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

Profile: {{PROFILE}}

Change to `light`, `standard`, `research`, or `academic` as needed.

## Project-specific operating policies

project-memory is a skeleton.
Customize these policies to fit the project:

- Capture trigger strength: {{CAPTURE_TRIGGER}} (light, standard, research, or academic)
- Review cadence:
- Archive policy:
- Tool-facing instructions:

Use the lightest policy that preserves the project's real continuity needs.
