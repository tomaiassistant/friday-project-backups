# AI Knowledge Project Memory

## Stable Context

- **Owner:** Shadhin (prefers "bro")
- **Friday:** Hermes assistant main — primary interface for Shadhin
- **Jerry:** OpenClaw assistant — secondary agent for coding/tasks
- **Tom:** Legacy Hermes assistant — knowledge source, now merged into Friday
- **AI Knowledge** renamed from **Brain Model** on 2026-06-12 (decision: [[2026-06-12-rename-to-ai-knowledge]])
- Broader direction: reusable markdown knowledge vault for feeding/grounding agents, not a single project record
- Structure: Obsidian-style markdown, folders by knowledge type, wikilinks, separation of raw/distilled

## Agents & Roles

| Agent | Platform | Role | Notes |
|-------|----------|------|-------|
| Friday | Hermes (Telegram, web) | Primary assistant | Main interface, memory, scheduling, coordination |
| Jerry | OpenClaw (VS Code, terminal) | Coding agent | Feature work, PRs, code review, prototypes |
| Tom | Legacy Hermes | Knowledge source | Historical context, decisions, specs |

## Working Principles

- Build architecture first; do not attempt to train a foundation model in v0.1
- Use existing AI models plus memory, reasoning, tools, and agent coordination
- Prefer clear markdown records over hidden assumptions
- Learn from Shadhin's corrections and preserve important lessons
- For v0.1, keep the system practical: existing models + markdown/project-file memory first, then add heavier retrieval if tests show it is needed
- If embeddings are added later, SQLite is recommended as first local store
- Provider output must stay advisory/generative only; local AI Knowledge memory, safety, and action policy remain authoritative
- High-risk actions require confirmation

## Key Decisions (Linked)

- [[2026-05-21-project-initialization]] — Project initialization with file-based coordination
- [[2026-05-22-budget-jarvis-core-first]] — Start with Budget Jarvis brain/router core
- [[2026-06-12-rename-to-ai-knowledge]] — Rename Brain Model to AI Knowledge
- [[2026-06-12-vps-root-smb-share]] — VPS root SMB share via Tailscale

## Active Projects

- **AI Knowledge** (this vault) — Knowledge base for all agents
- **ListingsFinder** — Streamlit app + scheduler, being integrated into Hermes as skill/MCP via TMCP
- **Budget Jarvis Core** — Python package for safe brain/router (in friday-project-backups)
- **Hermes Agent** — Core agent platform, skills, plugins, TMCP gateway
- **VPS Infrastructure** — n8n (5678), aapanel (15041), Hermes web (3000), nginx (80)

## Daily Work Window

- **08:00 Asia/Dhaka** — Tom/Jerry daily Brain Model/AI Knowledge work window
- Tracked in: `tasks/0003-daily-8am-work-window.md`

## VPS Environment

- **IP:** 79.108.225.121
- **Disk:** 50GB, 32% used (was 20GB 86% before migration)
- **RAM:** 3.7GB, 2.6GB available
- **Services:** n8n (Docker, port 5678), aapanel (15041), nginx (80), Hermes web (3000→5173)
- **Backups:** Daily to GitHub (friday-project-backups), Google Drive configured

## Backup Cron Jobs (All Fixed with Git LFS)

| Job | Schedule | Script | Status |
|-----|----------|--------|--------|
| Hermes backup | 0 2 * * * | push_hermes_backup_daily.sh | ✓ LFS enabled |
| Projects backup | 10 2 * * * | push_projects_backup_daily.sh | ✓ LFS enabled |
| Brain Model backup | 0 2 * * * | push_brain_model_daily.sh | ✓ Configured |

## Prototype History Preserved

- Budget Jarvis v0.1 coding started with safe brain/router core
- Mark XXXIX studied as architectural reference only (no code copied)
- Hermes skills system built for reusable workflows
- TMCP gateway established for multi-agent coordination