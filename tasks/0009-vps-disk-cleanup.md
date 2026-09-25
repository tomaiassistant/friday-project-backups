# Task: VPS Disk Cleanup Cron

**Created:** 2026-06-12
**Agent:** Friday (Hermes)
**Status:** Active
**Priority:** Medium
**Schedule:** Weekly Sunday 02:00 Asia/Dhaka

## Description

Weekly cron job to clean up VPS disk space.

## Current Cron

- **When:** Sunday 02:00 Asia/Dhaka
- **Commands:** n8n SQLite VACUUM, Docker prune, temp file cleanup

## Status

- Running on old VPS, needs verification on new VPS
- n8n SQLite VACUUM when full
- Hermes web cleanup

## Related

- [[PROJECT_MEMORY]] (VPS Environment)
- [[decisions/2026-06-12-vps-root-smb-share]]