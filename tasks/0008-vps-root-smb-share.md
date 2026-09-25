# Task: VPS Root SMB Share Setup

**Created:** 2026-06-12
**Agent:** Friday (Hermes)
**Status:** Pending
**Priority:** Medium

## Description

Set up Samba share for VPS root filesystem accessible via Tailscale from Windows.

## Decision Reference

- [[decisions/2026-06-12-vps-root-smb-share]]

## Implementation Policy

- Share name: `vps-root`
- Share path: `/`
- SMB user: `shadhin`
- Samba `hosts allow`/`hosts deny` for localhost and Tailscale range only
- Firewall: TCP 445 only on `lo` and `tailscale0`
- Keep credentials out of AI Knowledge notes

## Risk

High privilege — root-level filesystem access. Restrict to Tailscale, rotate password if Windows PC compromised.

## Status

- VPS has Tailscale installed
- Samba not yet configured
- Need to create SMB user and configure share

## Related

- [[PROJECT_MEMORY]] (VPS Environment)
- [[decisions/2026-06-12-vps-root-smb-share]]