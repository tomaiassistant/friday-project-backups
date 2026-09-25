# Spec 0004 - Layered Provider Replacement Roadmap

**Owner:** Shadhin
**Agents:** Friday (Hermes), Jerry (OpenClaw)
**Created:** 2026-05-29
**Status:** Active roadmap
**Related code:** `budget_jarvis_core/capability_layers.py`

## Goal

Build the AI Knowledge so it can gradually replace direct dependence on AI model providers. The target is not one giant model first. The target is a layered brain system where each capability can move from provider-required to provider-assisted to provider-optional to local AI Knowledge control.

## Core Principle

We replace providers by capability, not all at once.

External models are currently strongest for broad reasoning and generation. Our AI Knowledge can become strongest at continuity, memory, decision policy, task control, safety, and personalized execution first. As those layers mature, providers become engines behind the AI Knowledge instead of the system itself.

## Layers

### 1. Input Understanding

**Purpose:** Turn user messages, transcripts, files, or events into structured intent, entities, constraints, and risk signals.

**Initial state:** Provider-assisted plus local router/risk rules.

**Replacement path:**
- Expand deterministic intent/risk/entity extraction
- Add confidence scores
- Use providers only when local extraction is uncertain
- Later add local models for ambiguous language

### 2. Memory

**Purpose:** Remember project state, user preferences, decisions, outcomes, and lessons.

**Initial state:** Mostly local through markdown files, JSON queue state, and project memory.

**Replacement path:**
- Index project files and daily logs
- Retrieve relevant facts before planning
- Attach freshness/source metadata
- Add embeddings or SQLite only when simple retrieval is insufficient

### 3. Reasoning

**Purpose:** Break down tasks, compare options, predict consequences, and create plans.

**Initial state:** Provider-required for complex synthesis.

**Replacement path:**
- Encode common reasoning patterns as local structured steps
- Evaluate local plans against criteria
- Use providers only for novel synthesis
- Cache successful reasoning traces

### 4. Decision Policy

**Purpose:** Enforce safety, privacy, confirmation gates, and action routing.

**Initial state:** Fully local (risk classifier, router, confirmation logic).

**Replacement path:**
- Keep fully local — this is the authority layer
- Providers may advise but never override

### 5. Action Execution

**Purpose:** Execute tools, scripts, API calls, and coordinate agents.

**Initial state:** Local execution (Hermes, OpenClaw, Windows worker, local scripts).

**Replacement path:**
- Keep fully local — execution is the trust boundary
- Providers generate code/templates only

### 6. Generation

**Purpose:** Produce natural language, code, documentation, summaries.

**Initial state:** Provider-required.

**Replacement path:**
- Template common responses locally
- Use providers for novel generation
- Fine-tune local models on successful generations

## Progress Tracking

| Layer | Current | Target | Notes |
|-------|---------|--------|-------|
| Input Understanding | Provider-assisted | Provider-optional | Router + risk classifier local |
| Memory | Local (markdown) | Local + embeddings | SQLite/embeddings when needed |
| Reasoning | Provider-required | Provider-assisted | Structured patterns first |
| Decision Policy | **Local (authority)** | **Local (authority)** | Never delegate |
| Action Execution | **Local (trust boundary)** | **Local (trust boundary)** | Never delegate |
| Generation | Provider-required | Provider-assisted | Templates + caching |

## Related

- [[specs/0001-v01-architecture-first-pass]]
- [[specs/0003-budget-jarvis-evolution-from-mark-xxxix]]
- [[plans/0001-budget-jarvis-v01-implementation-plan]]