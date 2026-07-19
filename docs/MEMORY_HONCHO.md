# Honcho memory and daily facts

Hermes built-in memory stays active even when Honcho is enabled. Honcho adds cross-session user/agent modeling, semantic search, session context, and persistent conclusions.

## Choose cloud or self-hosted

### Fastest path: Honcho Cloud

```bash
hermes memory setup honcho
hermes memory status
```

Choose OAuth or enter an API key through the local setup flow. Do not paste the key into chat or Git.

### Self-hosted

Run Honcho using its current official repository/docs, including its database and model-provider requirements:

- <https://github.com/plastic-labs/honcho>
- <https://docs.honcho.dev/v3/guides/integrations/hermes>

Then configure Hermes with `hermes memory setup honcho` and the self-hosted base URL. Keep deployment credentials and `honcho.json` private.

## Recommended modes

Honcho's `recallMode` and `writeFrequency` solve different problems:

| Setting | Meaning |
|---|---|
| `hybrid` | automatic context injection plus explicit Honcho tools |
| `context` | automatic context only; tools hidden |
| `tools` | no automatic injection; agent searches/reasons explicitly |
| `writeFrequency: async` | save turns in the background after responses |

For an advanced agent with disciplined recall, `tools` + `async` keeps the prompt smaller and lets the agent query Honcho intentionally. For beginners who want continuity without remembering tool names, `hybrid` is simpler.

Example self-hosted shape—copy locally, then replace placeholders outside Git:

```json
{
  "baseUrl": "http://127.0.0.1:8000",
  "hosts": {
    "hermes": {
      "enabled": true,
      "aiPeer": "assistant",
      "peerName": "owner",
      "workspace": "presence-stack",
      "recallMode": "tools",
      "writeFrequency": "async",
      "saveMessages": true
    }
  }
}
```

Use one user peer plus one AI peer per durable Hermes profile. Do not reuse another deployment's workspace or peers.

## What gets saved continuously

With message saving enabled and asynchronous write frequency, Hermes sends conversation turns to Honcho after responses. Honcho builds representations/cards from those sessions. This provides ongoing capture; a separate daily cron is not required merely to ingest messages.

## Daily durable-fact review

Raw conversation storage and curated facts are different. Use a daily review only to promote stable facts, corrections, preferences, environment facts, and decisions into the right durable layer.

Recommended prompt for a once-daily Hermes cron:

```text
Review today's local Hermes sessions and Honcho context. Identify only durable facts that will still matter in a week: owner preferences/corrections, stable environment facts, long-lived relationships, and reusable lessons. Do not save task progress, completed-work logs, temporary paths, IDs, secrets, or raw transcripts. Deduplicate against built-in memory and existing Honcho conclusions. Save approved categories through the memory or honcho_conclude tools, then report counts and categories only. If nothing qualifies, stay silent.
```

Create it with `hermes cron create` or the Hermes cron UI. Attach only memory/session-search tools, keep owner data local, and test the job manually before scheduling. If the cron will write memories, decide whether the owner wants write approval/staging.

## Fact placement

| Information | Store |
|---|---|
| small critical fact always needed | built-in `MEMORY.md` or `USER.md` |
| exact prior conversation | session search |
| semantic context/user model | Honcho |
| reusable procedure | skill |
| long structured note/source of truth | Obsidian |
| temporary task state | task system/session, not durable memory |

## Verify

```bash
hermes memory status
hermes doctor
```

Then run a harmless sequence:

1. tell the agent a synthetic preference;
2. start a new session;
3. query Honcho search/context;
4. confirm the synthetic fact is found;
5. delete the synthetic conclusion/message if it should not persist.

Never test with secrets, addresses, real credentials, or sensitive family/client material.
