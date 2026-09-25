# Budget Jarvis Core v0.1 Prototype

**Owner:** Shadhin
**Agents:** Friday (Hermes), Jerry (OpenClaw)
**Created by:** Friday (Hermes)
**Date:** 2026-05-28
**Updated:** 2026-09-25
**Status:** First usable core documentation; project recall, confidence, escalation, and advisory-only provider-review stub support added
**Related files:**
- `specs/0003-budget-jarvis-evolution-from-mark-xxxix.md`
- `plans/0001-budget-jarvis-v01-implementation-plan.md`
- `tasks/0005-start-budget-jarvis-v01-coding.md`
- `docs/budget-jarvis-core-progress.md`

## Purpose

This document explains how to use the first Budget Jarvis brain/router core prototype.

The prototype proves the safe control layer before live microphone, screen, browser, email, or PC-control integration. It can accept a text transcript, classify risk, choose a broad tool category, expose whether confirmation is required, optionally queue work through in-memory primitives, and write simple project memory/log entries through local filesystem helpers.

## Current Scope

Implemented Python package (to be re-created in AI Knowledge vault):

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

- control the Windows PC
- click, type, or read the screen
- use the microphone
- open browsers or submit forms
- send Telegram/WhatsApp/email messages
- publish public posts
- delete files
- change infrastructure
- handle credentials

It only:

1. routes a transcript to a broad tool category
2. classifies low/medium/high risk
3. marks high-risk routes as requiring confirmation
4. optionally queues work for later execution
5. writes project memory/logs locally

## Usage

```bash
# Run brain loop with a transcript
python -m budget_jarvis_core.cli "please recall the project status" --brain-loop

# Run with provider review stub
python -m budget_jarvis_core.cli "please handle the vague thing" --brain-loop --provider-review-stub
```

## Related

- [[docs/budget-jarvis-core-progress]]
- [[specs/0003-budget-jarvis-evolution-from-mark-xxxix]]
- [[plans/0001-budget-jarvis-v01-implementation-plan]]