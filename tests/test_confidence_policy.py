from dataclasses import dataclass

from budget_jarvis_core import JarvisState, TaskQueue, run_brain_loop
from budget_jarvis_core.router import ToolCategory


@dataclass(frozen=True)
class ConfidenceScenario:
    name: str
    transcript: str
    context: tuple[str, ...]
    queue_complex: bool
    expected_category: ToolCategory
    expected_confidence: float
    expected_blocked: bool
    expected_escalation: bool
    expected_confirmation: bool
    expected_queue: bool
    expected_writeback: bool
    expected_state: JarvisState


SCENARIOS = (
    ConfidenceScenario(
        name="grounded low-risk project recall",
        transcript="summarize Brain Model progress from the project files",
        context=("Task 0005 is in progress", "Latest suite result: 120 tests passed"),
        queue_complex=False,
        expected_category=ToolCategory.PROJECT_FILES,
        expected_confidence=0.85,
        expected_blocked=False,
        expected_escalation=False,
        expected_confirmation=False,
        expected_queue=False,
        expected_writeback=True,
        expected_state=JarvisState.THINKING,
    ),
    ConfidenceScenario(
        name="medium-risk local edit can queue but stays non-executing",
        transcript="edit the Brain Model task file with today's confidence policy progress",
        context=(),
        queue_complex=True,
        expected_category=ToolCategory.PROJECT_FILES,
        expected_confidence=0.65,
        expected_blocked=False,
        expected_escalation=False,
        expected_confirmation=False,
        expected_queue=True,
        expected_writeback=True,
        expected_state=JarvisState.THINKING,
    ),
    ConfidenceScenario(
        name="ambiguous unknown route blocks for review",
        transcript="please handle the vague thing",
        context=(),
        queue_complex=True,
        expected_category=ToolCategory.UNKNOWN,
        expected_confidence=0.25,
        expected_blocked=True,
        expected_escalation=True,
        expected_confirmation=False,
        expected_queue=False,
        expected_writeback=False,
        expected_state=JarvisState.WAITING_FOR_CONFIRMATION,
    ),
    ConfidenceScenario(
        name="recalled context does not rescue unknown route",
        transcript="please handle the vague thing",
        context=("Brain Model task 0005 is in progress",),
        queue_complex=True,
        expected_category=ToolCategory.UNKNOWN,
        expected_confidence=0.25,
        expected_blocked=True,
        expected_escalation=True,
        expected_confirmation=False,
        expected_queue=False,
        expected_writeback=False,
        expected_state=JarvisState.WAITING_FOR_CONFIRMATION,
    ),
    ConfidenceScenario(
        name="conflicting high-risk communication stays blocked",
        transcript="draft a Telegram reply and send message to him with the project memory",
        context=("Only draft communication without sending as Shadhin",),
        queue_complex=True,
        expected_category=ToolCategory.COMMUNICATION,
        expected_confidence=0.80,
        expected_blocked=True,
        expected_escalation=False,
        expected_confirmation=True,
        expected_queue=False,
        expected_writeback=False,
        expected_state=JarvisState.WAITING_FOR_CONFIRMATION,
    ),
)


def test_confidence_policy_scenarios(tmp_path):
    for index, scenario in enumerate(SCENARIOS, start=1):
        queue = TaskQueue(id_factory=lambda index=index: f"scenario-{index:04d}")
        result = run_brain_loop(
            scenario.transcript,
            recalled_context=scenario.context,
            queue=queue,
            queue_complex=scenario.queue_complex,
            project_path=tmp_path,
            write_reflection=True,
            date=f"2026-06-{index:02d}",
        )

        assert result.route.tool_category is scenario.expected_category, scenario.name
        assert result.confidence == scenario.expected_confidence, scenario.name
        assert result.blocked is scenario.expected_blocked, scenario.name
        assert result.escalation_required is scenario.expected_escalation, scenario.name
        assert result.confirmation_required is scenario.expected_confirmation, scenario.name
        assert result.state is scenario.expected_state, scenario.name
        assert (result.queued_task is not None) is scenario.expected_queue, scenario.name
        assert (result.writeback_path is not None) is scenario.expected_writeback, scenario.name
        assert bool(queue.list_tasks()) is scenario.expected_queue, scenario.name

        if scenario.expected_blocked:
            assert "Blocked before action" in result.planned_action, scenario.name
            assert "status: blocked_pending_confirmation" in result.reflection, scenario.name
        else:
            assert "status: planned_non_executing" in result.reflection, scenario.name
