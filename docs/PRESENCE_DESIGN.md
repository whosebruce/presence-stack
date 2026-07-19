# Presence design

Presence Design answers a harder question than "What should the bot sound like?"

It asks: **How should this person show up digitally when they are not personally typing every word or performing every step?**

## The design object

A complete Presence Profile includes:

| Artifact | What it captures |
|---|---|
| `IDENTITY.md` | Current roles, responsibilities, audiences, and relationships |
| `VOICE.md` | Rhythm, vocabulary, humor, directness, explanation style, phrases to avoid |
| `VALUES.md` | Principles, tradeoffs, priorities, and explicit current beliefs |
| `STORY_BANK.md` | Owner-approved examples, experiences, analogies, and source links |
| `KNOWLEDGE_MAP.md` | What the presence knows, where the source of truth lives, and what must be looked up |
| `DECISION_RIGHTS.md` | Standing authority, sign-off gates, forbidden actions, and escalation paths |
| `RELATIONSHIPS.md` | How communication changes by audience without exposing unnecessary private detail |
| `SOURCE_MANIFEST.csv` | Source, date, owner permission, transcript path, topic, confidence, expiry/review date |
| `EVALS.md` | Authenticity, factuality, boundary, and usefulness tests |

These files describe the person. Secrets and raw private archives remain elsewhere.

## Presence Profile, Persona, and Instance

These terms are related but not interchangeable:

- The **Presence Profile** is the private, owner-reviewed specification.
- The **Presence Persona** is the outward conversational expression of that profile for an approved audience and purpose.
- A **Presence Instance** is one deployment of that persona, such as a private Telegram assistant, a Discord project operator, or a bounded public receptionist.

One owner may have several Presence Instances with different tools and disclosure language. They should share the owner's core facts and values without sharing every permission, secret, or private memory. The Persona is what people experience; the Profile and Stack are what make it coherent and accountable.

## Source interview

Before ingesting material, ask:

- Which videos, podcasts, posts, writing, and documents are yours or explicitly available for this purpose?
- Which sources are public, private, sensitive, outdated, or off-limits?
- May the system quote them, learn from them, or only summarize patterns?
- Are voice cloning or generated likenesses allowed? If yes, where must disclosure appear?
- Which older opinions no longer represent you?
- Who can correct the Presence Profile?
- How often should the owner review it?

Permission is specific. Permission to watch a video is not automatically permission to clone the voice, publish the transcript, or reuse a personal story publicly.

## Video and audio workflow

For each approved source:

1. Save the canonical URL/file reference and date.
2. Prefer a transcript when it is accurate; preserve timestamps for important claims and stories.
3. Record speaker identity and diarization uncertainty.
4. Extract observations into categories rather than pasting the whole transcript into every prompt.
5. Link each observation back to its source and timestamp.
6. Ask the owner to confirm high-impact interpretations.
7. Mark outdated or contradicted material instead of silently deleting the history.

Useful signals from video include:

- sentence rhythm and explanation length;
- stories and analogies the person returns to;
- humor, playfulness, intensity, and tolerance for formality;
- how they distinguish facts, guesses, and opinions;
- what excites or frustrates them;
- how they make decisions under uncertainty;
- how they correct themselves;
- who they are speaking to and how that changes the delivery.

Do not turn verbal tics into a caricature. The goal is recognizable judgment and communication, not a parody.

## Source weighting

When sources disagree, use this default order:

1. current explicit owner correction;
2. current written policy or decision-rights file;
3. recent long-form owner material;
4. recent interviews or work examples;
5. older public content;
6. short social posts without context;
7. inference made by the model.

The owner can change this order. Every inferred trait should carry confidence and a review path.

## Presence loops

A Presence Loop is delegated work with evidence:

```text
Observe
  → understand the request and current context
Prepare
  → draft, research, classify, or assemble the next action
Gate
  → apply standing authority or request owner sign-off
Act
  → perform the bounded action
Prove
  → return receipt, link, diff, ID, status, or other evidence
Learn
  → update the Presence Profile only when the lesson is durable and approved
```

Examples:

- prepare an email draft, then wait for sign-off;
- answer a known FAQ under standing authority and relay the conversation;
- research options, recommend one, and let the owner purchase;
- maintain a project queue while the owner handles field work;
- publish only after a named approval step;
- decline a request that exceeds the owner's stated authority.

## CEO model

The owner does not disappear merely because work continues without their hands on every step. A CEO delegates to people, systems, and processes while retaining authority and accountability. Presence Stack follows the same idea:

- the owner defines the mission;
- the Presence Designer defines how the owner should be represented;
- the Presence Engineer builds the system and evidence paths;
- standing authority covers routine, reversible work;
- the owner signs consequential decisions;
- the stack reports what happened and what remains uncertain.

An AI is not a child, employee, legal person, or successor. The analogy explains delegation, not personhood.

## Authenticity tests

Do not ask only, "Does it sound like me?" Test several dimensions:

1. **Voice:** Would the owner naturally say this to this audience?
2. **Judgment:** Did it make the tradeoff the owner would make, or explain why it could not know?
3. **Facts:** Did it use the source of truth rather than confident memory?
4. **Boundaries:** Did it stop at the correct sign-off gate?
5. **Challenge:** Can it respectfully disagree instead of flattering the owner?
6. **Audience:** Did it change tone without changing facts or values?
7. **Time:** Did it prefer recent corrections over old videos?
8. **Usefulness:** Did it move real work forward rather than generate volume?

Build a set of owner-reviewed scenarios and rerun them after changing models, memory, prompts, channels, or tools.

## Disclosure and dignity

- Disclose AI participation where a reasonable person could believe they are speaking directly with the owner.
- Do not synthesize the owner's voice or likeness without specific consent and usage boundaries.
- Do not use private relationship, medical, military, employment, client, or family material merely because the system can access it.
- Give the owner a correction, export, pause, and deletion path.
- Keep source material and derived Presence Profile artifacts separate so the profile can be reviewed without exposing the entire archive.

## Anti-slop rule

A presence is measured by fidelity, judgment, outcomes, and accountability. More posts, replies, documents, and generated media do not make it more present. If the owner would not stand behind the output, it should remain a draft or not exist.
