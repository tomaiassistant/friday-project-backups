# AI Knowledge Roadmap

## Phase 1 - Foundation (Current)

- [x] Define AI Knowledge purpose and structure
- [x] Set up markdown vault structure with folders
- [x] Create operating rules for agents
- [x] Establish daily backup to GitHub (brain-model branch)
- [x] Seed vault with existing project context from friday-project-backups

## Phase 2 - Memory Core

- [ ] Implement daily memory capture from agent sessions
- [ ] Build long-term project memory with distilled facts
- [ ] Add people/preference memory
- [ ] Create decision memory with rationale
- [ ] Add retrieval rules before answering/acting

## Phase 3 - Reasoning & Agent Loop

- [ ] Build observe → recall → reason → act → reflect → writeback loop
- [ ] Add task handoff between Jerry (OpenClaw) and Friday (Hermes)
- [ ] Add self-review for assumptions, privacy, correctness
- [ ] Implement scheduled work at 08:00 Asia/Dhaka daily

## Phase 4 - Integration & Testing

- [ ] Connect to ListingsFinder automation
- [ ] Connect to VPS monitoring (n8n, aapanel, Hermes web)
- [ ] Test against real tasks from Shadhin
- [ ] Measure recall, planning quality, privacy behavior, usefulness
- [ ] Prepare AI Knowledge v0.1 report

## Phase 5 - Provider Replacement (Layered)

- [ ] Input understanding: local intent/risk/entity extraction
- [ ] Memory: local retrieval + embeddings when needed
- [ ] Reasoning: structured local patterns + provider for synthesis
- [ ] Decision: local policy first, provider advisory only
- [ ] Action: local execution, provider for generation only