# 2026-09-28 — ECC Adoption Review

Reviewed github.com/affaan-m/ECC (agent harness optimization, ~269K stars,
GitHub trending). Decision: adopt ideas selectively, skip AgentShield
(enterprise/roadmap, not open yet).

## Adopted for Hermes (~/.hermes/skills/)

- `search-first` — research-before-coding with Adopt/Extend/Compose/Build matrix
- `architecture-decision-records` — ADR format + workflow
- `deep-research` — cited multi-source research report workflow
- `security-review` — security checklist (secrets, injection, authz, XSS, CSRF)
- `agent-architecture-audit` — 12-layer agent diagnostic
- `continuous-learning` — instinct-based learning, confidence scoring, promotion

## Adopted for AI Knowledge (this vault)

- `docs/learning-pipeline.md` — instinct format, confidence bands, scope rules,
  promotion criteria, session-end reflection checklist
- `OPERATING_RULES.md` — decision logging now requires full ADR sections
  (Context / Decision / Alternatives Considered / Consequences)

## Not adopted

- AgentShield security scanner (enterprise roadmap, not an open tool yet)
- ECC installers/plugin system (Claude/Codex-specific, not portable to Hermes)

## Related

- [[OPERATING_RULES]]
- [[PROJECT_MEMORY]]
