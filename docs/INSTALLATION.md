# Installation runbook

This is the short index. The executable sequence is [BUILD_ORDER.md](BUILD_ORDER.md).

## 0. Clone and inspect

```bash
git clone https://github.com/whosebruce/presence-stack.git
cd presence-stack
python3 scripts/verify_repo.py
python3 scripts/privacy_scan.py
```

Agents should read [../AGENTS.md](../AGENTS.md) and [../INSTALL_PROMPT.md](../INSTALL_PROMPT.md).

## 1. Design before install

```bash
python3 -m presence_stack.onboard
```

Decide:

- first channel and audience;
- approved sources;
- Presence Profile scope;
- standing authority, sign-off, and forbidden actions;
- first 30-day Presence Loop;
- hardware tier and budget.

## 2. Inventory and backup

Record CPU, RAM, virtualization, disks/SMART, controller, NIC, GPU/iGPU, OS/data, network, UPS, and backup destination in owner-private storage. Test one restore before changing storage or installing a hypervisor.

## 3. Install Hermes

Use the live official docs: <https://hermes-agent.nousresearch.com/docs/getting-started/installation>

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes doctor
hermes chat -q "Reply with exactly: base chat works"
```

Prove base chat before configuring gateways, memory providers, MCP, or self-hosted services.

## 4. Apply secure defaults

Follow [HERMES_SUPERCHARGE.md](HERMES_SUPERCHARGE.md). Enable secret redaction, smart/manual approvals, checkpoints, and only required tools.

## 5. Add modules in order

1. private owner channel;
2. built-in memory/session search;
3. optional Honcho;
4. optional SearXNG/Firecrawl;
5. optional Obsidian/SMB;
6. optional Composio/Google Workspace;
7. optional Open Design and coding agents;
8. optional specialist profiles;
9. optional bounded receptionist;
10. optional storage/media/local inference.

Every optional module has a dedicated guide linked from [README.md](../README.md).

## 6. Prove one Presence Loop

The loop must return evidence:

```text
Observe → Prepare → Gate → Act → Prove → Learn
```

Draft-first loops are safest for the first 30 days.

## 7. Accept operationally

Run [VERIFICATION.md](VERIFICATION.md). Verify authorization, unknown-user denial, reboot persistence, backup restore, spend caps, revocation paths, privacy scan, and no owner-private Git state.

Only then call the stack operational.
