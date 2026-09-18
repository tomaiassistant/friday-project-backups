# Task 0009 — VPS Disk Cleanup

Status: completed
Date: 2026-06-12
Links: [[PROJECT]], [[OPERATING_RULES]], [[PROJECT_MEMORY]], [[2026-06-12 Log]]

## Request

Shadhin asked Friday to clean unused files from the VPS because only about 1.49 GB was free.

## Actions

Safe cleanup:

- Cleaned apt package cache and apt lists.
- Removed temporary build/download folders from `/tmp`.
- Removed rebuildable caches: pip, npm, electron, Playwright, node-gyp, TypeScript, uv.
- Vacuumed system journal to a smaller size.
- Removed old local Hermes backup ZIPs from 2026-06-09 and 2026-06-10, keeping recent backups from 2026-06-11 and 2026-06-12.
- Removed rebuildable TMCP local dependencies/build output:
  - `/root/projects/TMCP/node_modules`
  - `/root/projects/TMCP/.next`

## Result

Root filesystem free space increased from about **1.5 GB** to about **6.0 GB**.

## Notes

- TMCP source code was kept. Dependencies can be restored with `npm install` inside `/root/projects/TMCP`.
- ListingsFinder `.venv` was kept to avoid breaking the app smoke-check workflow.
- Docker/containerd was not pruned because the active image/container showed `0B` reclaimable.
