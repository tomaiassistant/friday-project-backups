"""Local file bridge for writing Budget Jarvis reflections into Brain Model files.

These helpers intentionally write only inside a provided project folder. They are
small deterministic filesystem primitives for v0.1: create missing directories,
append simple markdown blocks, and avoid overwriting existing task files.
"""

from __future__ import annotations

from datetime import date as Date
from pathlib import Path
import re
from typing import Union

PathLike = Union[str, Path]


def append_daily_log(project_path: PathLike, text: str, date: Date | str | None = None) -> Path:
    """Append a markdown note to ``shared/logs/YYYY-MM-DD.md``.

    If the dated log file does not exist, it is created with a top-level date
    heading. ``date`` may be injected as a ``datetime.date`` or ISO date string
    for deterministic tests.
    """

    cleaned_text = _require_text("text", text)
    day = _format_date(date)
    log_path = Path(project_path) / "shared" / "logs" / f"{day}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if not log_path.exists():
        log_path.write_text(f"# {day}\n", encoding="utf-8")

    _append_block(log_path, "Budget Jarvis Memory Bridge", cleaned_text)
    return log_path


def write_task(project_path: PathLike, task_id: str, title: str, body: str) -> Path:
    """Create a task markdown file without overwriting existing task files.

    The filename is ``tasks/{task_id}-{slugified-title}.md``. Empty identifiers,
    titles, or bodies raise ``ValueError``; an existing file raises
    ``FileExistsError`` so accidental task loss is not possible.
    """

    cleaned_task_id = _require_text("task_id", task_id)
    cleaned_title = _require_text("title", title)
    cleaned_body = _require_text("body", body)
    slug = _slugify(cleaned_title)

    task_path = Path(project_path) / "tasks" / f"{cleaned_task_id}-{slug}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)

    if task_path.exists():
        raise FileExistsError(f"task file already exists: {task_path}")

    task_path.write_text(
        f"# {cleaned_title}\n\n"
        f"- Task ID: {cleaned_task_id}\n"
        f"- Status: open\n\n"
        f"## Body\n\n"
        f"{cleaned_body}\n",
        encoding="utf-8",
    )
    return task_path


def append_project_memory(project_path: PathLike, text: str) -> Path:
    """Append a durable note to ``memory/PROJECT_MEMORY.md``.

    The memory file and its parent folder are created if needed. Existing memory
    content is preserved and the new note is appended as a simple markdown block.
    """

    cleaned_text = _require_text("text", text)
    memory_path = Path(project_path) / "memory" / "PROJECT_MEMORY.md"
    memory_path.parent.mkdir(parents=True, exist_ok=True)

    if not memory_path.exists():
        memory_path.write_text("# Brain Model Project Memory\n", encoding="utf-8")

    _append_block(memory_path, "Budget Jarvis Memory Entry", cleaned_text)
    return memory_path


def _append_block(path: Path, heading: str, text: str) -> None:
    existing = path.read_text(encoding="utf-8")
    separator = "\n" if existing.endswith("\n") else "\n\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{separator}## {heading}\n\n{text}\n")


def _format_date(value: Date | str | None) -> str:
    if value is None:
        return Date.today().isoformat()
    if isinstance(value, Date):
        return value.isoformat()
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("date must not be empty")
    # Validate ISO calendar date while preserving the exact normalized string.
    Date.fromisoformat(cleaned)
    return cleaned


def _require_text(name: str, value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{name} must not be empty")
    return cleaned


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "task"
