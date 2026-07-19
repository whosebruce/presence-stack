# Sizing and the Agent-vs-Jellyfin Decision

## Facts to collect before choosing

- exact CPU model and generation;
- Intel iGPU/Quick Sync, dedicated GPU, or neither;
- installed/max RAM;
- OS/boot disk and number/type/capacity of data disks;
- whether an HBA/storage controller can be passed through;
- Ethernet speed and internet upload;
- number of local/remote Jellyfin users and expected 1080p/4K transcodes;
- cloud-model versus local-model Hermes;
- whether an always-on Mac already exists for BlueBubbles;
- backup destination and UPS availability.

Use `forms/PRESENCE_INTAKE.md` and the included adviser.

## Resource envelope

| Component | Lean planning allocation | Important qualifier |
|---|---:|---|
| Proxmox host | 2 GB RAM + guest needs | ZFS/Ceph need more; production requires headroom. |
| TrueNAS | 8 GB RAM minimum | Two same-sized storage devices are the published starting point; virtual disks are not recommended for important data. |
| Jellyfin Linux | 4 GB can work; 8 GB recommended | GPU/iGPU matters more than CPU for video transcoding. Direct play is far lighter. |
| Hermes with hosted model | 2–4 GB lean; 4–8 GB comfortable | Browser automation, builds, and concurrent tools increase needs. |
| SearXNG + Firecrawl | 2–8+ GB combined | Firecrawl's supporting services and crawl concurrency can grow quickly. |
| Local LLM | hardware-specific | 64K context is the current Hermes minimum; measure real model residency and concurrency. |

These are planning allocations, not guarantees.

## Decision rules

### Choose Hermes first when

- the primary value is inbox/message triage, research, reminders, documents, or remote task execution;
- the model will be hosted through ChatGPT/Codex, Nous, OpenRouter, or another provider;
- RAM is limited and there is no useful transcoding GPU;
- the owner has little media or already streams elsewhere.

### Choose Jellyfin first when

- the primary value is a private media library;
- media disks already exist;
- most clients direct-play, or a supported Intel iGPU is available;
- remote upload bandwidth and user count are known.

### Run both when

- there is at least 16 GB RAM for a deliberately lean non-TrueNAS layout, or preferably 32 GB for the separated Proxmox layout;
- storage and backup are solved;
- Jellyfin has a hardware acceleration path;
- Hermes uses a hosted model;
- service isolation and reboot recovery have been tested.

## Why Intel matters for Jellyfin

Jellyfin's current guide recommends Intel N100 or newer suitable Intel integrated graphics for low-power systems and 8 GB RAM for an average deployment. It explicitly warns that CPU-only video transcoding—especially HDR tone mapping—can overwhelm powerful CPUs. Linux QSV is the preferred mainstream Intel acceleration path.

## Virtualized TrueNAS warning

TrueNAS documents 8 GB RAM as its minimum and warns against regular production virtualization backed by ordinary virtual disks. If virtualizing it under Proxmox, pass through the HBA/controller or disks and keep independent backups. If the owner's box is small or the controller layout is unknown, use simpler Linux storage first rather than copying a large-lab design blindly.

## Purchase target if the old box is inadequate

For a compact 2026 starter that can run hosted-model Hermes plus Jellyfin:

- Intel N100 or a used 8th-generation-or-newer Intel desktop/SFF with non-`F` CPU;
- 16 GB RAM minimum, 32 GB preferred for virtualization/services;
- 100+ GB SSD for OS, Jellyfin metadata, and transcode cache;
- CMR data disks sized for the library and a separate backup;
- wired gigabit Ethernet;
- UPS for storage reliability.

An N100 is excellent for low-power Jellyfin and a cloud-model agent, but many mini PCs have poor internal disk expansion. Storage topology—not benchmark score—may make a used SFF/tower the better TrueNAS choice.

## First verification tests

- one real Hermes tool call and a resumed session;
- one Jellyfin direct-play stream;
- one forced lower-bitrate transcode while observing iGPU use;
- simultaneous transcode + Hermes tool call;
- reboot and confirm every intended service returns;
- restore one test file from backup.
