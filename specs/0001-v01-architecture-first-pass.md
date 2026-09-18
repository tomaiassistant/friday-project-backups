# Brain Model v0.1 Architecture - First Pass

- Owner: Shadhin
- Agents: Jerry / OpenClaw, Tom / Hermes
- Created by: Tom / Hermes
- Date: 2026-05-22
- Status: draft

## Goal

Brain Model v0.1 should prove that Shadhin can have a persistent, useful AI brain made from existing agents, memory, tools, and coordination rules.

It is not a trained foundation model in v0.1. It is a working system loop.

## v0.1 Loop

```text
observe -> capture -> recall -> reason -> act -> reflect -> write back
```

## Layers

### 1. Input / Observe

Initial v0.1 sources:

- Direct Telegram/WhatsApp conversations with Shadhin
- Project files in `/home/ubuntu/.openclaw/workspace/projects/brain-model/`
- Hermes and OpenClaw session history when needed
- User-approved files/tasks/research

Potential later sources:

- Email/calendar
- Browser activity summaries
- PC worker events
- Dealio/OpenClaw/Jerry project logs

### 2. Capture

Raw observations should be stored separately from distilled memory.

Recommended stores:

- `shared/logs/YYYY-MM-DD.md` for agent coordination logs
- `memory/PROJECT_MEMORY.md` for durable project facts
- `decisions/YYYY-MM-DD-topic.md` for important decisions
- `tasks/NNNN-topic.md` for active work

### 3. Recall

Before answering or acting on Brain Model work, agents should inspect:

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
- Coordinate between Jerry and Tom
- Summarize progress to Shadhin

Actions needing Shadhin confirmation:

- Sending public posts/messages as him
- Emailing people
- Deleting important files
- Exposing private memory externally
- Major infrastructure changes

### 6. Reflect / Write Back

After work, agents should update at least one of:

- task status/result
- coordination log
- project memory
- decision record

## First Implementation Direction

Build a minimal memory core that can:

1. ingest a markdown note or task,
2. classify it as raw note / durable memory / decision / task,
3. retrieve relevant snippets for a prompt,
4. produce a response with cited project files,
5. write back a short reflection.

## Evaluation Scenarios

Initial tests should check:

- Recall: remembers Brain Model purpose and current tasks.
- Privacy: refuses or asks before sharing private memory outside approved context.
- Usefulness: turns vague Shadhin instructions into concrete task files.
- Coordination: Jerry and Tom can exchange handoff files without losing context.
- Accuracy: separates known facts from assumptions.

## Open Questions

1. Should v0.1 store embeddings locally, or start with markdown + keyword search?
2. Which data sources are allowed on day one?
3. Should Brain Model have a single canonical memory store or per-agent memory synced through project files?
4. What are the top 10 real Shadhin tasks we should use for evaluation?
