# Agent Communication Protocol

This file defines how Jerry and Tom coordinate on the Brain Model project.

## Shared Path

```text
/home/ubuntu/.openclaw/workspace/projects/brain-model/shared/
```

## Directory Roles

- `shared/inbox/` - messages or requests for the other agent.
- `shared/outbox/` - completed responses or handoff notes.
- `shared/logs/` - chronological coordination logs.
- `memory/` - project-specific durable memory.
- `decisions/` - important decisions with date, reason, and owner.
- `tasks/` - active task files.
- `specs/` - design documents and technical specs.
- `experiments/` - prototypes, tests, and trial results.

## Message Format

Create a Markdown file using this pattern:

```text
YYYY-MM-DD-HHMM-from-agent-to-agent-topic.md
```

Example:

```text
2026-05-21-2215-jerry-to-tom-memory-design.md
```

Each message should use this structure:

```markdown
# Message Title

- From:
- To:
- Date:
- Status: open | answered | archived
- Related files:

## Context

## Request

## Response / Notes

## Next Action
```

## Rules

- Do not overwrite another agent's work unless Shadhin explicitly asks.
- If editing a shared file, add date and agent name.
- Keep raw observations separate from conclusions.
- Mark assumptions clearly.
- Record major decisions in `decisions/`.
- Record durable project knowledge in `memory/`.
- Use `tasks/` for active implementation work.

## Privacy

This project may contain private context about Shadhin and his systems. Do not copy contents into public places, group chats, or external tools unless Shadhin approves.

