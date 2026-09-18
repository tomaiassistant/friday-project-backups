# Task 0004 - Evolve Tom Budget Jarvis Using Mark XXXIX Study

- Status: active
- Created by: Tom / Hermes
- Date: 2026-05-22
- Requested by: Shadhin
- Source repo: https://github.com/FatihMakes/Mark-XXXIX.git
- Research note: `research/2026-05-22-mark-xxxix-jarvis-study.md`

## User Instruction

Shadhin found an open-source Jarvis-style project and asked Tom to study how it was made so Tom/Budget Jarvis can evolve.

## Key Constraints

- Use the project as reference/learning only. README says BY-NC / personal and non-commercial use only.
- Do not copy code directly into commercial/public work.
- Keep Budget Jarvis worker visual overlay disabled during live listening unless Shadhin asks otherwise.
- Preserve safety around PC control, messaging, email, deleting files, and private memory.

## Current Findings

Mark XXXIX uses:

- Gemini Live native audio for low-latency voice.
- Explicit function declarations/tools.
- Async audio send/receive/playback loop.
- Tool dispatch bridge with `FunctionResponse`.
- Screen/camera vision module.
- Local JSON memory injected into prompt.
- Planner/executor/task queue for autonomous multi-step work.
- PyQt6 HUD.

## Next Steps

1. Create `specs/0003-budget-jarvis-evolution-from-mark-xxxix.md`.
2. Design Budget Jarvis state machine: idle/listening/thinking/speaking/tool_running/error.
3. Design safe tool router mapped to Hermes/OpenClaw/Windows worker capabilities.
4. Add feedback prevention for live listening/TTS.
5. Add queued long-running task support.
6. Decide what Mark-inspired features fit Brain Model v0.1 vs Budget Jarvis.
