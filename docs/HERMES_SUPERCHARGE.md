# Hermes supercharge guide

The goal is not to install every tool. It is to give a fresh Hermes a strong model, safe actions, durable identity, searchable history, useful skills, and verified integrations.

## 1. Install and prove the base

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes doctor
hermes chat -q "Reply with exactly: Hermes base works"
```

Official docs: <https://hermes-agent.nousresearch.com/docs/>

## 2. Secure defaults

```bash
hermes config set security.redact_secrets true
hermes config set privacy.redact_pii true
hermes config set approvals.mode smart
hermes config set checkpoints.enabled true
```

Restart the session/gateway after changes that are read at startup. Keep cron approvals denied or tightly scoped; unattended jobs cannot ask the owner a question.

## 3. Enable capability classes deliberately

```bash
hermes tools
hermes tools list
```

Recommended private-owner toolsets when needed:

- web/search and extract;
- browser;
- terminal and file;
- code execution;
- vision and image generation;
- memory and session search;
- skills;
- cron;
- delegation;
- messaging;
- MCP.

A public receptionist should get a much smaller set.

## 4. Identity and project context

- `~/.hermes/SOUL.md` — durable agent identity/voice.
- `AGENTS.md` — project architecture, commands, boundaries, and conventions.
- `/personality` — temporary session overlay.
- profiles — separate agents with separate config, memory, sessions, skills, tokens, and gateways.

See `PERSONALITIES_PROFILES.md`.

## 5. Memory layers

Use each layer for a different job:

| Layer | Purpose |
|---|---|
| `MEMORY.md` / `USER.md` | Small curated facts injected every session |
| session search | Find actual prior messages on demand |
| skills | Reusable procedures learned from work |
| Honcho | Deep cross-session context, peer modeling, semantic search, conclusions |
| Obsidian | Human-readable durable source of truth and large structured context |

Do not dump raw archives into always-loaded memory.

## 6. Messaging and scheduling

```bash
hermes gateway setup
hermes gateway install
hermes gateway status
hermes cron list
```

Pair/allowlist the owner. Create recurring work only after the equivalent manual loop succeeds. Require receipts such as message IDs, URLs, diffs, files, or status codes.

## 7. MCP and external tools

```bash
hermes mcp
hermes mcp list
hermes mcp test <server-name>
```

Read each MCP manifest/source and select only the tools required. OAuth completion is not proof; run a read-only tool against the exact target app.

## 8. Profiles and subagents

Profiles are durable independent agents. Delegated subagents are short-lived workers. Use profiles for distinct personalities, channels, tokens, memories, and standing responsibilities; use subagents for bounded parallel tasks.

## 9. Health and drift

```bash
hermes --version
hermes config check
hermes doctor
hermes status --all
hermes memory status
hermes mcp list
hermes profile list
```

Update deliberately, preserve local config, and verify after updates. Do not paste a live `config.yaml` into public repositories; build sanitized examples instead.
