# Open Design, Claude Code, and Codex CLI

Open Design is a local-first design workspace that can use Hermes, Claude Code, Codex CLI, and other coding agents. It exposes MCP tools for projects and artifacts.

Official project: <https://github.com/nexu-io/open-design>

## Preferred installation path

Use the current release installer from <https://open-design.ai/> when available for the target OS. For Linux source/dev mode, follow the repository's `QUICKSTART.md` and current Node/pnpm requirements rather than copying an old private install.

A typical source flow is:

```bash
git clone https://github.com/nexu-io/open-design.git "$HOME/open-design"
cd "$HOME/open-design"
# Read QUICKSTART.md and AGENTS.md for the checked-out release.
corepack enable
pnpm install
pnpm --filter @open-design/daemon build
pnpm tools-dev start web --daemon-port 7456 --web-port 7457
```

Open Design currently targets Node 24 and a pinned pnpm release; confirm the live repository before installation.

Verify:

```bash
curl -fsS http://127.0.0.1:7456/api/health
```

Keep it on loopback by default. Non-loopback binding requires authentication and a deliberate network design.

## Connect Open Design to Hermes

Open Design can install its MCP integration directly:

```bash
od mcp install hermes --print
od mcp install hermes
hermes mcp test open-design
hermes mcp list
```

Use `--print` first to review changes. Start a fresh Hermes session after the MCP is added.

## Claude Code

Use Anthropic's current native installer or official package path shown at:

<https://docs.anthropic.com/en/docs/claude-code/setup>

Current minimums include 4 GB RAM, a supported OS, internet, and a standard shell. Authenticate through Claude Code's official login. Do not copy another person's credential store.

Verify:

```bash
claude --version
claude doctor
```

## Codex CLI

Use OpenAI's current official installation instructions:

<https://developers.openai.com/codex/cli/>

Authenticate through the owner's ChatGPT/Codex flow or API account. Hermes' OpenAI Codex OAuth and Codex CLI credentials may be importable between supported stores, but each owner must authorize their own account.

Verify:

```bash
codex --version
```

## Connect coding agents to Open Design

```bash
od mcp install claude --print
od mcp install codex --print
```

Apply only after reviewing the printed changes. Open Design can then commission those agents for artifacts. Hermes can also control Open Design through its own MCP connection.

## Recommended division of labor

- Hermes: context, tools, files, messaging, memory, orchestration, approvals.
- Open Design: artifact projects, design systems, prototypes, decks, visual deliverables.
- Claude Code/Codex: coding and implementation engines.
- Human owner: direction, sensitive inputs, consequential sign-off, final taste.

## Security

- keep Open Design daemon on localhost/LAN/Tailscale;
- require a token before binding beyond loopback;
- treat third-party Open Design plugins as code execution;
- inspect plugin source/manifests;
- keep design source files separate from credentials;
- verify exported HTML/PDF/PPTX visually before delivery;
- do not assume a successful MCP test proves an agent can complete a real artifact—run a small synthetic generation.
