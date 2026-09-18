"""Tests for Budget Jarvis state primitives."""

import pytest

from budget_jarvis_core.state import JarvisState, can_listen


def test_all_expected_states_exist() -> None:
    assert {state.value for state in JarvisState} == {
        "idle",
        "listening",
        "thinking",
        "speaking",
        "tool_running",
        "waiting_for_confirmation",
        "error",
    }


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (JarvisState.IDLE, True),
        (JarvisState.LISTENING, True),
        (JarvisState.THINKING, True),
        (JarvisState.ERROR, True),
        (JarvisState.SPEAKING, False),
        (JarvisState.TOOL_RUNNING, False),
        (JarvisState.WAITING_FOR_CONFIRMATION, False),
        ("speaking", False),
    ],
)
def test_can_listen_rules(state: JarvisState | str, expected: bool) -> None:
    assert can_listen(state) is expected


def test_can_listen_rejects_unknown_state() -> None:
    with pytest.raises(ValueError):
        can_listen("unknown")
