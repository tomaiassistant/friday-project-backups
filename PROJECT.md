# AI Knowledge

## Purpose

Build **AI Knowledge**: Shadhin's agent knowledge vault and reusable intelligence resource.

This is not just one project record. It is a structured markdown knowledge base that agents can read, retrieve from, and write back to — similar to an Obsidian vault for agent memory.

## Direction

The old **Brain Model** name described the first idea: a digital brain. The broader direction is now **AI Knowledge**:

- collect useful project knowledge, decisions, research, lessons, workflows, and context
- keep raw notes separate from distilled long-term memory
- make the files easy for Hermes, Jerry, and future agents to use as grounding data
- preserve clear links between tasks, decisions, docs, specs, logs, and memory
- support future RAG/search/agent-feeding without locking the knowledge to one app or one model

## People and Agents

- **Owner:** Shadhin
- **Friday:** Hermes assistant main
- **Jerry:** OpenClaw assistant
- **Tom:** legacy Hermes assistant knowledge/source

## Vault Structure

AI Knowledge should stay markdown-first and Obsidian-friendly:

```text
PROJECT.md              # overview and purpose
OPERATING_RULES.md      # how agents write/read this vault
ROADMAP.md              # direction and milestones
memory/                 # distilled stable knowledge
docs/                   # explanations and guides
specs/                  # architecture/specification notes
tasks/                  # actionable work records
decisions/              # architectural or policy decisions
research/               # source notes and studies
shared/logs/            # short daily/event logs
shared/inbox/           # messages from other agents
shared/outbox/          # messages to other agents
plans/                  # implementation plans
```

## Core Capabilities

1. Capture information from conversations, files, tasks, emails, web research, and project work.
2. Store raw notes separately from distilled long-term memory.
3. Retrieve relevant knowledge before answering or acting.
4. Reason through observe → recall → reason → act → reflect → writeback loop.
5. Coordinate between agents via shared inbox/outbox.
6. Schedule timed work and follow-ups.