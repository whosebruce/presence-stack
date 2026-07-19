# Composio and Google Workspace

Composio is the broad SaaS action layer. Google Workspace is one set of OAuth-connected apps behind it. This is separate from the model provider and separate from Google/Gemini API keys.

## Install/connect Composio as an MCP server

Use the current Composio MCP endpoint and authentication method shown by Composio. A generic Hermes shape is:

```yaml
mcp_servers:
  composio:
    url: "https://connect.composio.dev/mcp"
    headers:
      x-consumer-api-key: "${COMPOSIO_API_KEY}"
    connect_timeout: 60
    timeout: 180
```

Store the real key locally through Hermes config/setup so it lands in `~/.hermes/.env`, not the YAML example or Git:

```bash
hermes config set COMPOSIO_API_KEY
```

If the current Composio dashboard provides a tool-router-specific MCP URL instead, use that private URL locally and do not publish it.

Restart Hermes, then verify:

```bash
hermes mcp test composio
hermes mcp list
```

A successful MCP connection means tools can be discovered. It does not prove any Google account is connected.

## Connect Google Workspace

From Composio's connection flow, connect only the apps needed:

- Gmail;
- Google Calendar;
- Google Drive;
- Google Docs;
- Google Sheets.

Prefer a dedicated assistant/service identity or a narrowly scoped owner-approved account. Review requested scopes before authorization. Do not grant write/send/delete access merely because it is available.

## Proof sequence

Run read-only proof calls first:

1. identity/account status;
2. list a small number of calendar events;
3. search Drive for a synthetic test folder;
4. read a synthetic Google Doc;
5. read a synthetic Sheet;
6. fetch Gmail metadata for a synthetic test message.

Do not start with sending email, creating meetings, moving files, or editing documents.

After read proof, test narrow writes with synthetic artifacts:

- create a draft email but do not send;
- create a private test document;
- write to a test spreadsheet tab;
- create then delete a test calendar event with owner approval.

Report returned IDs/URLs and delete synthetic artifacts when appropriate.

## Authority map

| Action | Recommended default |
|---|---|
| search/read own Drive/Docs | standing authority within approved folders |
| summarize inbox metadata | standing authority |
| draft email | standing authority |
| send/reply | sign-off required until trust is earned |
| create calendar hold | sign-off or narrow standing rule |
| invite external guests | sign-off required |
| edit shared/client document | sign-off required |
| delete mail/files/events | forbidden or explicit one-time approval |
| change OAuth/security settings | owner only |

## Google auth is not Gemini auth

Google Workspace OAuth tokens do not automatically authorize Gemini model calls. Vision/model routing requires a Gemini API key, Vertex credentials, OpenRouter, Nous Portal, or another supported provider.

## Credential hygiene

- do not paste OAuth callbacks, refresh tokens, or API keys into chat;
- do not commit Composio router URLs if they contain private identifiers;
- verify connection status after OAuth;
- revoke unused Google/Composio grants;
- keep an audit of which app/tool can read or mutate which data;
- start with drafts and synthetic artifacts.
