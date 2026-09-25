# Budget Jarvis Evolution from Mark XXXIX - v0.1 Spec

**Owner:** Shadhin
**Created by:** Friday (Hermes)
**Date:** 2026-05-22
**Status:** Draft
**Reference study:** `research/2026-05-22-mark-xxxix-jarvis-study.md`

## Goal

Build the real Tom/Budget Jarvis virtual brain by combining a Mark-style realtime voice/action layer with AI Knowledge memory, reasoning, and safe tool execution.

## Principle

We use Mark XXXIX as an architectural reference only. We do not copy its code. The final system should be our own implementation, connected to Hermes, OpenClaw/Jerry, AI Knowledge project memory, and the Windows worker.

## High-Level Architecture

```text
Live voice input
→ STT / transcript stream
→ AI Knowledge recall
→ reasoning/planning
→ safe tool router
→ action execution through Hermes/OpenClaw/Windows worker
→ voice/Telegram response
→ reflection + memory/project writeback
```

## Why This Is Better Than Command-Only Jarvis

**Command-only Jarvis:**
- hears a command
- chooses a tool
- runs it
- replies

**Tom Brain Jarvis:**
- hears Shadhin naturally
- restores context from memory/session/project files
- reasons before acting
- separates facts/assumptions/questions
- asks before sensitive actions
- coordinates with Jerry/OpenClaw
- writes learning back into AI Knowledge
- commits project progress to GitHub

## v0.1 Modules

### 1. Voice Session Layer

Responsibilities:
- Keep fast live listening
- Handle slow/fast/accented Bangla/Banglish/unfluent speech as well as possible
- Produce reliable transcripts
- Allow text fallback through Telegram
- Avoid feedback loops by pausing mic ingestion while Tom is speaking

Initial implementation options:
- Keep current Windows mic worker as baseline
- Add a cleaner state machine before replacing STT/model choices
- Later evaluate native realtime audio APIs if they improve latency/accuracy

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
- Don't listen while speaking, tool_running, or waiting_for_confirmation
- Transition to `waiting_for_confirmation` on high-risk actions
- Return to `idle` on completion or error

### 3. Recall Layer

- Read PROJECT.md, PROJECT_MEMORY.md, relevant specs/tasks/decisions
- Retrieve last N log entries
- Check inbox/outbox for coordination messages
- Return structured context bundle

### 4. Reasoning Layer

- Break down task into steps
- Identify facts, assumptions, open questions
- Assess risks and privacy
- Choose tool category via router
- Generate plan with checkpoints

### 5. Safe Tool Router

- Classify intent → tool_category
- Classify risk (low/medium/high)
- Mark high-risk → confirmation required
- Return ActionRoute with next_action

### 6. Action Execution

- Route to Hermes, OpenClaw, Windows worker, or local script
- Execute with timeout and error handling
- Return result to reasoning layer

### 7. Response Generation

- Generate natural language response
- Include reasoning summary if useful
- Queue voice synthesis if in voice mode

### 8. Reflection & Writeback

- Record outcome in shared/logs/
- Update PROJECT_MEMORY.md with new stable facts
- Update task status
- Commit to GitHub

## Related

- [[specs/0001-v01-architecture-first-pass]]
- [[specs/0004-layered-provider-replacement-roadmap]]
- [[plans/0001-budget-jarvis-v01-implementation-plan]]
- [[research/2026-05-22-mark-xxxix-jarvis-study]]