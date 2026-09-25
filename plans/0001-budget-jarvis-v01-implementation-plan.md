# Budget Jarvis v0.1 Implementation Plan

> **For Friday:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build the first real coding foundation for Tom/Budget Jarvis: a safe brain/router core that can receive a transcript, recall context hooks, classify risk, choose actions, queue long work, and write back project state.

**Architecture:** Start with a local Python package inside the AI Knowledge repo. Keep it independent from live mic/PC-control at first so we can test the brain logic safely before connecting it to the Windows worker.

**Tech Stack:** Python 3.11+, pytest, markdown/json project files, Hermes/OpenClaw integration later.

---

## Milestone 1 - Core Package Skeleton

### Task 1: Create Python package skeleton

**Objective:** Add the initial package and test folders.

**Files:**
- Create: `budget_jarvis_core/__init__.py`
- Create: `budget_jarvis_core/state.py`
- Create: `budget_jarvis_core/risk.py`
- Create: `budget_jarvis_core/router.py`
- Create: `budget_jarvis_core/task_queue.py`
- Create: `budget_jarvis_core/memory_bridge.py`
- Create: `tests/test_state.py`
- Create: `tests/test_risk.py`

**Steps:**
1. Create empty modules and simple docstrings.
2. Add pytest smoke tests importing each module.
3. Run: `python -m pytest tests/test_state.py tests/test_risk.py -v`
4. Commit: `feat: add Budget Jarvis core skeleton`

### Task 2: Implement state machine enum

**Objective:** Define explicit states for the live assistant.

**Files:**
- Modify: `budget_jarvis_core/state.py`
- Modify: `tests/test_state.py`

**States:**
- `idle`
- `listening`
- `thinking`
- `speaking`
- `tool_running`
- `waiting_for_confirmation`
- `error`

**Steps:**
1. Write tests for valid states and transition helper.
2. Implement `JarvisState` enum.
3. Implement `can_listen(state)` returning false for `speaking`, `tool_running`, `waiting_for_confirmation`.
4. Run tests.
5. Commit: `feat: add Jarvis state machine primitives`

### Task 3: Implement risk classifier

**Objective:** Classify transcript risk level and confirmation requirement.

**Files:**
- Modify: `budget_jarvis_core/risk.py`
- Modify: `tests/test_risk.py`

**Risk Levels:** `low`, `medium`, `high`
**High-risk patterns:** email, public posting, file deletion, payments, credentials, infrastructure changes, messaging as Shadhin.

**Steps:**
1. Write tests for risk classification.
2. Implement `classify_risk(text)` returning `RiskDecision`.
3. Run tests.
5. Commit: `feat: add risk classifier`

---

## Milestone 2 - Router & Recall

### Task 4: Implement safe transcript router

**Objective:** Route transcript to tool category with risk assessment.

**Files:**
- Modify: `budget_jarvis_core/router.py`
- Modify: `tests/test_router.py`

**ToolCategory values:** `project_files`, `memory`, `openclaw`, `windows_worker`, `browser`, `schedule`, `research`, `communication`, `unknown`

**Steps:**
1. Write tests for routing.
2. Implement `route_transcript(transcript)` returning `ActionRoute`.
3. Integrate `classify_risk()` for every transcript.
4. Run tests.
5. Commit: `feat: add safe transcript router`

### Task 5: Implement project recall

**Objective:** Read project files and return structured context.

**Files:**
- Modify: `budget_jarvis_core/project_recall.py`
- Modify: `tests/test_project_recall.py`

**Steps:**
1. Implement `recall_context()` reading PROJECT.md, PROJECT_MEMORY.md, recent logs.
3. Return structured context bundle.
3. Run tests.
5. Commit: `feat: add project recall`

---

## Milestone 3 - Queue & Writeback

### Task 6: Implement task queue

**Objective:** Queue long-running work with persistence.

**Files:**
- Modify: `budget_jarvis_core/task_queue.py`
- Modify: `budget_jarvis_core/task_store.py`
- Modify: `tests/test_task_queue.py`
- Modify: `tests/test_task_store.py`

**Steps:**
1. Implement in-memory queue with JSON persistence.
2. Add task status tracking (pending/running/done/failed).
3. Run tests.
5. Commit: `feat: add task queue and store`

### Task 7: Implement memory bridge

**Objective:** Write project memory and logs.

**Files:**
- Modify: `budget_jarvis_core/memory_bridge.py`
- Modify: `tests/test_memory_bridge.py`

**Steps:**
1. Implement `write_memory(fact)` → PROJECT_MEMORY.md
2. Implement `write_log(entry)` → shared/logs/YYYY-MM-DD.md
3. Run tests.
5. Commit: `feat: add memory bridge`

---

## Milestone 4 - Integration & Tests

### Task 8: Brain loop integration

**Objective:** Wire all components into observe→recall→reason→act→reflect loop.

**Files:**
- Modify: `budget_jarvis_core/brain_loop.py`
- Modify: `tests/test_brain_loop.py`

**Steps:**
1. Implement `BrainLoop.run(transcript)` orchestrating all layers.
2. Handle confirmation gates for high-risk.
3. Run integration tests.
5. Commit: `feat: add brain loop integration`

### Task 9: CLI & confidence policy

**Objective:** Add CLI and confidence evaluation.

**Files:**
- Modify: `budget_jarvis_core/cli.py`
- Modify: `budget_jarvis_core/confidence.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_confidence_policy.py`

**Steps:**
1. Add CLI entry point.
2. Implement confidence scoring with escalation rules.
3. Run tests.
5. Commit: `feat: add CLI and confidence policy`

### Task 10: Provider review stub

**Objective:** Add advisory-only provider review interface.

**Files:**
- Modify: `budget_jarvis_core/provider_review.py`
- Modify: `tests/test_provider_review.py`

**Steps:**
1. Define typed review request/result objects.
2. Implement stub returning advisory-only placeholder.
3. Run tests.
5. Commit: `feat: add provider review stub`

---

## Milestone 5 - Deployment Prep

### Task 11: Web API wrapper

**Objective:** FastAPI wrapper for Hermes integration.

**Files:**
- Modify: `budget_jarvis_core/web.py`
- Modify: `tests/test_web.py`

**Steps:**
1. Add `/route` and `/brain-loop` endpoints.
2. Add authentication/rate limiting.
3. Run tests.
5. Commit: `feat: add web API wrapper`

### Task 12: Documentation & Examples

**Objective:** Document usage for Hermes and OpenClaw.

**Files:**
- Modify: `docs/budget-jarvis-core-v01.md`
- Modify: `docs/budget-jarvis-core-progress.md`

---

## Related

- [[specs/0001-v01-architecture-first-pass]]
- [[specs/0003-budget-jarvis-evolution-from-mark-xxxix]]
- [[specs/0004-layered-provider-replacement-roadmap]]
- [[tasks/0005-start-budget-jarvis-v01-coding]]