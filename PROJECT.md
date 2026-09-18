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
```

## Core Capabilities

1. Capture information from conversations, files, tasks, emails, web research, and project work.
2. Store raw notes separately from distilled long-term memory.
3. Retrieve relevant knowledge before answering or acting.
4. Reason through goals, constraints, risks, and next actions.
5. Coordinate work between Friday, Jerry, and future agents through shared markdown files.
6. Write back lessons, decisions, and important context.
7. Protect private data and avoid sharing memory in the wrong context.
8. Grow into a reusable agent-feeding knowledge resource, not a single-project notebook.

## Architecture Idea

- **Input layer:** chat messages, notes, files, links, future connectors.
- **Knowledge layer:** markdown vault, memory files, decisions, project context.
- **Retrieval layer:** search, tags, wikilinks, future embeddings/RAG.
- **Reasoning layer:** planning, reflection, task decomposition, critique.
- **Action layer:** code writing, browser automation, email/calendar actions with permission.
- **Coordination layer:** shared files that agents can read and update.
- **Evaluation layer:** tests that measure recall, usefulness, privacy, and execution quality.

## Success Criteria

- Agents can quickly find the right context without hallucinating.
- Knowledge is stored in clean markdown, not hidden only in chat.
- Notes are reusable across projects and agents.
- Important decisions are traceable.
- The vault can later power retrieval, training data prep, or agent context injection.
