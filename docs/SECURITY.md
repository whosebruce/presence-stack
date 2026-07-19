# Security and Identity Boundaries

Presence Engineering is powerful because the agent can act. That also makes identity, authorization, and blast-radius design part of the product—not cleanup work.

## Hard rules

- One owner, one set of accounts. Never clone another person's live Hermes home, Apple ID, ChatGPT login, memory workspace, bot token, or API key.
- Secrets stay in local credential/config stores with restrictive permissions; never in Discord, GitHub, Obsidian, screenshots, examples, or shell history.
- Unknown/public contacts never reach a terminal-capable agent directly.
- Default-deny gateway authorization: use allowlists and DM pairing; do not enable allow-all for a bot with tools.
- Keep Proxmox, TrueNAS, Hermes admin, Jellyfin admin, SearXNG admin, and Firecrawl admin LAN/Tailscale-only unless a reviewed reverse-proxy design requires otherwise.
- Separate human approval from machine execution for money, messages, deletion, account changes, public posting, and sensitive files.
- Disclose when a caller or sender is interacting with an AI receptionist.

## Identity layout

Recommended separate identities:

- owner administrative email;
- agent/service email;
- separate Discord/Telegram application/bot;
- separate Apple identity and optional line for BlueBubbles business use;
- per-service API keys with spend caps;
- separate Honcho workspace/peers for the owner;
- non-root Linux service account for Hermes.

Do not reuse the Presence Designer's or installer's identities on another owner's deployment.

## Hermes baseline

Follow the live [Hermes security guide](https://hermes-agent.nousresearch.com/docs/user-guide/security/). At minimum:

- keep dangerous-command approvals enabled (`smart` or `manual`);
- enable only required toolsets;
- pair/allowlist users;
- use Docker/another isolated terminal backend for untrusted workloads when practical;
- keep secrets in Hermes' `.env`/auth stores, not normal config or repos;
- use provider spend caps and low-balance alerts;
- verify `hermes doctor` and gateway authorization after every major change.

## Receptionist pattern

```text
Public message/call
  → bounded intake model with no general tools
  → FAQ or structured lead summary
  → owner queue
  → explicit owner approval
  → privileged agent performs a narrow action
```

The receptionist should be able to collect name, callback route, organization, request, urgency, deadline, and consent to relay. It should not browse private files, execute shell commands, send arbitrary outbound messages, quote binding prices, or claim human identity.

## Storage and backup

- ZFS/RAID is availability, not backup.
- Maintain a separate backup target and test restores.
- Give Hermes access only to intended datasets/shares.
- Snapshot before upgrades or migrations, but do not call snapshots an offsite backup.
- Use a UPS for storage hosts when possible.

## Network

- Prefer wired Ethernet for the server.
- Use Tailscale/VPN for remote administration.
- Use HTTPS and authentication for any deliberately exposed service.
- Do not port-forward admin dashboards casually.
- Place public/receptionist workloads in a separate VM/container/VLAN when the hardware supports it.

## Release checklist

Before publishing a derived repository:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/privacy_scan.py
git diff --check
git fsck --full
```

Then scan the exact index, reachable history, and a fresh public clone. A clean working tree alone is not proof that old commits or Git objects are clean.
