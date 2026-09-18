"""Local web test interface for the Brain Model prototype.

The interface is intentionally local and non-executing. It lets Shadhin submit a
transcript, optional recalled context, and a queue toggle, then inspect the same
safe brain-loop JSON returned by the CLI.
"""

from __future__ import annotations

import argparse
import html
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Mapping, Sequence
from urllib.parse import parse_qs, urlparse

from .brain_loop import run_brain_loop
from .cli import brain_loop_to_dict
from .task_queue import TaskQueue

FormData = Mapping[str, Sequence[str]]


def render_index_html() -> str:
    """Return the single-page Brain Model test UI."""

    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Brain Model Test Lab</title>
  <style>
    :root { color-scheme: dark; --bg: #0f172a; --panel: #111827; --muted: #94a3b8; --text: #e5e7eb; --accent: #38bdf8; --warn: #fbbf24; --ok: #34d399; --bad: #fb7185; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top left, #1e3a8a 0, transparent 30%), var(--bg); color: var(--text); }
    main { max-width: 1100px; margin: 0 auto; padding: 32px 18px 48px; }
    .hero { margin-bottom: 22px; }
    h1 { margin: 0 0 8px; font-size: clamp(32px, 5vw, 56px); letter-spacing: -0.05em; }
    .subtitle { color: var(--muted); max-width: 760px; line-height: 1.6; }
    .grid { display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 18px; align-items: start; }
    .card { background: color-mix(in srgb, var(--panel) 92%, transparent); border: 1px solid rgba(148, 163, 184, 0.22); border-radius: 18px; padding: 18px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.24); }
    label { display: block; font-weight: 700; margin: 14px 0 8px; }
    textarea, input[type=text] { width: 100%; border: 1px solid rgba(148, 163, 184, 0.28); border-radius: 14px; padding: 12px; background: #020617; color: var(--text); font: inherit; }
    textarea { min-height: 140px; resize: vertical; }
    .context { min-height: 110px; }
    .row { display: flex; align-items: center; gap: 10px; margin: 14px 0; color: var(--muted); }
    button { cursor: pointer; border: 0; border-radius: 999px; padding: 12px 18px; color: #00111f; background: linear-gradient(135deg, var(--accent), var(--ok)); font-weight: 800; font-size: 15px; }
    button:disabled { opacity: 0.55; cursor: wait; }
    .hint { color: var(--muted); font-size: 14px; line-height: 1.5; }
    .result-head { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }
    .pill { border-radius: 999px; padding: 6px 10px; font-size: 13px; font-weight: 800; background: rgba(148, 163, 184, 0.15); }
    .pill.ok { color: var(--ok); }
    .pill.warn { color: var(--warn); }
    .pill.bad { color: var(--bad); }
    pre { overflow: auto; margin: 0; padding: 14px; border-radius: 14px; background: #020617; border: 1px solid rgba(148, 163, 184, 0.18); color: #d1fae5; min-height: 360px; white-space: pre-wrap; }
    .examples { display: grid; gap: 8px; margin-top: 12px; }
    .example { text-align: left; width: 100%; background: rgba(56, 189, 248, 0.12); color: var(--text); border: 1px solid rgba(56, 189, 248, 0.2); }
    code { color: #bae6fd; }
    @media (max-width: 820px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>Brain Model Test Lab</h1>
      <p class="subtitle">Run the current non-executing Brain Model loop from your browser. It routes a transcript, applies safety/risk checks, optionally queues safe complex work in memory, and shows the full JSON result.</p>
    </section>
    <section class="grid">
      <form id="brain-form" class="card">
        <label for="transcript">Transcript / command</label>
        <textarea id="transcript" name="transcript" placeholder="Example: summarize Brain Model progress" required>summarize Brain Model progress</textarea>

        <label for="context">Recalled context, one item per line</label>
        <textarea id="context" class="context" name="context" placeholder="Task 0005 is in progress&#10;Queue store exists"></textarea>

        <div class="row">
          <input id="queue_complex" name="queue_complex" type="checkbox">
          <label for="queue_complex" style="margin:0">Queue safe complex work</label>
        </div>
        <button id="submit" type="submit">Run brain loop</button>
        <p class="hint">API endpoint: <code>POST /api/brain-loop</code>. This UI does not execute external tools, send messages, or write files.</p>
        <div class="examples">
          <button class="example" type="button" data-example="edit the Brain Model task file">Safe queued project work</button>
          <button class="example" type="button" data-example="send email to the client with the update">High-risk confirmation block</button>
        </div>
      </form>
      <section class="card">
        <div class="result-head">
          <span id="status-pill" class="pill">waiting</span>
          <span id="risk-pill" class="pill">risk: n/a</span>
          <span id="confirm-pill" class="pill">confirmation: n/a</span>
        </div>
        <pre id="result">Submit a transcript to see Brain Model JSON here.</pre>
      </section>
    </section>
  </main>
  <script>
    const form = document.getElementById('brain-form');
    const submit = document.getElementById('submit');
    const result = document.getElementById('result');
    const statusPill = document.getElementById('status-pill');
    const riskPill = document.getElementById('risk-pill');
    const confirmPill = document.getElementById('confirm-pill');

    function setPills(payload) {
      const loop = payload.brain_loop || {};
      const route = loop.route || {};
      statusPill.textContent = payload.ok ? `state: ${loop.state || 'unknown'}` : 'error';
      statusPill.className = `pill ${payload.ok ? 'ok' : 'bad'}`;
      riskPill.textContent = `risk: ${route.risk_level || 'n/a'}`;
      riskPill.className = `pill ${route.risk_level === 'high' ? 'bad' : route.risk_level === 'medium' ? 'warn' : 'ok'}`;
      confirmPill.textContent = `confirmation: ${loop.confirmation_required ? 'yes' : 'no'}`;
      confirmPill.className = `pill ${loop.confirmation_required ? 'warn' : 'ok'}`;
    }

    function parseJsonResponse(text) {
      try {
        return JSON.parse(text);
      } catch (error) {
        // Some public tunnels/proxies can prepend a short status token before
        // the JSON body. Keep the UI usable by recovering the first JSON
        // object, while still exposing the raw response when parsing fails.
        const firstObject = text.indexOf('{');
        const lastObject = text.lastIndexOf('}');
        if (firstObject !== -1 && lastObject > firstObject) {
          try {
            return JSON.parse(text.slice(firstObject, lastObject + 1));
          } catch (_) {
            // Fall through to a clear diagnostic payload below.
          }
        }
        return {
          ok: false,
          error: String(error),
          raw_response_start: text.slice(0, 500)
        };
      }
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      submit.disabled = true;
      result.textContent = 'Thinking...';
      try {
        const response = await fetch('/api/brain-loop', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            ...(new URLSearchParams(window.location.search).get('token') ? { 'X-Brain-Model-Token': new URLSearchParams(window.location.search).get('token') } : {})
          },
          body: new URLSearchParams(new FormData(form))
        });
        const payload = parseJsonResponse(await response.text());
        if (!response.ok && payload.ok !== false) {
          payload.ok = false;
          payload.http_status = response.status;
        }
        setPills(payload);
        result.textContent = JSON.stringify(payload, null, 2);
      } catch (error) {
        const payload = { ok: false, error: String(error) };
        setPills(payload);
        result.textContent = JSON.stringify(payload, null, 2);
      } finally {
        submit.disabled = false;
      }
    });

    for (const button of document.querySelectorAll('[data-example]')) {
      button.addEventListener('click', () => {
        document.getElementById('transcript').value = button.dataset.example;
      });
    }
  </script>
</body>
</html>"""


def _first_value(form: FormData, key: str) -> str:
    values = form.get(key, [])
    return values[0] if values else ""


def _context_lines(raw_context: str) -> list[str]:
    return [line.strip() for line in raw_context.splitlines() if line.strip()]


def build_brain_loop_payload(form: FormData) -> dict[str, Any]:
    """Build a JSON-safe brain-loop payload from parsed form data."""

    transcript = _first_value(form, "transcript")
    context = _context_lines(_first_value(form, "context"))
    queue_complex = bool(form.get("queue_complex"))

    try:
        result = run_brain_loop(
            transcript,
            recalled_context=context,
            queue=TaskQueue() if queue_complex else None,
            queue_complex=queue_complex,
        )
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}

    return {"ok": True, "brain_loop": brain_loop_to_dict(result)}


class BrainModelRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler for the local single-page Brain Model test UI."""

    server_version = "BrainModelTestLab/0.1"

    def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
        if not self._is_authorized():
            self._send_json({"ok": False, "error": "unauthorized"}, status=401)
            return
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            self._send_html(render_index_html())
            return
        self._send_json({"ok": False, "error": "not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802 - stdlib hook name
        if not self._is_authorized():
            self._send_json({"ok": False, "error": "unauthorized"}, status=401)
            return
        if urlparse(self.path).path != "/api/brain-loop":
            self._send_json({"ok": False, "error": "not found"}, status=404)
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length).decode("utf-8")
        content_type = self.headers.get("Content-Type", "")
        if content_type.startswith("multipart/form-data"):
            payload = {"ok": False, "error": "multipart form uploads are not supported; send URL-encoded form data"}
        else:
            payload = build_brain_loop_payload(parse_qs(body, keep_blank_values=True))
        status = 200 if payload.get("ok") else 400
        self._send_json(payload, status=status)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - stdlib signature
        """Silence default request logging for cleaner terminal output."""

    def _is_authorized(self) -> bool:
        token = getattr(self.server, "access_token", None)
        if not token:
            return True
        header_token = self.headers.get("X-Brain-Model-Token", "")
        query_token = _first_value(parse_qs(urlparse(self.path).query), "token")
        return header_token == token or query_token == token

    def _send_html(self, html_text: str, *, status: int = 200) -> None:
        encoded = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, payload: dict[str, Any], *, status: int = 200) -> None:
        encoded = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def build_server(host: str = "127.0.0.1", port: int = 8787, access_token: str | None = None) -> ThreadingHTTPServer:
    """Return a configured local Brain Model web server."""

    server = ThreadingHTTPServer((host, port), BrainModelRequestHandler)
    server.access_token = access_token
    return server


def main(argv: Sequence[str] | None = None) -> int:
    """Run the local Brain Model web test server."""

    parser = argparse.ArgumentParser(description="Run the local Brain Model web test interface.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind. Use 0.0.0.0 only on trusted networks.")
    parser.add_argument("--port", type=int, default=8787, help="Port to bind.")
    parser.add_argument("--access-token", default=os.environ.get("BRAIN_MODEL_WEB_TOKEN"), help="Optional access token for public tunnels.")
    args = parser.parse_args(argv)

    server = build_server(args.host, args.port, access_token=args.access_token)
    url_host = "localhost" if args.host in {"127.0.0.1", "0.0.0.0"} else args.host
    suffix = f"?token={html.escape(args.access_token)}" if args.access_token else ""
    print(f"Brain Model Test Lab running at http://{html.escape(url_host)}:{server.server_address[1]}{suffix}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Brain Model Test Lab.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
