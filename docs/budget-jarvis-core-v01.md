# Budget Jarvis Core v0.1 Prototype

- Owner: Shadhin
- Agents: Tom / Hermes, Jerry / OpenClaw
- Created by: Tom / Hermes
- Date: 2026-05-28
- Updated: 2026-06-03
- Status: first usable core documentation; project recall, confidence, escalation, and advisory-only provider-review stub support added
- Related files:
  - `specs/0003-budget-jarvis-evolution-from-mark-xxxix.md`
  - `plans/0001-budget-jarvis-v01-implementation-plan.md`
  - `tasks/0005-start-budget-jarvis-v01-coding.md`
  - `docs/budget-jarvis-core-progress.md`

## Purpose

This document explains how to use the first Budget Jarvis brain/router core prototype.

The prototype proves the safe control layer before live microphone, screen, browser, email, or PC-control integration. It can accept a text transcript, classify risk, choose a broad tool category, expose whether confirmation is required, optionally queue work through in-memory primitives, and write simple project memory/log entries through local filesystem helpers.

## Current Scope

Implemented Python package:

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

Implemented tests:

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
tests/test_web.py
```

## Important Safety Boundary

The v0.1 core is intentionally **non-executing**.

It does **not**:

- control the Windows PC;
- click, type, or read the screen;
- use the microphone;
- open browsers or submit forms;
- send Telegram/WhatsApp/email messages;
- publish public posts;
- delete files;
- change infrastructure;
- handle credentials.

It only:

1. routes a transcript to a broad tool category;
2. classifies low/medium/high risk;
3. marks high-risk requests with `requires_confirmation: true`;
4. provides a suggested next action;
5. supports an in-memory task queue for future orchestration;
6. supports local JSON task queue snapshots for future resumable work;
7. supports deterministic local project-memory recall over markdown and optional
   queue state;
8. exposes local decision confidence and escalation reasons for unclear routes;
9. builds a typed advisory-only provider-review request/result boundary without
   calling providers;
10. supports local Brain Model daily-log/task/memory writeback helpers;
11. runs a minimal observe -> recall -> reason -> act -> reflect pass without
   external execution.

## State Primitives

`JarvisState` represents the future live assistant loop:

- `idle`
- `listening`
- `thinking`
- `speaking`
- `tool_running`
- `waiting_for_confirmation`
- `error`

`can_listen(state)` prevents overlapping audio/action behavior. It returns `False` while Jarvis is speaking, running tools, or waiting for confirmation.

## Risk Classifier

Use `classify_risk(text)` to classify a transcript before action.

Return object fields:

- `level`: `low`, `medium`, or `high`
- `requires_confirmation`: boolean
- `reason`: short reason string
- `matched_terms`: matched risk keywords

Risk policy:

- **Low:** read, summarize, inspect, review, draft local notes/specs, plan.
- **Medium:** edit local project files, commit/push private repo, run safe local commands, install local packages, create project tasks.
- **High:** outbound email/messages, public posting, deletion, payment/bank/account actions, credential handling, production/infrastructure changes, messaging people as Shadhin.

High-risk actions always require Shadhin's confirmation before any future execution layer may act.

## Router

Use `route_transcript(transcript)` to convert a transcript into an `ActionRoute`.

Route fields:

- `intent`
- `tool_category`
- `risk_level`
- `requires_confirmation`
- `reason`
- `next_action`

Current tool categories:

- `project_files`
- `memory`
- `openclaw`
- `windows_worker`
- `browser`
- `schedule`
- `research`
- `communication`
- `unknown`

The router always calls the risk classifier and preserves confirmation gates.

## Minimal Brain Loop

Use `run_brain_loop(transcript, ...)` when the caller needs the first complete
non-executing brain pass instead of route-only output.

It returns `BrainLoopResult` with:

- `transcript`
- `state`
- `route`
- `recalled_context`
- `planned_action`
- `queued_task`
- `reflection`
- `writeback_path`
- `confirmation_required`
- `blocked`
- `confidence`
- `escalation_required`
- `escalation_reason`

Example:

```python
from budget_jarvis_core import TaskQueue, run_brain_loop

queue = TaskQueue()
result = run_brain_loop(
    "edit the Brain Model task file with today's progress",
    recalled_context=["Task 0005 is in progress"],
    queue=queue,
    queue_complex=True,
)

print(result.state)                 # thinking
print(result.route.tool_category)   # project_files
print(result.queued_task.id)        # task-0001, if default queue is empty
```

Brain-loop safety behavior:

- high-risk transcripts return `state=waiting_for_confirmation`;
- high-risk transcripts set `blocked=True` and `confirmation_required=True`;
- high-risk transcripts do not queue tasks;
- high-risk transcripts do not write completion-style reflections to daily logs;
- high-risk confirmation gates are never relaxed by confidence scoring;
- unknown or low-confidence routes set `escalation_required=True`, explain the
  reason, and ask for Shadhin clarification or typed provider review before
  queueing work or writing completion-style logs;
- safe queueing only happens when `queue` is supplied and `queue_complex=True`;
- local daily-log reflection writeback only happens when `write_reflection=True`
  and `project_path` is supplied.

## Decision Confidence and Escalation

`run_brain_loop()` now estimates route confidence locally without provider calls.
The score is conservative and audit-only: it cannot override the risk classifier
or any high-risk confirmation gate.

Current v0.1 behavior:

- known low-risk routes start at about `0.75` confidence;
- known medium-risk project-local routes start at about `0.65` confidence;
- source-labelled recalled context adds a small confidence boost;
- `unknown` routes use low confidence (`0.25`) and always escalate;
- escalated routes do not queue tasks or write completion-style daily logs.

Escalation means the brain loop should ask Shadhin for clarification or request a
typed provider review. Provider review remains advisory only: it must not execute
actions or relax safety boundaries.

## Provider Review Stub

`provider_review.py` implements the first local boundary for future provider
assistance. It is intentionally a stub: no provider is called, no network access
is used, and no local decision is changed.

Core functions:

- `build_provider_review_request(result)` converts a `BrainLoopResult` into a
  typed `ProviderReviewRequest` with layer, intent, route/risk metadata,
  confidence, escalation reason, recalled context, local decision, allowed
  outputs, and forbidden actions.
- `run_provider_review_stub(request)` returns `ProviderReviewResult` with
  `advisory_only=True` and `provider_called=False`.
- `provider_review_result_to_dict(result)` serializes the review result for CLI
  and tests.

Provider review cannot override route category, risk level, confirmation
requirements, blocked state, queue/writeback policy, or local safety policy.
Default forbidden actions include tool execution, sending messages, modifying
files, queueing tasks, writing project memory, downgrading risk, removing
confirmation, or unblocking blocked results.

## Project-Memory Recall

Use `recall_project_context(project_path, query, ...)` to collect local,
source-labelled grounding snippets before a brain-loop run. It reads markdown
from project memory, tasks, specs, decisions, docs, shared inbox/outbox, and
shared logs. If `queue_store_path` is supplied, it also reads local JSON queue
state through `JsonTaskQueueStore`.

Example:

```python
from budget_jarvis_core import recall_context_strings, run_brain_loop

context = recall_context_strings(
    "/home/ubuntu/.openclaw/workspace/projects/brain-model",
    "Budget Jarvis memory recall next step",
    queue_store_path="state/queue.json",
)
result = run_brain_loop("summarize Budget Jarvis progress", recalled_context=context)
```

The recall layer is deterministic and provider-free in v0.1: simple token-overlap
ranking, compact snippets, no embeddings, no network calls, and no external
write actions.

## CLI Usage

Run from the Brain Model project root:

```bash
cd /home/ubuntu/.openclaw/workspace/projects/brain-model
python3 -m budget_jarvis_core.cli "summarize Brain Model progress"
```

Expected behavior:

- prints JSON;
- serializes enums as primitive strings;
- includes top-level `confirmation_required`;
- includes a `route` object;
- includes a `log` object in route-only mode;
- performs no external action.

Example shape:

```json
{
  "confirmation_required": false,
  "log": {
    "dry_run": true,
    "path": null,
    "requested": false,
    "text": null,
    "written": false
  },
  "route": {
    "intent": "summarize Brain Model progress",
    "next_action": "read or update approved Brain Model project files, then log the result",
    "reason": "project-file keyword detected; risk: read-only or summarization request",
    "requires_confirmation": false,
    "risk_level": "low",
    "tool_category": "project_files"
  }
}
```

To run the full non-executing brain loop from the terminal, pass
`--brain-loop`:

```bash
python3 -m budget_jarvis_core.cli \
  "summarize Brain Model progress" \
  --brain-loop \
  --context "Task 0005 is in progress"
```

Brain-loop CLI output includes:

- `brain_loop.state`
- `brain_loop.route`
- `brain_loop.recalled_context`
- `brain_loop.planned_action`
- `brain_loop.queued_task`
- `brain_loop.reflection`
- `brain_loop.writeback_path`
- `brain_loop.confirmation_required`
- `brain_loop.blocked`
- `brain_loop.confidence`
- `brain_loop.escalation_required`
- `brain_loop.escalation_reason`

Safe complex work can be placed into an in-memory queue with
`--brain-loop --queue-complex`. High-risk transcripts still stop at
`waiting_for_confirmation`, return `blocked: true`, and do not create queued
tasks or write completion-style logs.

To let the CLI collect local project-memory snippets itself before the brain
loop, pass `--recall-project PATH`:

```bash
python3 -m budget_jarvis_core.cli \
  "summarize Brain Model project recall progress" \
  --brain-loop \
  --recall-project /home/ubuntu/.openclaw/workspace/projects/brain-model \
  --recall-max-items 5
```

Optional `--queue-store state/queue.json` includes local persisted queue state in
recall. `--recall-project` is only allowed with `--brain-loop`; route-only mode
stays simple and does not read project files.

Unknown-route example:

```bash
python3 -m budget_jarvis_core.cli \
  "please handle the vague thing" \
  --brain-loop \
  --queue-complex
```

Expected brain-loop behavior: `tool_category: unknown`, `confidence: 0.25`,
`escalation_required: true`, no queued task, and planned action asking for
clarification or typed provider review.

To attach the advisory-only provider-review stub to the brain-loop JSON:

```bash
python3 -m budget_jarvis_core.cli \
  "please handle the vague thing" \
  --brain-loop \
  --provider-review-stub
```

Expected provider-review behavior: `provider_called: false`,
`advisory_only: true`, a typed request under `provider_review.request`, and no
change to `brain_loop.blocked`, `brain_loop.queued_task`, or
`brain_loop.writeback_path`.

## CLI Safety / Risk Examples

### Low-risk project summary

```bash
python3 -m budget_jarvis_core.cli "summarize Brain Model progress"
```

Expected:

- `tool_category`: `project_files`
- `risk_level`: `low`
- `confirmation_required`: `false`

### Medium-risk project edit

```bash
python3 -m budget_jarvis_core.cli "edit the Brain Model task file and commit the update"
```

Expected:

- `tool_category`: `project_files`
- `risk_level`: `medium`
- `confirmation_required`: `false`

Reason: this is project-local/private-repo work and is allowed inside the already-approved Brain Model work window, with normal logging and git verification.

### High-risk outbound message

```bash
python3 -m budget_jarvis_core.cli "send message to him on WhatsApp as Shadhin"
```

Expected:

- `tool_category`: `communication`
- `risk_level`: `high`
- `confirmation_required`: `true`
- `next_action`: asks Shadhin for confirmation before external/risky action

### High-risk destructive action

```bash
python3 -m budget_jarvis_core.cli "delete the project files"
```

Expected:

- `risk_level`: `high`
- `confirmation_required`: `true`

No deletion is performed by this prototype.

## Daily Log Writeback

The CLI can prepare a project daily-log entry.

By default, `--write-log` is a dry run only:

```bash
python3 -m budget_jarvis_core.cli \
  "summarize Brain Model progress" \
  --write-log
```

Expected:

- `log.requested`: `true`
- `log.dry_run`: `true`
- `log.written`: `false`
- `log.text`: populated with the would-be log entry

Real daily-log writeback requires all of these:

- `--write-log`
- `--real-write`
- explicit `--project-path`

Example:

```bash
python3 -m budget_jarvis_core.cli \
  "summarize Brain Model progress" \
  --write-log \
  --real-write \
  --project-path /home/ubuntu/.openclaw/workspace/projects/brain-model
```

This appends to:

```text
shared/logs/YYYY-MM-DD.md
```

For deterministic testing or backfilled logs, pass `--log-date YYYY-MM-DD`.

## Memory Bridge Helpers

`memory_bridge.py` provides local project-file helpers:

- `append_daily_log(project_path, text, date=None)`
- `write_task(project_path, task_id, title, body)`
- `append_project_memory(project_path, text)`

Safety behavior:

- validates empty inputs;
- creates parent folders;
- appends simple markdown blocks;
- refuses to overwrite task files;
- writes only to the provided local project path.

## Task Queue

`TaskQueue` is an in-memory queue for future long-running voice/text tasks.

It supports:

- `submit(...)`
- `list_tasks(...)`
- `get(...)`
- `start(...)`
- `complete(...)`
- `fail(...)`

Task states:

- `pending`
- `running`
- `completed`
- `failed`

The v0.1 queue has no worker/retry system yet. That remains intentional while the brain loop is non-executing.

`JsonTaskQueueStore` in `task_store.py` can persist a `TaskQueue` snapshot to a
local JSON file and load it back later while preserving task order, status,
timestamps, result/error, and metadata. This is local state persistence only;
it does not execute tasks or sync externally.

## Verification

Run the full test suite from the project root:

```bash
cd /home/ubuntu/.openclaw/workspace/projects/brain-model
python3 -m pytest -v
```

Expected suite target after the 2026-06-01 confidence/escalation addition:

```text
120 passed
```

If `pytest` is missing in a fresh environment, install or activate the test environment first. Do not treat missing `pytest` as a product-code failure.

## Integration Notes for Next Milestone

Before connecting live mic, browser, Windows worker, or communication tools:

1. Keep `route_transcript()` as the first safety gate after transcript capture.
2. Block all `requires_confirmation: true` routes until Shadhin confirms.
3. Keep PC/browser/communication integrations dry-run first.
4. Record meaningful results through `memory_bridge.py`.
5. Use `TaskQueue` for long work so voice interaction is not blocked.
6. Add tests before each new execution capability.

## Current Next Step

Decision confidence and escalation are now available in the brain loop and CLI JSON. The next implementation step should test the confidence policy against more realistic evaluation scenarios, then add an advisory provider-review stub only if it preserves the non-executing boundary.
