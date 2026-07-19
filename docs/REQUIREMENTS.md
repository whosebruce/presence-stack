# Hardware, OS, and service requirements

These tiers separate the lightweight agent from self-hosted research, storage, media, and local inference. They are planning envelopes, not guarantees.

## Supported starting platforms

Hermes supports Linux, macOS, WSL2, native Windows, and Android/Termux. For an always-on server, current Ubuntu Server or Debian is the simplest default. macOS is required for BlueBubbles/iMessage.

## Tier A — minimum functional Hermes

Use when the model and web tools are hosted.

- 2 CPU cores
- 4 GB RAM
- 20 GB free SSD
- stable internet
- no GPU required

This can run Hermes CLI, built-in memory, light tools, and one gateway, but browser builds, multiple profiles, Firecrawl, and concurrent agents can exhaust it.

## Tier B — comfortable personal Presence Stack

Recommended minimum for a person who wants the same general functions as the reference stack while using hosted models:

- 4 CPU cores
- 8–16 GB RAM
- 50–100 GB SSD
- wired network when always-on
- Docker/Compose
- tested backup
- optional NAS share

This comfortably supports Hermes, one or two gateways/profiles, SearXNG, moderate tooling, Obsidian/SMB access, Composio, and coding CLIs. Put Firecrawl on the same host only if memory remains healthy.

## Tier C — reference-class orchestration host

For several profiles, local MCP services, Open Design, coding agents, heavier browser/build workloads, and colocated SearXNG/Firecrawl:

- 8 CPU cores
- 24–32 GB RAM
- 100+ GB SSD, with additional space for projects/artifacts
- 4 GB swap as a safety net, not a substitute for RAM
- Docker/Compose
- separate backup target
- optional NAS and Tailscale

The live reference orchestration VM is in this class: 8 virtual CPUs, about 24 GB RAM, and roughly a 100 GB system disk. That is evidence of a comfortable deployment, not a mandatory minimum.

## Tier D — local AI/media host

Local inference is optional and separate from Hermes' hosted-model requirements.

For useful large local text/vision models, local Whisper, media transcoding, or video generation:

- 8–16 CPU cores
- 32–64+ GB RAM
- 1 TB or larger NVMe if storing models/media
- NVIDIA GPU with 16–24+ GB VRAM for serious workloads, or Apple Silicon sized to the model
- additional power, cooling, and backup planning

The reference stack uses a separate 24 GB VRAM GPU host for optional local workloads. The primary Hermes model remains hosted; a GPU is not required to reproduce most functions.

## Component planning allocations

| Component | Lean RAM | Comfortable RAM | Notes |
|---|---:|---:|---|
| Hermes with hosted model | 2–4 GB | 4–8 GB | Browser, builds, and subagents increase demand |
| SearXNG | 0.5–1 GB | 1–2 GB | Search only |
| Firecrawl stack | 4 GB | 8+ GB | API, browser worker, queues, cache/database; concurrency matters |
| Open Design | 2–4 GB | 4–8 GB | Node build and browser export can spike |
| Honcho client | small | small | Cloud mode; self-hosted server/database needs separate sizing |
| Jellyfin | 4 GB | 8 GB | iGPU/GPU matters for transcoding |
| TrueNAS | 8 GB minimum | 16+ GB | Storage topology and backup matter more than copying a lab design |

## Storage and network cautions

- ZFS/RAID redundancy is not backup.
- Do not virtualize important TrueNAS pools on ordinary virtual disks.
- Do not mount an entire NAS admin surface into Hermes.
- SMB performance and safety depend on one canonical vault, locking behavior, and backups.
- Use Tailscale/VPN instead of public admin ports.
- BlueBubbles requires an always-on Mac signed into the intended Messages identity.

## Model requirement

Choose a strong tool-calling model with a large context window. Hermes and model capabilities change quickly, so use `hermes model` and the live provider docs rather than freezing an old model list into automation.
