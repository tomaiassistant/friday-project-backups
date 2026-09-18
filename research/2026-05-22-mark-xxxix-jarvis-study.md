# Mark XXXIX Jarvis Study for Tom / Budget Jarvis Evolution

- Source: https://github.com/FatihMakes/Mark-XXXIX.git
- Local research clone: `/home/ubuntu/.hermes/research/Mark-XXXIX`
- Commit inspected: `d3e8504`
- Date: 2026-05-22
- Researcher: Tom / Hermes
- License note: README states Creative Commons BY-NC 4.0 / personal and non-commercial use only. Treat as learning/reference, not copy-paste into commercial work.

## What Mark XXXIX Is

Mark XXXIX is a local Python desktop voice assistant using Gemini Live audio. It combines:

- realtime microphone streaming
- realtime audio response playback
- function/tool calling
- screen/camera vision
- OS/browser/file/computer controls
- long-term JSON memory
- PyQt6 Jarvis-style HUD
- background task queue for multi-step tasks

## Core Architecture Observed

### 1. Live voice loop

File: `main.py`

Key pattern:

```text
sounddevice mic input -> Gemini Live session -> receive audio + transcriptions -> play audio output
```

Important implementation ideas:

- Uses `google.genai.Client(...).aio.live.connect(...)`.
- Uses Gemini native audio preview model: `models/gemini-2.5-flash-native-audio-preview-12-2025`.
- Sends mic chunks as `audio/pcm` at 16 kHz.
- Plays returned audio at 24 kHz.
- Keeps separate async tasks for sending realtime audio, receiving model events, listening mic, and playing audio.
- Avoids mic feedback by not sending mic input while assistant is speaking.

### 2. Tool declaration layer

File: `main.py`

Mark defines a large `TOOL_DECLARATIONS` list directly in the main process. Gemini can call tools like:

- `open_app`
- `web_search`
- `weather_report`
- `send_message`
- `reminder`
- `youtube_video`
- `screen_process`
- `computer_settings`
- `browser_control`
- `file_controller`
- `desktop_control`
- `code_helper`
- `dev_agent`
- `agent_task`
- `computer_control`
- `game_updater`
- `flight_finder`
- `file_processor`
- `save_memory`
- `shutdown_jarvis`

This is the main lesson: voice assistant power comes from a clear, explicit tool API, not just the voice model.

### 3. Execution bridge

File: `main.py`, method `_execute_tool`

Pattern:

```text
Gemini function call -> dispatch by tool name -> run Python function in executor/thread -> send FunctionResponse back
```

Important implementation ideas:

- Blocking tools are wrapped with `loop.run_in_executor`.
- Vision runs in a thread and speaks directly.
- Tool errors are caught and spoken back.
- Tool results are sent back to the live model through `send_tool_response`.

### 4. Planner / autonomous task path

Files:

- `agent/planner.py`
- `agent/executor.py`
- `agent/task_queue.py`
- `agent/error_handler.py`

Pattern:

```text
user complex goal -> planner creates JSON steps -> executor runs tools -> retries/replans on failure -> summarizes
```

Useful details:

- Planner is constrained to known tools.
- Max 5 steps.
- Executor injects previous results into later file-writing steps.
- Executor retries each step up to 3 times.
- Queue runs long tasks asynchronously with IDs and status.

This maps well to Brain Model's planned `observe -> recall -> reason -> act -> reflect` loop.

### 5. Memory model

File: `memory/memory_manager.py`

Pattern:

```json
{
  "identity": {},
  "preferences": {},
  "projects": {},
  "relationships": {},
  "wishes": {},
  "notes": {}
}
```

Important implementation ideas:

- Memory is a small local JSON file: `memory/long_term.json`.
- Updates are category/key/value with an `updated` date.
- Values are truncated.
- Overall memory is capped around 2200 chars.
- Memory is formatted into the system prompt before each live session.

For Tom/Budget Jarvis, this confirms our current memory direction is right, but we need stronger project memory + privacy boundaries than Mark.

### 6. Vision module

File: `actions/screen_processor.py`

Pattern:

```text
capture screen/camera -> compress image -> send to Gemini Live vision/audio session -> answer by audio
```

Useful details:

- Uses `mss` for screen capture.
- Uses OpenCV for camera.
- Compresses images to JPEG around 640x360 quality 60 before sending.
- Auto-detects camera index.
- Runs a separate persistent vision session thread.

This is useful for Budget Jarvis visual awareness, but we should keep our current overlay-disabled live mode unless explicitly needed.

### 7. UI / HUD

File: `ui.py`

Pattern:

- PyQt6 HUD window
- animated rings/pulse/particles
- status states: listening/thinking/speaking/muted
- chat log panel
- API key entry
- drag/drop file upload
- system metrics via psutil

Useful lesson: visual status matters. For Budget Jarvis, a tiny optional status indicator may be better than a heavy overlay.

### 8. Browser and OS control

Files:

- `actions/browser_control.py`
- `actions/computer_control.py`
- `actions/computer_settings.py`
- `actions/file_controller.py`

Patterns:

- Browser control uses Playwright and real browser profile discovery.
- Direct computer control uses PyAutoGUI / clipboard / screenshots / hotkeys.
- There are cross-platform branches for Windows/macOS/Linux.
- Screenshot save path is restricted to safe roots.

For Tom, we should prefer verified actions, screenshots, and safe path restrictions before clicks/typing.

## Strong Ideas to Borrow

1. **Realtime native audio session** for low-latency conversation.
2. **Explicit tool declaration catalog** for assistant actions.
3. **Tool dispatch bridge** that returns structured results to the voice model.
4. **Feedback prevention**: stop listening while speaking.
5. **Task queue** for long-running work so voice chat stays responsive.
6. **Planner -> executor -> replan loop** for complex tasks.
7. **Small memory injected into prompt** plus durable project memory elsewhere.
8. **Vision as a separate module/session**, not mixed into the main loop.
9. **File upload processor** as a single routing tool.
10. **Status UI / HUD** for user confidence.

## What Not to Copy Directly

1. Do not copy code directly into our project because repo is BY-NC/personal/non-commercial.
2. Do not use generated arbitrary code execution as a default path; it is risky.
3. Do not let browser/OS tools act without verification for sensitive actions.
4. Do not keep secrets in `config/api_keys.json` inside a repo.
5. Do not build a heavy overlay into Budget Jarvis live mode; Shadhin asked to keep worker visual overlay disabled during live mode.
6. Do not rely on a small 2200-char memory as the only brain; Brain Model needs layered memory.

## Recommended Tom / Budget Jarvis Evolution Plan

### Phase 1 - Safer live voice foundation

- Keep current Budget Jarvis mic loop.
- Add better state machine: `idle/listening/thinking/speaking/tool_running/error`.
- Add feedback guard: do not listen while TTS is playing.
- Keep overlay disabled by default.

### Phase 2 - Tool router

Define a clear tool API similar to Mark, but backed by Hermes/OpenClaw tools:

- message Shadhin
- read/write project files
- search sessions/memory
- ask Jerry/OpenClaw
- control Windows worker safely
- screenshot/analyze screen only when approved or explicitly requested
- schedule reminders/cron jobs

### Phase 3 - Task queue

Add queued background tasks for voice commands:

```text
voice command -> classify simple vs complex -> simple tool call or queued task -> status update -> completion notification
```

### Phase 4 - Brain Model memory bridge

Bridge live Budget Jarvis with Brain Model:

- raw live transcripts saved separately
- durable facts promoted only when useful
- project decisions written into Brain Model files
- private memory not exposed in group contexts

### Phase 5 - Vision-on-demand

Add optional screen/camera vision:

- capture one frame only when requested
- compress before model analysis
- require explicit permission for camera
- log when vision was used

## Immediate Next Implementation Task

Create a Budget Jarvis v0.1 architecture spec that merges:

- Hermes Telegram/cloud memory
- Windows mic worker live listening
- OpenClaw/Jerry coordination
- Brain Model project memory
- safe tool router
- daily GitHub-backed project workflow

Suggested file:

`specs/0003-budget-jarvis-evolution-from-mark-xxxix.md`
