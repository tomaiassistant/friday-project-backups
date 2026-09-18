# Spec 0004 - Layered Provider Replacement Roadmap

- Owner: Shadhin
- Agents: Jerry / OpenClaw, Tom / Hermes
- Created: 2026-05-29
- Status: active roadmap
- Related code: `budget_jarvis_core/capability_layers.py`

## Goal

Build the Brain Model so it can gradually replace direct dependence on AI model providers. The target is not one giant model first. The target is a layered brain system where each capability can move from provider-required to provider-assisted to provider-optional to local Brain Model control.

## Core Principle

We replace providers by capability, not all at once.

External models are currently strongest for broad reasoning and generation. Our Brain Model can become strongest at continuity, memory, decision policy, task control, safety, and personalized execution first. As those layers mature, providers become engines behind the Brain Model instead of the system itself.

## Layers

### 1. Input Understanding

Purpose: turn user messages, transcripts, files, or events into structured intent, entities, constraints, and risk signals.

Initial state: provider-assisted plus local router/risk rules.

Replacement path:

- expand deterministic intent/risk/entity extraction;
- add confidence scores;
- use providers only when local extraction is uncertain;
- later add local models for ambiguous language.

### 2. Memory

Purpose: remember project state, user preferences, decisions, outcomes, and lessons.

Initial state: mostly local through markdown files, JSON queue state, and project memory.

Replacement path:

- index project files and daily logs;
- retrieve relevant facts before planning;
- attach freshness/source metadata;
- add embeddings or SQLite only when simple retrieval is insufficient.

### 3. Reasoning

Purpose: break down tasks, compare options, predict consequences, and create plans.

Initial state: provider-required for complex synthesis.

Replacement path:

- encode common reasoning patterns as local structured steps;
- evaluate local plans against provider plans;
- keep provider calls for hard/ambiguous tasks;
- train or tune local reasoning later if examples are strong enough.

### 4. Decision

Purpose: decide what to do next, what not to do, when to ask Shadhin, and when to queue or delegate.

Initial state: local router/risk rules plus provider judgment.

Replacement path:

- add decision scores and confidence thresholds;
- make safety gates deterministic;
- track outcomes and revise policies;
- allow providers to advise, but not override local safety policy.

### 5. Generation

Purpose: produce text, code, reports, messages, and explanations.

Initial state: provider-required for high-quality flexible output.

Replacement path:

- separate structured output from prose generation;
- use templates for routine reports/status updates;
- use local models for private/basic generation;
- keep frontier providers for hard coding, complex writing, and high-stakes work until local quality is proven.

### 6. Action

Purpose: execute approved tasks through files, tools, browser, schedules, messages, and future Windows-worker integration.

Initial state: local tools with strict confirmation gates.

Replacement path:

- keep actions deterministic and auditable;
- require confirmation for high-risk external actions;
- start with non-executing adapters;
- add execution only after tests and logs prove safety.

### 7. Reflection

Purpose: review what happened, update memory, record mistakes, and improve future behavior.

Initial state: local daily logs and project memory.

Replacement path:

- standardize reflection records;
- tag decisions, failures, successes, and unresolved risks;
- feed reflections into future planning;
- use providers only for deep review or summarization.

### 8. Learning

Purpose: improve the Brain Model over time from tests, outcomes, and examples.

Initial state: manual improvements by Jerry/Tom with provider assistance.

Replacement path:

- create evaluation cases for tasks and decisions;
- store expected vs actual results;
- use regression tests as the first learning loop;
- later fine-tune or train local components from high-quality examples.

## Provider Replacement Levels

- `required`: the layer still needs an external provider for useful quality.
- `assisted`: the Brain Model handles structure/policy, provider helps with language or judgment.
- `optional`: the Brain Model can run locally for routine work, provider is an upgrade path.
- `local`: the Brain Model handles the layer without provider dependency.

## Current Implementation

`budget_jarvis_core/capability_layers.py` records the first typed capability map. It identifies:

- replacement-ready layers: memory, action, reflection, and routine input handling;
- provider-required layers: complex reasoning, generation, and learning;
- next steps for each layer.

## Near-Term Build Order

1. Add project-memory recall over markdown and queue state. **Done 2026-05-30; CLI brain-loop integration added 2026-05-31.**
2. Add decision confidence and escalation thresholds to `run_brain_loop()`.
3. Add structured generation templates for routine status/task reports.
4. Add evaluation cases comparing local Brain Model output against provider output.
5. Add a provider interface so providers become swappable engines behind the Brain Model, not direct owners of behavior.

## Collaboration Split

Jerry should continue building local OpenClaw-side code, tests, memory, docs, and CLI integrations.

Tom/Hermes should review the layered roadmap during the next work window, compare it against Hermes capabilities, and suggest the safest provider-router interface for Hermes/OpenClaw/Windows-worker integration.

## Hermes Provider-Router Notes - 2026-05-30

Tom/Hermes review: Hermes should sit behind the Brain Model as a swappable advisory/generation engine, not as the owner of memory, safety policy, or action authority.

Recommended routing hooks:

- **Input understanding hook:** provider may parse ambiguous transcripts into intent/entities, but local `risk.py` and `router.py` remain the first gate and final safety source.
- **Reasoning hook:** provider may create or critique plans for complex tasks; local Brain Model should attach recalled memory, constraints, risk level, and expected output schema before calling it.
- **Generation hook:** provider may write prose/code for hard cases; routine reports/status updates should move toward local templates first.
- **Review hook:** provider may review local decisions and tests, but cannot downgrade confirmation requirements or execute actions.

Safe fallback interface:

1. Local Brain Model attempts deterministic recall/routing/decision first.
2. If local confidence is low or output quality needs help, call a provider adapter with a typed request: `layer`, `intent`, `recalled_context`, `risk_level`, `allowed_outputs`, and `forbidden_actions`.
3. If the preferred provider fails, try a local model or alternate provider only for the same typed request and only within the same forbidden-action boundary.
4. If all engines fail, return a safe degraded result: queued local task, ask-Shadhin blocker, or no-op summary.

Windows-worker handoff boundary:

- The Windows worker should receive only approved, structured action requests after Brain Model routing, risk classification, and confirmation checks.
- High-risk actions remain blocked until Shadhin confirms; provider output must never become direct Windows-worker commands.
- First Windows integration should be a non-executing adapter that records intended clicks/commands and audit logs before live control is allowed.

## Success Definition

The Brain Model is ready to replace providers for a layer when:

- it has deterministic tests;
- it has clear safety behavior;
- it records source/context/outcome;
- it performs routine cases without provider calls;
- provider output is optional or only used as an upgrade path.
