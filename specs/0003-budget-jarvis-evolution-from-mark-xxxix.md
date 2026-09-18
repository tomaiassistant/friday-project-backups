# Budget Jarvis Evolution from Mark XXXIX - v0.1 Spec

- Owner: Shadhin
- Created by: Tom / Hermes
- Date: 2026-05-22
- Status: draft
- Reference study: `research/2026-05-22-mark-xxxix-jarvis-study.md`

## Goal

Build the real Tom/Budget Jarvis virtual brain by combining a Mark-style realtime voice/action layer with Brain Model memory, reasoning, and safe tool execution.

## Principle

We use Mark XXXIX as an architectural reference only. We do not copy its code. The final system should be our own implementation, connected to Hermes, OpenClaw/Jerry, Brain Model project memory, and the Windows worker.

## High-Level Architecture

```text
Live voice input
→ STT / transcript stream
→ Brain Model recall
→ reasoning/planning
→ safe tool router
→ action execution through Hermes/OpenClaw/Windows worker
→ voice/Telegram response
→ reflection + memory/project writeback
```

## Why This Is Better Than Command-Only Jarvis

Command-only Jarvis:

- hears a command
- chooses a tool
- runs it
- replies

Tom Brain Jarvis:

- hears Shadhin naturally
- restores context from memory/session/project files
- reasons before acting
- separates facts/assumptions/questions
- asks before sensitive actions
- coordinates with Jerry/OpenClaw
- writes learning back into Brain Model
- commits project progress to GitHub

## v0.1 Modules

### 1. Voice Session Layer

Responsibilities:

- Keep fast live listening.
- Handle slow/fast/accented Bangla/Banglish/unfluent speech as well as possible.
- Produce reliable transcripts.
- Allow text fallback through Telegram.
- Avoid feedback loops by pausing mic ingestion while Tom is speaking.

Initial implementation options:

- Keep current Windows mic worker as baseline.
- Add a cleaner state machine before replacing STT/model choices.
- Later evaluate native realtime audio APIs if they improve latency/accuracy.

### 2. State Machine

States:

- `idle`
- `listening`
- `thinking`
- `speaking`
- `tool_running`
- `waiting_for_confirmation`
- `error`

Rules:

- Do not listen while speaking.
- Do not run sensitive tools without confirmation.
- Always log major state transitions for debugging.
- If voice fails, notify through Telegram with the transcript/error.

### 3. Brain Model Reasoning Layer

Before action, Tom should recall:

1. Hermes user memory/profile.
2. Brain Model project memory/files.
3. Relevant recent sessions.
4. Jerry/OpenClaw updates when useful.

Then reason through:

- intent
- required tools
- risk level
- whether confirmation is needed
- expected output
- memory/writeback requirements

### 4. Safe Tool Router

Tool categories:

- `communication`: Telegram/WhatsApp updates to Shadhin.
- `project_files`: Brain Model read/write/commit/push.
- `memory`: durable facts and project memory.
- `openclaw`: ask Jerry, inspect OpenClaw project state.
- `windows_worker`: screenshots, active window, keyboard/mouse actions.
- `browser`: controlled web actions with one-tab/safe verification.
- `schedule`: reminders/cron jobs.
- `research`: web/repo/codebase inspection.

Risk classes:

- Low: read files, summarize, create local notes/specs.
- Medium: edit local project files, commit/push to private repo, run safe commands.
- High: sending messages as Shadhin, email, deleting files, payment/account actions, public posting, credential handling, major infrastructure changes.

High-risk actions require Shadhin confirmation.

### 5. Task Queue

Long-running voice tasks should not block conversation.

Pattern:

```text
voice request
→ classify as simple or complex
→ if complex, create queued task
→ return task id/status to Shadhin
→ work in background
→ notify on completion
→ write result to Brain Model
```

### 6. Vision On Demand

Screen/camera vision should be explicit and safe.

Rules:

- Screen capture only when requested or when needed for a PC-control task.
- Camera capture only with explicit permission.
- Compress images before model analysis.
- Log when vision was used.
- Keep visual overlay disabled during live listening unless Shadhin asks.

### 7. Reflection and Writeback

After meaningful work:

- update project task file
- append coordination log
- update durable project memory if needed
- commit and push Brain Model repo
- brief Shadhin update

## v0.1 Acceptance Criteria

1. Tom can take a voice/text command and decide whether it needs recall, planning, action, or confirmation.
2. Tom can run at least 5 safe tool actions through the router.
3. Tom can queue one long-running project task and report completion.
4. Tom can write result summaries to Brain Model files.
5. Tom can coordinate with Jerry/OpenClaw during a task.
6. Tom avoids feedback loops during live voice mode.
7. Tom never performs high-risk actions without confirmation.

## Coding Start Gate

We can start coding when these three docs exist:

1. `specs/0003-budget-jarvis-evolution-from-mark-xxxix.md` — this file.
2. `plans/0001-budget-jarvis-v01-implementation-plan.md` — bite-sized coding plan.
3. `tasks/0005-start-budget-jarvis-v01-coding.md` — active implementation task.

## First Coding Target

Build a small local Python package/prototype inside Brain Model:

```text
budget_jarvis_core/
  __init__.py
  state.py
  router.py
  risk.py
  task_queue.py
  memory_bridge.py
  tests/
```

First feature:

- parse an input transcript
- classify risk
- select a safe tool route
- return action plan
- log result

No PC-control or live mic changes in the first coding task. Start with the brain/router core first.
