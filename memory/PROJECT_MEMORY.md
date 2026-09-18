# AI Knowledge Project Memory

## Stable Context

- Shadhin renamed the broader **Brain Model** direction to **AI Knowledge** on 2026-06-12.
- AI Knowledge should be a reusable markdown knowledge vault for feeding and grounding agents, not only a single project record.
- The structure should stay Obsidian-style: clear markdown notes, folders by knowledge type, wikilinks where useful, and separation between raw notes, decisions, tasks, logs, and distilled memory.
- Shadhin wants AI Knowledge to help train/feed agents over time through project knowledge, lessons, workflows, research, and decisions.
- The old Brain Model work remains useful as the first implementation/prototype inside the wider AI Knowledge direction.
- Jerry is Shadhin's OpenClaw assistant.
- Friday is Shadhin's Hermes assistant main.
- Tom is the legacy Hermes assistant/source whose knowledge should be preserved.
- Jerry, Friday, and future agents should share data and coordinate through this project folder.
- Tom's daily Brain Model/AI Knowledge work window is **08:00 Asia/Dhaka**, requested by Shadhin and tracked in `tasks/0003-daily-8am-work-window.md`.

## Working Principles

- Build architecture first; do not attempt to train a foundation model in v0.1.
- Use existing AI models plus memory, reasoning, tools, and agent coordination.
- Prefer clear markdown records over hidden assumptions.
- Learn from Shadhin's corrections and preserve important lessons.
- For v0.1, keep the system practical: existing models plus markdown/project-file memory first, then add heavier retrieval if tests show it is needed.
- If embeddings are added later, Friday currently recommends SQLite as the first local store; this is a recommendation, not a final Shadhin decision.
- Provider output must stay advisory/generative only; local AI Knowledge memory, safety, and action policy remain authoritative.
- High-risk actions require confirmation.

## Prototype History Preserved

- Budget Jarvis v0.1 coding started with the safe brain/router core first: state machine and risk classifier before live mic, PC-control, or external-action integration.
- Budget Jarvis v0.1 has a tested non-executing transcript router (`route_transcript`) that selects broad tool categories and preserves high-risk confirmation gates.
- Budget Jarvis v0.1 has a tested in-memory `TaskQueue` and local JSON queue persistence.
- Budget Jarvis v0.1 has tested local project writeback helpers in `memory_bridge.py`.
- Budget Jarvis v0.1 has a tested non-executing CLI prototype and minimal brain loop: observe -> recall -> reason -> act -> reflect.
- The CLI supports local project-memory recall with `--recall-project PATH` and guardrails.
- Confidence/escalation policy, provider-review boundary, project recall, and local queue persistence are tested.
- On 2026-06-09, Shadhin asked Friday/Hermes to continue Tom's Brain Model role after Tom's server crash. Friday cloned the repo to `/root/projects/brain-model`, set up `.venv`, verified tests, and should write future AI Knowledge-related knowledge, tasks, decisions, and implementation summaries into this repository.
- Shadhin specifically reminded Friday on 2026-06-12 to keep AI Knowledge files connected like an Obsidian vault and to add useful data/skills during related work; see `tasks/0007-rename-to-ai-knowledge.md` and `tasks/0008-vps-root-smb-share.md`.
- VPS root SMB mapping for Windows was configured on 2026-06-12 as Tailscale-only: share `\\100.89.9.69\vps-root`, SMB user `shadhin`, credentials stored outside the vault at `/root/smb-credentials-vps-root.txt`; see `decisions/2026-06-12-vps-root-smb-share.md`.
- VPS disk cleanup on 2026-06-12 improved `/` free space from about 1.5 GB to about 6.0 GB by removing caches, temp files, old local backup ZIPs, and rebuildable TMCP `node_modules`/`.next`; see `tasks/0009-vps-disk-cleanup.md`.
