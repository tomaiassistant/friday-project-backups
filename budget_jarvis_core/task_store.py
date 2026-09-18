"""Local JSON persistence for Budget Jarvis task queues.

The store is intentionally simple: it saves and loads queue snapshots from a
project-local JSON file. It does not run workers, sync externally, or bypass
the queue's confirmation model.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .task_queue import TaskQueue, task_from_record


class JsonTaskQueueStore:
    """Persist a TaskQueue snapshot to a local JSON file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> TaskQueue:
        """Load a queue from disk, returning an empty queue if no file exists."""

        if not self.path.exists():
            return TaskQueue()

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("task queue store must contain a JSON array")

        tasks = []
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError("task queue records must be JSON objects")
            tasks.append(task_from_record(item))
        return TaskQueue.from_tasks(tasks)

    def save(self, queue: TaskQueue) -> Path:
        """Write a queue snapshot atomically and return the store path."""

        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_name(f"{self.path.name}.tmp")
        tmp_path.write_text(_dumps(queue.snapshot()), encoding="utf-8")
        tmp_path.replace(self.path)
        return self.path


def _dumps(records: list[dict[str, Any]]) -> str:
    return json.dumps(records, indent=2, sort_keys=True) + "\n"
