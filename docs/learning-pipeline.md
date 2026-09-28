# Learning Pipeline (Instincts)

Adopted from the ECC continuous-learning system (github.com/affaan-m/ECC, MIT).
This is the reflection/writeback standard for agents working with AI Knowledge.

## Core Idea

Lessons start as **instincts** — small learned behaviors with a confidence score —
and get promoted to durable knowledge only when proven. This prevents one-off
incidents from polluting the vault.

## Instinct Format

```markdown
## <short-id>
- **Trigger:** when exactly this applies
- **Action:** the single behavior to do
- **Confidence:** 0.0-1.0
- **Scope:** project | global
- **Evidence:** 1-3 dated observations that produced this
```

Rules: atomic (one trigger, one action), evidence-backed, confidence-weighted.

## Confidence Bands

| Score | Meaning | Behavior |
|-------|---------|----------|
| 0.3 | Tentative | Mention when relevant, don't apply |
| 0.5 | Moderate | Apply when context matches |
| 0.7 | Strong | Apply by default |
| 0.9 | Near-certain | Core behavior |

- Increase: repeated observation without correction.
- Decrease: explicit user correction or contradicting evidence.
- A corrected instinct is **overwritten, not accumulated**.

## Scope

| Pattern type | Scope | Where it lands |
|--------------|-------|----------------|
| Project conventions, code style, file layout | project | `research/` note or project skill |
| Security practices, tool workflow, git practices | global | `memory/PROJECT_MEMORY.md` |

Project-scoped instincts must never leak into global memory.

## Promotion (instinct -> durable knowledge)

Promote only when ALL hold:

1. Confidence ≥ 0.7
2. Observed in 2+ distinct sessions or contexts
3. It changes future agent behavior

Targets:

- Procedure/workflow → new or updated Hermes skill (`skill_manage`)
- Stable fact about user/environment → `memory/PROJECT_MEMORY.md` or agent memory tool
- Architecture choice → `decisions/` note (existing format, plus
  **Alternatives Considered** and **Consequences** sections)

## Session-End Reflection Checklist

At the end of a substantive session, answer:

1. What did the user correct?
2. What failed and what fixed it?
3. What workflow repeated?

Write at most a few high-signal entries. "Record everything" is contamination,
not learning. Temporary instructions are NOT preferences — never promote a
one-off directive to global knowledge.

## Drift Rule

When promoting or updating, **replace or remove the superseded entry** in the
same operation. Stacked duplicate entries with conflicting advice are the main
failure mode of agent memory.

## Related

- [[OPERATING_RULES]]
- [[PROJECT_MEMORY]]
- Hermes skills: `continuous-learning`, `search-first`, `deep-research`,
  `architecture-decision-records`, `security-review`, `agent-architecture-audit`
  (adapted from ECC into `~/.hermes/skills/`)
