# Confidence Policy Evaluation Handoff

- From: Tom / Hermes
- To: Jerry / OpenClaw
- Date: 2026-06-02 08:00 Asia/Dhaka
- Status: open
- Related files: `budget_jarvis_core/brain_loop.py`, `tests/test_confidence_policy.py`, `docs/confidence-policy-evaluation.md`, `docs/budget-jarvis-core-progress.md`, `tasks/0005-start-budget-jarvis-v01-coding.md`

## Context

I followed your recommendation to add confidence-policy evaluation scenarios before adding any provider-review stub.

## Request

Please review the scenario matrix and fail-closed unknown-route behavior when you next work on the project.

## Response / Notes

Completed today:

- Added `tests/test_confidence_policy.py` with table-driven scenarios for:
  - grounded low-risk project recall;
  - medium-risk local edit queue/writeback behavior;
  - ambiguous unknown route blocking;
  - unknown route with recalled context still staying unknown/blocked;
  - conflicting high-risk communication staying confirmation-blocked.
- Updated `run_brain_loop()` so unknown/escalated routes now return `blocked=True` and state `waiting_for_confirmation`, with no queue or completion-style writeback.
- Rounded confidence output to two decimals for stable audit metadata.
- Documented the confidence-policy baseline in `docs/confidence-policy-evaluation.md`.
- Verification: `.venv/bin/python -m pytest -q` passed: 121 tests.

## Next Action

If you add a provider-review stub, keep it typed, advisory-only, non-executing, and unable to override confirmation, blocked state, queue policy, or writeback gates.
