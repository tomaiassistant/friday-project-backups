# Budget Jarvis v0.1 Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build the first real coding foundation for Tom/Budget Jarvis: a safe brain/router core that can receive a transcript, recall context hooks, classify risk, choose actions, queue long work, and write back project state.

**Architecture:** Start with a local Python package inside the Brain Model repo. Keep it independent from live mic/PC-control at first so we can test the brain logic safely before connecting it to the Windows worker.

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

**Objective:** Classify actions into low/medium/high risk.

**Files:**
- Modify: `budget_jarvis_core/risk.py`
- Modify: `tests/test_risk.py`

**Rules:**

- Low: read, summarize, create local notes/specs.
- Medium: edit project files, commit/push private repo, run safe commands.
- High: email, public post, delete files, payment/account actions, credential handling, major infra changes, messaging people as Shadhin.

**Steps:**

1. Write tests for 10 sample commands.
2. Implement `RiskLevel` enum.
3. Implement `classify_risk(text: str) -> RiskDecision`.
4. Include `requires_confirmation` bool.
5. Run tests.
6. Commit: `feat: add command risk classifier`

## Milestone 2 - Safe Router

### Task 4: Define route model

**Objective:** Create a simple action route object.

**Files:**
- Modify: `budget_jarvis_core/router.py`
- Create: `tests/test_router.py`

**Route fields:**

- `intent`
- `tool_category`
- `risk_level`
- `requires_confirmation`
- `reason`
- `next_action`

**Steps:**

1. Write tests for creating a route from a low-risk command.
2. Implement dataclass `ActionRoute`.
3. Run tests.
4. Commit: `feat: add action route model`

### Task 5: Implement basic transcript router

**Objective:** Convert a transcript into an action route.

**Files:**
- Modify: `budget_jarvis_core/router.py`
- Modify: `tests/test_router.py`

**Initial route categories:**

- `project_files`
- `memory`
- `openclaw`
- `windows_worker`
- `browser`
- `schedule`
- `research`
- `communication`
- `unknown`

**Steps:**

1. Write tests for representative commands.
2. Implement keyword-based first pass router.
3. Use `classify_risk` inside router.
4. Run tests.
5. Commit: `feat: route transcripts to safe tool categories`

## Milestone 3 - Task Queue and Memory Bridge

### Task 6: Implement in-memory task queue

**Objective:** Queue complex tasks without blocking voice conversation.

**Files:**
- Modify: `budget_jarvis_core/task_queue.py`
- Create: `tests/test_task_queue.py`

**Steps:**

1. Write tests for submitting, listing, completing, failing tasks.
2. Implement `TaskStatus`, `QueuedTask`, `TaskQueue`.
3. Keep it in-memory for v0.1.
4. Run tests.
5. Commit: `feat: add Budget Jarvis task queue`

### Task 7: Implement project memory bridge

**Objective:** Write task/reflection summaries into Brain Model files.

**Files:**
- Modify: `budget_jarvis_core/memory_bridge.py`
- Create: `tests/test_memory_bridge.py`

**Steps:**

1. Write tests using a temporary project folder.
2. Implement `append_daily_log(project_path, text, date=None)`.
3. Implement `write_task(project_path, task_id, title, body)`.
4. Implement `append_project_memory(project_path, text)`.
5. Run tests.
6. Commit: `feat: add Brain Model memory bridge`

## Milestone 4 - First End-to-End Brain Run

### Task 8: Add CLI prototype

**Objective:** Test brain/router flow from terminal.

**Files:**
- Create: `budget_jarvis_core/cli.py`
- Create: `tests/test_cli.py`

**Command:**

```bash
python -m budget_jarvis_core.cli "summarize Brain Model progress"
```

**Expected:**

- prints route JSON
- says whether confirmation is required
- optionally writes a daily log in dry-run or real mode

**Steps:**

1. Write minimal CLI test.
2. Implement CLI with argparse.
3. Run tests.
4. Manually test command.
5. Commit: `feat: add Budget Jarvis brain CLI prototype`

### Task 9: Integration check and documentation

**Objective:** Document how to use the first prototype.

**Files:**
- Create: `docs/budget-jarvis-core-v01.md`
- Modify: `README.md` if it exists, otherwise skip.

**Steps:**

1. Write usage docs.
2. Include safety/risk examples.
3. Run full test suite: `python -m pytest -v`.
4. Commit: `docs: document Budget Jarvis core prototype`

---

## Coding Start Decision

Coding can start after Shadhin confirms, or during the next 8:00 AM Brain Model work window if no blocking question exists.

First coding command will be:

```bash
cd /home/ubuntu/.openclaw/workspace/projects/brain-model
python -m pytest -v
```

Then begin Task 1.
