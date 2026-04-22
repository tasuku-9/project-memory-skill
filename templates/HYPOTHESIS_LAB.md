# Hypothesis Lab

This file records ideas that are plausible but not yet confirmed.

A hypothesis is not current truth. It must be tested, decided, or explicitly accepted before being promoted to `CURRENT_STATE.md`.

Do not promote anything directly from this file to `CURRENT_STATE.md`.

## Operating rule

The AI agent should capture new ideas here automatically during the chat or coding session.
Do not require the human to explicitly ask for logging.
Prefer over-capturing here over losing a potentially useful idea.

## Status meanings

- `raw`: captured spark, discomfort, or half-formed thought
- `active`: a live working hypothesis worth tracking
- `tested`: linked to research, observation, or comparison work
- `promoted`: moved into `CURRENT_STATE.md`, `ROADMAP.md`, or `DECISION_LOG.md`
- `dropped`: no longer worth carrying as a live hypothesis

## Raw sparks

Use this section for low-commitment captures.
These may be vague, incomplete, or speculative.

### SPK-{{DATE}}-001

- date: {{DATE}}
- status: raw
- spark: Structured memory may reduce context drift better than a single README or chat transcript.
- why worth keeping: Different information types age differently and should not be trusted equally.
- next step: Try the workflow for several sessions and compare recovery quality.
- related files:
  - `RESEARCH_LOG.md`
  - `DECISION_LOG.md`

## Working hypotheses

Use this section for ideas that have recurring relevance, clearer structure, or a defined next step.

```md
## HYP-YYYY-MM-DD-001 - Short title

- date:
- status: active | tested | promoted | dropped
- hypothesis:
- why it seems plausible:
- what would support it:
- what would weaken or falsify it:
- cheapest useful test:
- related research:
- related decisions:
- promotion target:
```

## HYP-{{DATE}}-001 - Structured memory reduces context drift

- date: {{DATE}}
- status: active
- hypothesis: A separated memory workspace will make long-running work easier to resume and migrate than a single README or chat transcript.
- why it seems plausible: Different information types age differently and should not be trusted equally.
- what would support it: Faster recovery after interruption; fewer contradictions; clearer decisions.
- what would weaken or falsify it: Users or agents stop updating the docs because the structure is too heavy.
- cheapest useful test: Run one project through the workflow for several sessions and audit the docs afterward.
- related research:
  - `RESEARCH_LOG.md`
- related decisions:
  - `DECISION_LOG.md`
- promotion target: `CURRENT_STATE.md` if repeatedly useful in practice.
