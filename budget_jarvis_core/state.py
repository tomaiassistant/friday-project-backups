"""State machine primitives for the Budget Jarvis assistant loop."""

from enum import StrEnum


class JarvisState(StrEnum):
    """Explicit runtime states for the assistant."""

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    TOOL_RUNNING = "tool_running"
    WAITING_FOR_CONFIRMATION = "waiting_for_confirmation"
    ERROR = "error"


_NON_LISTENING_STATES = {
    JarvisState.SPEAKING,
    JarvisState.TOOL_RUNNING,
    JarvisState.WAITING_FOR_CONFIRMATION,
}


def can_listen(state: JarvisState | str) -> bool:
    """Return whether mic/listening ingestion is safe in the given state.

    Budget Jarvis must not listen while speaking, while a tool is running, or
    while waiting for explicit confirmation. Strings are accepted so callers can
    pass persisted or UI state values directly.
    """

    normalized = JarvisState(state)
    return normalized not in _NON_LISTENING_STATES
