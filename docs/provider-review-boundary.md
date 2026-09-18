# Provider Review Boundary

- Date: 2026-06-03
- Agent: Tom / Hermes
- Status: implemented local advisory-only stub
- Related code: `budget_jarvis_core/provider_review.py`, `budget_jarvis_core/cli.py`
- Related tests: `tests/test_provider_review.py`, `tests/test_cli.py`

## Purpose

Define the first safe interface for future provider assistance without letting provider output own Brain Model behavior.

The v0.1 implementation is a **stub only**. It builds and serializes typed review requests, then returns a local placeholder result. It does not call Hermes, OpenAI, OpenClaw, a browser, network APIs, or any external model.

## Current Objects

`ProviderReviewLayer` identifies which Brain Model layer needs review:

- `input_understanding`
- `reasoning`
- `decision`
- `generation`
- `review`

`ProviderReviewRequest` includes:

- `layer`
- `intent`
- `tool_category`
- `risk_level`
- `confidence`
- `escalation_required`
- `escalation_reason`
- `recalled_context`
- `local_decision`
- `allowed_outputs`
- `forbidden_actions`

`ProviderReviewResult` includes:

- `advisory_only`
- `provider_called`
- `recommendation`
- `cannot_override`
- original `request`

## Safety Contract

Provider review is advisory only. It cannot override:

- `route.tool_category`
- `route.risk_level`
- `confirmation_required`
- `blocked`
- `queued_task`
- `writeback_path`
- local safety policy

Default forbidden actions include:

- executing tools;
- sending messages;
- modifying files;
- enqueueing tasks;
- writing project memory;
- downgrading risk;
- removing confirmation requirements;
- unblocking blocked results.

## CLI Smoke Example

```bash
python -m budget_jarvis_core.cli \
  "please handle the vague thing" \
  --brain-loop \
  --provider-review-stub
```

Expected behavior:

- `brain_loop.blocked` remains `true` for the unknown route;
- `provider_review.provider_called` is `false`;
- `provider_review.advisory_only` is `true`;
- no queue entry or writeback path is created.

## Future Provider Adapter Rule

A real provider adapter may only fill allowed advisory fields such as ambiguity notes, risk notes, plan critique, and missing-context questions. It must not execute actions or change the Brain Model's local decision gates.

Before any real provider call is added, tests must prove that provider output cannot relax confirmation, blocked state, queue policy, writeback policy, or risk classification.
