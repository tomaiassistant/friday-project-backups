# 2026-06-12 — VPS Root SMB Share Decision

**Links:** [[0008-vps-root-smb-share]], [[PROJECT]], [[OPERATING_RULES]], [[PROJECT_MEMORY]]

## Decision

For Shadhin's Windows-to-VPS workflow, expose the VPS root filesystem through Samba as a Tailscale-only network share.

## Rationale

- Shadhin already installed SMB and connected Tailscale on the VPS
- Windows can map SMB shares directly as network drives
- Tailscale gives a private network path without exposing the share publicly

## Implementation Policy

- Share name: `vps-root`
- Share path: `/`
- SMB user: `shadhin`
- Use Samba `hosts allow`/`hosts deny` to permit localhost and Tailscale range only
- Use firewall rules to allow TCP 445 only on `lo` and `tailscale0`
- Keep credentials out of AI Knowledge notes

## Risk

This is high privilege because the share uses root-level filesystem access. Keep it restricted to Tailscale and rotate the SMB password if the Windows PC is compromised.

## Related

- [[PROJECT_MEMORY]] (VPS Environment section)
- [[tasks/0008-vps-root-smb-share]]