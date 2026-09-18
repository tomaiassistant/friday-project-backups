"""Tests for Budget Jarvis in-memory task queue."""

from datetime import UTC, datetime, timedelta

import pytest

from budget_jarvis_core.task_queue import QueuedTask, TaskQueue, TaskStatus, task_from_record, task_to_record


class StepClock:
    def __init__(self) -> None:
        self.current = datetime(2026, 5, 24, 2, 0, tzinfo=UTC)

    def __call__(self) -> datetime:
        value = self.current
        self.current += timedelta(seconds=1)
        return value


def test_submit_creates_pending_task_with_deterministic_id() -> None:
    queue = TaskQueue(id_factory=lambda: "task-alpha", clock=StepClock())

    task = queue.submit(
        "  Summarize project progress  ",
        "  Use project files only.  ",
        metadata={"risk_level": "low"},
    )

    assert isinstance(task, QueuedTask)
    assert task.id == "task-alpha"
    assert task.title == "Summarize project progress"
    assert task.description == "Use project files only."
    assert task.status is TaskStatus.PENDING
    assert task.result is None
    assert task.error is None
    assert task.metadata == {"risk_level": "low"}
    assert task.created_at == datetime(2026, 5, 24, 2, 0, tzinfo=UTC)
    assert task.updated_at == task.created_at


def test_submit_rejects_empty_title() -> None:
    queue = TaskQueue(id_factory=lambda: "task-empty")

    with pytest.raises(ValueError, match="title"):
        queue.submit("   ")


def test_list_tasks_returns_in_insertion_order_and_filters_by_status() -> None:
    ids = iter(["task-1", "task-2", "task-3"])
    queue = TaskQueue(id_factory=lambda: next(ids), clock=StepClock())

    first = queue.submit("first")
    second = queue.submit("second")
    third = queue.submit("third")
    queue.complete(second.id, "done")

    assert [task.id for task in queue.list_tasks()] == [first.id, second.id, third.id]
    assert [task.id for task in queue.list_tasks(TaskStatus.PENDING)] == [first.id, third.id]
    assert [task.id for task in queue.list_tasks("completed")] == [second.id]


def test_get_unknown_task_raises_key_error() -> None:
    queue = TaskQueue()

    with pytest.raises(KeyError, match="unknown task id"):
        queue.get("missing")


def test_start_moves_pending_task_to_running_and_updates_timestamp() -> None:
    queue = TaskQueue(id_factory=lambda: "task-run", clock=StepClock())
    task = queue.submit("run tests")

    running = queue.start(task.id)

    assert running.status is TaskStatus.RUNNING
    assert running.updated_at > running.created_at
    assert queue.get(task.id) == running


def test_complete_can_finish_running_task_with_result() -> None:
    queue = TaskQueue(id_factory=lambda: "task-complete", clock=StepClock())
    task = queue.submit("write docs")
    queue.start(task.id)

    completed = queue.complete(task.id, "Documentation updated")

    assert completed.status is TaskStatus.COMPLETED
    assert completed.result == "Documentation updated"
    assert completed.error is None
    assert completed.updated_at > completed.created_at


def test_complete_can_finish_pending_task_for_small_synchronous_work() -> None:
    queue = TaskQueue(id_factory=lambda: "task-fast")
    task = queue.submit("quick note")

    completed = queue.complete(task.id)

    assert completed.status is TaskStatus.COMPLETED
    assert completed.result == ""


def test_fail_records_error_and_clears_result() -> None:
    queue = TaskQueue(id_factory=lambda: "task-fail", clock=StepClock())
    task = queue.submit("call partner agent")
    queue.start(task.id)

    failed = queue.fail(task.id, "OpenClaw timed out")

    assert failed.status is TaskStatus.FAILED
    assert failed.error == "OpenClaw timed out"
    assert failed.result is None
    assert failed.updated_at > failed.created_at


def test_fail_rejects_empty_error() -> None:
    queue = TaskQueue(id_factory=lambda: "task-no-error")
    task = queue.submit("unsafe failure")

    with pytest.raises(ValueError, match="error"):
        queue.fail(task.id, "  ")


@pytest.mark.parametrize(
    "terminal_action",
    [
        lambda queue, task_id: queue.start(task_id),
        lambda queue, task_id: queue.complete(task_id, "again"),
        lambda queue, task_id: queue.fail(task_id, "again"),
    ],
)
def test_completed_task_rejects_illegal_transitions(terminal_action) -> None:
    queue = TaskQueue(id_factory=lambda: "task-terminal")
    task = queue.submit("terminal")
    queue.complete(task.id, "done")

    with pytest.raises(ValueError, match="cannot"):
        terminal_action(queue, task.id)


def test_failed_task_rejects_illegal_transitions() -> None:
    queue = TaskQueue(id_factory=lambda: "task-failed")
    task = queue.submit("terminal failure")
    queue.fail(task.id, "failed")

    with pytest.raises(ValueError, match="cannot"):
        queue.complete(task.id, "later")


def test_duplicate_generated_id_is_rejected() -> None:
    queue = TaskQueue(id_factory=lambda: "same-id")
    queue.submit("first")

    with pytest.raises(ValueError, match="duplicate"):
        queue.submit("second")


def test_snapshot_serializes_tasks_in_insertion_order() -> None:
    ids = iter(["task-a", "task-b"])
    queue = TaskQueue(id_factory=lambda: next(ids), clock=StepClock())
    first = queue.submit("first", metadata={"risk_level": "low"})
    second = queue.submit("second")
    queue.complete(second.id, "done")

    snapshot = queue.snapshot()

    assert [record["id"] for record in snapshot] == [first.id, second.id]
    assert snapshot[0]["metadata"] == {"risk_level": "low"}
    assert snapshot[1]["status"] == "completed"
    assert snapshot[1]["result"] == "done"


def test_task_record_round_trip_preserves_fields() -> None:
    queue = TaskQueue(id_factory=lambda: "task-round", clock=StepClock())
    task = queue.submit("round trip", "persist me", metadata={"tool_category": "project_files"})
    queue.start(task.id)
    task = queue.complete(task.id, "saved")

    restored = task_from_record(task_to_record(task))

    assert restored == task


def test_from_tasks_rejects_duplicate_loaded_ids() -> None:
    task = QueuedTask(id="task-dup", title="duplicate")

    with pytest.raises(ValueError, match="duplicate task id loaded"):
        TaskQueue.from_tasks([task, task])


def test_task_from_record_rejects_bad_metadata() -> None:
    queue = TaskQueue(id_factory=lambda: "task-bad-meta", clock=StepClock())
    record = task_to_record(queue.submit("bad metadata"))
    record["metadata"] = ["not", "an", "object"]

    with pytest.raises(ValueError, match="metadata"):
        task_from_record(record)
