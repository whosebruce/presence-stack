# Presence Stack

**A privacy-first, agent-readable deployment harness for turning a fresh Hermes Agent into an owner-controlled digital presence.**

Presence Stack is for someone who wants a capable personal agent (memory, research, files, app connections, messaging) without copying another person's setup or handing a public chatbot the keys. It is a staged build order, a set of module guides, sanitized example configs, and four small Python helpers that plan and check the work. The helpers never install anything; you or your agent do that one gated stage at a time.

Status: v1.0.0, published July 2026. Model names and prices below are dated to that release.

## Quick start

Requires Python 3.10+. The helpers use only the standard library.

```bash
git clone https://github.com/whosebruce/presence-stack.git
cd presence-stack
python3 -m presence_stack.onboard
```

The onboarding asks about how you already communicate before it asks about software, and it collects no secrets. It writes `PLAN.md` and `plan.json` to `./presence-plan/` (gitignored). Use `--output-dir ~/.presence-stack/plan` to keep the plan with the rest of your private state, `--dry-run` to print it instead, or `--answers config/onboarding-example.json` to run from a JSON file.

Then give your agent [INSTALL_PROMPT.md](INSTALL_PROMPT.md). Agents that load `AGENTS.md` automatically get the installation contract and privacy boundaries directly; others should start with [AGENT_README.md](AGENT_README.md).

## The concept

People say they "vibe coded" an app. Presence Stack names the larger system around a person:

- **Presence Design** defines how a person should show up digitally: voice, values, knowledge, relationships, channels, boundaries, and decision rights.
- A **Presence Designer** conducts discovery and turns owner-approved source material into an explicit, reviewable Presence Profile.
- The **Presence Profile** is the private source of truth for identity, voice, values, knowledge, stories, relationships, and decision rights.
- The **Presence Persona** is the outward expression people encounter in an approved context.
- **Presence Engineering** implements and operates the model, memory, tools, channels, storage, security, approvals, and proof loops.
- The **Presence Stack** is the resulting system.

The owner remains principal and accountable. The digital presence can research, prepare, communicate, and carry delegated work, but it acts only under written standing authority or owner sign-off.

The phrase "Presence Engineering" has prior uses. This project does not claim to have invented the words. Its contribution is a practical, whole-person, owner-controlled stack. See the dated [category landscape](docs/CATEGORY_LANDSCAPE-2026-07.md).

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

The repository does **not** copy another person's accounts, API keys, configuration, messages, memories, Presence Profile, private network, authority rules, or trust history.

## Helper commands

| Command | What it does |
| --- | --- |
| `python3 -m presence_stack.onboard` | Plain-language interview that recommends a first channel, flags when a public receptionist boundary is needed, and writes a starter Presence Plan |
| `python3 -m presence_stack.estimate config/cost-example.json` | One-time, monthly, and first-year cost estimate from a JSON worksheet (OpenRouter credits, Honcho usage, electricity, fixed items) |
| `python3 -m presence_stack.recommend config/hardware-example.json` | Suggests a starting architecture from sanitized hardware facts, with warnings and deferred services |
| `python3 -m presence_stack.doctor` | Readiness report for Python, Git, Hermes, optional tools, Hermes config, and optional service settings; reports whether a key is set, never its value |

`estimate` and `recommend` accept `--json`. `doctor` accepts `--json` and `--strict` (non-zero exit when a required check is not ready). After `pip install -e .` the same tools are available as `presence-onboard`, `presence-cost`, `presence-recommend`, and `presence-doctor`.

## Three ways in

**Fresh agent or operator.** Clone the repository, paste [INSTALL_PROMPT.md](INSTALL_PROMPT.md) into the new agent, and let it read [AGENTS.md](AGENTS.md). It should ask one question at a time, get your approval for each module, and show real verification after every stage.

**Human installing by hand.** Read the [build order](docs/BUILD_ORDER.md), [requirements](docs/REQUIREMENTS.md), [security](docs/SECURITY.md), and the [Hermes supercharge guide](docs/HERMES_SUPERCHARGE.md), then only the module guides you need, then [verification](docs/VERIFICATION.md). For a longer private interview, use the written [Presence Intake](forms/PRESENCE_INTAKE.md).

**Existing Hermes user.** Run `python3 -m presence_stack.doctor` and use the report to choose missing modules. Do not replace a live `config.yaml` wholesale.

## Build order

Each stage is a gate: prove it works before moving on. Full commands are in [docs/BUILD_ORDER.md](docs/BUILD_ORDER.md).

| Stage | Gate |
| --- | --- |
| 0 | Owner design: intake, source permissions, and decision rights |
| 1 | Hardware/OS inventory and one tested restore |
| 2 | Base Hermes install, `hermes doctor`, and one successful chat |
| 3 | Secure defaults: secret redaction, smart approvals, checkpoints, least-privilege tools |
| 4 | One private owner channel with pairing/allowlist and unknown-user denial |
| 5 | Continuity: built-in memory and session search, optional Honcho |
| 6 | Research: SearXNG search and Firecrawl extraction (optional) |
| 7 | Durable files: Obsidian on a private SMB share (optional) |
| 8 | Action and creation tools: Composio/Google Workspace, Open Design and coding agents, specialist profiles (optional) |
| 9 | One bounded Presence Loop that returns evidence |
| 10 | Operational acceptance: reboot, restore, spend limits, privacy, unknown-user denial |

## Module guides

| Module | Guide | Required? |
| --- | --- | --- |
| Sanitized capability map | [REFERENCE_STACK.md](docs/REFERENCE_STACK.md) | Read first |
| Hardware/OS tiers | [REQUIREMENTS.md](docs/REQUIREMENTS.md), [SIZING.md](docs/SIZING.md) | Yes |
| Models, OpenRouter, budget | [MODELS_AND_BUDGET.md](docs/MODELS_AND_BUDGET.md), [COSTS-2026-07.md](docs/COSTS-2026-07.md) | Yes |
| Hermes safety/tools | [HERMES_SUPERCHARGE.md](docs/HERMES_SUPERCHARGE.md) | Yes |
| Channel selection/migration | [CHANNEL_CHOOSER.md](docs/CHANNEL_CHOOSER.md) | Yes |
| Presence Profile method | [PRESENCE_DESIGN.md](docs/PRESENCE_DESIGN.md) | Yes |
| Security boundaries | [SECURITY.md](docs/SECURITY.md) | Yes |
| Acceptance tests | [VERIFICATION.md](docs/VERIFICATION.md) | Yes |
| SearXNG + Firecrawl | [WEB_RESEARCH.md](docs/WEB_RESEARCH.md) | Optional |
| Honcho + daily facts | [MEMORY_HONCHO.md](docs/MEMORY_HONCHO.md) | Optional |
| Obsidian + SMB | [OBSIDIAN_SMB.md](docs/OBSIDIAN_SMB.md) | Optional |
| Composio + Google | [COMPOSIO_GOOGLE.md](docs/COMPOSIO_GOOGLE.md) | Optional |
| Open Design + coding CLIs | [OPEN_DESIGN_CODING_AGENTS.md](docs/OPEN_DESIGN_CODING_AGENTS.md) | Optional |
| Personalities + profiles | [PERSONALITIES_PROFILES.md](docs/PERSONALITIES_PROFILES.md) | Optional |

## Hardware tiers

| Tier | CPU | RAM | Disk | Use |
| --- | ---: | ---: | ---: | --- |
| Minimum Hermes | 2 cores | 4 GB | 20 GB | hosted model, light CLI/gateway |
| Comfortable personal stack | 4 cores | 8–16 GB | 50–100 GB | Hermes, SearXNG, integrations, light profiles |
| Reference-class orchestrator | 8 cores | 24–32 GB | 100+ GB | profiles, Firecrawl, Open Design, builds/browser |
| Optional local-AI/media host | 8–16 cores | 32–64+ GB | 1 TB+ | local models/STT/media; 16–24+ GB VRAM recommended |

The reference orchestration VM is about 8 vCPU, 24 GB RAM, and a 100 GB system disk. A separate 24 GB VRAM host handles optional local workloads. The primary model is hosted, so a GPU is not required for most functions. Details: [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md).

## Model pattern

- **Primary:** the strongest OpenAI Codex tool-calling model available through the owner's own OAuth account. At the v1.0.0 release that was GPT-5.6 Sol.
- **Vision:** Gemini 3.1 Flash Lite through OpenRouter, or the current equivalent the provider lists.
- **OpenRouter:** optional starter credit around **$50**, protected by a hard spend cap and alert.
- **Fallbacks:** explicit, tested, and separately capped. Never silent, uncontrolled spend.

Model catalogs and prices change. Use `hermes model` and the official provider pages rather than treating this README as a catalog.

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

Hermes credentials stay in Hermes' own `.env`/auth/MCP token stores. [.env.example](.env.example) lists the variable names the doctor looks for; fill a copy under `~/.presence-stack/`, never in the repository. `.gitignore` excludes real enrollment files, secrets, inventories, databases, logs, reports, and generated Presence Plans.

## Public receptionist boundary

```text
Unknown sender
  → bounded FAQ/intake presence
  → structured summary
  → owner queue
  → explicit sign-off
  → private Hermes performs only the narrow approved action
```

Unknown users must never enter the same full-power agent that can read private files, run shell commands, send arbitrary messages, administer accounts, or make payments. [Local-First AI Receptionist](https://github.com/whosebruce/local-first-ai-receptionist) is one implementation of this boundary.

## Included examples

- [Sanitized Hermes config sections](config/hermes-sanitized.yaml.example)
- [Self-hosted Honcho shape](config/honcho-selfhost.example.json)
- [Generic SOUL template](templates/SOUL.md.example)
- [Loopback SearXNG Compose](deploy/searxng/compose.yaml)
- [Onboarding answers](config/onboarding-example.json), [cost worksheet](config/cost-example.json), and [hardware facts](config/hardware-example.json) for the helpers

Examples contain no working credentials and must be adapted locally.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_repo.py
python3 scripts/privacy_scan.py
python3 -m presence_stack.doctor
```

`verify_repo.py` checks required files and that every local Markdown link resolves. The privacy scanner checks the working tree, the exact Git index, and reachable history, and prints category, file, and line only. Operator-specific markers belong in a gitignored `local-patterns.txt`, one literal per line. GitHub Actions runs the tests, the three example helper runs, `doctor --json`, and both scripts on every push and pull request.

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

MIT. See [LICENSE](LICENSE). Maintained by [@whosebruce](https://github.com/whosebruce).
