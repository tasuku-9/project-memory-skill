# Decision Log

This file records meaningful decisions and their rationale.

Use it when future readers may ask:

- why did we choose this?
- what alternatives were considered?
- what changed our mind?
- when should we revisit this?

Newest entries can go at the top or bottom, but stay consistent.

## Entry template

```md
## DEC-YYYY-MM-DD-001 - Short title

- date:
- decision:
- status: active | superseded | reversed | experimental
- context:
- alternatives considered:
- rationale:
- evidence:
- risks / tradeoffs:
- expected impact:
- human_brief_update: yes | no
- human_brief_reason:
- revisit when:
- related files:
```

## DEC-{{DATE}}-001 - Initial memory structure

- date: {{DATE}}
- decision: Use separated continuity documents instead of relying on chat history or a single README.
- status: active
- context: Long-running work needs to survive chat loss, model migration, and interrupted research sessions.
- alternatives considered:
  - keep everything in chat history
  - keep everything in README
  - keep informal notes only
- rationale: Separating current truth, plans, decisions, evidence, hypotheses, human summaries, and recovery notes reduces context drift.
- evidence: This workspace was initialized from a continuity memory template.
- risks / tradeoffs: More files require clearer routing rules.
- expected impact: Easier recovery and safer handoff between humans and models.
- human_brief_update: yes
- human_brief_reason: The project structure and decision surface changed for any human joining the workspace.
- revisit when: The file set feels too heavy, duplicated, or underused.
- related files:
  - `DOCS_GUIDE.md`
  - `CONTEXT_MANIFEST.md`
