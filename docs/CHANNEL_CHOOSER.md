# Channel chooser

The best first channel is usually the one the owner already opens without thinking. Presence Stack should fit the person before asking the person to fit the stack.

## Questions to ask

Ask one at a time and explain unfamiliar terms.

1. Where do you already spend most of your communication time?
2. Who will speak with this presence: only you, a small team, a community, customers/public contacts, or a mixture?
3. Do you want one continuous conversation or separate project channels and threads?
4. Does your team already use Slack?
5. Is native iMessage important enough to keep a Mac running all the time?
6. Do you send many voice notes, pictures, documents, or long discussions?
7. Are you willing to manage bot permissions, channels, and roles?
8. What might you want six months from now?

## Comparison

| Channel | Fits best | Advantages | Tradeoffs |
|---|---|---|---|
| Telegram | Solo owner, fast personal start, mobile-first use | Low setup friction; good media and voice support; works well as one direct conversation; topics can add organization later | Less natural for a large project workspace; bot identity is separate from ordinary human messaging; complex teams may outgrow one chat |
| Discord | Projects, communities, multi-agent operations, visible work queues | Channels, threads, roles, voice, files, and strong separation between topics; good when several people or agents collaborate | More setup and permission decisions; context can fragment across channels/threads; can feel like overkill for one person |
| Slack | Existing workplace or client team | Familiar workplace structure, channels, threads, app permissions, searchable operational conversations | Best value when the team already lives there; retention and app capabilities depend on the workspace plan; less natural as a personal assistant home |
| BlueBubbles / iMessage | Apple-native personal or dedicated business identity | The owner uses the Messages app they already know; contacts do not need another app; images/files feel native | Requires an always-on Mac signed into Messages; Apple identity and optional phone line need careful separation; no Discord-style project channels; public senders need a bounded receptionist layer |
| CLI / Desktop | Private operator, builder, or first test | Smallest trust surface; easiest place to verify Hermes before opening a gateway; excellent for setup and recovery | Not always available from a phone; weak for teams or public communication |
| Multiple channels | Mature presence serving different contexts | Private owner channel, team workspace, and public intake can each have the right security boundary | More identities, routing, testing, and cost; never assume history or permissions automatically carry across channels |

Hermes supports additional platforms. The choices above cover the most common Presence Stack paths; consult the current [Hermes messaging documentation](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) before deployment.

## Simple recommendations

- **Only me, simplest mobile start:** Telegram.
- **I already live in iMessage and own an always-on Mac:** BlueBubbles, with a private allowlist.
- **My team already uses Slack:** Slack. Do not create a Discord migration project without a reason.
- **I want projects, channels, a community, or several specialist agents:** Discord.
- **I am still testing whether I want this:** CLI/Desktop first.
- **Public receptionist:** any public transport may be used, but route it through a separate tool-isolated intake service.

## Telegram to Discord without starting over

The channel is not the person's identity. Keep the Presence Profile in durable files/memory and use this sequence:

1. Keep Telegram working as the owner's private fallback.
2. Create the Discord application/server/channel structure.
3. Add Discord to the same Hermes gateway or to a deliberately separate profile.
4. Configure Discord allowlists/pairing, admin roles, and thread behavior.
5. Copy no raw Telegram credentials or private chat logs into Discord.
6. Test one private Discord channel with harmless tasks.
7. Verify that Presence Profile, memory provider, skills, approval rules, and owner identity resolve correctly.
8. Announce Discord as the new project home while Telegram remains the recovery/urgent channel.
9. After an observation period, either retain both for different contexts or retire the old route deliberately.

Existing channel transcripts do not automatically become a clean shared context. Durable identity belongs in the Presence Profile and approved memory, not in one giant chat history.

## Slack to Discord or Discord to Slack

Do not frame either move as an upgrade by default. They solve different social problems.

- Add the target platform in parallel.
- Recreate only the necessary channels and permissions.
- Move durable policies, project maps, and Presence Profile files—not every casual message.
- Test delivery, threads, files, approvals, and unknown-user behavior.
- Keep a named transition period and rollback channel.

## Private, team, and public homes

A mature stack may use:

```text
Telegram or iMessage → private owner conversation
Slack or Discord     → team/project operations
Public SMS/iMessage  → bounded receptionist intake
CLI/Desktop          → setup, recovery, and sensitive administration
```

Do not merge those trust levels merely because one gateway technically can connect to all of them.
