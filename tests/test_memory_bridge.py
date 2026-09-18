"""Tests for Budget Jarvis project memory bridge."""

from datetime import date

import pytest

from budget_jarvis_core.memory_bridge import (
    append_daily_log,
    append_project_memory,
    write_task,
)


def test_append_daily_log_creates_dated_file_and_parent_folders(tmp_path) -> None:
    log_path = append_daily_log(
        tmp_path,
        "  Implemented memory bridge.  ",
        date=date(2026, 5, 25),
    )

    assert log_path == tmp_path / "shared" / "logs" / "2026-05-25.md"
    assert log_path.read_text(encoding="utf-8") == (
        "# 2026-05-25\n\n"
        "## Budget Jarvis Memory Bridge\n\n"
        "Implemented memory bridge.\n"
    )


def test_append_daily_log_appends_to_existing_file_without_overwriting(tmp_path) -> None:
    log_dir = tmp_path / "shared" / "logs"
    log_dir.mkdir(parents=True)
    log_path = log_dir / "2026-05-25.md"
    log_path.write_text("# 2026-05-25\n\nExisting note.\n", encoding="utf-8")

    returned_path = append_daily_log(tmp_path, "Second note.", date="2026-05-25")

    assert returned_path == log_path
    assert log_path.read_text(encoding="utf-8") == (
        "# 2026-05-25\n\n"
        "Existing note.\n\n"
        "## Budget Jarvis Memory Bridge\n\n"
        "Second note.\n"
    )


@pytest.mark.parametrize("text", ["", "   "])
def test_append_daily_log_rejects_empty_text(tmp_path, text) -> None:
    with pytest.raises(ValueError, match="text"):
        append_daily_log(tmp_path, text, date="2026-05-25")


def test_write_task_creates_slugged_task_file(tmp_path) -> None:
    task_path = write_task(
        tmp_path,
        "  0006  ",
        "  Add Brain Loop CLI  ",
        "  Route a transcript and print JSON.  ",
    )

    assert task_path == tmp_path / "tasks" / "0006-add-brain-loop-cli.md"
    assert task_path.read_text(encoding="utf-8") == (
        "# Add Brain Loop CLI\n\n"
        "- Task ID: 0006\n"
        "- Status: open\n\n"
        "## Body\n\n"
        "Route a transcript and print JSON.\n"
    )


@pytest.mark.parametrize(
    ("task_id", "title", "body", "message"),
    [
        ("", "Title", "Body", "task_id"),
        ("0006", "   ", "Body", "title"),
        ("0006", "Title", "", "body"),
    ],
)
def test_write_task_rejects_empty_inputs(tmp_path, task_id, title, body, message) -> None:
    with pytest.raises(ValueError, match=message):
        write_task(tmp_path, task_id, title, body)


def test_write_task_does_not_overwrite_existing_file(tmp_path) -> None:
    first_path = write_task(tmp_path, "0006", "Add CLI", "First body")

    with pytest.raises(FileExistsError, match="already exists"):
        write_task(tmp_path, "0006", "Add CLI", "Second body")

    assert "First body" in first_path.read_text(encoding="utf-8")
    assert "Second body" not in first_path.read_text(encoding="utf-8")


def test_append_project_memory_creates_file_and_parent_folder(tmp_path) -> None:
    memory_path = append_project_memory(tmp_path, "  Memory bridge can append durable notes.  ")

    assert memory_path == tmp_path / "memory" / "PROJECT_MEMORY.md"
    assert memory_path.read_text(encoding="utf-8") == (
        "# Brain Model Project Memory\n\n"
        "## Budget Jarvis Memory Entry\n\n"
        "Memory bridge can append durable notes.\n"
    )


def test_append_project_memory_appends_without_overwriting(tmp_path) -> None:
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True)
    memory_path = memory_dir / "PROJECT_MEMORY.md"
    memory_path.write_text("# Brain Model Project Memory\n\nExisting memory.\n", encoding="utf-8")

    returned_path = append_project_memory(tmp_path, "Second memory.")

    assert returned_path == memory_path
    assert memory_path.read_text(encoding="utf-8") == (
        "# Brain Model Project Memory\n\n"
        "Existing memory.\n\n"
        "## Budget Jarvis Memory Entry\n\n"
        "Second memory.\n"
    )


def test_append_project_memory_rejects_empty_text(tmp_path) -> None:
    with pytest.raises(ValueError, match="text"):
        append_project_memory(tmp_path, "  ")


def test_bridge_functions_are_exported_from_package() -> None:
    from budget_jarvis_core import (  # noqa: PLC0415
        append_daily_log as exported_daily_log,
        append_project_memory as exported_project_memory,
        write_task as exported_write_task,
    )

    assert exported_daily_log is append_daily_log
    assert exported_project_memory is append_project_memory
    assert exported_write_task is write_task
