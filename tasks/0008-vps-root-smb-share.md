# Task 0008 — VPS Root SMB Share

Status: completed
Date: 2026-06-12
Links: [[PROJECT]], [[OPERATING_RULES]], [[PROJECT_MEMORY]], [[2026-06-12-vps-root-smb-share]]

## Request

Shadhin asked Friday to create SMB credentials and settings so the VPS root directory can be mapped as a Windows network drive over Tailscale.

## Implementation

- Configured Samba share `vps-root` pointing to `/`.
- Created SMB user `shadhin`.
- Restricted SMB access at Samba level to localhost and Tailscale range only.
- Added firewall rules for TCP 445:
  - allow `lo`
  - allow `tailscale0`
  - drop other TCP 445 traffic
- Added a systemd oneshot service to reapply the TCP 445 firewall rules after reboot.

## Result

- Tailscale IP: `100.89.9.69`
- Windows share path: `\\100.89.9.69\vps-root`
- Credential file on VPS: `/root/smb-credentials-vps-root.txt`
- Verified Samba config with `testparm`.
- Verified `smbd` is active.
- Verified TCP 445 accepts local connection to the Tailscale IP.

## Safety Note

This share maps the VPS root filesystem. It is powerful and should stay Tailscale-only. Do not store the SMB password inside this vault.
