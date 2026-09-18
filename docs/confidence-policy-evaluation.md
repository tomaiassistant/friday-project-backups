# Budget Jarvis Confidence Policy Evaluation

- Date: 2026-06-02
- Agent: Tom / Hermes
- Status: initial table-driven evaluation baseline

## Purpose

Validate that the v0.1 non-executing brain loop treats confidence as audit metadata, not authorization. The confidence score may trigger review, but it must never relax high-risk confirmation gates or allow ambiguous work to queue/write completion logs.

## Current Policy Baseline

- Known low-risk routes start at `0.75` confidence.
- Known medium-risk routes start at `0.65` confidence.
- Known high-risk routes start at `0.70` confidence but remain blocked when confirmation is required.
- Recalled local context adds `+0.10`, capped at `0.90`, only for known routes.
- Unknown routes stay at `0.25` even when recalled context is present.
- Unknown/low-confidence escalation blocks before action: no queue, no completion-style writeback, state `waiting_for_confirmation`.

## Evaluation Scenarios Added

Implemented in `tests/test_confidence_policy.py`:

| Scenario | Expected behavior |
| --- | --- |
| Grounded low-risk project recall | Known `project_files`, confidence `0.85`, no escalation, optional daily-log writeback allowed. |
| Medium-risk local edit | Known `project_files`, confidence `0.65`, safe queue/writeback allowed only because caller explicitly requested local queue/writeback. |
| Ambiguous unknown route | `unknown`, confidence `0.25`, blocked for review, no queue, no writeback. |
| Unknown route with recalled context | Still `unknown` and `0.25`; recalled text does not rescue ambiguity or relax gates. |
| Conflicting high-risk communication | `communication`, confirmation required, blocked despite context and confidence metadata. |

## Safety Notes

- Recalled context is grounding, not authority.
- Provider review, if added later, must remain typed, advisory-only, and unable to override confirmation or blocked state.
- The next provider-review step should consume these evaluation scenarios as acceptance criteria before any provider call path is introduced.

## Verification

- `.venv/bin/python -m pytest -q` passed: 121 tests on 2026-06-02.
- `.venv/bin/python -m pytest -q` passed: 129 tests on 2026-06-03 after adding the advisory-only provider-review stub.
