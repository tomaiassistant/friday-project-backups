"""Tests for local JSON task queue persistence."""

import json

import pytest

from budget_jarvis_core import JsonTaskQueueStore, TaskQueue


def test_load_missing_store_returns_empty_queue(tmp_path) -> None:
    store = JsonTaskQueueStore(tmp_path / "queue.json")

    queue = store.load()

    assert queue.list_tasks() == []


def test_save_and_load_round_trips_queue(tmp_path) -> None:
    ids = iter(["task-1", "task-2"])
    queue = TaskQueue(id_factory=lambda: next(ids))
    first = queue.submit("Review Brain Model docs", metadata={"risk_level": "low"})
    second = queue.submit("Update local task file")
    queue.complete(second.id, "updated")
    store = JsonTaskQueueStore(tmp_path / "state" / "queue.json")

    saved_path = store.save(queue)
    loaded = store.load()

    assert saved_path == tmp_path / "state" / "queue.json"
    assert [task.id for task in loaded.list_tasks()] == [first.id, second.id]
    assert loaded.get(first.id).metadata == {"risk_level": "low"}
    assert loaded.get(second.id).result == "updated"


def test_save_writes_json_array(tmp_path) -> None:
    queue = TaskQueue(id_factory=lambda: "task-json")
    queue.submit("Persist queue")
    store = JsonTaskQueueStore(tmp_path / "queue.json")

    store.save(queue)

    raw = json.loads((tmp_path / "queue.json").read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    assert raw[0]["id"] == "task-json"


def test_load_rejects_non_array_json(tmp_path) -> None:
    path = tmp_path / "queue.json"
    path.write_text('{"bad": true}', encoding="utf-8")

    with pytest.raises(ValueError, match="JSON array"):
        JsonTaskQueueStore(path).load()


def test_load_rejects_non_object_records(tmp_path) -> None:
    path = tmp_path / "queue.json"
    path.write_text('["bad"]', encoding="utf-8")

    with pytest.raises(ValueError, match="JSON objects"):
        JsonTaskQueueStore(path).load()
