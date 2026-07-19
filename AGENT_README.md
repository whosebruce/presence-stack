# Agent handoff guide

This file exists for agents that do not automatically load `AGENTS.md`. Read [AGENTS.md](AGENTS.md) first; it is the operational contract. Then follow [docs/BUILD_ORDER.md](docs/BUILD_ORDER.md).

## Mission

Build a new owner's Presence Stack with capability classes similar to the sanitized [reference stack](docs/REFERENCE_STACK.md), without copying any person's identity, data, credentials, configuration, private routes, or authority rules.

## Interview behavior

1. Ask one plain-language question at a time.
2. Explain every product term before asking the owner to choose it.
3. Recommend the channel where the owner already spends time.
4. Summarize important answers and let the owner correct them.
5. Separate known facts, owner statements, source-derived observations, and model inference.
6. Ask the owner to enter secrets only through official OAuth/device flows or local hidden prompts.
7. Never solicit tokens, passwords, phone numbers, addresses, Apple IDs, recovery codes, private archives, or platform IDs in chat.

The non-secret onboarding helper is:

```bash
python3 -m presence_stack.onboard
```

## Presence design

- Study only sources approved for this purpose.
- Preserve provenance, dates, and timestamps for important observations.
- Build explicit Presence Profile artifacts instead of stuffing a life archive into one prompt.
- Current owner corrections outrank old sources.
- Voice/likeness synthesis requires separate consent and disclosure rules.
- Test voice, judgment, facts, audience fit, respectful challenge, and authority boundaries.

## Installation rule

Do not install everything blindly. Mark every module as required, optional, or skipped:

- base Hermes and model;
- private channel;
- secure defaults;
- built-in memory/session search;
- Honcho;
- SearXNG/Firecrawl;
- Obsidian/SMB;
- Composio/Google Workspace;
- Open Design/Claude Code/Codex;
- specialist profiles;
- receptionist;
- local models/media/storage.

Run each module's real verification before continuing.

## Security

- Keep owner-private state under `~/.presence-stack/` and Hermes credentials in Hermes stores.
- Unknown/public users go through a separate bounded receptionist.
- Keep admin services localhost/LAN/Tailscale-first.
- Use smart/manual command approvals and least-privilege tools.
- Profiles do not create filesystem isolation; use containers/VMs/narrow mounts when needed.
- Never reuse the installer's accounts, keys, model subscriptions, Apple identity, memory workspace, or source material.

## Final report

Report:

- chosen architecture tier;
- modules enabled and skipped;
- model/provider names without credentials;
- Presence Profile paths and source counts, not contents;
- authority/sign-off map;
- verification commands and pass/fail counts;
- one-time/monthly planning range;
- unresolved decisions and risks.

Never report secret values, personal identifiers, private network details, platform IDs, raw source archives, or private message content.
