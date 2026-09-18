from datetime import date

import pytest

from budget_jarvis_core import BrainLoopResult, JarvisState, TaskQueue, run_brain_loop
from budget_jarvis_core.router import ToolCategory


def test_low_risk_loop_returns_structured_non_executing_plan():
    result = run_brain_loop(
        "summarize Brain Model progress",
        recalled_context=["Task 0005 is in progress", "  ", "Docs complete"],
    )

    assert isinstance(result, BrainLoopResult)
    assert result.transcript == "summarize Brain Model progress"
    assert result.state is JarvisState.THINKING
    assert result.route.tool_category is ToolCategory.PROJECT_FILES
    assert result.confirmation_required is False
    assert result.blocked is False
    assert result.recalled_context == ("Task 0005 is in progress", "Docs complete")
    assert "Prepare a low-risk suggested action only" in result.planned_action
    assert result.queued_task is None
    assert result.writeback_path is None
    assert result.confidence == 0.85
    assert result.escalation_required is False
    assert result.escalation_reason is None
    assert "status: planned_non_executing" in result.reflection
    assert "confidence: 0.85" in result.reflection


def test_empty_transcript_is_rejected():
    with pytest.raises(ValueError, match="transcript must not be empty"):
        run_brain_loop("   ")


def test_high_risk_loop_blocks_without_queue_or_writeback(tmp_path):
    queue = TaskQueue(id_factory=lambda: "task-9999")

    result = run_brain_loop(
        "delete the project files and send message to him",
        queue=queue,
        queue_complex=True,
        project_path=tmp_path,
        write_reflection=True,
        date=date(2026, 5, 29),
    )

    assert result.state is JarvisState.WAITING_FOR_CONFIRMATION
    assert result.confirmation_required is True
    assert result.blocked is True
    assert result.queued_task is None
    assert result.writeback_path is None
    assert queue.list_tasks() == []
    assert not (tmp_path / "shared" / "logs" / "2026-05-29.md").exists()
    assert "Blocked before action" in result.planned_action
    assert "status: blocked_pending_confirmation" in result.reflection
    assert result.confidence == 0.70
    assert result.escalation_required is False


def test_safe_complex_loop_can_queue_task():
    queue = TaskQueue(id_factory=lambda: "task-0001")

    result = run_brain_loop(
        "edit the Brain Model task file with today's progress",
        queue=queue,
        queue_complex=True,
    )

    assert result.route.risk_level.value == "medium"
    assert result.queued_task is not None
    assert result.queued_task.id == "task-0001"
    assert result.queued_task.metadata == {
        "transcript": "edit the Brain Model task file with today's progress",
        "tool_category": "project_files",
        "risk_level": "medium",
        "requires_confirmation": False,
    }
    assert queue.get("task-0001") == result.queued_task
    assert "queued_task: task-0001" in result.reflection
    assert result.confidence == 0.65
    assert result.escalation_required is False


def test_unknown_route_escalates_without_queue_or_writeback(tmp_path):
    queue = TaskQueue(id_factory=lambda: "task-0002")

    result = run_brain_loop(
        "please handle the vague thing",
        queue=queue,
        queue_complex=True,
        project_path=tmp_path,
        write_reflection=True,
        date="2026-06-01",
    )

    assert result.route.tool_category is ToolCategory.UNKNOWN
    assert result.state is JarvisState.WAITING_FOR_CONFIRMATION
    assert result.confidence == 0.25
    assert result.escalation_required is True
    assert result.escalation_reason is not None
    assert "unknown route" in result.escalation_reason
    assert result.blocked is True
    assert result.queued_task is None
    assert result.writeback_path is None
    assert queue.list_tasks() == []
    assert "Blocked before action" in result.planned_action
    assert "status: blocked_pending_confirmation" in result.reflection
    assert "escalation_required: True" in result.reflection
    assert not (tmp_path / "shared" / "logs" / "2026-06-01.md").exists()


def test_write_reflection_requires_project_path():
    with pytest.raises(ValueError, match="project_path is required"):
        run_brain_loop("summarize Brain Model progress", write_reflection=True)


def test_safe_loop_can_append_daily_log_reflection(tmp_path):
    result = run_brain_loop(
        "summarize Brain Model progress",
        project_path=tmp_path,
        write_reflection=True,
        date="2026-05-29",
    )

    expected_path = tmp_path / "shared" / "logs" / "2026-05-29.md"
    assert result.writeback_path == expected_path
    content = expected_path.read_text(encoding="utf-8")
    assert "# 2026-05-29" in content
    assert "## Budget Jarvis Memory Bridge" in content
    assert "status: planned_non_executing" in content
    assert "transcript: summarize Brain Model progress" in content
