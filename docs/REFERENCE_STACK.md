# Sanitized reference stack

This is the capability map that inspired the repository. It intentionally omits private addresses, IDs, accounts, paths, prompts, memories, routing rules, customer data, and credentials.

## Core operating model

| Layer | Reference choice | Portable lesson |
|---|---|---|
| Agent runtime | Hermes Agent | One agent core across CLI, messaging, cron, skills, tools, memory, and subagents |
| Primary model | Current strongest available OpenAI Codex model through OAuth | Use a strong tool-calling model as primary; fail closed rather than silently spending through an unintended provider |
| Auxiliary vision | Gemini Flash-class vision through OpenRouter | Route screenshots/images to a fast vision-capable model without moving the whole agent |
| Search | Self-hosted SearXNG | Keep routine search private and low-cost |
| Extraction | Self-hosted Firecrawl | Convert pages into agent-readable content; accept weaker anti-bot performance than the cloud service |
| Built-in continuity | Hermes memory + session search + skills | Curated always-loaded facts, searchable transcripts, and reusable procedures solve different problems |
| Deep memory | Honcho | Store sessions, model user/agent peers, search context, and persist conclusions |
| Durable knowledge | Obsidian vault on a private share | Human-readable source of truth outside any single chat platform |
| SaaS actions | Composio MCP | Add OAuth-backed app tools without placing app credentials in prompts or repositories |
| Workspace apps | Google Workspace | Email, calendar, documents, drive, and sheets behind least-privilege OAuth |
| Design | Open Design | Local-first artifact workspace controlled through MCP by Hermes and coding agents |
| Coding agents | Claude Code and Codex CLI | Separate coding/design engines available to Hermes and Open Design |
| Personalities | Hermes `SOUL.md` + isolated profiles | Durable identities and specialist roles should have separate memory, sessions, tokens, and gateway state |
| Live channels | Discord/Telegram; optional BlueBubbles | The channel is an interface, not the person's identity |
| Scheduling | Hermes cron | Daily facts, briefings, reminders, and maintenance jobs should be auditable and bounded |
| Safety | Smart approvals, secret redaction, checkpoints, pairing/allowlists | Capability without authority boundaries is not a Presence Stack |

## Optional infrastructure

- Docker/Compose for SearXNG, Firecrawl, and supporting services.
- Tailscale for private remote administration.
- NAS/SMB for the Obsidian vault and large assets.
- Separate Mac for BlueBubbles/iMessage.
- Proxmox/TrueNAS only when storage, RAM, controller passthrough, and backup justify them.
- Separate GPU host for Ollama/local models, local STT, or image/video workloads.
- A bounded public receptionist that relays to the private agent.
- A dashboard or mission-control layer for status; it is not the source of identity or truth.

## What this repository does not copy

- the reference owner's Presence Profile or `SOUL.md`;
- memories, Honcho peer cards, session history, or Obsidian vault;
- profile names, routing, channels, platform IDs, or contact details;
- provider tokens, OAuth grants, API keys, bot credentials, or account IDs;
- private network topology, hostnames, mounts, or service addresses;
- business/family/client authority rules;
- local source patches or deployment-specific overrides.

A new owner can reproduce the capability classes. They must build their own presence, permissions, and trust history.
