# Copy/paste prompt for a fresh agent

Use this after cloning the repository. It is intentionally secret-free.

```text
Read AGENTS.md and README.md completely. Treat this repository as a privacy-safe deployment harness, not as permission to clone another person's identity or configuration.

Interview me one plain-language question at a time. Do not ask me to paste secrets or personal identifiers into chat. Use official OAuth/device-code flows or local hidden prompts for credentials.

First produce a non-secret plan that selects one of the architecture tiers in docs/REQUIREMENTS.md and marks every module as required, optional, or skipped. Then build in the order defined in docs/BUILD_ORDER.md.

After every module, run its real verification command and show pass/fail evidence. Stop on failed security, privacy, backup, authorization, or unknown-user-denial checks. Keep private data under ~/.presence-stack/ and Hermes credentials in Hermes' own stores. Never commit generated owner data.

Start with the owner intake and base Hermes install. Do not install the entire stack blindly.
```

## Why the prompt is staged

A one-command installer cannot safely decide:

- which sources the owner consents to use;
- whether a public receptionist is appropriate;
- which messages or files the agent may access;
- whether a Mac, NAS, GPU, or hypervisor exists;
- which actions need owner sign-off;
- which accounts and billing limits belong to the new owner.

The agent can perform the work, but the owner must define identity, permissions, and consequential authority.
