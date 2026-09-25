# Mark XXXIX Jarvis Study for Tom / Budget Jarvis Evolution

**Source:** https://github.com/FatihMakes/Mark-XXXIX.git
**Local research clone:** `/root/.hermes/research/Mark-XXXIX`
**Commit inspected:** `d3e8504`
**Date:** 2026-05-22
**Researcher:** Tom / Hermes (now Friday)
**License note:** README states Creative Commons BY-NC 4.0 / personal and non-commercial use only. Treat as learning/reference, not copy-paste into commercial work.

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

**File:** `main.py`

Key pattern:

```text
sounddevice mic input → Gemini Live session → receive audio + transcriptions → play audio output
```

Important implementation ideas:

- Uses `google.genai.Client(...).aio.live.connect(...)`
- Uses Gemini native audio preview model: `models/gemini-2.5-flash-native-audio-preview-12-2025`
- Sends mic chunks as `audio/pcm` at 16 kHz
- Plays returned audio at 24 kHz
- Keeps separate async tasks for sending realtime audio, receiving model events, listening mic, and playing audio
- Avoids mic feedback by not sending mic input while assistant is speaking

### 2. Tool declaration layer

**File:** `main.py`

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

This is the main lesson: voice assistant power comes from broad tool declarations that the LLM can invoke directly.

### 3. Memory system

**File:** `memory.py`

- Uses JSON file for long-term memory
- Simple key-value with timestamps
- `save_memory(key, value)` and `recall_memory(key)` functions
- No embeddings, no structured retrieval — just exact key lookup

### 4. Task queue

**File:** `task_queue.py`

- Background asyncio queue for multi-step tasks
- Tasks are dicts with `steps` list
- Worker processes steps sequentially
- Supports pause/resume/cancel

### 5. Computer control

**File:** `computer_control.py`

- Uses `pyautogui` for mouse/keyboard
- Uses `PIL`/`mss` for screenshots
- Exposes `click`, `type`, `scroll`, `screenshot`, `get_mouse_position`

### 6. Browser control

**File:** `browser_control.py`

- Uses Playwright for browser automation
- Exposes `navigate`, `click`, `fill`, `extract_text`, `screenshot`

## Key Takeaways for Budget Jarvis

1. **State machine is critical** — Mark uses implicit state (speaking/listening flags). We make it explicit with `JarvisState` enum.

2. **Tool declarations drive capability** — We'll start with router → tool_category, then expand to fine-grained tools.

3. **Memory must be structured** — Mark's JSON key-value is too simple. We use markdown + project recall + future embeddings.

4. **Safety first** — Mark has no risk classifier or confirmation gates. Our Budget Jarvis core adds these before execution.

5. **Separation of concerns** — Mark puts everything in `main.py`. We split into: state, risk, router, recall, queue, memory, brain_loop.

6. **No code copying** — Per Shadhin's decision, Mark XXXIX is architectural reference only.

## Related

- [[specs/0003-budget-jarvis-evolution-from-mark-xxxix]]
- [[plans/0001-budget-jarvis-v01-implementation-plan]]
- [[decisions/2026-05-22-budget-jarvis-core-first]]