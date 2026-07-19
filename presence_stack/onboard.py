"""Beginner-friendly Presence Stack onboarding and channel recommendation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CHANNELS = {"telegram", "discord", "slack", "imessage", "cli", "none"}
AUDIENCES = {"solo", "team", "community", "public", "mixed"}

CHANNEL_LABELS = {
    "telegram": "Telegram",
    "discord": "Discord",
    "slack": "Slack",
    "imessage": "BlueBubbles / iMessage",
    "cli": "CLI / Desktop",
}

CHANNEL_SUMMARIES = {
    "telegram": "A low-friction personal starting point with strong mobile, voice, and media use.",
    "discord": "A project and community workspace with channels, threads, roles, files, and room for several agents.",
    "slack": "A team workspace choice when the people involved already work in Slack.",
    "imessage": "An Apple-native personal channel that requires an always-on Mac running BlueBubbles.",
    "cli": "The smallest private trust surface for initial setup, testing, recovery, and sensitive administration.",
}


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def _validate(answers: dict[str, Any]) -> dict[str, Any]:
    clean = {
        "current_channel": str(answers.get("current_channel", "none")).lower(),
        "audience": str(answers.get("audience", "solo")).lower(),
        "organized_projects": _bool(answers.get("organized_projects", False)),
        "apple_native": _bool(answers.get("apple_native", False)),
        "simplest_start": _bool(answers.get("simplest_start", True)),
        "future_channel": str(answers.get("future_channel", "none")).lower(),
        "source_types": list(answers.get("source_types", [])),
        "first_outcome": str(answers.get("first_outcome", "Define one useful 30-day Presence Loop.")),
    }
    if clean["current_channel"] not in CHANNELS:
        raise ValueError(f"current_channel must be one of {sorted(CHANNELS)}")
    if clean["future_channel"] not in CHANNELS:
        raise ValueError(f"future_channel must be one of {sorted(CHANNELS)}")
    if clean["audience"] not in AUDIENCES:
        raise ValueError(f"audience must be one of {sorted(AUDIENCES)}")
    return clean


def _score_channels(answers: dict[str, Any]) -> dict[str, int]:
    scores = {name: 0 for name in CHANNEL_LABELS}
    audience = answers["audience"]
    if audience == "solo":
        scores.update(telegram=5, imessage=4, cli=3, discord=1, slack=0)
    elif audience == "team":
        scores.update(slack=5, discord=4, telegram=1, imessage=0, cli=1)
    elif audience == "community":
        scores.update(discord=7, telegram=2, slack=1, imessage=0, cli=0)
    elif audience == "public":
        scores.update(discord=3, telegram=3, slack=2, imessage=2, cli=0)
    else:
        scores.update(discord=5, slack=3, telegram=3, imessage=2, cli=1)

    if answers["organized_projects"]:
        scores["discord"] += 4
        scores["slack"] += 4
    if answers["apple_native"]:
        scores["imessage"] += 6
    if answers["simplest_start"]:
        scores["telegram"] += 3
        scores["cli"] += 2
    return scores


def build_plan(raw_answers: dict[str, Any]) -> dict[str, Any]:
    answers = _validate(raw_answers)
    scores = _score_channels(answers)
    current = answers["current_channel"]

    if current != "none":
        primary = current
        primary_reason = "Start where the owner already communicates; habit is part of the design."
    else:
        primary = max(scores, key=lambda name: scores[name])
        primary_reason = "No current channel was selected, so the recommendation follows audience and workflow needs."

    future = answers["future_channel"]
    if future in {"none", primary}:
        future = "none"
        if primary not in {"discord", "slack"} and answers["organized_projects"]:
            future = "discord" if answers["audience"] in {"community", "mixed", "public"} else "slack"
        elif primary == "telegram" and answers["audience"] == "community":
            future = "discord"

    public_boundary = answers["audience"] in {"public", "mixed"}
    migration = []
    if future != "none":
        migration = [
            f"Keep {CHANNEL_LABELS[primary]} working as the private fallback.",
            f"Add {CHANNEL_LABELS[future]} in parallel with a narrow allowlist/pairing configuration.",
            "Move the approved Presence Profile and decision rules, not raw private chat history or credentials.",
            "Test harmless messages, files, threads, approvals, and unknown-user denial.",
            "Choose the new primary home only after an observation period; keep or retire the old route deliberately.",
        ]

    return {
        "answers": answers,
        "primary_channel": primary,
        "primary_label": CHANNEL_LABELS[primary],
        "primary_reason": primary_reason,
        "primary_summary": CHANNEL_SUMMARIES[primary],
        "future_channel": future,
        "future_label": CHANNEL_LABELS.get(future),
        "public_boundary_required": public_boundary,
        "migration_steps": migration,
        "first_outcome": answers["first_outcome"],
        "source_types": answers["source_types"],
        "next_steps": [
            "Complete the private Presence Intake one question at a time.",
            "Record source permissions before analyzing videos, writing, audio, or documents.",
            "Create the Presence Profile and ask the owner to correct it.",
            "Define standing authority, sign-off gates, forbidden actions, and evidence requirements.",
            f"Verify one private conversation in {CHANNEL_LABELS[primary]} before adding more channels or tools.",
            "Build one useful 30-day Presence Loop and review it with the owner.",
        ],
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# First Presence Plan",
        "",
        f"## Start in {plan['primary_label']}",
        "",
        plan["primary_reason"],
        "",
        plan["primary_summary"],
        "",
        "## First outcome",
        "",
        plan["first_outcome"],
        "",
        "## Trust boundary",
        "",
    ]
    if plan["public_boundary_required"]:
        lines.append("Public or mixed audiences require a separate tool-isolated receptionist. Unknown contacts must not reach the privileged private agent.")
    else:
        lines.append("Begin as a private, allowlisted/pairing-only owner channel. Add broader audiences only after the private baseline works.")

    sources = plan["source_types"]
    lines.extend(["", "## Approved source types", ""])
    lines.extend(f"- {item}" for item in sources) if sources else lines.append("- None selected yet. Record permission before ingestion.")

    if plan["future_channel"] != "none":
        lines.extend(["", f"## Later path to {plan['future_label']}", ""])
        lines.extend(f"{index}. {step}" for index, step in enumerate(plan["migration_steps"], 1))

    lines.extend(["", "## Next steps", ""])
    lines.extend(f"{index}. {step}" for index, step in enumerate(plan["next_steps"], 1))
    return "\n".join(lines)


def _ask_choice(question: str, choices: list[str], default: str) -> str:
    display = "/".join(choices)
    while True:
        answer = input(f"{question} [{display}] (default: {default}): ").strip().lower() or default
        if answer in choices:
            return answer
        print(f"Please choose one of: {', '.join(choices)}")


def _ask_yes_no(question: str, default: bool) -> bool:
    label = "Y/n" if default else "y/N"
    answer = input(f"{question} [{label}]: ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes"}


def interactive_answers() -> dict[str, Any]:
    print("Presence Stack asks about your life before it asks about software. No secrets are collected.\n")
    current = _ask_choice(
        "Where do you already spend the most communication time?",
        ["telegram", "discord", "slack", "imessage", "cli", "none"],
        "none",
    )
    audience = _ask_choice(
        "Who should interact with this presence first?",
        ["solo", "team", "community", "public", "mixed"],
        "solo",
    )
    organized = _ask_yes_no("Do you need separate projects, channels, or threads?", False)
    apple = _ask_yes_no("Is native iMessage important, and can an always-on Mac be used?", False)
    simple = _ask_yes_no("Is the simplest possible first setup the priority?", True)
    future = _ask_choice(
        "Is there a channel you already expect to add later?",
        ["none", "telegram", "discord", "slack", "imessage", "cli"],
        "none",
    )
    source_text = input(
        "Which owner-approved source types may the presence study? "
        "(comma-separated: videos, writing, audio, documents; blank for none): "
    ).strip()
    first_outcome = input("What should this presence make easier in its first 30 days? ").strip()
    return {
        "current_channel": current,
        "audience": audience,
        "organized_projects": organized,
        "apple_native": apple,
        "simplest_start": simple,
        "future_channel": future,
        "source_types": [item.strip() for item in source_text.split(",") if item.strip()],
        "first_outcome": first_outcome or "Define one useful 30-day Presence Loop.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, help="Use a non-secret JSON answers file instead of the interview")
    parser.add_argument("--output-dir", type=Path, default=Path("presence-plan"), help="Private output directory")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without writing files")
    args = parser.parse_args()

    answers = json.loads(args.answers.read_text(encoding="utf-8")) if args.answers else interactive_answers()
    plan = build_plan(answers)
    markdown = render_markdown(plan)
    if args.dry_run:
        print(markdown)
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "PLAN.md").write_text(markdown + "\n", encoding="utf-8")
    print(f"Wrote private starter plan to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
