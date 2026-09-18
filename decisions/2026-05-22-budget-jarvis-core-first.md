# Decision: Start Budget Jarvis Brain/Router Core First

- Date: 2026-05-22
- Owner: Shadhin
- Recorded by: Tom / Hermes
- Status: accepted for v0.1 implementation path

## Decision

Begin coding with the Budget Jarvis brain/router core before live mic, PC-control, or external-action integration.

## Reason

The core package gives Brain Model a safe execution foundation:

- explicit assistant states,
- command risk classification,
- future safe tool routing,
- future queueing for long-running work,
- future project memory/writeback bridge.

This supports the Brain Model v0.1 goal of existing models + memory + reasoning + tools while avoiding unsafe direct connection to live voice or PC control too early.

## Constraints

- No high-risk external action without Shadhin's confirmation.
- No live mic/PC-control changes in the first coding milestone.
- Use Mark XXXIX only as architectural inspiration; do not copy its code.
- Keep project-critical context written in the Brain Model folder.

## Alternatives Considered

1. Build a standalone markdown memory core first.
2. Start with live voice/PC control integration.

The brain/router core was preferred because it wraps memory work in a safer action-control layer and is testable locally.
