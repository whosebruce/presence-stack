# Presence Stack

**A privacy-first, agent-readable deployment harness for turning a fresh Hermes Agent into an owner-controlled digital presence.**

Repository: <https://github.com/whosebruce/presence-stack>

```bash
git clone https://github.com/whosebruce/presence-stack.git
cd presence-stack
python3 -m presence_stack.onboard
```

Then give your agent [INSTALL_PROMPT.md](INSTALL_PROMPT.md). Agents that automatically read `AGENTS.md` will receive the installation contract and privacy boundaries directly.

## What this gives you

This repository documents and verifies the capability classes behind a mature Hermes setup:

- current Hermes Agent install and secure defaults;
- a strong primary model plus explicit fallback/budget policy;
- OpenRouter-funded auxiliary vision;
- self-hosted SearXNG search and Firecrawl extraction;
- built-in memory, session search, skills, and optional Honcho;
- daily durable-fact review without saving temporary noise;
- Obsidian as a human-readable source of truth on a private SMB share;
- Composio MCP with Google Workspace OAuth;
- Open Design connected to Hermes, Claude Code, and Codex CLI;
- durable `SOUL.md` identity and separate specialist profiles;
- Discord, Telegram, Slack, CLI/Desktop, or optional BlueBubbles/iMessage;
- cron, subagents, approvals, checkpoints, receipts, and verification;
- hardware tiers from a small hosted-model box to a separate 24 GB VRAM local-AI host.

It does **not** copy another person's accounts, API keys, configuration, messages, memories, Presence Profile, private network, authority rules, or trust history.

## The concept

People say, “I vibe coded this app.” Presence Stack gives us language for a larger system:

- **Presence Design** defines how a person should show up digitally: voice, values, knowledge, relationships, channels, boundaries, and decision rights.
- A **Presence Designer** conducts discovery and turns owner-approved source material into an explicit, reviewable Presence Profile.
- The **Presence Profile** is the private source of truth for identity, voice, values, knowledge, stories, relationships, and decision rights.
- The **Presence Persona** is the outward expression people encounter in an approved context.
- **Presence Engineering** implements and operates the model, memory, tools, channels, storage, security, approvals, and proof loops.
- The **Presence Stack** is the resulting system.

The owner remains principal and accountable. The digital presence can research, prepare, communicate, and carry delegated work, but it acts only under written standing authority or owner sign-off.

The phrase “Presence Engineering” has prior uses. This project does not claim to have invented the words. Its contribution is a practical, whole-person, owner-controlled stack. See the dated [category landscape](docs/CATEGORY_LANDSCAPE-2026-07.md).

## A second brain remembers. A presence acts.

```text
Owner-approved sources + current corrections
                    ↓
             Presence Profile
                    ↓
       Identity + memory + decision rights
                    ↓
     Hermes + tools + files + app connections
                    ↓
             Presence Persona
                    ↓
      Observe → Prepare → Gate → Act → Prove → Learn
```

A channel is only an interface. The durable identity stays portable across Telegram, Discord, Slack, iMessage, CLI/Desktop, and future channels.

## Start with questions, not software

A newcomer should not need to know what Hermes, Honcho, MCP, Firecrawl, or an API key is.

```bash
python3 -m presence_stack.onboard
```

The onboarding begins with ordinary questions:

1. Where do you already spend communication time?
2. Who should interact with the presence first?
3. Do you need one conversation or projects/channels/threads?
4. What should become easier in the first 30 days?
5. Which videos, writing, audio, and documents may be studied?
6. What may the system prepare, do under standing authority, pause for sign-off, or never do?
7. What evidence must return after an action?

Use the written [Presence Intake](forms/PRESENCE_INTAKE.md) for a longer private interview.

## Fast paths

### 1. Fresh agent/operator

1. Clone the repository.
2. Copy [INSTALL_PROMPT.md](INSTALL_PROMPT.md) into the new agent.
3. Let it read [AGENTS.md](AGENTS.md).
4. Answer one question at a time.
5. Approve modules in stages.
6. Require real verification after every stage.

### 2. Human installing manually

Read:

1. [Build order](docs/BUILD_ORDER.md)
2. [Requirements](docs/REQUIREMENTS.md)
3. [Security](docs/SECURITY.md)
4. [Hermes supercharge guide](docs/HERMES_SUPERCHARGE.md)
5. The module guides you actually need
6. [Verification](docs/VERIFICATION.md)

### 3. Existing Hermes user

Run:

```bash
python3 -m presence_stack.doctor
```

It reports command/configuration presence without displaying secret values. Use the report to choose missing modules; do not replace a live `config.yaml` wholesale.

## Recommended build order

1. Presence intake, source permissions, channel, and decision rights.
2. Hardware/network/storage inventory and tested backup.
3. Base Hermes, model login, `hermes doctor`, and one successful chat.
4. Secret redaction, smart approvals, checkpoints, and least-privilege tools.
5. One private owner channel with allowlist/pairing.
6. Built-in memory and session search.
7. Optional Honcho.
8. Optional SearXNG + Firecrawl.
9. Optional Obsidian/SMB.
10. Optional Composio/Google Workspace and Open Design/coding agents.
11. Optional specialist profiles.
12. One bounded Presence Loop with evidence.
13. Reboot, restore, spend-limit, privacy, and unknown-user-denial tests.

Full sequence: [docs/BUILD_ORDER.md](docs/BUILD_ORDER.md).

## Capability modules

| Module | Guide | Required? |
|---|---|---|
| Sanitized capability map | [REFERENCE_STACK.md](docs/REFERENCE_STACK.md) | Read first |
| Hardware/OS tiers | [REQUIREMENTS.md](docs/REQUIREMENTS.md) | Yes |
| Models, OpenRouter, budget | [MODELS_AND_BUDGET.md](docs/MODELS_AND_BUDGET.md) | Yes |
| Hermes safety/tools | [HERMES_SUPERCHARGE.md](docs/HERMES_SUPERCHARGE.md) | Yes |
| SearXNG + Firecrawl | [WEB_RESEARCH.md](docs/WEB_RESEARCH.md) | Optional |
| Honcho + daily facts | [MEMORY_HONCHO.md](docs/MEMORY_HONCHO.md) | Optional |
| Obsidian + SMB | [OBSIDIAN_SMB.md](docs/OBSIDIAN_SMB.md) | Optional |
| Composio + Google | [COMPOSIO_GOOGLE.md](docs/COMPOSIO_GOOGLE.md) | Optional |
| Open Design + coding CLIs | [OPEN_DESIGN_CODING_AGENTS.md](docs/OPEN_DESIGN_CODING_AGENTS.md) | Optional |
| Personalities + profiles | [PERSONALITIES_PROFILES.md](docs/PERSONALITIES_PROFILES.md) | Optional |
| Channel selection/migration | [CHANNEL_CHOOSER.md](docs/CHANNEL_CHOOSER.md) | Yes |
| Presence Profile method | [PRESENCE_DESIGN.md](docs/PRESENCE_DESIGN.md) | Yes |
| Security boundaries | [SECURITY.md](docs/SECURITY.md) | Yes |
| Acceptance tests | [VERIFICATION.md](docs/VERIFICATION.md) | Yes |

## Minimum hardware

| Tier | CPU | RAM | Disk | Use |
|---|---:|---:|---:|---|
| Minimum Hermes | 2 cores | 4 GB | 20 GB | hosted model, light CLI/gateway |
| Comfortable personal stack | 4 cores | 8–16 GB | 50–100 GB | Hermes, SearXNG, integrations, light profiles |
| Reference-class orchestrator | 8 cores | 24–32 GB | 100+ GB | profiles, Firecrawl, Open Design, builds/browser |
| Optional local-AI/media host | 8–16 cores | 32–64+ GB | 1 TB+ | local models/STT/media; 16–24+ GB VRAM recommended |

The reference orchestration VM is approximately 8 vCPU, 24 GB RAM, and a 100 GB system disk. A separate 24 GB VRAM host handles optional local workloads. The primary model is hosted, so a GPU is not required for most functions.

Details: [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md).

## Recommended model pattern

- **Primary:** strongest current OpenAI Codex tool-calling model available through the owner's OAuth account. At this release, the reference uses GPT-5.6 Sol.
- **Vision:** Gemini 3.1 Flash Lite through OpenRouter, or the current equivalent shown by the provider.
- **OpenRouter:** optional starter credit around **$50**, protected by a hard spend cap and alert.
- **Fallbacks:** explicit, tested, and separately capped—never silent uncontrolled spend.

Model catalogs and prices change. Use `hermes model` and official provider pages rather than treating this README as a permanent catalog.

## Private state stays private

Recommended owner-private root:

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

Hermes credentials stay in Hermes' own `.env`/auth/MCP token stores. This repository ignores real enrollment, secrets, inventories, databases, logs, reports, and generated Presence Plans.

## Public receptionist boundary

```text
Unknown sender
  → bounded FAQ/intake presence
  → structured summary
  → owner queue
  → explicit sign-off
  → private Hermes performs only the narrow approved action
```

Unknown users must never enter the same full-power agent that can read private files, run shell commands, send arbitrary messages, administer accounts, or make payments.

## Included examples

- [sanitized Hermes config sections](config/hermes-sanitized.yaml.example)
- [self-hosted Honcho shape](config/honcho-selfhost.example.json)
- [generic SOUL template](templates/SOUL.md.example)
- [loopback SearXNG Compose](deploy/searxng/compose.yaml)
- onboarding, cost, and hardware example JSON

Examples contain no working credentials and must be adapted locally.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_repo.py
python3 scripts/privacy_scan.py
python3 -m presence_stack.doctor
```

The privacy scanner checks the working tree and, once Git exists, the exact index and reachable history. Operator-specific markers belong in gitignored `local-patterns.txt`.

## Non-goals

- undisclosed impersonation, voice cloning, or deepfakes;
- scraping private material without permission;
- freezing a person into old beliefs;
- sharing another person's accounts, identity, memories, or API credentials;
- connecting the public to a privileged agent;
- installing every service regardless of need;
- claiming local models equal frontier hosted models;
- treating RAID/ZFS or sync as backup;
- publishing a live `config.yaml` with identifiers or private routes.

## License

MIT. See [LICENSE](LICENSE).
