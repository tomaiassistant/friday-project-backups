"""Tests for Budget Jarvis risk classification."""

import pytest

from budget_jarvis_core.risk import RiskDecision, RiskLevel, classify_risk


@pytest.mark.parametrize(
    ("command", "expected_level", "requires_confirmation"),
    [
        ("read the Brain Model project status", RiskLevel.LOW, False),
        ("summarize the latest Jerry update", RiskLevel.LOW, False),
        ("draft a new memory architecture spec", RiskLevel.LOW, False),
        ("create note about today's idea", RiskLevel.LOW, False),
        ("edit the project task file", RiskLevel.MEDIUM, False),
        ("commit and push the private repo", RiskLevel.MEDIUM, False),
        ("run command pytest for safe local tests", RiskLevel.MEDIUM, False),
        ("send email to the client", RiskLevel.HIGH, True),
        ("delete important files from the project", RiskLevel.HIGH, True),
        ("post publicly from my account", RiskLevel.HIGH, True),
        ("handle the API key and password", RiskLevel.HIGH, True),
        ("make a payment from my bank", RiskLevel.HIGH, True),
        ("send message on WhatsApp as me", RiskLevel.HIGH, True),
    ],
)
def test_classify_risk_examples(
    command: str, expected_level: RiskLevel, requires_confirmation: bool
) -> None:
    decision = classify_risk(command)

    assert isinstance(decision, RiskDecision)
    assert decision.level is expected_level
    assert decision.requires_confirmation is requires_confirmation
    assert decision.reason


def test_high_risk_wins_over_medium_terms() -> None:
    decision = classify_risk("edit the file then delete the original")

    assert decision.level is RiskLevel.HIGH
    assert decision.requires_confirmation is True
    assert "delete" in decision.matched_terms


def test_unknown_command_defaults_to_low_risk() -> None:
    decision = classify_risk("what should we do next")

    assert decision.level is RiskLevel.LOW
    assert decision.requires_confirmation is False
