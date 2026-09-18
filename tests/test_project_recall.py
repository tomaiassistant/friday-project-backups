"""Tests for local project-memory recall."""

import pytest

from budget_jarvis_core import TaskQueue, JsonTaskQueueStore, recall_context_strings, recall_project_context


def test_recall_markdown_returns_ranked_source_labelled_items(tmp_path) -> None:
    memory_dir = tmp_path / "memory"
    specs_dir = tmp_path / "specs"
    memory_dir.mkdir()
    specs_dir.mkdir()
    (memory_dir / "PROJECT_MEMORY.md").write_text(
        "# Brain Model Project Memory\n"
        "- Budget Jarvis v0.1 now has local JSON queue persistence.\n"
        "- Unrelated note.\n",
        encoding="utf-8",
    )
    (specs_dir / "0004.md").write_text(
        "# Layered Provider Replacement Roadmap\n"
        "Memory recall over markdown and queue state is next.\n",
        encoding="utf-8",
    )

    items = recall_project_context(tmp_path, "Budget Jarvis memory queue recall", max_items=3)

    assert len(items) == 3
    assert items[0].score >= items[1].score
    assert "memory/PROJECT_MEMORY.md" in items[0].source
    assert "Budget Jarvis" in items[0].text
    assert items[0].as_context().startswith("memory/PROJECT_MEMORY.md:")


def test_recall_context_strings_formats_for_brain_loop(tmp_path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "progress.md").write_text("Brain loop recall uses local context.\n", encoding="utf-8")

    context = recall_context_strings(tmp_path, "brain loop local context")

    assert context == ("docs/progress.md:1: Brain loop recall uses local context.",)


def test_recall_can_include_queue_state(tmp_path) -> None:
    queue = TaskQueue(id_factory=lambda: "task-queue")
    queue.submit(
        "Review provider fallback",
        "Add Hermes provider-router notes before Windows worker handoff.",
        metadata={"risk_level": "low"},
    )
    store_path = tmp_path / "state" / "queue.json"
    JsonTaskQueueStore(store_path).save(queue)

    items = recall_project_context(
        tmp_path,
        "provider fallback windows worker",
        queue_store_path="state/queue.json",
    )

    assert items
    assert items[0].source == "state/queue.json#task-queue"
    assert "Review provider fallback" in items[0].text
    assert "risk_level=low" in items[0].text


def test_recall_ignores_missing_markdown_dirs_and_missing_queue_store(tmp_path) -> None:
    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "PROJECT_MEMORY.md").write_text("Memory layer is local.\n", encoding="utf-8")

    items = recall_project_context(tmp_path, "memory local", queue_store_path="missing/queue.json")

    assert len(items) == 1
    assert items[0].source.startswith("memory/PROJECT_MEMORY.md:")


def test_recall_validates_query_and_limit(tmp_path) -> None:
    with pytest.raises(ValueError, match="searchable term"):
        recall_project_context(tmp_path, "the and of")

    with pytest.raises(ValueError, match="max_items"):
        recall_project_context(tmp_path, "brain", max_items=0)
