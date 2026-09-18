"""In-memory queue primitives for long-running Budget Jarvis tasks.

The v0.1 queue is deliberately synchronous and non-persistent. It gives the
brain/router core a safe place to record complex work that should not block a
voice/text interaction, without introducing workers, threads, or external
storage yet.
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from itertools import count
from typing import Any


class TaskStatus(StrEnum):
    """Lifecycle states for a queued Budget Jarvis task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class QueuedTask:
    """A single queued unit of work.

    ``result`` and ``error`` stay empty until a terminal status is reached.
    ``metadata`` is for safe local context such as route category, risk level,
    or project file references; it should not be used to bypass confirmation
    gates for risky actions.
    """

    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    result: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskQueue:
    """Small in-memory task queue for Budget Jarvis v0.1."""

    def __init__(
        self,
        *,
        id_factory: Callable[[], str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._counter = count(1)
        self._id_factory = id_factory or self._default_id_factory
        self._clock = clock or (lambda: datetime.now(UTC))
        self._tasks: dict[str, QueuedTask] = {}

    @classmethod
    def from_tasks(
        cls,
        tasks: Iterable[QueuedTask],
        *,
        id_factory: Callable[[], str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> "TaskQueue":
        """Build a queue from existing task records."""

        queue = cls(id_factory=id_factory, clock=clock)
        for task in tasks:
            if task.id in queue._tasks:
                raise ValueError(f"duplicate task id loaded: {task.id}")
            queue._tasks[task.id] = task
        return queue

    def submit(
        self,
        title: str,
        description: str = "",
        *,
        metadata: dict[str, Any] | None = None,
    ) -> QueuedTask:
        """Add a pending task and return the stored immutable task object."""

        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("task title must not be empty")

        task_id = self._new_unique_id()
        now = self._clock()
        task = QueuedTask(
            id=task_id,
            title=normalized_title,
            description=description.strip(),
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            metadata=dict(metadata or {}),
        )
        self._tasks[task_id] = task
        return task

    def list_tasks(self, status: TaskStatus | str | None = None) -> list[QueuedTask]:
        """Return queued tasks in insertion order, optionally filtered by status."""

        if status is None:
            return list(self._tasks.values())

        wanted = TaskStatus(status)
        return [task for task in self._tasks.values() if task.status is wanted]

    def snapshot(self) -> list[dict[str, Any]]:
        """Return JSON-safe records for all tasks in insertion order."""

        return [task_to_record(task) for task in self.list_tasks()]

    def get(self, task_id: str) -> QueuedTask:
        """Return a task by id or raise ``KeyError`` if it does not exist."""

        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"unknown task id: {task_id}") from exc

    def start(self, task_id: str) -> QueuedTask:
        """Move a pending task to running."""

        task = self.get(task_id)
        self._ensure_status(task, {TaskStatus.PENDING}, "start")
        return self._store(replace(task, status=TaskStatus.RUNNING, updated_at=self._clock()))

    def complete(self, task_id: str, result: str = "") -> QueuedTask:
        """Mark a pending/running task as completed."""

        task = self.get(task_id)
        self._ensure_status(
            task,
            {TaskStatus.PENDING, TaskStatus.RUNNING},
            "complete",
        )
        return self._store(
            replace(
                task,
                status=TaskStatus.COMPLETED,
                updated_at=self._clock(),
                result=result,
                error=None,
            )
        )

    def fail(self, task_id: str, error: str) -> QueuedTask:
        """Mark a pending/running task as failed with an error summary."""

        normalized_error = error.strip()
        if not normalized_error:
            raise ValueError("task error must not be empty")

        task = self.get(task_id)
        self._ensure_status(task, {TaskStatus.PENDING, TaskStatus.RUNNING}, "fail")
        return self._store(
            replace(
                task,
                status=TaskStatus.FAILED,
                updated_at=self._clock(),
                result=None,
                error=normalized_error,
            )
        )

    def _default_id_factory(self) -> str:
        return f"task-{next(self._counter):04d}"

    def _new_unique_id(self) -> str:
        task_id = self._id_factory()
        if task_id in self._tasks:
            raise ValueError(f"duplicate task id generated: {task_id}")
        return task_id

    def _store(self, task: QueuedTask) -> QueuedTask:
        self._tasks[task.id] = task
        return task

    @staticmethod
    def _ensure_status(
        task: QueuedTask,
        allowed: Iterable[TaskStatus],
        action: str,
    ) -> None:
        allowed_set = set(allowed)
        if task.status not in allowed_set:
            allowed_values = ", ".join(sorted(status.value for status in allowed_set))
            raise ValueError(
                f"cannot {action} task {task.id} from {task.status.value}; "
                f"allowed: {allowed_values}"
            )


def task_to_record(task: QueuedTask) -> dict[str, Any]:
    """Serialize a queued task into a JSON-safe dictionary."""

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "result": task.result,
        "error": task.error,
        "metadata": task.metadata,
    }


def task_from_record(record: dict[str, Any]) -> QueuedTask:
    """Deserialize a queued task record from a JSON dictionary."""

    try:
        task_id = _require_text(record, "id")
        title = _require_text(record, "title")
        description = str(record.get("description", ""))
        status = TaskStatus(record.get("status", TaskStatus.PENDING.value))
        created_at = _parse_datetime(record["created_at"], "created_at")
        updated_at = _parse_datetime(record["updated_at"], "updated_at")
    except KeyError as exc:
        raise ValueError(f"missing task field: {exc.args[0]}") from exc

    metadata = record.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("task metadata must be an object")

    return QueuedTask(
        id=task_id,
        title=title,
        description=description,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        result=record.get("result"),
        error=record.get("error"),
        metadata=dict(metadata),
    )


def _require_text(record: dict[str, Any], field_name: str) -> str:
    value = record[field_name]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"task {field_name} must be a non-empty string")
    return value


def _parse_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"task {field_name} must be an ISO datetime string")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"task {field_name} must include timezone info")
    return parsed
