# Rename Brain Model to AI Knowledge

Date: 2026-06-12

## Decision

The broader system direction is renamed from **Brain Model** to **AI Knowledge**.

## Reason

Shadhin wants this to be more than a single project dataset. It should become a reusable knowledge resource for agents: a markdown vault that can feed, ground, and later help train/prepare agent memory.

## Structure Direction

Keep it Obsidian-style:

- markdown-first
- clear folders by note type
- linked notes where useful
- stable memory separated from logs/tasks/research/decisions
- agent-readable files as the source of truth

## Compatibility Note

The local folder may stay `/root/projects/brain-model` temporarily so existing cron, backups, tests, and scripts do not break. Public naming and documentation should use **AI Knowledge** going forward.
