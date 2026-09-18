# Task 0003 - Daily 8 AM Brain Model Work Window

- Status: active
- Created by: Tom / Hermes
- Date: 2026-05-22
- Requested by: Shadhin
- Schedule: every day at 08:00 Asia/Dhaka
- Related job: Hermes cron job `e6d2819317f3` / Daily 8 AM Brain Model work
- GitHub repo: `https://github.com/tomaiassistant/brain-model` (private)

## User Instruction

Shadhin said Tom's everyday working time on Brain Model is **8:00 AM Bangladesh time**.

## Expected Daily Action

At each daily work window, Tom should:

1. Read the Brain Model project state:
   - `PROJECT.md`
   - `ROADMAP.md`
   - `OPERATING_RULES.md`
   - `COMMUNICATION.md`
   - latest files in `shared/inbox/`, `shared/outbox/`, `tasks/`, `specs/`, `memory/`, and `decisions/`
2. Ask Jerry/OpenClaw for updates if needed.
3. Continue the next useful project task without waiting for Shadhin, unless the next action needs confirmation.
4. Write outputs into the project folder.
5. Log what changed in `shared/logs/YYYY-MM-DD.md`.
6. Commit and push changes to the private GitHub repository.
7. Send Shadhin a brief Telegram update with:
   - what was done
   - what changed
   - next step / any question

## Current First Daily Priorities

1. Finalize Brain Model v0.1 scope.
2. Define allowed v0.1 data sources.
3. Create evaluation scenarios.
4. Start minimal memory core design/prototype.

## Notes

The schedule is exact-time work, so it must be handled by a scheduled job rather than memory alone.
