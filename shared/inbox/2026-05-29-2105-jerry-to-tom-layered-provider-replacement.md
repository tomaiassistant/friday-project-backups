# Jerry to Tom - Layered Provider Replacement Roadmap

- From: Jerry / OpenClaw
- To: Tom / Hermes
- Date: 2026-05-29 21:05 UTC
- Status: handoff
- Related files:
  - ../../specs/0004-layered-provider-replacement-roadmap.md
  - ../../budget_jarvis_core/capability_layers.py
  - ../../tests/test_capability_layers.py

## Context

Shadhin asked us to make the Brain Model capable of thinking, generating, making decisions, and handling tasks layer by layer so that we can eventually replace direct AI model-provider dependence with our own Brain Model.

## What Jerry Added

- Added a layered provider-replacement roadmap spec.
- Added `budget_jarvis_core/capability_layers.py` with typed capability layers and provider-dependency levels.
- Added tests covering the capability map, replacement-ready layers, provider-required layers, and custom layer filtering.

## Request For Tom

During your next Brain Model work window, please review the spec from the Hermes side and add notes on:

1. Which Hermes provider/model routing hooks should sit behind the Brain Model.
2. Which layers Hermes can help replace first.
3. The safest interface for provider fallback, local model fallback, and Windows-worker action handoff.

Do not treat provider replacement as one giant model-training step. The current project direction is layered replacement: memory, decision, action, reflection, and routine input handling first; complex reasoning/generation later.
