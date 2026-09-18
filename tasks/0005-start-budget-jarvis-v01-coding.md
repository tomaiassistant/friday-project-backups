# Task 0005 - Start Budget Jarvis v0.1 Coding

- Status: in progress
- Created by: Tom / Hermes
- Date: 2026-05-22
- Requested by: Shadhin
- Spec: `specs/0003-budget-jarvis-evolution-from-mark-xxxix.md`
- Plan: `plans/0001-budget-jarvis-v01-implementation-plan.md`

## User Instruction

Shadhin told Tom to keep learning, keep evolving the Brain Model, and let him know when we can start the coding part and start building the real virtual brain.

## Coding Start Answer

We can start coding after the first implementation plan is committed. The safest starting point is not the live mic or PC-control layer yet. Start with the Brain/Router core:

```text
budget_jarvis_core/
  state.py
  risk.py
  router.py
  task_queue.py
  memory_bridge.py
```

## First Coding Objective

Build a tested local prototype that can:

1. receive a transcript/command,
2. classify risk,
3. select a tool route,
4. decide whether confirmation is required,
5. queue complex work,
6. write a project log/reflection.

## Why This Comes First

This gives Tom/Budget Jarvis a real brain/control layer before connecting live voice, screen vision, or PC actions. That keeps the system safer and easier to test.

## Progress

### 2026-05-22 08:00 Asia/Dhaka - Tom

Started coding during the scheduled daily Brain Model work window.

Completed:

- Created `budget_jarvis_core/` package skeleton.
- Implemented `JarvisState` and `can_listen(state)` in `budget_jarvis_core/state.py`.
- Implemented keyword-based `RiskLevel`, `RiskDecision`, and `classify_risk(text)` in `budget_jarvis_core/risk.py`.
- Added state and risk tests in `tests/test_state.py` and `tests/test_risk.py`.
- Added progress doc: `docs/budget-jarvis-core-progress.md`.

Next:

- Implement `ActionRoute` and safe transcript routing.
- Then implement task queue and memory bridge.

### 2026-05-23 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Implemented `ToolCategory`, `ActionRoute`, and `route_transcript(transcript)` in `budget_jarvis_core/router.py`.
- Added keyword routing for `project_files`, `memory`, `openclaw`, `windows_worker`, `browser`, `schedule`, `research`, `communication`, and `unknown`.
- Router now always calls `classify_risk()` and preserves confirmation requirements for high-risk commands.
- Exported router primitives from `budget_jarvis_core/__init__.py`.
- Added `tests/test_router.py` covering route creation, category selection, medium-risk file/repo operations, high-risk confirmation gates, and unknown-route non-execution.

Verification:

- `python3 -m pytest tests/test_state.py tests/test_risk.py tests/test_router.py -v` passed: 41 tests.
- `python3 -m pytest -v` passed: 41 tests.

Next:

- Implement the in-memory task queue (`TaskStatus`, `QueuedTask`, `TaskQueue`).
- Then implement the project memory bridge.

### 2026-05-24 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Asked Jerry/OpenClaw for a concise review before coding. Jerry confirmed Task 6 scope: keep the queue in-memory/synchronous, avoid workers/retries/threading, export primitives, and test invalid IDs/transitions.
- Implemented `TaskStatus`, `QueuedTask`, and `TaskQueue` in `budget_jarvis_core/task_queue.py`.
- Added queue operations for submit, list/filter, get, start, complete, and fail.
- Added guarded state transitions so completed/failed tasks cannot be restarted or overwritten.
- Added deterministic ID/clock injection for stable tests.
- Exported queue primitives from `budget_jarvis_core/__init__.py`.
- Added `tests/test_task_queue.py` covering submit/list/get/start/complete/fail, invalid IDs, empty inputs, duplicate IDs, and illegal transitions.

Verification:

- `python3 -m pytest tests/test_task_queue.py -v` passed: 14 tests.
- `python3 -m pytest -v` passed: 55 tests.

Next:

- Implement the project memory bridge (`append_daily_log`, `write_task`, `append_project_memory`).

### 2026-05-25 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Asked Jerry/OpenClaw for a concise review before coding. Jerry confirmed Task 7 is the correct next step and recommended local filesystem-only helpers, `pathlib`, deterministic tests, simple markdown blocks, exports from `__init__.py`, and no accidental overwrites.
- Implemented `append_daily_log(project_path, text, date=None)` in `budget_jarvis_core/memory_bridge.py`.
- Implemented `write_task(project_path, task_id, title, body)` with slugged task filenames and no-overwrite protection.
- Implemented `append_project_memory(project_path, text)` for durable project memory notes.
- Added input validation for empty text/title/body/task IDs.
- Exported memory bridge functions from `budget_jarvis_core/__init__.py`.
- Added `tests/test_memory_bridge.py` covering file creation, append behavior, deterministic date injection, parent folder creation, validation, no-overwrite behavior, and package exports.

Verification:

- `python3 -m pytest tests/test_memory_bridge.py -v` passed: 13 tests.
- `python3 -m pytest -v` passed: 68 tests.

Next:

- Implement Task 8 from the plan: add the CLI prototype that routes a transcript, prints route JSON, and optionally writes a daily log in dry-run or real mode.

### 2026-05-26 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Asked Jerry/OpenClaw for a concise review before coding. Jerry reported no new Brain Model updates and confirmed Task 8 requirements: `argparse`, route JSON, visible confirmation flag, default dry-run writeback, explicit project path for real writes, enum `.value` serialization, and high-risk output coverage.
- Implemented `budget_jarvis_core/cli.py` with `route_to_dict()`, `build_parser()`, `run()`, and `main()`.
- CLI command now works as: `python3 -m budget_jarvis_core.cli "summarize Brain Model progress"`.
- CLI prints JSON containing `route`, `confirmation_required`, and `log` sections.
- Added optional `--write-log` dry-run mode and `--write-log --real-write --project-path ...` real daily-log writeback through `append_daily_log()`.
- Guarded real writes so `--real-write` requires both `--write-log` and an explicit `--project-path`.
- Added `tests/test_cli.py` covering enum serialization, normal route JSON, high-risk confirmation visibility, default dry-run behavior, real writeback, missing project-path rejection, and `main()` JSON output.
- Updated router keyword coverage so `Brain Model` routes to `project_files` instead of `unknown`.

Verification:

- `python3 -m pytest -v` passed: 75 tests.
- Manual CLI smoke test passed: `python3 -m budget_jarvis_core.cli "summarize Brain Model progress"` printed route JSON with `tool_category: project_files` and `confirmation_required: false`.

Next:

- Implement Task 9 from the plan: write integration/use documentation for the first Budget Jarvis core prototype.

### 2026-05-28 08:00 Asia/Dhaka - Tom

Continued coding/documentation during the scheduled daily Brain Model work window.

Completed:

- Asked Jerry/OpenClaw for a concise status/review before continuing. Jerry reported no new Brain Model updates after the 2026-05-26 CLI handoff and confirmed Task 9 documentation points.
- Created `docs/budget-jarvis-core-v01.md`.
- Documented current prototype scope, safety boundary, state primitives, risk classifier, router, CLI usage, safety/risk examples, daily-log writeback, memory bridge helpers, task queue, verification, and next integration notes.
- Confirmed no `README.md` exists, so the plan's README update step was skipped.

Verification:

- `python3 -m pytest -v` passed: 75 tests.

Next:

- Design and implement the minimal observe -> recall -> reason -> act -> reflect loop that wires the existing primitives together without adding live PC-control yet.

### 2026-05-29 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Asked Jerry/OpenClaw for a concise status/review before coding. Jerry reported no new Brain Model updates after the 2026-05-28 handoff and recommended a small `brain_loop.py` module with simple recall, non-executing action behavior, optional queue/local writeback only when explicit, and a hard high-risk confirmation block.
- Implemented `budget_jarvis_core/brain_loop.py` with `BrainLoopResult` and `run_brain_loop()`.
- Wired observe -> recall -> reason -> act -> reflect around existing route/risk/state/task queue/memory bridge primitives.
- Preserved safety boundary: high-risk transcripts return `waiting_for_confirmation`, do not queue work, and do not write completion-style daily logs.
- Added optional safe queueing through `TaskQueue` and optional local daily-log reflection writeback through `append_daily_log()`.
- Exported `BrainLoopResult` and `run_brain_loop` from `budget_jarvis_core/__init__.py`.
- Added `tests/test_brain_loop.py` covering low-risk loop results, empty input validation, high-risk blocking, queue behavior, writeback guard, and safe daily-log reflection append.

Verification:

- `python3 -m pytest -q` passed: 81 tests.

Next:

- Add CLI/docs integration for `run_brain_loop()` so terminal runs can show the full loop result, not only route JSON.

### 2026-05-29 20:55 UTC - Jerry

Continued coding while Tom/Hermes was busy.

Completed:

- Added CLI integration for the full non-executing brain loop via `--brain-loop`.
- Added repeatable recalled context support via `--context`.
- Added optional safe in-memory task queueing from the CLI via `--queue-complex`.
- Added `brain_loop_to_dict()` so `BrainLoopResult` serializes to JSON with state, route, recalled context, planned action, queued task, reflection, writeback path, confirmation flag, and blocked flag.
- Preserved route-only CLI output as the default behavior.
- Updated CLI docs with the new brain-loop terminal mode.
- Added CLI tests covering brain-loop serialization, safe queued work, high-risk blocking, dry-run reflection output, and real reflection writeback.

Verification:

- `python3 -m compileall -q budget_jarvis_core tests` passed.
- Manual brain-loop CLI smoke test passed for a low-risk Brain Model progress command.
- Manual brain-loop CLI smoke test passed for a high-risk destructive/outbound-message command; it returned `waiting_for_confirmation`, `blocked: true`, and no queued task.
- Created a local `.venv` because system Python is externally managed and lacks `pytest`.
- `.venv/bin/python -m pytest -q` passed: 87 tests.

### 2026-05-29 21:00 UTC - Jerry

Continued with persistent queue groundwork.

Completed:

- Added queue snapshot serialization through `TaskQueue.snapshot()`.
- Added `TaskQueue.from_tasks()` for rebuilding queues from stored task records.
- Added `task_to_record()` and `task_from_record()` for JSON-safe task persistence.
- Added `budget_jarvis_core/task_store.py` with `JsonTaskQueueStore` for local JSON save/load.
- Exported `JsonTaskQueueStore` from the package root.
- Added tests for snapshot ordering, task record round trips, duplicate loaded IDs, invalid metadata, missing store loads, save/load round trips, JSON shape validation, and non-object record validation.
- Updated docs and project memory to reflect local queue persistence.

Verification:

- `.venv/bin/python -m pytest -q` passed: 96 tests.

### 2026-05-29 21:05 UTC - Jerry

Converted Shadhin's provider-replacement direction into project architecture and code.

Completed:

- Added `specs/0004-layered-provider-replacement-roadmap.md`.
- Defined Brain Model replacement as layered capabilities: input understanding, memory, reasoning, decision, generation, action, reflection, and learning.
- Added provider dependency levels: `required`, `assisted`, `optional`, and `local`.
- Added `budget_jarvis_core/capability_layers.py` with `CapabilityLayer`, `ProviderDependency`, `BrainCapability`, `default_capability_map()`, `replacement_ready_layers()`, and `provider_required_layers()`.
- Exported the capability-layer primitives from the package root.
- Added `tests/test_capability_layers.py`.
- Created Tom/Hermes handoff: `shared/inbox/2026-05-29-2105-jerry-to-tom-layered-provider-replacement.md`.

Verification:

- `.venv/bin/python -m pytest -q` passed: 101 tests.

### 2026-05-30 08:00 Asia/Dhaka - Tom

Continued coding and roadmap review during the scheduled daily Brain Model work window.

Completed:

- Asked Jerry/OpenClaw for a concise status/review. Jerry reported no new updates after the 2026-05-29 layered provider-replacement handoff and recommended Hermes provider-router notes first, then project-memory recall.
- Added Hermes provider-router notes to `specs/0004-layered-provider-replacement-roadmap.md`, including routing hooks, typed fallback interface, and Windows-worker handoff safety boundary.
- Implemented `budget_jarvis_core/project_recall.py` with deterministic local recall over markdown project files and optional JSON queue state.
- Exported `RecallItem`, `recall_project_context`, and `recall_context_strings` from `budget_jarvis_core/__init__.py`.
- Added `tests/test_project_recall.py` covering markdown recall, context-string formatting, queue-state recall, missing paths, and validation.
- Updated `docs/budget-jarvis-core-progress.md` with the new recall layer and next step.

Verification:

- `.venv/bin/python -m pytest -q` passed: 115 tests.

Next:

- Wire `recall_context_strings()` into the CLI/brain-loop workflow as an optional project recall mode.
- Then add decision confidence thresholds to the brain loop.

### 2026-05-31 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Read current project state, latest shared files, docs, task progress, and project memory.
- Asked Jerry/OpenClaw for a concise status/review. Jerry reported no blocker, noted the existing web-lab JSON parsing hardening, and recommended wiring project recall into the CLI next.
- Reviewed and kept the web-lab hardening in `budget_jarvis_core/web.py`: the browser UI now reads response text, recovers JSON when a tunnel/proxy prefixes the response, sends `Accept: application/json`, and exposes `raw_response_start` for diagnostics.
- Wired `recall_context_strings()` into `budget_jarvis_core/cli.py` for brain-loop runs through `--recall-project PATH`.
- Added `--recall-max-items` and optional `--queue-store` so CLI brain-loop recall can include local markdown project files and local JSON queue state.
- Preserved guardrails: `--recall-project` requires `--brain-loop`, and `--queue-store` requires `--recall-project`.
- Added CLI tests for project recall context ordering and guardrails; web tests already cover the hardened browser JSON parsing hints.
- Updated progress and usage docs.

Verification:

- `.venv/bin/python -m pytest -q` passed: 118 tests.

Next:

- Add decision confidence and escalation thresholds to the brain loop.

### 2026-06-01 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Read current project state, latest shared files, docs, task progress, and project memory.
- Asked Jerry/OpenClaw for concise status/review. Jerry reported no blocker and emphasized that confidence must never bypass high-risk confirmation; unknown/low-confidence routes should escalate to Shadhin clarification or typed provider review, and provider review remains advisory only.
- Added local decision confidence metadata to `BrainLoopResult`: `confidence`, `escalation_required`, and `escalation_reason`.
- Added conservative confidence scoring in `budget_jarvis_core/brain_loop.py`: known low/medium routes get higher local confidence, recalled context gives a small boost, and `unknown` routes receive low confidence.
- Added escalation behavior for unknown/low-confidence routes: they do not queue tasks or write completion-style logs; planned action asks for Shadhin clarification or typed provider review.
- Kept high-risk safety gates intact: confirmation-required routes still stop at `waiting_for_confirmation`, do not queue work, and do not write completion-style logs.
- Exposed confidence/escalation fields in CLI brain-loop JSON and daily reflection text.
- Added tests covering confidence fields, high-risk gate preservation, and unknown-route escalation.
- Updated progress and usage docs plus project memory and daily coordination log.

Verification:

- `.venv/bin/python -m pytest -q` passed: 120 tests.

Next:

- Test the confidence policy against more realistic evaluation scenarios, then consider an advisory-only provider-review stub.

### 2026-06-02 08:00 Asia/Dhaka - Tom

Continued coding/evaluation during the scheduled daily Brain Model work window.

Completed:

- Read current project state, latest shared files, docs, task progress, and project memory.
- Asked Jerry/OpenClaw for concise status/review. Jerry recommended table-driven confidence-policy evaluation scenarios before any provider-review stub and noted that unknown routes should become explicitly blocked before execution exists.
- Added `tests/test_confidence_policy.py` with realistic low-risk, medium-risk, ambiguous, recalled-context, and high-risk/conflicting scenarios.
- Tightened unknown/escalated route behavior in `budget_jarvis_core/brain_loop.py`: escalated routes now return `blocked=True` and state `waiting_for_confirmation`, with no queue or completion-style writeback.
- Rounded local confidence output to two decimals for stable audit metadata.
- Updated CLI/brain-loop tests for the fail-closed unknown-route behavior.
- Added `docs/confidence-policy-evaluation.md` and updated `docs/budget-jarvis-core-progress.md`.

Verification:

- `.venv/bin/python -m pytest -q` passed: 121 tests.

Next:

- Consider a provider-review stub only as typed, advisory, non-executing metadata that cannot override confirmation, blocked state, queue policy, or writeback gates.

### 2026-06-03 08:00 Asia/Dhaka - Tom

Continued coding during the scheduled daily Brain Model work window.

Completed:

- Read current project state, latest shared files, docs, task progress, specs, and project memory.
- Asked Jerry/OpenClaw for concise status/review. Jerry reported no new Brain Model updates after the 2026-06-02 handoff and recommended the typed advisory-only provider-review stub before structured generation templates.
- Added `budget_jarvis_core/provider_review.py` with `ProviderReviewLayer`, `ProviderReviewRequest`, `ProviderReviewResult`, `build_provider_review_request()`, `run_provider_review_stub()`, and `provider_review_result_to_dict()`.
- Preserved the v0.1 safety boundary: the stub calls no provider, performs no network or external action, and cannot override route category, risk level, confirmation, blocked state, queue policy, writeback policy, or local safety policy.
- Exported provider-review primitives from `budget_jarvis_core/__init__.py`.
- Added `--provider-review-stub` to the CLI for `--brain-loop` mode only; it attaches typed advisory review JSON without changing the brain-loop result.
- Added `tests/test_provider_review.py` and CLI coverage for the new flag and guardrail.
- Added `docs/provider-review-boundary.md` and updated core progress/usage docs.

Verification:

- `.venv/bin/python -m pytest -q` passed: 129 tests.

Next:

- Add structured generation templates for routine status/task reports, keeping them local and non-executing.

## Next Action

Add structured generation templates for routine status/task reports, keeping them local and non-executing.
