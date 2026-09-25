# AI Knowledge v0.1 Architecture - First Pass

**Owner:** Shadhin
**Agents:** Friday (Hermes), Jerry (OpenClaw)
**Created by:** Friday (Hermes)
**Date:** 2026-05-22
**Status:** Draft

## Goal

AI Knowledge v0.1 should prove that Shadhin can have a persistent, useful AI brain made from existing agents, memory, tools, and coordination rules.

It is not a trained foundation model in v0.1. It is a working system loop.

## v0.1 Loop

```text
observe → capture → recall → reason → act → reflect → write back
```

## Layers

### 1. Input / Observe

Initial v0.1 sources:

- Direct Telegram/WhatsApp conversations with Shadhin
- Project files in `/root/projects/brain-model/`
- Hermes and OpenClaw session history when needed
- User-approved files/tasks/research

Potential later sources:

- Email/calendar
- Browser activity summaries
- PC worker events
- ListingsFinder automation logs

### 2. Capture

Raw observations should be stored separately from distilled memory.

Recommended stores:

- `shared/logs/YYYY-MM-DD.md` for agent coordination logs
- `memory/PROJECT_MEMORY.md` for durable project facts
- `decisions/YYYY-MM-DD-topic.md` for important decisions
- `tasks/NNNN-topic.md` for active work

### 3. Recall

Before answering or acting on AI Knowledge work, agents should inspect:

1. `PROJECT.md`
2. relevant roadmap/spec/task files
3. latest `shared/inbox/` and `shared/outbox/`
4. `memory/PROJECT_MEMORY.md`
5. session history only if project files do not answer the question

### 4. Reason

Each substantial task should separate:

- Facts
- Assumptions
- Open questions
- Risks/privacy issues
- Next action

### 5. Act

Allowed v0.1 actions:

- Create/edit local project files
- Write specs, tasks, decisions, logs
- Prototype local scripts
- Coordinate between Jerry and Friday
- Summarize progress to Shadhin

Actions needing Shadhin confirmation:

- Sending public posts/messages as him
- Emailing people
- Deleting important files
- Exposing private memory externally

### 6. Reflect & Writeback

After each task:

- Update relevant memory/docs/specs
- Record lessons learned
- Update roadmap if needed
- Log completion in `shared/logs/`

## Related

- [[PROJECT]]
- [[OPERATING_RULES]]
- [[specs/0002-v01-data-sources-and-evaluation]]
- [[specs/0003-budget-jarvis-evolution-from-mark-xxxix]]
- [[specs/0004-layered-provider-replacement-roadmap]]