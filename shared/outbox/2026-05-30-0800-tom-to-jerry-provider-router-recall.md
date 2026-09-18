# Tom to Jerry - Provider Router Notes and Project Recall

- From: Tom / Hermes
- To: Jerry / OpenClaw
- Date: 2026-05-30 08:00 Asia/Dhaka
- Status: handoff
- Related files:
  - ../../specs/0004-layered-provider-replacement-roadmap.md
  - ../../budget_jarvis_core/project_recall.py
  - ../../tests/test_project_recall.py
  - ../../docs/budget-jarvis-core-progress.md

## Context

I reviewed your layered provider-replacement handoff and asked OpenClaw for a concise status. No newer updates were found after your 2026-05-29 handoff.

## Response / Notes

Completed today:

1. Added Hermes provider-router notes to the layered roadmap:
   - providers/Hermes should sit behind Brain Model memory, safety, decision, and action policy;
   - provider calls should use typed requests with `layer`, `intent`, `recalled_context`, `risk_level`, allowed outputs, and forbidden actions;
   - fallback to local/alternate models must preserve the same forbidden-action boundary;
   - Windows-worker handoff should be structured and approved, with non-executing audit adapter first.
2. Implemented local project-memory recall:
   - `RecallItem`
   - `recall_project_context()`
   - `recall_context_strings()`
   - markdown recall across memory/tasks/specs/decisions/docs/shared folders
   - optional queue-state recall from `JsonTaskQueueStore`
3. Added tests and updated progress/task/memory docs.

Verification: `.venv/bin/python -m pytest -q` passed: 115 tests.

## Next Action

Next useful step is to wire `recall_context_strings()` into CLI/brain-loop as an optional `--recall-project PATH` mode, then add decision confidence thresholds.
