"""Transcript-to-tool routing for Budget Jarvis.

The router is intentionally conservative in v0.1: it does not execute tools.
It classifies the requested action, selects a broad tool category, and carries
risk/confirmation metadata forward for the future brain loop.
"""

from dataclasses import dataclass
from enum import StrEnum

from .risk import RiskLevel, classify_risk


class ToolCategory(StrEnum):
    """Initial safe tool categories for Budget Jarvis routing."""

    PROJECT_FILES = "project_files"
    MEMORY = "memory"
    OPENCLAW = "openclaw"
    WINDOWS_WORKER = "windows_worker"
    BROWSER = "browser"
    SCHEDULE = "schedule"
    RESEARCH = "research"
    COMMUNICATION = "communication"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ActionRoute:
    """A non-executing route decision for one transcript or command."""

    intent: str
    tool_category: ToolCategory
    risk_level: RiskLevel
    requires_confirmation: bool
    reason: str
    next_action: str


_ROUTE_KEYWORDS: tuple[tuple[ToolCategory, tuple[str, ...], str], ...] = (
    (
        ToolCategory.COMMUNICATION,
        (
            "email",
            "send mail",
            "message",
            "whatsapp",
            "telegram",
            "public post",
            "post publicly",
            "tweet",
            "reply to",
        ),
        "communication keyword detected",
    ),
    (
        ToolCategory.OPENCLAW,
        ("openclaw", "jerry", "partner agent", "other agent", "agent handoff"),
        "OpenClaw/Jerry coordination keyword detected",
    ),
    (
        ToolCategory.SCHEDULE,
        ("schedule", "cron", "remind", "reminder", "tomorrow", "at 8", "8 am"),
        "scheduling keyword detected",
    ),
    (
        ToolCategory.WINDOWS_WORKER,
        (
            "windows",
            "pc",
            "screen",
            "mouse",
            "keyboard",
            "click",
            "desktop",
            "app",
        ),
        "Windows worker / PC-control keyword detected",
    ),
    (
        ToolCategory.BROWSER,
        ("browser", "website", "web page", "open url", "login page", "chrome"),
        "browser automation keyword detected",
    ),
    (
        ToolCategory.RESEARCH,
        ("research", "search web", "web research", "github", "study", "investigate"),
        "research keyword detected",
    ),
    (
        ToolCategory.MEMORY,
        ("memory", "remember", "recall", "learn", "lesson", "project memory"),
        "memory keyword detected",
    ),
    (
        ToolCategory.PROJECT_FILES,
        (
            "project file",
            "task file",
            "spec",
            "decision",
            "log",
            "readme",
            "roadmap",
            "write file",
            "edit",
            "commit",
            "push",
            "brain model project",
            "brain model",
        ),
        "project-file keyword detected",
    ),
)


def _normalize(transcript: str) -> str:
    return f" {transcript.strip().lower()} "


def _select_category(normalized: str) -> tuple[ToolCategory, str]:
    for category, keywords, reason in _ROUTE_KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            return category, reason
    return ToolCategory.UNKNOWN, "no route keyword detected"


def _next_action_for(category: ToolCategory, requires_confirmation: bool) -> str:
    if requires_confirmation:
        return "ask Shadhin for confirmation before taking any external or risky action"

    next_actions = {
        ToolCategory.PROJECT_FILES: "read or update approved Brain Model project files, then log the result",
        ToolCategory.MEMORY: "retrieve or write approved project memory with citations",
        ToolCategory.OPENCLAW: "prepare a concise coordination request or handoff for Jerry/OpenClaw",
        ToolCategory.WINDOWS_WORKER: "prepare a dry-run Windows worker plan; do not control the PC yet",
        ToolCategory.BROWSER: "prepare a browser/research plan; do not submit forms or credentials",
        ToolCategory.SCHEDULE: "create or update an approved task/schedule record when authorized",
        ToolCategory.RESEARCH: "perform approved research and save cited notes into the project folder",
        ToolCategory.COMMUNICATION: "draft communication only; do not send as Shadhin without confirmation",
        ToolCategory.UNKNOWN: "ask for clarification or route to planning before executing tools",
    }
    return next_actions[category]


def route_transcript(transcript: str) -> ActionRoute:
    """Route a transcript into a safe, non-executing action decision.

    The router always calls ``classify_risk`` first. High-risk decisions keep
    ``requires_confirmation=True`` regardless of the selected tool category.
    """

    intent = transcript.strip()
    normalized = _normalize(transcript)
    risk = classify_risk(transcript)
    category, route_reason = _select_category(normalized)
    reason = f"{route_reason}; risk: {risk.reason}"

    return ActionRoute(
        intent=intent,
        tool_category=category,
        risk_level=risk.level,
        requires_confirmation=risk.requires_confirmation,
        reason=reason,
        next_action=_next_action_for(category, risk.requires_confirmation),
    )
