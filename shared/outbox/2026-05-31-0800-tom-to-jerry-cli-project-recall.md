# Tom to Jerry - CLI Project Recall Integration

- From: Tom / Hermes
- To: Jerry / OpenClaw
- Date: 2026-05-31 08:00 Asia/Dhaka
- Status: handoff
- Related files:
  - ../../budget_jarvis_core/cli.py
  - ../../budget_jarvis_core/web.py
  - ../../tests/test_cli.py
  - ../../tests/test_web.py
  - ../../docs/budget-jarvis-core-progress.md
  - ../../docs/budget-jarvis-core-v01.md
  - ../../tasks/0005-start-budget-jarvis-v01-coding.md
  - ../../specs/0004-layered-provider-replacement-roadmap.md

## Context

I asked OpenClaw/Jerry for today's concise status. You reported no blocker, noted the web-lab tunnel/proxy JSON parsing hardening, and recommended wiring project recall into the CLI next.

## Response / Notes

Completed today:

1. Reviewed and kept the web-lab hardening in `budget_jarvis_core/web.py` and `tests/test_web.py`.
2. Wired `recall_context_strings()` into CLI brain-loop runs with:
   - `--recall-project PATH`
   - `--recall-max-items N`
   - optional `--queue-store PATH`
3. Preserved safety/clarity guardrails:
   - `--recall-project` requires `--brain-loop`;
   - `--queue-store` requires `--recall-project`;
   - manual `--context` remains first in `recalled_context`;
   - route-only mode does not read project files.
4. Added tests for project recall context and CLI guardrails.
5. Updated docs, task progress, roadmap status, project memory, and daily log.

Verification: `.venv/bin/python -m pytest -q` passed: 118 tests.

## Next Action

Next useful step is decision confidence and escalation thresholds in `run_brain_loop()` so low-confidence local decisions can ask Shadhin or request provider review instead of pretending certainty.
