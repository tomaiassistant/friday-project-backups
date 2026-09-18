"""Minimal non-executing Budget Jarvis brain loop.

This module wires the existing v0.1 primitives into one safe flow:
observe -> recall -> reason -> act -> reflect.  The loop deliberately does not
run external tools, control a PC/browser, send messages, or bypass confirmation.
It only returns a structured result, optionally queues safe local work, and can
write a local Brain Model daily-log reflection when explicitly requested.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .memory_bridge import PathLike, append_daily_log
from .risk import RiskLevel
from .router import ActionRoute, ToolCategory, route_transcript
from .state import JarvisState
from .task_queue import QueuedTask, TaskQueue


@dataclass(frozen=True)
class BrainLoopResult:
    """Structured result from one non-executing brain-loop pass."""

    transcript: str
    state: JarvisState
    route: ActionRoute
    recalled_context: tuple[str, ...]
    planned_action: str
    queued_task: QueuedTask | None
    reflection: str
    writeback_path: Path | None
    confirmation_required: bool
    blocked: bool
    confidence: float
    escalation_required: bool
    escalation_reason: str | None


def run_brain_loop(
    transcript: str,
    *,
    recalled_context: Sequence[str] | None = None,
    queue: TaskQueue | None = None,
    queue_complex: bool = False,
    project_path: PathLike | None = None,
    write_reflection: bool = False,
    date: object | None = None,
) -> BrainLoopResult:
    """Run one safe observe -> recall -> reason -> act -> reflect pass.

    The act phase is intentionally non-executing. High-risk transcripts are
    blocked at ``waiting_for_confirmation`` and never queue work or write a
    completion-style reflection. Medium/low-risk transcripts produce a suggested
    action. If ``queue_complex`` is true and a queue is provided, safe work is
    recorded in the in-memory queue. If ``write_reflection`` is true,
    ``project_path`` is required and a local daily-log reflection is appended for
    non-blocked work only.
    """

    observed = _require_transcript(transcript)
    route = route_transcript(observed)
    context = _normalize_context(recalled_context)
    confidence = _estimate_confidence(route, context)
    escalation_reason = _escalation_reason(route, confidence)

    if route.requires_confirmation:
        planned_action = (
            "Blocked before action: ask Shadhin for explicit confirmation before "
            "continuing. No tools, queue writes, or completion writeback were run."
        )
        reflection = _build_reflection(
            observed,
            route,
            context,
            planned_action,
            None,
            blocked=True,
            confidence=confidence,
            escalation_reason=escalation_reason,
        )
        return BrainLoopResult(
            transcript=observed,
            state=JarvisState.WAITING_FOR_CONFIRMATION,
            route=route,
            recalled_context=context,
            planned_action=planned_action,
            queued_task=None,
            reflection=reflection,
            writeback_path=None,
            confirmation_required=True,
            blocked=True,
            confidence=confidence,
            escalation_required=escalation_reason is not None,
            escalation_reason=escalation_reason,
        )

    if escalation_reason is not None:
        planned_action = (
            "Blocked before action: ask Shadhin for clarification or request typed "
            "provider review. Do not queue work or write completion-style logs until "
            "the route is clear."
        )
        reflection = _build_reflection(
            observed,
            route,
            context,
            planned_action,
            None,
            blocked=True,
            confidence=confidence,
            escalation_reason=escalation_reason,
        )
        return BrainLoopResult(
            transcript=observed,
            state=JarvisState.WAITING_FOR_CONFIRMATION,
            route=route,
            recalled_context=context,
            planned_action=planned_action,
            queued_task=None,
            reflection=reflection,
            writeback_path=None,
            confirmation_required=False,
            blocked=True,
            confidence=confidence,
            escalation_required=True,
            escalation_reason=escalation_reason,
        )

    planned_action = _plan_safe_action(route, context)
    queued_task = _maybe_queue_task(queue, queue_complex, observed, route, planned_action)
    reflection = _build_reflection(
        observed,
        route,
        context,
        planned_action,
        queued_task,
        blocked=False,
        confidence=confidence,
        escalation_reason=None,
    )
    writeback_path = _maybe_write_reflection(project_path, write_reflection, reflection, date)

    return BrainLoopResult(
        transcript=observed,
        state=JarvisState.THINKING,
        route=route,
        recalled_context=context,
        planned_action=planned_action,
        queued_task=queued_task,
        reflection=reflection,
        writeback_path=writeback_path,
        confirmation_required=False,
        blocked=False,
        confidence=confidence,
        escalation_required=False,
        escalation_reason=None,
    )


def _require_transcript(transcript: str) -> str:
    observed = transcript.strip()
    if not observed:
        raise ValueError("transcript must not be empty")
    return observed


def _normalize_context(recalled_context: Sequence[str] | None) -> tuple[str, ...]:
    if recalled_context is None:
        return ()
    return tuple(item.strip() for item in recalled_context if item and item.strip())


def _plan_safe_action(route: ActionRoute, context: tuple[str, ...]) -> str:
    context_note = (
        f"Use {len(context)} recalled context item(s) as local grounding. "
        if context
        else "No recalled context supplied; proceed from transcript and route only. "
    )
    if route.risk_level is RiskLevel.MEDIUM:
        return (
            context_note
            + "Prepare a project-local action plan or queue entry; perform no external side effects. "
            + route.next_action
        )
    return context_note + "Prepare a low-risk suggested action only. " + route.next_action


def _estimate_confidence(route: ActionRoute, context: tuple[str, ...]) -> float:
    """Estimate route confidence for v0.1 without provider calls.

    The score is advisory and must never relax high-risk confirmation gates. It
    only helps the loop decide when to ask for clarification or typed provider
    review before action.
    """

    if route.tool_category is ToolCategory.UNKNOWN:
        return 0.25

    base_by_risk = {
        RiskLevel.LOW: 0.75,
        RiskLevel.MEDIUM: 0.65,
        RiskLevel.HIGH: 0.70,
    }
    confidence = base_by_risk[route.risk_level]
    if context:
        confidence += 0.10
    return round(min(confidence, 0.90), 2)


def _escalation_reason(route: ActionRoute, confidence: float, *, threshold: float = 0.60) -> str | None:
    """Return a human-readable escalation reason when local routing is weak."""

    if route.tool_category is ToolCategory.UNKNOWN:
        return "unknown route: ask Shadhin for clarification or request typed provider review"
    if confidence < threshold:
        return f"low confidence ({confidence:.2f} below {threshold:.2f}): request review before action"
    return None


def _maybe_queue_task(
    queue: TaskQueue | None,
    queue_complex: bool,
    transcript: str,
    route: ActionRoute,
    planned_action: str,
) -> QueuedTask | None:
    if queue is None or not queue_complex:
        return None
    return queue.submit(
        title=f"Budget Jarvis brain-loop task: {route.tool_category.value}",
        description=planned_action,
        metadata={
            "transcript": transcript,
            "tool_category": route.tool_category.value,
            "risk_level": route.risk_level.value,
            "requires_confirmation": route.requires_confirmation,
        },
    )


def _maybe_write_reflection(
    project_path: PathLike | None,
    write_reflection: bool,
    reflection: str,
    date: object | None,
) -> Path | None:
    if not write_reflection:
        return None
    if project_path is None:
        raise ValueError("project_path is required when write_reflection is true")
    return append_daily_log(project_path, reflection, date=date)  # type: ignore[arg-type]


def _build_reflection(
    transcript: str,
    route: ActionRoute,
    context: tuple[str, ...],
    planned_action: str,
    queued_task: QueuedTask | None,
    *,
    blocked: bool,
    confidence: float,
    escalation_reason: str | None,
) -> str:
    if blocked:
        status = "blocked_pending_confirmation"
    elif escalation_reason is not None:
        status = "escalated_needs_review"
    else:
        status = "planned_non_executing"
    queue_line = f"queued_task: {queued_task.id}" if queued_task else "queued_task: none"
    context_lines = "\n".join(f"  - {item}" for item in context) if context else "  - none"
    escalation_line = escalation_reason if escalation_reason is not None else "none"
    return (
        f"status: {status}\n"
        f"transcript: {transcript}\n"
        f"tool_category: {route.tool_category.value}\n"
        f"risk_level: {route.risk_level.value}\n"
        f"confidence: {confidence:.2f}\n"
        f"escalation_required: {escalation_reason is not None}\n"
        f"escalation_reason: {escalation_line}\n"
        f"confirmation_required: {route.requires_confirmation}\n"
        f"reason: {route.reason}\n"
        f"recalled_context:\n{context_lines}\n"
        f"planned_action: {planned_action}\n"
        f"{queue_line}"
    )
