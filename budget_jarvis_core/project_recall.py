"""Local project-memory recall for Budget Jarvis.

The recall layer reads project-local markdown and optional queue JSON state to
produce small, source-labelled grounding snippets. It is intentionally simple for
v0.1: deterministic keyword scoring, no embeddings, no network calls, and no
external provider dependency.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .memory_bridge import PathLike
from .task_store import JsonTaskQueueStore

_DEFAULT_MARKDOWN_DIRS = (
    "memory",
    "tasks",
    "specs",
    "decisions",
    "docs",
    "shared/inbox",
    "shared/outbox",
    "shared/logs",
)
_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


@dataclass(frozen=True)
class RecallItem:
    """One local memory snippet selected for grounding."""

    source: str
    text: str
    score: int

    def as_context(self) -> str:
        """Return a compact source-labelled context string."""

        return f"{self.source}: {self.text}"


def recall_project_context(
    project_path: PathLike,
    query: str,
    *,
    max_items: int = 5,
    markdown_dirs: Iterable[str] = _DEFAULT_MARKDOWN_DIRS,
    queue_store_path: PathLike | None = None,
) -> tuple[RecallItem, ...]:
    """Recall local Brain Model context relevant to ``query``.

    The function only reads files under ``project_path`` plus an optional queue
    store path. Markdown lines are scored by token overlap with the query and
    returned with relative source paths. Queue tasks are summarized from local
    JSON state when a queue store is supplied.
    """

    root = Path(project_path)
    terms = _query_terms(query)
    if max_items < 1:
        raise ValueError("max_items must be at least 1")
    if not terms:
        raise ValueError("query must contain at least one searchable term")

    candidates: list[RecallItem] = []
    candidates.extend(_recall_markdown(root, terms, markdown_dirs))
    if queue_store_path is not None:
        candidates.extend(_recall_queue(root, Path(queue_store_path), terms))

    ranked = sorted(candidates, key=lambda item: (-item.score, item.source, item.text))
    return tuple(ranked[:max_items])


def recall_context_strings(
    project_path: PathLike,
    query: str,
    *,
    max_items: int = 5,
    queue_store_path: PathLike | None = None,
) -> tuple[str, ...]:
    """Return recall results formatted for ``run_brain_loop(recalled_context=...)``."""

    return tuple(
        item.as_context()
        for item in recall_project_context(
            project_path,
            query,
            max_items=max_items,
            queue_store_path=queue_store_path,
        )
    )


def _recall_markdown(root: Path, terms: set[str], markdown_dirs: Iterable[str]) -> list[RecallItem]:
    items: list[RecallItem] = []
    for relative_dir in markdown_dirs:
        directory = root / relative_dir
        if not directory.exists() or not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            if not _is_under(path, root):
                continue
            for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                text = _normalize_snippet(raw_line)
                if not text:
                    continue
                score = _score_text(text, terms)
                if score:
                    source = f"{path.relative_to(root)}:{line_number}"
                    items.append(RecallItem(source=source, text=text, score=score))
    return items


def _recall_queue(root: Path, queue_store_path: Path, terms: set[str]) -> list[RecallItem]:
    store_path = queue_store_path if queue_store_path.is_absolute() else root / queue_store_path
    queue = JsonTaskQueueStore(store_path).load()
    items: list[RecallItem] = []
    for task in queue.list_tasks():
        metadata_bits = " ".join(f"{key}={value}" for key, value in sorted(task.metadata.items()))
        text = _normalize_snippet(
            f"queue task {task.id} [{task.status.value}] {task.title}. {task.description} {metadata_bits}"
        )
        score = _score_text(text, terms)
        if score:
            source = f"{store_path.relative_to(root) if _is_under(store_path, root) else store_path}#{task.id}"
            items.append(RecallItem(source=str(source), text=text, score=score))
    return items


def _query_terms(query: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9_-]{1,}", query.lower())
        if token not in _STOPWORDS
    }


def _score_text(text: str, terms: set[str]) -> int:
    lower = text.lower()
    score = sum(1 for term in terms if term in lower)
    if text.startswith("#"):
        score += 1
    return score


def _normalize_snippet(text: str, *, limit: int = 240) -> str:
    normalized = " ".join(text.strip().split())
    if not normalized:
        return ""
    return normalized if len(normalized) <= limit else normalized[: limit - 1].rstrip() + "…"


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True
