# Build order: from fresh Hermes to a capable Presence Stack

This runbook produces a system with similar *capability classes* to the reference stack without copying private configuration or identity.

## Stage 0 — owner design gate

Run:

```bash
python3 -m presence_stack.onboard
```

Create private, owner-reviewed artifacts under `~/.presence-stack/presence-profile/`:

- `IDENTITY.md`
- `VOICE.md`
- `VALUES.md`
- `STORY_BANK.md`
- `KNOWLEDGE_MAP.md`
- `DECISION_RIGHTS.md`
- `RELATIONSHIPS.md`
- `SOURCE_MANIFEST.csv`
- `EVALS.md`

Do not continue until source permissions and decision rights are explicit.

## Stage 1 — inventory and backup gate

Record hardware and OS facts locally, not in Git. Run the adviser:

```bash
python3 -m presence_stack.recommend config/hardware-example.json
```

Test one restore before repartitioning, installing Proxmox, changing storage, or mounting the only copy of an Obsidian vault.

## Stage 2 — base Hermes gate

Use the live official installation instructions:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes doctor
hermes chat -q "Reply with: base chat works"
```

Desktop users may use the official Hermes Desktop installer instead. Do not add integrations until the base chat and doctor pass.

## Stage 3 — secure defaults gate

```bash
hermes config set security.redact_secrets true
hermes config set approvals.mode smart
hermes config set checkpoints.enabled true
hermes tools
```

Enable only the toolsets needed by the owner. Start a new session after changing toolsets. Keep terminal/file access private; use a Docker terminal backend for higher isolation when appropriate.

## Stage 4 — private channel gate

```bash
hermes gateway setup
hermes gateway install
hermes gateway status
```

Use the channel the owner already uses. Prove:

1. the owner can send and receive a harmless message;
2. a stranger is denied, paired, or routed to a bounded receptionist;
3. the gateway returns after reboot/logout.

## Stage 5 — continuity gate

Built-in memory and session search are already available. Verify them before adding an external provider. If deeper modeling is useful, follow `MEMORY_HONCHO.md`.

## Stage 6 — research gate

Follow `WEB_RESEARCH.md`:

- SearXNG for private/free search;
- Firecrawl for extraction;
- a cheap auxiliary model for long-page summarization if desired.

Prove one known search and one known extraction separately.

## Stage 7 — durable files gate

Follow `OBSIDIAN_SMB.md`. Use one canonical vault and a tested backup. Mount only the share/dataset the agent needs, not unrestricted NAS administration.

## Stage 8 — action and creation tools gate

Install only what has a real use case:

- Composio + Google Workspace: `COMPOSIO_GOOGLE.md`
- Open Design + Claude Code/Codex: `OPEN_DESIGN_CODING_AGENTS.md`
- specialist profiles/personas: `PERSONALITIES_PROFILES.md`

Each external app starts with a read-only proof before write actions.

## Stage 9 — first Presence Loop

Implement one bounded loop:

```text
Observe → Prepare → Gate → Act → Prove → Learn
```

Good first loops:

- daily calendar/inbox briefing that drafts but does not send;
- research brief saved to Obsidian with sources;
- meeting preparation with owner sign-off;
- weekly project summary with links and unresolved decisions.

## Stage 10 — operational acceptance

Run `docs/VERIFICATION.md`. The stack is operational only when:

- base chat, tools, memory, search/extract, and chosen integrations pass;
- owner authorization and unknown-user denial pass;
- services survive a reboot;
- one backup restore passes;
- spend limits and credential revocation paths are documented;
- no owner secrets or generated private state are tracked by Git.
