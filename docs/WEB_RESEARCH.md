# Self-hosted web research: SearXNG + Firecrawl

The reference pattern splits search from extraction:

```text
query → SearXNG → ranked URLs
URL → Firecrawl → readable Markdown/text
long page → auxiliary model → compact context
```

SearXNG is search-only. Firecrawl handles extraction and can also search, but the split keeps routine search private and inexpensive.

## SearXNG

### Install

```bash
mkdir -p "$HOME/presence-services/searxng/config"
cd "$HOME/presence-services/searxng"
cp /path/to/presence-stack/deploy/searxng/compose.yaml .
cp /path/to/presence-stack/deploy/searxng/settings.yml config/settings.yml
docker compose up -d
```

The included deployment binds to loopback by default. Replace the generated `server.secret_key` locally before any broader exposure; do not commit it.

### Required JSON output

Hermes needs JSON search results. The example enables:

```yaml
search:
  formats:
    - html
    - json
```

Verify:

```bash
curl -fsS "http://127.0.0.1:8888/search?q=hermes+agent&format=json" \
  | python3 -c 'import json,sys; print(len(json.load(sys.stdin).get("results", [])))'
```

A positive result count is the gate. HTTP 403 usually means JSON output is still disabled.

## Firecrawl

Self-hosting Firecrawl changes frequently and includes API, browser worker, Redis/queues, and database services. Use the official compose stack rather than copying a stale private compose file:

```bash
git clone https://github.com/firecrawl/firecrawl.git "$HOME/presence-services/firecrawl"
cd "$HOME/presence-services/firecrawl"
# Read SELF_HOST.md and the supplied .env.example for the checked-out release.
# Configure locally; do not commit the resulting .env.
docker compose up -d
```

Official guide: <https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md>

For a private loopback/LAN instance, choose intentionally whether database authentication is enabled. Disabling auth is acceptable only when network controls prevent untrusted access. Self-hosted Firecrawl does not include every proprietary cloud anti-bot capability; protected sites may fail.

Verify the health/API route specified by the checked-out Firecrawl release, then scrape one stable public page. Record status and output length, not scraped private content.

## Wire Hermes

Use Hermes' config command so secrets and settings go to the right store:

```bash
hermes config set SEARXNG_URL http://127.0.0.1:8888
hermes config set FIRECRAWL_API_URL http://127.0.0.1:3002
hermes config set web.search_backend searxng
hermes config set web.extract_backend firecrawl
```

If Firecrawl auth is enabled, add its API key through Hermes' local setup/config flow. Do not commit it.

Start a fresh Hermes session, then test:

```text
Search the web for the official Hermes Agent documentation and return its URL.
Extract the Hermes installation page and summarize the install choices.
```

## Remote services

If SearXNG/Firecrawl run on another host:

- use a private hostname/Tailscale address;
- keep admin/metrics routes private;
- firewall the service to the Hermes host;
- use HTTPS/auth if traffic leaves a trusted private network;
- do not publish private addresses in this repository.

## Resource and failure notes

- SearXNG is light; Firecrawl is not. Plan 4–8+ GB RAM for Firecrawl depending on concurrency.
- Cap concurrent crawls before scheduling recurring jobs.
- A successful search does not prove extraction works; test both.
- A successful HTTP 200 does not prove useful extraction; verify non-empty readable output.
- CAPTCHA/Cloudflare failure on self-hosted Firecrawl is not necessarily a broken install.
