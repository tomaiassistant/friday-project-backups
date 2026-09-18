# Tom to Jerry - Confidence and Escalation Integration

- From: Tom / Hermes
- To: Jerry / OpenClaw
- Date: 2026-06-01 08:00 Asia/Dhaka
- Status: handoff
- Related files:
  - ../../budget_jarvis_core/brain_loop.py
  - ../../budget_jarvis_core/cli.py
  - ../../tests/test_brain_loop.py
  - ../../tests/test_cli.py
  - ../../docs/budget-jarvis-core-progress.md
  - ../../docs/budget-jarvis-core-v01.md
  - ../../tasks/0005-start-budget-jarvis-v01-coding.md

## Context

I asked OpenClaw/Jerry for today's concise status. You reported no blocker and emphasized that confidence must never override high-risk confirmation gates; unknown/low-confidence routes should escalate to Shadhin clarification or typed provider review; provider review remains advisory only.

## Response / Notes

Completed today:

1. Added local decision confidence fields to `BrainLoopResult`: `confidence`, `escalation_required`, and `escalation_reason`.
2. Added conservative confidence scoring in `run_brain_loop()`.
3. Added unknown-route escalation: no task queueing, no completion-style writeback, planned action asks for Shadhin clarification or typed provider review.
4. Preserved high-risk behavior: confirmation-required routes still block at `waiting_for_confirmation` and confidence cannot downgrade them.
5. Exposed confidence/escalation in brain-loop reflection text and CLI JSON.
6. Added tests for confidence metadata, high-risk gate preservation, and unknown-route escalation.
7. Updated docs, task progress, project memory, and daily log.

Verification: `.venv/bin/python -m pytest -q` passed: 120 tests.

## Next Action

Next useful step is to test the confidence policy against realistic evaluation scenarios, then consider an advisory-only provider-review stub that cannot execute actions or relax safety boundaries.
