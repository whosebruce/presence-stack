# Presence Stack agent contract

This repository is a privacy-safe deployment harness for building a new owner's Hermes-based Presence Stack. It is not a clone of any person's live agent.

## Start here

1. Read `README.md`, `docs/BUILD_ORDER.md`, `docs/SECURITY.md`, and `docs/REQUIREMENTS.md`.
2. Run `python3 -m presence_stack.onboard` or interview the owner one plain-language question at a time.
3. Produce a non-secret plan before installing anything.
4. Build in stages. Stop after each gate and prove it works.
5. Keep all owner data, inventories, tokens, OAuth grants, bot IDs, source material, and generated Presence Profiles outside this repository.

## Hard boundaries

- Never ask the owner to paste an API key, OAuth token, password, recovery code, phone number, address, Apple ID, private message archive, or private source archive into chat.
- Use official setup wizards, device-code OAuth, or local hidden prompts for authentication.
- Never copy another person's `~/.hermes`, `SOUL.md`, memories, Honcho workspace, bot token, Apple identity, or config.
- Never commit `.env`, `honcho.json`, `auth.json`, OAuth stores, bot IDs, local inventory, mount credentials, logs, databases, session history, or generated Presence Profile files.
- Unknown/public users must not reach an agent with unrestricted terminal, browser, file, messaging, payment, or admin tools.
- Do not expose admin UIs to the public internet by default. Prefer localhost, LAN, Tailscale, or a reviewed authenticated reverse proxy.
- Do not disable command approvals to make installation easier. Use `smart` or `manual` approvals.
- Do not promise that a local model will match a frontier hosted model. Local inference is optional and separately sized.

## Required build order

1. Owner intake, source permissions, channel choice, and decision rights.
2. Hardware/network/storage inventory and tested backup.
3. Base Hermes install, model login, `hermes doctor`, and one successful chat.
4. Secret redaction, smart approvals, checkpoints, and least-privilege toolsets.
5. One private owner channel with pairing/allowlist and unknown-user denial.
6. Built-in memory and session search.
7. Optional Honcho, with the owner choosing cloud vs self-host and recall mode.
8. Optional SearXNG search and Firecrawl extraction.
9. Optional Obsidian/SMB durable files.
10. Optional Composio/Google Workspace, Open Design, coding agents, and specialist profiles.
11. One harmless Presence Loop that returns evidence.
12. Reboot persistence, backup restore, spend-cap, privacy, and security verification.

## Private local state

Use an untracked owner-private root such as:

```text
~/.presence-stack/
├── plan/
├── inventory/
├── presence-profile/
├── sources/
├── transcripts/
├── secrets/
├── reports/
└── change-log/
```

Create it with restrictive permissions. Use Hermes' own config and auth stores for Hermes credentials.

## Verification contract

Before reporting a module complete, return the exact command and pass/fail result. At minimum:

```bash
hermes --version
hermes doctor
hermes memory status
hermes mcp list
python3 -m presence_stack.doctor
python3 scripts/verify_repo.py
python3 scripts/privacy_scan.py
```

For gateway work, also prove owner access and unknown-user denial. For storage, restore one test file. For public publication, scan tree, exact Git index, reachable history, and a fresh remote clone.

## Final report format

Report only:

- architecture tier selected;
- modules enabled and intentionally skipped;
- model/provider names without credentials;
- service URLs as localhost, hostnames, or redacted addresses;
- verification commands and counts;
- one-time/monthly planning range;
- unresolved owner decisions and risks;
- private artifact paths as `~`-relative paths where safe.

Do not include personal identifiers, raw source content, private addresses, platform IDs, tokens, or secret values.
