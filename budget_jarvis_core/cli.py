"""Command-line prototype for the Budget Jarvis brain/router flow.

The CLI is intentionally non-executing: it routes a transcript, prints JSON, and
can optionally write a simple daily log through the local Brain Model memory
bridge. Dry-run is the default for writeback safety.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .brain_loop import BrainLoopResult, run_brain_loop
from .memory_bridge import append_daily_log
from .project_recall import recall_context_strings
from .provider_review import (
    build_provider_review_request,
    provider_review_result_to_dict,
    run_provider_review_stub,
)
from .router import ActionRoute, route_transcript
from .task_queue import TaskQueue


def route_to_dict(route: ActionRoute) -> dict[str, str | bool]:
    """Serialize an ``ActionRoute`` using primitive JSON-safe values."""

    return {
        "intent": route.intent,
        "tool_category": route.tool_category.value,
        "risk_level": route.risk_level.value,
        "requires_confirmation": route.requires_confirmation,
        "reason": route.reason,
        "next_action": route.next_action,
    }


def brain_loop_to_dict(result: BrainLoopResult) -> dict[str, Any]:
    """Serialize a BrainLoopResult using primitive JSON-safe values."""

    queued_task = None
    if result.queued_task is not None:
        queued_task = {
            "id": result.queued_task.id,
            "title": result.queued_task.title,
            "description": result.queued_task.description,
            "status": result.queued_task.status.value,
            "metadata": result.queued_task.metadata,
        }

    return {
        "transcript": result.transcript,
        "state": result.state.value,
        "route": route_to_dict(result.route),
        "recalled_context": list(result.recalled_context),
        "planned_action": result.planned_action,
        "queued_task": queued_task,
        "reflection": result.reflection,
        "writeback_path": str(result.writeback_path) if result.writeback_path else None,
        "confirmation_required": result.confirmation_required,
        "blocked": result.blocked,
        "confidence": result.confidence,
        "escalation_required": result.escalation_required,
        "escalation_reason": result.escalation_reason,
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="python -m budget_jarvis_core.cli",
        description="Route a transcript through the Budget Jarvis v0.1 brain prototype.",
    )
    parser.add_argument("transcript", help="Transcript or command to route safely.")
    parser.add_argument(
        "--brain-loop",
        action="store_true",
        help="Run the full non-executing observe/recall/reason/act/reflect loop.",
    )
    parser.add_argument(
        "--context",
        action="append",
        default=[],
        help="Recalled context item for --brain-loop. Repeat for multiple items.",
    )
    parser.add_argument(
        "--recall-project",
        type=Path,
        help="Project folder to read for local markdown recall in --brain-loop mode.",
    )
    parser.add_argument(
        "--recall-max-items",
        type=int,
        default=5,
        help="Maximum project recall items to add when --recall-project is used.",
    )
    parser.add_argument(
        "--queue-store",
        type=Path,
        help="Optional local JSON queue-state path to include in project recall.",
    )
    parser.add_argument(
        "--queue-complex",
        action="store_true",
        help="In --brain-loop mode, queue safe work in an in-memory queue.",
    )
    parser.add_argument(
        "--provider-review-stub",
        action="store_true",
        help=(
            "In --brain-loop mode, attach a typed advisory-only provider review stub. "
            "No provider is called and local safety gates are unchanged."
        ),
    )
    parser.add_argument(
        "--write-log",
        action="store_true",
        help="Prepare a daily-log writeback. Dry-run unless --real-write is also passed.",
    )
    parser.add_argument(
        "--real-write",
        action="store_true",
        help="Actually append the daily log. Requires --write-log and --project-path.",
    )
    parser.add_argument(
        "--project-path",
        type=Path,
        help="Brain Model project folder for real daily-log writeback.",
    )
    parser.add_argument(
        "--log-date",
        help="Optional ISO date for deterministic daily-log writeback, e.g. 2026-05-26.",
    )
    parser.add_argument(
        "--log-text",
        help="Optional daily-log text. Defaults to a summary of the route decision.",
    )
    return parser


def _default_log_text(route: ActionRoute) -> str:
    confirmation = "requires confirmation" if route.requires_confirmation else "no confirmation required"
    return (
        "CLI prototype routed transcript "
        f"`{route.intent}` to `{route.tool_category.value}` "
        f"with `{route.risk_level.value}` risk; {confirmation}."
    )


def _build_log_result(args: argparse.Namespace, route: ActionRoute) -> dict[str, str | bool | None]:
    if not args.write_log:
        return {"requested": False, "dry_run": True, "written": False, "path": None, "text": None}

    log_text = args.log_text.strip() if args.log_text else _default_log_text(route)

    if not args.real_write:
        return {
            "requested": True,
            "dry_run": True,
            "written": False,
            "path": None,
            "text": log_text,
        }

    if args.project_path is None:
        raise ValueError("--project-path is required when using --real-write")

    log_path = append_daily_log(args.project_path, log_text, date=args.log_date)
    return {
        "requested": True,
        "dry_run": False,
        "written": True,
        "path": str(log_path),
        "text": log_text,
    }


def _build_recalled_context(args: argparse.Namespace) -> tuple[str, ...]:
    """Combine explicit CLI context with optional local project recall."""

    context = tuple(item.strip() for item in args.context if item and item.strip())
    if args.recall_project is None:
        return context

    project_context = recall_context_strings(
        args.recall_project,
        args.transcript,
        max_items=args.recall_max_items,
        queue_store_path=args.queue_store,
    )
    return context + project_context


def run(argv: Sequence[str] | None = None) -> dict[str, Any]:
    """Run the CLI flow and return the JSON-compatible payload."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.real_write and not args.write_log:
        parser.error("--real-write requires --write-log")

    if args.real_write and args.project_path is None:
        parser.error("--project-path is required when using --real-write")
    if args.recall_project is not None and not args.brain_loop:
        parser.error("--recall-project requires --brain-loop")
    if args.queue_store is not None and args.recall_project is None:
        parser.error("--queue-store requires --recall-project")
    if args.provider_review_stub and not args.brain_loop:
        parser.error("--provider-review-stub requires --brain-loop")
    if args.brain_loop:
        recalled_context = _build_recalled_context(args)
        result = run_brain_loop(
            args.transcript,
            recalled_context=recalled_context,
            queue=TaskQueue() if args.queue_complex else None,
            queue_complex=args.queue_complex,
            project_path=args.project_path,
            write_reflection=args.write_log and args.real_write,
            date=args.log_date,
        )
        payload = {
            "brain_loop": brain_loop_to_dict(result),
            "confirmation_required": result.confirmation_required,
            "escalation_required": result.escalation_required,
        }
        if args.provider_review_stub:
            review_request = build_provider_review_request(result)
            review_result = run_provider_review_stub(review_request)
            payload["provider_review"] = provider_review_result_to_dict(review_result)
        if args.write_log and not args.real_write:
            payload["log"] = {
                "requested": True,
                "dry_run": True,
                "written": False,
                "path": None,
                "text": result.reflection,
            }
        return payload

    route = route_transcript(args.transcript)
    payload: dict[str, Any] = {
        "route": route_to_dict(route),
        "confirmation_required": route.requires_confirmation,
        "log": _build_log_result(args, route),
    }
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""

    try:
        payload = run(argv)
    except ValueError as exc:
        build_parser().exit(status=2, message=f"error: {exc}\n")

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
