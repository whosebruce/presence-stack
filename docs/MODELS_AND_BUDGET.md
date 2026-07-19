# Model routing and budget

## Recommended routing pattern

### Primary agent

Use the strongest current tool-calling model available through a provider/account the owner controls.

The reference stack uses the current OpenAI Codex model available through ChatGPT OAuth. As of this repository release, that model is GPT-5.6 Sol. Configure it through:

```bash
hermes model
```

Select **OpenAI Codex** and complete the device-code login. Do not put OAuth tokens in `.env` or Git.

### OpenRouter reserve

OpenRouter is useful for:

- auxiliary vision;
- fallback models;
- specialist subagents;
- models not available through the primary subscription.

A practical starter deposit is **about $50**, with a hard provider spend limit and low-balance alert. It is seed credit, not a promise that every user will spend $50 per month.

Store the key through the Hermes setup/config flow or locally in `~/.hermes/.env`. Never commit it.

### Vision

A fast Gemini Flash-class vision model through OpenRouter is the reference choice for screenshots, photos, OCR, and browser visual QA:

```bash
hermes config set agent.image_input_mode auto
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model google/gemini-3.1-flash-lite
```

Model catalogs change. If that exact model is unavailable, choose the current Gemini Flash vision model shown by OpenRouter/Hermes and record the substitution.

### Cheap auxiliary tasks

Long-page summarization, titles, compression, approval classification, and narrow subagents do not always need the primary model. Configure them through:

```bash
hermes model
# Configure auxiliary models
```

Do not route everything to a cheap model merely to reduce cost. Weak tool calling and poor verification can cost more than the tokens saved.

## Safe fallback policy

- Make fallback explicit.
- Ensure the fallback provider has a separate spend cap.
- Do not silently route a failed OAuth primary into an expensive API key.
- For sensitive work, require the same data-handling policy on every fallback.
- Test fallback with a harmless call before relying on it.

## Budget worksheet

| Item | Planning approach |
|---|---|
| Primary model/subscription | Owner-selected plan; verify current pricing directly |
| OpenRouter | Optional starter credit around $50; hard cap and alert |
| Honcho | Cloud usage or self-hosted compute/database |
| Composio | Current plan based on connected apps/tool calls |
| Storage/backup | One-time hardware plus offsite copy |
| Domain/phone/Mac | Only if public presence or BlueBubbles requires it |
| Electricity | Measure average watts × local utility rate |

Use `config/cost-example.json` and:

```bash
python3 -m presence_stack.estimate config/cost-example.json
```

All prices are dated snapshots. Recheck official pricing before quoting a deployment.
