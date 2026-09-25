# Budget Jarvis Core Progress

**Date:** 2026-05-23
**Updated:** 2026-09-25
**Agent:** Friday (Hermes)
**Status:** Milestone 1 ready to start — package skeleton

## Implemented (from friday-project-backups)

Initial Python package structure exists in backup repo:

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

## Current Capabilities (from backup)

### State primitives

`JarvisState` defines:
- `idle`
- `listening`
- `thinking`
- `speaking`
- `tool_running`
- `waiting_for_confirmation`
- `error`

`can_listen(state)` returns `False` while speaking, running tools, or waiting for confirmation.

### Risk classifier

`classify_risk(text)` returns `RiskDecision` with:
- `level`: `low`, `medium`, `high`
- `requires_confirmation`
- `reason`
- `matched_terms`

### Safe transcript router

`route_transcript(transcript)` returns `ActionRoute` with:
- `intent`
- `tool_category`
- `risk_level`
- `requires_confirmation`
- `reason`
- `next_action`

## Next: Re-implement in AI Knowledge Repo

The backup code exists but is not in the current AI Knowledge vault. Next step is to create the package structure here and re-implement with the improved architecture.

## Related

- [[plans/0001-budget-jarvis-v01-implementation-plan]]
- [[specs/0003-budget-jarvis-evolution-from-mark-xxxix]]
- [[tasks/0005-start-budget-jarvis-v01-coding]]