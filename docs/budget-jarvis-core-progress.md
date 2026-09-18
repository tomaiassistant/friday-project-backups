# Budget Jarvis Core Progress

- Date: 2026-05-23
- Updated: 2026-06-03
- Agent: Tom / Hermes
- Status: minimal non-executing brain loop prototype with project recall, confidence policy evaluation, escalation support, and an advisory-only provider-review stub

## Implemented

Initial Python package:

```text
budget_jarvis_core/
  __init__.py
  brain_loop.py
  state.py
  risk.py
  router.py
  task_queue.py
  task_store.py
  project_recall.py
  provider_review.py
  memory_bridge.py
  cli.py
  web.py
```

Tests:

```text
tests/test_state.py
tests/test_risk.py
tests/test_router.py
tests/test_task_queue.py
tests/test_task_store.py
tests/test_project_recall.py
tests/test_provider_review.py
tests/test_memory_bridge.py
tests/test_cli.py
tests/test_brain_loop.py
tests/test_confidence_policy.py
tests/test_web.py
```

## Current Capabilities

### State primitives

`JarvisState` defines:

- `idle`
- `listening`
- `thinking`
- `speaking`
- `tool_running`
- `waiting_for_confirmation`
- `error`

`can_listen(state)` returns `False` while speaking, running tools, or waiting for confirmation to prevent voice feedback loops and unsafe overlapping actions.

### Risk classifier

`classify_risk(text)` returns a `RiskDecision` with:

- `level`: `low`, `medium`, or `high`
- `requires_confirmation`
- `reason`
- `matched_terms`

High-risk actions include email, public posting, deleting files, payments/account actions, credential handling, major infrastructure changes, and messaging people as Shadhin.

### Safe transcript router

`route_transcript(transcript)` returns an `ActionRoute` with:

- `intent`
- `tool_category`
- `risk_level`
- `requires_confirmation`
- `reason`
- `next_action`

Initial `ToolCategory` values:

- `project_files`
- `memory`
- `openclaw`
- `windows_worker`
- `browser`
- `schedule`
- `research`
- `communication`
- `unknown`

The router is non-executing. It picks a broad tool category, calls `classify_risk()` for every transcript, and keeps high-risk actions behind `requires_confirmation=True`.

### Advisory-only provider review stub

`provider_review.py` defines the typed boundary for future provider assistance without making any provider calls yet.

Implemented primitives:

- `ProviderReviewLayer` for `input_understanding`, `reasoning`, `decision`, `generation`, and `review`.
- `ProviderReviewRequest` with layer, intent, route/risk metadata, confidence, escalation reason, recalled context, local decision, allowed outputs, and forbidden actions.
- `ProviderReviewResult` with `advisory_only=True`, `provider_called=False`, a recommendation, and a `cannot_override` policy list.
- `build_provider_review_request(result)` to convert a `BrainLoopResult` into the typed request.
- `run_provider_review_stub(request)` to exercise the boundary locally without external execution.
- `provider_review_result_to_dict(result)` for JSON-safe CLI/test output.

Safety boundary: provider review cannot override route category, risk level, confirmation requirements, blocked state, queue policy, writeback policy, or local safety policy. The CLI flag `--provider-review-stub` is only available in `--brain-loop` mode and does not call any external provider.

### In-memory task queue

`TaskQueue` provides a small synchronous queue for complex work that should not block a voice/text interaction.

Implemented primitives:

- `TaskStatus`: `pending`, `running`, `completed`, `failed`.
- `QueuedTask`: immutable dataclass with `id`, `title`, `description`, `status`, timestamps, result/error fields, and metadata.
- `TaskQueue.submit(...)` for adding pending tasks.
- `TaskQueue.list_tasks(...)` and `TaskQueue.get(...)` for inspection.
- `TaskQueue.start(...)`, `TaskQueue.complete(...)`, and `TaskQueue.fail(...)` with guarded transitions.

The queue is intentionally in-memory for v0.1. It avoids background workers, thread-safety complexity, or persistence until the brain loop needs them.

### Project memory bridge

`memory_bridge.py` provides local filesystem writeback helpers for Brain Model project files:

- `append_daily_log(project_path, text, date=None)` creates/appends `shared/logs/YYYY-MM-DD.md` with deterministic date injection for tests.
- `write_task(project_path, task_id, title, body)` creates `tasks/{task_id}-{slugified-title}.md` and refuses to overwrite an existing task file.
- `append_project_memory(project_path, text)` creates/appends `memory/PROJECT_MEMORY.md`.

The helpers strip inputs, reject empty text/title/body/task IDs, create parent folders, and append simple markdown blocks only. They do not perform external writes.

### CLI brain/router prototype

`python3 -m budget_jarvis_core.cli "summarize Brain Model progress"` now runs the first end-to-end terminal prototype. It:

- routes the transcript through `route_transcript()`;
- prints JSON with primitive enum values, `confirmation_required`, `reason`, and `next_action`;
- keeps high-risk transcripts visibly gated behind confirmation;
- supports optional `--write-log` dry-runs by default;
- supports full non-executing `--brain-loop` output;
- can add local project-memory snippets to brain-loop context with `--recall-project PATH`;
- only writes a real daily log when both `--write-log --real-write` and an explicit `--project-path` are provided.

The CLI remains non-executing: it routes and logs only.

### Local web test lab

`python3 -m budget_jarvis_core.web --host 127.0.0.1 --port 8787` starts a local browser UI for testing the current Brain Model loop. It provides:

- a transcript textarea;
- recalled-context input, one item per line;
- a `Queue safe complex work` toggle;
- visible state/risk/confirmation pills;
- full JSON output from the same non-executing `run_brain_loop()` path;
- URL-encoded API endpoint: `POST /api/brain-loop`.

Safety boundary: the web interface does not execute external tools, send messages, or write files. High-risk actions are still blocked behind confirmation and safe queueing is in-memory only.

### Minimal brain loop

`run_brain_loop(transcript, ...)` now wires the core primitives into a safe
observe -> recall -> reason -> act -> reflect pass. It returns a
`BrainLoopResult` with:

- normalized transcript;
- current loop state;
- route/risk decision;
- recalled local context strings;
- non-executing planned action;
- optional in-memory queued task;
- reflection text;
- optional local daily-log writeback path;
- confirmation/blocking flags.

Safety boundary:

- high-risk transcripts stop at `waiting_for_confirmation`;
- high-risk transcripts do not queue tasks or write completion-style logs;
- low/medium-risk transcripts only produce a suggested action unless explicit
  local queue/writeback options are supplied;
- real writeback is limited to `append_daily_log()` inside the provided project
  path.

### Local project-memory recall

`project_recall.py` adds deterministic local recall over Brain Model project files
and optional JSON queue state. It provides:

- `RecallItem(source, text, score)` with `as_context()` for source-labelled
  grounding strings;
- `recall_project_context(project_path, query, max_items=5, queue_store_path=None)`;
- `recall_context_strings(...)` for direct use with
  `run_brain_loop(recalled_context=...)`.

The recall layer reads markdown in `memory/`, `tasks/`, `specs/`, `decisions/`,
`docs/`, and shared communication/log folders. If a local queue JSON store is
provided, it also summarizes matching queued tasks. It uses simple token-overlap
scoring for v0.1 and makes no embedding, network, or provider calls.

## Verification

- 2026-05-22: `python3 -m pytest -v` passed: 25 tests.
- 2026-05-23: `python3 -m pytest -v` passed: 41 tests.
- 2026-05-24: `python3 -m pytest -v` passed: 55 tests.
- 2026-05-25: `python3 -m pytest -v` passed: 68 tests.
- 2026-05-26: `python3 -m pytest -v` passed: 75 tests.
- 2026-05-26: Manual CLI smoke test passed: `python3 -m budget_jarvis_core.cli "summarize Brain Model progress"` printed route JSON with `tool_category: project_files` and `confirmation_required: false`.
- 2026-05-28: Created `docs/budget-jarvis-core-v01.md` with usage, safety/risk examples, dry-run and real writeback examples, memory bridge notes, task queue notes, and next integration guidance.
- 2026-05-28: `python3 -m pytest -v` passed: 75 tests.
- 2026-05-29: Added `budget_jarvis_core/brain_loop.py`, exported
  `BrainLoopResult` and `run_brain_loop`, and added `tests/test_brain_loop.py`.
- 2026-05-29: `python3 -m pytest -q` passed: 81 tests.
- 2026-05-29: Jerry added CLI integration for the full non-executing brain
  loop with `--brain-loop`, repeatable `--context`, optional `--queue-complex`,
  and JSON serialization for `BrainLoopResult`.
- 2026-05-29: Manual CLI smoke tests passed for low-risk brain-loop output and
  high-risk blocking output.
- 2026-05-29: Created a local `.venv` for verification because system Python is
  externally managed and does not include `pytest`; `.venv/bin/python -m pytest
  -q` passed: 87 tests.
- 2026-05-29: Jerry added local JSON task queue persistence with
  `JsonTaskQueueStore`, queue snapshot serialization, task record
  deserialization, and tests for save/load, invalid store shapes, duplicate
  loaded IDs, bad metadata, and snapshot ordering.
- 2026-05-29: `.venv/bin/python -m pytest -q` passed: 96 tests.
- 2026-05-29: Jerry added the layered provider-replacement roadmap in
  `specs/0004-layered-provider-replacement-roadmap.md`, added typed capability
  tracking in `budget_jarvis_core/capability_layers.py`, and created a Tom
  handoff for Hermes-side review.
- 2026-05-29: `.venv/bin/python -m pytest -q` passed: 101 tests.
- 2026-05-29: Tom added local web test interface in `budget_jarvis_core/web.py`
  with a single-page UI and `POST /api/brain-loop` endpoint.
- 2026-05-29: `.venv/bin/python -m pytest -q` passed: 109 tests.
- 2026-05-30: Tom added Hermes provider-router notes to the layered roadmap and
  implemented local project-memory recall over markdown plus optional JSON queue
  state in `budget_jarvis_core/project_recall.py`.
- 2026-05-30: `.venv/bin/python -m pytest -q` passed: 115 tests.
- 2026-05-31: Reviewed and kept the web-lab JSON parsing hardening for tunnel/proxy-prefixed responses, wired `recall_context_strings()` into CLI `--brain-loop` through `--recall-project PATH`, and added tests for project recall context plus CLI guardrails.
- 2026-05-31: `.venv/bin/python -m pytest -q` passed: 118 tests.
- 2026-06-01: Tom added brain-loop decision confidence and escalation metadata. `BrainLoopResult` now exposes `confidence`, `escalation_required`, and `escalation_reason`; unknown routes escalate to Shadhin clarification or typed provider review without queueing work or writing completion-style logs; CLI brain-loop JSON and reflections include the new audit fields.
- 2026-06-01: `.venv/bin/python -m pytest -q` passed: 120 tests.
- 2026-06-02: Tom added table-driven confidence-policy evaluation scenarios in `tests/test_confidence_policy.py` and documented the baseline in `docs/confidence-policy-evaluation.md`. Unknown/escalated routes now fail closed with `blocked=True` and `waiting_for_confirmation` before any future execution path exists.
- 2026-06-02: `.venv/bin/python -m pytest -q` passed: 121 tests.

## Next Implementation Step

Consider adding provider-review stubs only as typed, advisory, non-executing metadata that cannot override confirmation, blocked state, queue policy, or writeback gates.
