"""Typed advisory-only provider review boundary for Brain Model v0.1.

This module defines the local schema for asking an external provider to review a
Brain Model decision later.  It deliberately performs no network/provider call
and cannot change routing, confirmation, blocked, queue, or writeback policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence

from .brain_loop import BrainLoopResult
from .risk import RiskLevel
from .router import ToolCategory


class ProviderReviewLayer(str, Enum):
    """Brain Model layer where advisory review may be requested."""

    INPUT_UNDERSTANDING = "input_understanding"
    REASONING = "reasoning"
    DECISION = "decision"
    GENERATION = "generation"
    REVIEW = "review"


@dataclass(frozen=True)
class ProviderReviewRequest:
    """Typed request shape for a future advisory provider adapter."""

    layer: ProviderReviewLayer
    intent: str
    tool_category: ToolCategory
    risk_level: RiskLevel
    confidence: float
    escalation_required: bool
    escalation_reason: str | None
    recalled_context: tuple[str, ...]
    local_decision: str
    allowed_outputs: tuple[str, ...]
    forbidden_actions: tuple[str, ...]


@dataclass(frozen=True)
class ProviderReviewResult:
    """Local non-executing result returned by the v0.1 review stub."""

    request: ProviderReviewRequest
    advisory_only: bool
    provider_called: bool
    recommendation: str
    cannot_override: tuple[str, ...]


DEFAULT_ALLOWED_OUTPUTS: tuple[str, ...] = (
    "intent_summary",
    "ambiguity_notes",
    "risk_notes",
    "plan_critique",
    "missing_context_questions",
)

DEFAULT_FORBIDDEN_ACTIONS: tuple[str, ...] = (
    "execute_tools",
    "send_messages",
    "modify_files",
    "enqueue_tasks",
    "write_project_memory",
    "downgrade_risk",
    "remove_confirmation_requirement",
    "unblock_blocked_result",
)

CANNOT_OVERRIDE: tuple[str, ...] = (
    "route.tool_category",
    "route.risk_level",
    "confirmation_required",
    "blocked",
    "queued_task",
    "writeback_path",
    "local safety policy",
)


def build_provider_review_request(
    result: BrainLoopResult,
    *,
    layer: ProviderReviewLayer = ProviderReviewLayer.REVIEW,
    allowed_outputs: Sequence[str] = DEFAULT_ALLOWED_OUTPUTS,
    forbidden_actions: Sequence[str] = DEFAULT_FORBIDDEN_ACTIONS,
) -> ProviderReviewRequest:
    """Build a typed review request from a local brain-loop result.

    The request is only a schema object.  It does not call a provider and does
    not mutate the supplied result.
    """

    local_decision = (
        f"state={result.state.value}; blocked={result.blocked}; "
        f"confirmation_required={result.confirmation_required}; "
        f"planned_action={result.planned_action}"
    )
    return ProviderReviewRequest(
        layer=layer,
        intent=result.route.intent,
        tool_category=result.route.tool_category,
        risk_level=result.route.risk_level,
        confidence=result.confidence,
        escalation_required=result.escalation_required,
        escalation_reason=result.escalation_reason,
        recalled_context=tuple(result.recalled_context),
        local_decision=local_decision,
        allowed_outputs=_require_non_empty_strings(allowed_outputs, "allowed_outputs"),
        forbidden_actions=_require_non_empty_strings(forbidden_actions, "forbidden_actions"),
    )


def run_provider_review_stub(request: ProviderReviewRequest) -> ProviderReviewResult:
    """Return a local advisory placeholder without calling any provider.

    This function exists so tests and future CLI flows can exercise the safety
    boundary before real provider adapters are introduced.
    """

    recommendation = (
        "No provider was called. Treat this as an advisory boundary check only; "
        "keep local routing, confirmation, blocked state, queue policy, and "
        "writeback gates unchanged."
    )
    return ProviderReviewResult(
        request=request,
        advisory_only=True,
        provider_called=False,
        recommendation=recommendation,
        cannot_override=CANNOT_OVERRIDE,
    )


def provider_review_result_to_dict(result: ProviderReviewResult) -> dict[str, object]:
    """Serialize a provider-review stub result using JSON-safe primitives."""

    request = result.request
    return {
        "advisory_only": result.advisory_only,
        "provider_called": result.provider_called,
        "recommendation": result.recommendation,
        "cannot_override": list(result.cannot_override),
        "request": {
            "layer": request.layer.value,
            "intent": request.intent,
            "tool_category": request.tool_category.value,
            "risk_level": request.risk_level.value,
            "confidence": request.confidence,
            "escalation_required": request.escalation_required,
            "escalation_reason": request.escalation_reason,
            "recalled_context": list(request.recalled_context),
            "local_decision": request.local_decision,
            "allowed_outputs": list(request.allowed_outputs),
            "forbidden_actions": list(request.forbidden_actions),
        },
    }


def _require_non_empty_strings(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    normalized = tuple(value.strip() for value in values if value and value.strip())
    if not normalized:
        raise ValueError(f"{field_name} must contain at least one non-empty string")
    return normalized
