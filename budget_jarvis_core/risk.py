"""Risk classification for Budget Jarvis commands before tool routing."""

from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    """Safety level for an intended action."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class RiskDecision:
    """Result of classifying a transcript or command."""

    level: RiskLevel
    requires_confirmation: bool
    reason: str
    matched_terms: tuple[str, ...] = ()


_HIGH_RISK_TERMS = {
    "email": "outbound email or mailbox access can expose private data or act as Shadhin",
    "send mail": "outbound email can act as Shadhin",
    "public post": "public posting is externally visible",
    "post publicly": "public posting is externally visible",
    "tweet": "social posting is externally visible",
    "delete": "destructive file/action request",
    "remove file": "destructive file/action request",
    "payment": "payment/account action",
    "pay ": "payment/account action",
    "bank": "financial/account action",
    "credential": "credential handling",
    "password": "credential handling",
    "api key": "credential handling",
    "ssh key": "credential handling",
    "production server": "major infrastructure change",
    "infrastructure": "major infrastructure change",
    "message him": "messaging people as Shadhin",
    "message her": "messaging people as Shadhin",
    "send message": "messaging people as Shadhin",
    "whatsapp": "messaging people as Shadhin",
}

_MEDIUM_RISK_TERMS = {
    "edit": "local project file modification",
    "modify": "local project file modification",
    "update file": "local project file modification",
    "write file": "local project file modification",
    "commit": "private repository commit/push",
    "push": "private repository commit/push",
    "run command": "safe local command execution",
    "execute": "safe local command execution",
    "install": "local environment/package change",
    "create task": "project task writeback",
}

_LOW_RISK_TERMS = {
    "read": "read-only or summarization request",
    "summarize": "read-only or summarization request",
    "summary": "read-only or summarization request",
    "review": "read-only or review request",
    "inspect": "read-only inspection request",
    "create note": "local note/spec drafting",
    "draft": "local note/spec drafting",
    "spec": "local note/spec drafting",
    "plan": "planning request",
}


def _find_matches(text: str, terms: dict[str, str]) -> tuple[str, ...]:
    return tuple(term for term in terms if term in text)


def classify_risk(text: str) -> RiskDecision:
    """Classify a command into low, medium, or high risk.

    The first implementation is intentionally conservative and keyword-based.
    High-risk matches always require confirmation. Medium-risk actions are safe
    for already-authorized project work but still marked as non-low risk so the
    router can add review/logging.
    """

    normalized = f" {text.strip().lower()} "

    high_matches = _find_matches(normalized, _HIGH_RISK_TERMS)
    if high_matches:
        reasons = sorted({_HIGH_RISK_TERMS[term] for term in high_matches})
        return RiskDecision(
            level=RiskLevel.HIGH,
            requires_confirmation=True,
            reason="; ".join(reasons),
            matched_terms=high_matches,
        )

    medium_matches = _find_matches(normalized, _MEDIUM_RISK_TERMS)
    if medium_matches:
        reasons = sorted({_MEDIUM_RISK_TERMS[term] for term in medium_matches})
        return RiskDecision(
            level=RiskLevel.MEDIUM,
            requires_confirmation=False,
            reason="; ".join(reasons),
            matched_terms=medium_matches,
        )

    low_matches = _find_matches(normalized, _LOW_RISK_TERMS)
    if low_matches:
        reasons = sorted({_LOW_RISK_TERMS[term] for term in low_matches})
        return RiskDecision(
            level=RiskLevel.LOW,
            requires_confirmation=False,
            reason="; ".join(reasons),
            matched_terms=low_matches,
        )

    return RiskDecision(
        level=RiskLevel.LOW,
        requires_confirmation=False,
        reason="no risky action terms detected; treat as low-risk until routed",
        matched_terms=(),
    )
