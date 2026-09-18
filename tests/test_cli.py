"""Tests for the Budget Jarvis CLI prototype."""

import json

import pytest

from budget_jarvis_core.cli import brain_loop_to_dict, main, route_to_dict, run
from budget_jarvis_core import run_brain_loop
from budget_jarvis_core.router import ToolCategory, route_transcript


def test_route_to_dict_serializes_enum_values() -> None:
    route = route_transcript("summarize Brain Model progress")

    payload = route_to_dict(route)

    assert payload["tool_category"] == ToolCategory.PROJECT_FILES.value
    assert payload["risk_level"] == "low"
    assert payload["requires_confirmation"] is False


def test_brain_loop_to_dict_serializes_full_result() -> None:
    result = run_brain_loop(
        "summarize Brain Model progress",
        recalled_context=["Task 0005 is in progress"],
    )

    payload = brain_loop_to_dict(result)

    assert payload["state"] == "thinking"
    assert payload["route"]["tool_category"] == ToolCategory.PROJECT_FILES.value
    assert payload["recalled_context"] == ["Task 0005 is in progress"]
    assert payload["queued_task"] is None
    assert payload["writeback_path"] is None
    assert payload["confirmation_required"] is False
    assert payload["blocked"] is False
    assert payload["confidence"] == 0.85
    assert payload["escalation_required"] is False
    assert payload["escalation_reason"] is None


def test_run_returns_route_json_payload_without_writeback() -> None:
    payload = run(["summarize Brain Model progress"])

    assert payload["route"]["intent"] == "summarize Brain Model progress"
    assert payload["route"]["risk_level"] == "low"
    assert payload["confirmation_required"] is False
    assert payload["log"] == {
        "requested": False,
        "dry_run": True,
        "written": False,
        "path": None,
        "text": None,
    }


def test_run_can_return_full_brain_loop_payload() -> None:
    payload = run([
        "summarize Brain Model progress",
        "--brain-loop",
        "--context",
        "Task 0005 is in progress",
    ])

    assert payload["confirmation_required"] is False
    assert payload["escalation_required"] is False
    assert payload["brain_loop"]["state"] == "thinking"
    assert payload["brain_loop"]["route"]["tool_category"] == "project_files"
    assert payload["brain_loop"]["recalled_context"] == ["Task 0005 is in progress"]
    assert payload["brain_loop"]["blocked"] is False
    assert "log" not in payload


def test_brain_loop_can_add_project_recall_context(tmp_path) -> None:
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    (memory_dir / "PROJECT_MEMORY.md").write_text(
        "# Project Memory\n- Brain Model progress includes project recall wiring.\n",
        encoding="utf-8",
    )

    payload = run([
        "summarize Brain Model project recall progress",
        "--brain-loop",
        "--context",
        "Manual context stays first",
        "--recall-project",
        str(tmp_path),
        "--recall-max-items",
        "1",
    ])

    recalled_context = payload["brain_loop"]["recalled_context"]
    assert recalled_context[0] == "Manual context stays first"
    assert len(recalled_context) == 2
    assert recalled_context[1].startswith("memory/PROJECT_MEMORY.md:")
    assert "project recall wiring" in recalled_context[1]


def test_project_recall_requires_brain_loop(tmp_path) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["summarize Brain Model progress", "--recall-project", str(tmp_path)])

    assert exc_info.value.code == 2


def test_queue_store_requires_project_recall(tmp_path) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["summarize Brain Model progress", "--brain-loop", "--queue-store", str(tmp_path / "queue.json")])

    assert exc_info.value.code == 2


def test_brain_loop_payload_keeps_high_risk_block_visible() -> None:
    payload = run(["delete the project files and send message", "--brain-loop", "--queue-complex"])

    assert payload["confirmation_required"] is True
    assert payload["escalation_required"] is False
    assert payload["brain_loop"]["state"] == "waiting_for_confirmation"
    assert payload["brain_loop"]["blocked"] is True
    assert payload["brain_loop"]["queued_task"] is None
    assert "Blocked before action" in payload["brain_loop"]["planned_action"]


def test_brain_loop_payload_exposes_unknown_route_escalation() -> None:
    payload = run(["please handle the vague thing", "--brain-loop", "--queue-complex"])

    assert payload["confirmation_required"] is False
    assert payload["escalation_required"] is True
    assert payload["brain_loop"]["route"]["tool_category"] == "unknown"
    assert payload["brain_loop"]["confidence"] == 0.25
    assert payload["brain_loop"]["escalation_required"] is True
    assert "unknown route" in payload["brain_loop"]["escalation_reason"]
    assert payload["brain_loop"]["queued_task"] is None
    assert "Blocked before action" in payload["brain_loop"]["planned_action"]
    assert payload["brain_loop"]["blocked"] is True


def test_brain_loop_can_attach_advisory_provider_review_stub() -> None:
    payload = run(["please handle the vague thing", "--brain-loop", "--provider-review-stub"])

    review = payload["provider_review"]
    assert review["advisory_only"] is True
    assert review["provider_called"] is False
    assert review["request"]["layer"] == "review"
    assert review["request"]["tool_category"] == "unknown"
    assert review["request"]["escalation_required"] is True
    assert "execute_tools" in review["request"]["forbidden_actions"]
    assert "blocked" in review["cannot_override"]
    assert payload["brain_loop"]["blocked"] is True
    assert payload["brain_loop"]["queued_task"] is None


def test_provider_review_stub_requires_brain_loop() -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["summarize Brain Model progress", "--provider-review-stub"])

    assert exc_info.value.code == 2


def test_brain_loop_can_queue_safe_complex_work() -> None:
    payload = run(["edit the Brain Model task file", "--brain-loop", "--queue-complex"])

    queued_task = payload["brain_loop"]["queued_task"]
    assert queued_task is not None
    assert queued_task["status"] == "pending"
    assert queued_task["metadata"]["tool_category"] == "project_files"
    assert queued_task["metadata"]["requires_confirmation"] is False


def test_run_keeps_high_risk_confirmation_visible() -> None:
    payload = run(["send email to the client with the update"])

    assert payload["route"]["tool_category"] == "communication"
    assert payload["route"]["risk_level"] == "high"
    assert payload["route"]["requires_confirmation"] is True
    assert payload["confirmation_required"] is True
    assert "confirmation" in payload["route"]["next_action"]


def test_write_log_defaults_to_dry_run_and_does_not_create_file(tmp_path) -> None:
    payload = run([
        "update the Brain Model task file",
        "--write-log",
        "--project-path",
        str(tmp_path),
        "--log-date",
        "2026-05-26",
    ])

    assert payload["log"]["requested"] is True
    assert payload["log"]["dry_run"] is True
    assert payload["log"]["written"] is False
    assert payload["log"]["path"] is None
    assert not (tmp_path / "shared" / "logs" / "2026-05-26.md").exists()


def test_brain_loop_write_log_dry_run_returns_reflection_without_file(tmp_path) -> None:
    payload = run([
        "summarize Brain Model progress",
        "--brain-loop",
        "--write-log",
        "--project-path",
        str(tmp_path),
        "--log-date",
        "2026-05-29",
    ])

    assert payload["log"]["requested"] is True
    assert payload["log"]["dry_run"] is True
    assert payload["log"]["written"] is False
    assert "status: planned_non_executing" in payload["log"]["text"]
    assert not (tmp_path / "shared" / "logs" / "2026-05-29.md").exists()


def test_real_write_requires_project_path() -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["summarize Brain Model progress", "--write-log", "--real-write"])

    assert exc_info.value.code == 2


def test_real_write_appends_daily_log(tmp_path) -> None:
    payload = run([
        "summarize Brain Model progress",
        "--write-log",
        "--real-write",
        "--project-path",
        str(tmp_path),
        "--log-date",
        "2026-05-26",
        "--log-text",
        "CLI routed a transcript safely.",
    ])

    log_path = tmp_path / "shared" / "logs" / "2026-05-26.md"
    assert payload["log"]["requested"] is True
    assert payload["log"]["dry_run"] is False
    assert payload["log"]["written"] is True
    assert payload["log"]["path"] == str(log_path)
    assert "CLI routed a transcript safely." in log_path.read_text(encoding="utf-8")


def test_brain_loop_real_write_appends_reflection(tmp_path) -> None:
    payload = run([
        "summarize Brain Model progress",
        "--brain-loop",
        "--write-log",
        "--real-write",
        "--project-path",
        str(tmp_path),
        "--log-date",
        "2026-05-29",
    ])

    log_path = tmp_path / "shared" / "logs" / "2026-05-29.md"
    assert payload["brain_loop"]["writeback_path"] == str(log_path)
    assert "status: planned_non_executing" in log_path.read_text(encoding="utf-8")


def test_main_prints_valid_json(capsys) -> None:
    exit_code = main(["summarize Brain Model progress"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["route"]["intent"] == "summarize Brain Model progress"
    assert payload["confirmation_required"] is False
