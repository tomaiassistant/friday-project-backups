# AI Knowledge Operating Rules

## Core Rule

AI Knowledge is the shared markdown knowledge vault for Shadhin's agents.

When Shadhin gives Friday, Jerry, or another agent a knowledge-related task, the agent should write useful context back into this vault instead of leaving it only in chat.

## Obsidian-Style Rules

1. Use clean markdown files.
2. Prefer short linked notes over giant mixed notes.
3. Use folders by knowledge type: `memory/`, `docs/`, `specs/`, `tasks/`, `decisions/`, `research/`, `shared/`.
4. Use clear titles and dates.
5. Use wikilinks where useful, e.g. `[[PROJECT]]`, `[[2026-06-12-rename-to-ai-knowledge]]`.
6. Separate facts, assumptions, decisions, tasks, and logs.
7. Keep stable knowledge in `memory/PROJECT_MEMORY.md`.
8. Do not store secrets, API keys, or private credentials in notes.

## Automatic Project Application

For AI Knowledge-related tasks, the agent should:

1. Capture the instruction in a task file when substantive.
2. Add or update a relevant memory/doc/spec/decision note.
3. Record important decisions in `decisions/`.
4. Add a short log entry in `shared/logs/`.
5. Write coordination messages for other agents if needed.
6. Preserve implementation notes and results.
7. Keep roadmap/project files updated when scope changes.

## Timed Instructions

When Shadhin gives a specific time for work, schedule the work instead of relying on memory.

Use scheduled jobs for:

- exact-time work
- delayed follow-ups
- reminders
- timed project checks
- scheduled implementation windows

Current local project path:

```text
/root/projects/brain-model/
```

Note: the folder path may remain `brain-model` for compatibility until backups/cron/deploy references are migrated.

## Task Intake Flow

For each new AI Knowledge task:

1. Create a task file in `tasks/`.
2. Add a short log entry in `shared/logs/`.
3. If another agent needs context, create a message in `shared/inbox/` or `shared/outbox/`.
4. If the task changes architecture, create a decision file in `decisions/`.
5. After completion, update the task status and write a result summary.

## Agent Coordination

Friday, Jerry, and future agents should treat this vault as the shared source of truth.

- Do not keep important context only in chat.
- Do not rely on hidden memory for project-critical information.
- If a task affects AI Knowledge, write it down.
- If work is scheduled for later, include exact time, timezone, and expected action.
