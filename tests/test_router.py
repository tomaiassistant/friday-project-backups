"""Tests for Budget Jarvis transcript routing."""

import pytest

from budget_jarvis_core.risk import RiskLevel
from budget_jarvis_core.router import ActionRoute, ToolCategory, route_transcript


def test_route_transcript_returns_action_route_for_low_risk_command() -> None:
    route = route_transcript("summarize the Brain Model project file status")

    assert isinstance(route, ActionRoute)
    assert route.intent == "summarize the Brain Model project file status"
    assert route.tool_category is ToolCategory.PROJECT_FILES
    assert route.risk_level is RiskLevel.LOW
    assert route.requires_confirmation is False
    assert route.reason
    assert "project" in route.next_action.lower()


@pytest.mark.parametrize(
    ("transcript", "expected_category"),
    [
        ("update the Brain Model task file", ToolCategory.PROJECT_FILES),
        ("remember this lesson in project memory", ToolCategory.MEMORY),
        ("ask Jerry through OpenClaw for a quick review", ToolCategory.OPENCLAW),
        ("click the Windows app button on my PC", ToolCategory.WINDOWS_WORKER),
        ("open the browser and inspect the website", ToolCategory.BROWSER),
        ("schedule a reminder for tomorrow at 8 AM", ToolCategory.SCHEDULE),
        ("research the GitHub repo and summarize findings", ToolCategory.RESEARCH),
        ("draft a WhatsApp message to him", ToolCategory.COMMUNICATION),
        ("what should we do next", ToolCategory.UNKNOWN),
    ],
)
def test_route_transcript_keyword_categories(
    transcript: str, expected_category: ToolCategory
) -> None:
    route = route_transcript(transcript)

    assert route.tool_category is expected_category
    assert route.reason
    assert route.next_action


def test_route_transcript_uses_risk_classifier_for_medium_risk() -> None:
    route = route_transcript("edit the project file and commit the private repo")

    assert route.tool_category is ToolCategory.PROJECT_FILES
    assert route.risk_level is RiskLevel.MEDIUM
    assert route.requires_confirmation is False
    assert "private repository" in route.reason


@pytest.mark.parametrize(
    "transcript",
    [
        "send email to the client with the update",
        "delete the task file after reading it",
        "post publicly from my account",
        "send message on WhatsApp as me",
    ],
)
def test_high_risk_routes_preserve_confirmation_requirement(transcript: str) -> None:
    route = route_transcript(transcript)

    assert route.risk_level is RiskLevel.HIGH
    assert route.requires_confirmation is True
    assert "confirmation" in route.next_action.lower()


def test_unknown_route_stays_non_executing() -> None:
    route = route_transcript("what should we do next")

    assert route.tool_category is ToolCategory.UNKNOWN
    assert route.risk_level is RiskLevel.LOW
    assert route.requires_confirmation is False
    assert "planning" in route.next_action
