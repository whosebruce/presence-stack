# Verification and acceptance tests

Do not call the stack complete because files exist. Exercise the real paths.

## Repository checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_repo.py
python3 scripts/privacy_scan.py
```

## Base Hermes

```bash
hermes --version
hermes config check
hermes doctor
hermes chat -q "Reply with exactly: base chat works"
```

Expected: current config version, no blocking doctor issues, and exact chat response.

## Security

```bash
hermes config get approvals.mode
hermes config get security.redact_secrets
hermes config get checkpoints.enabled
hermes tools list
```

Expected: approvals are `smart` or `manual`; redaction enabled; checkpoints enabled where wanted; no unnecessary tools on public profiles.

## Memory

```bash
hermes memory status
```

Run a synthetic write/recall/delete test. Confirm new sessions can recover the synthetic fact through the intended memory layer. Do not use personal or secret test content.

## Search and extract

```bash
curl -fsS "http://127.0.0.1:8888/search?q=hermes+agent&format=json" \
  | python3 -c 'import json,sys; assert json.load(sys.stdin).get("results"); print("SearXNG: PASS")'
```

Then ask Hermes to search for and extract a stable official page. Record separate pass/fail results.

## Obsidian/SMB

```bash
findmnt -T /mnt/obsidian-vault
mountpoint -q /mnt/obsidian-vault
```

Create/read/delete a synthetic note only after owner approval. Restore one test note from backup into a temporary location.

## MCP

```bash
hermes mcp list
hermes mcp test composio
hermes mcp test open-design
```

MCP connection is only layer one. Run one read-only tool for the exact connected app and one synthetic Open Design artifact.

## Coding agents

```bash
claude --version
claude doctor
codex --version
```

Run a harmless one-file temp project smoke test if those tools are part of the deployment.

## Messaging/gateway

```bash
hermes gateway status
```

Prove:

- owner receives a harmless reply;
- attachment behavior is as intended;
- unknown user is denied/paired/bounded;
- gateway restarts after logout/reboot;
- public profile cannot invoke private tools.

## Profiles

```bash
hermes profile list
```

For each profile, verify identity, memory, working directory, token separation, tool scope, and forbidden actions.

## Presence Loop

A complete loop must return evidence:

```text
Observed request
Prepared result
Applied authority/sign-off rule
Performed bounded action
Returned receipt/URL/file/diff/status
Captured only stable learning
```

## Cost and limits

- provider spend cap visible in provider dashboard;
- OpenRouter low-balance/spend alert enabled if used;
- scheduled jobs inventoried;
- no unbounded crawl/concurrency loop;
- fallback provider and spend behavior tested.

## Reboot and disaster recovery

- intended services enabled and active after reboot;
- backup restore verified;
- credential revocation steps documented;
- owner knows how to stop gateways/cron jobs;
- owner-private artifacts are not tracked by Git.

## Public release gate

Before publishing:

```bash
git diff --check
git fsck --full
python3 scripts/privacy_scan.py --surface tree --surface index --surface history
```

After publishing, clone the public HTTPS URL into a fresh temporary directory and rerun the complete repository checks. Confirm the remote HEAD equals the reviewed local commit.
