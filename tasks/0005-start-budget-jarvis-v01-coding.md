# Task: Start Budget Jarvis v0.1 Coding

**Created:** 2026-09-25
**Agent:** Friday (Hermes)
**Status:** Ready to start
**Priority:** High
**Milestone:** 1 - Core Package Skeleton

## Description

Begin implementing the Budget Jarvis v0.1 core package per the implementation plan. Start with Milestone 1, Task 1: Create Python package skeleton.

## Files to Create

```
budget_jarvis_core/
  __init__.py
  state.py
  risk.py
  router.py
  task_queue.py
  memory_bridge.py
tests/
  test_state.py
  test_risk.py
```

## Steps

1. Create package directory structure
2. Add empty modules with docstrings
3. Add pytest smoke tests
4. Run tests: `python -m pytest tests/test_state.py tests/test_risk.py -v`
5. Commit: `feat: add Budget Jarvis core skeleton`

## Dependencies

- Python 3.11+
- pytest
- AI Knowledge vault structure exists

## Related

- [[plans/0001-budget-jarvis-v01-implementation-plan]]
- [[specs/0001-v01-architecture-first-pass]]
- [[decisions/2026-05-22-budget-jarvis-core-first]]