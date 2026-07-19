# Personalities, SOUL.md, and specialist profiles

Hermes has three different identity/control layers:

| Layer | Scope | Use |
|---|---|---|
| `SOUL.md` | durable per Hermes instance/profile | stable identity, voice, communication defaults |
| `/personality` | current session overlay | temporary teacher/creative/technical mode |
| profile | independent Hermes home/process | separate memory, sessions, config, tokens, skills, cron, and gateway |

## Create the main Presence Persona

Edit:

```text
~/.hermes/SOUL.md
```

Use `templates/SOUL.md.example` as structure, not as an identity to copy. Build the real file from owner-approved Presence Profile artifacts.

Good SOUL content:

- role and relationship to the owner;
- tone and directness;
- uncertainty and disagreement posture;
- audience adaptation;
- stylistic constraints;
- disclosure and identity boundaries.

Do not put secrets, private paths, temporary project instructions, or a complete life archive in SOUL.md.

## Session personalities

Use built-in overlays:

```text
/personality concise
/personality technical
/personality teacher
/personality creative
```

Custom overlays can be defined under `agent.personalities` in `config.yaml`. Keep them short and task-mode-specific.

## Create specialist agents

```bash
hermes profile create researcher --description "Finds and verifies sources; writes evidence-backed briefs."
hermes profile create creator --description "Creates copy, designs, and content from approved source material."
hermes profile create operator --description "Runs bounded operational checks and returns receipts."
```

Configure each profile separately:

```bash
researcher setup
researcher doctor
creator setup
creator doctor
operator setup
operator doctor
```

Each gateway needs a distinct bot/application token. Hermes blocks accidental token reuse for supported platforms, but the owner should still maintain explicit account separation.

## Clone versus blank

- Blank profile: safest for a genuinely different trust boundary.
- `--clone`: copies config, `.env`, SOUL, and skills while starting fresh memory/sessions.
- `--clone-all`: broader copy; inappropriate when the new profile must not inherit credentials or private state.

For public/receptionist roles, start blank. Do not clone the private owner's full-power profile.

## Honcho multi-profile pattern

Use one owner peer/workspace with one distinct AI peer per profile when shared owner context is appropriate. A specialist should have its own AI identity and observations. Public users should resolve to separate peers; do not collapse everyone into the owner's private peer.

## Specialist authority table

| Profile | Typical tools | Default authority |
|---|---|---|
| main/private | broad owner-approved tools | prepare + bounded standing actions |
| researcher | web, files, memory | read/research/write briefs; no external sending |
| creator | files, Open Design, media | generate drafts/artifacts; publishing gated |
| operator | terminal, monitoring, selected apps | reversible checks/actions; destructive changes gated |
| receptionist | structured intake/relay only | no terminal/private files/admin/payment |

## Verification

For every profile:

```bash
<profile> doctor
<profile> gateway status
```

Then test:

- correct name/voice;
- correct memory separation;
- correct working directory;
- correct tool visibility;
- correct bot token/channel;
- correct owner authorization;
- forbidden action refusal;
- restart persistence.

Profiles are state separation, not automatic filesystem sandboxing. Use containers/VMs and narrow mounts when real isolation is required.
