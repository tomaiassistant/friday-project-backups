"""Tests for the Brain Model local web test interface."""

import json
import threading
from urllib.error import HTTPError
from urllib.parse import parse_qs
from urllib.request import Request, urlopen

from budget_jarvis_core.web import (
    build_brain_loop_payload,
    build_server,
    render_index_html,
)


def test_render_index_html_contains_test_form_and_api_hint() -> None:
    html = render_index_html()

    assert "Brain Model Test Lab" in html
    assert "name=\"transcript\"" in html
    assert "name=\"context\"" in html
    assert "Queue safe complex work" in html
    assert "POST /api/brain-loop" in html
    assert "parseJsonResponse(await response.text())" in html
    assert "raw_response_start" in html


def test_build_brain_loop_payload_runs_safe_loop_with_context() -> None:
    form = parse_qs(
        "transcript=summarize+Brain+Model+progress"
        "&context=Task+0005+is+in+progress%0AQueue+store+exists"
        "&queue_complex=on"
    )

    payload = build_brain_loop_payload(form)

    assert payload["ok"] is True
    assert payload["brain_loop"]["state"] == "thinking"
    assert payload["brain_loop"]["recalled_context"] == [
        "Task 0005 is in progress",
        "Queue store exists",
    ]
    assert payload["brain_loop"]["queued_task"] is not None
    assert payload["brain_loop"]["confirmation_required"] is False


def test_build_brain_loop_payload_blocks_high_risk_actions() -> None:
    form = parse_qs("transcript=send+email+to+the+client&queue_complex=on")

    payload = build_brain_loop_payload(form)

    assert payload["ok"] is True
    assert payload["brain_loop"]["blocked"] is True
    assert payload["brain_loop"]["queued_task"] is None
    assert payload["brain_loop"]["confirmation_required"] is True


def test_build_brain_loop_payload_reports_empty_transcript_error() -> None:
    payload = build_brain_loop_payload(parse_qs("transcript=+"))

    assert payload["ok"] is False
    assert payload["error"] == "transcript must not be empty"


def test_build_server_returns_http_server_bound_to_requested_host() -> None:
    server = build_server("127.0.0.1", 0, access_token="secret")
    try:
        host, port = server.server_address
        assert host == "127.0.0.1"
        assert port > 0
        assert server.RequestHandlerClass is not None
        assert server.access_token == "secret"
    finally:
        server.server_close()


def test_payload_is_json_serializable() -> None:
    payload = build_brain_loop_payload(parse_qs("transcript=summarize+progress"))

    encoded = json.dumps(payload, sort_keys=True)

    assert "summarize progress" in encoded


def test_http_server_serves_page_and_urlencoded_api() -> None:
    server = build_server("127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        with urlopen(base_url, timeout=5) as response:
            html = response.read().decode("utf-8")
        assert "Brain Model Test Lab" in html

        request = Request(
            f"{base_url}/api/brain-loop",
            data=b"transcript=summarize+Brain+Model+progress&queue_complex=on",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert payload["ok"] is True
        assert payload["brain_loop"]["route"]["intent"] == "summarize Brain Model progress"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_http_server_returns_400_for_empty_transcript() -> None:
    server = build_server("127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = Request(
            f"http://127.0.0.1:{server.server_address[1]}/api/brain-loop",
            data=b"transcript=",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        try:
            urlopen(request, timeout=5)
        except HTTPError as exc:
            payload = json.loads(exc.read().decode("utf-8"))
            assert exc.code == 400
            assert payload["ok"] is False
            assert payload["error"] == "transcript must not be empty"
        else:  # pragma: no cover - defensive assertion branch
            raise AssertionError("expected HTTP 400")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_http_server_requires_token_when_configured() -> None:
    server = build_server("127.0.0.1", 0, access_token="secret-token")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        try:
            urlopen(base_url, timeout=5)
        except HTTPError as exc:
            payload = json.loads(exc.read().decode("utf-8"))
            assert exc.code == 401
            assert payload["error"] == "unauthorized"
        else:  # pragma: no cover - defensive assertion branch
            raise AssertionError("expected HTTP 401")

        with urlopen(f"{base_url}/?token=secret-token", timeout=5) as response:
            html = response.read().decode("utf-8")
        assert "Brain Model Test Lab" in html

        request = Request(
            f"{base_url}/api/brain-loop",
            data=b"transcript=summarize+Brain+Model+progress",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Brain-Model-Token": "secret-token",
            },
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert payload["ok"] is True
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
