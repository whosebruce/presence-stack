"""Estimate one-time and recurring Presence Stack costs from JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HOURS_PER_MONTH = 365.25 * 24 / 12


def _sum_values(values: dict[str, Any]) -> float:
    return sum(float(value) for value in values.values())


def openrouter_purchase_charge(config: dict[str, Any]) -> tuple[float, float]:
    credits = float(config.get("initial_credits", 0))
    fee_rate = float(config.get("credit_purchase_fee_rate", 0.055))
    minimum_fee = float(config.get("minimum_purchase_fee", 0.80))
    fee = max(credits * fee_rate, minimum_fee) if credits > 0 else 0.0
    return credits + fee, fee


def honcho_monthly_cost(config: dict[str, Any]) -> float:
    ingestion = float(config.get("ingestion_million_tokens_per_month", 0))
    ingestion_rate = float(config.get("ingestion_cost_per_million", 0))
    query_counts = config.get("reasoning_queries_per_month", {})
    query_rates = config.get("reasoning_cost_per_query", {})
    query_cost = sum(
        float(count) * float(query_rates.get(level, 0))
        for level, count in query_counts.items()
    )
    return ingestion * ingestion_rate + query_cost


def power_monthly_cost(config: dict[str, Any]) -> float:
    watts = float(config.get("average_watts", 0))
    rate = float(config.get("electricity_usd_per_kwh", 0))
    uptime = float(config.get("uptime_fraction", 1))
    if not 0 <= uptime <= 1:
        raise ValueError("power.uptime_fraction must be between 0 and 1")
    return watts / 1000 * HOURS_PER_MONTH * uptime * rate


def estimate(config: dict[str, Any]) -> dict[str, Any]:
    one_time_items = config.get("one_time", {})
    monthly_items = config.get("monthly_fixed", {})
    openrouter = config.get("openrouter", {})
    honcho = config.get("honcho", {})
    power = config.get("power", {})

    openrouter_charge, openrouter_fee = openrouter_purchase_charge(openrouter)
    honcho_cost = honcho_monthly_cost(honcho)
    power_cost = power_monthly_cost(power)
    monthly_openrouter = float(openrouter.get("monthly_usage_budget", 0))

    one_time_base = _sum_values(one_time_items)
    monthly_base = _sum_values(monthly_items)
    one_time_total = one_time_base + openrouter_charge
    monthly_total = monthly_base + monthly_openrouter + honcho_cost + power_cost

    return {
        "name": config.get("name", "Presence Stack estimate"),
        "one_time": {
            "base_items": round(one_time_base, 2),
            "openrouter_initial_credits_and_fee": round(openrouter_charge, 2),
            "openrouter_purchase_fee": round(openrouter_fee, 2),
            "total": round(one_time_total, 2),
        },
        "monthly": {
            "fixed_items": round(monthly_base, 2),
            "openrouter_usage_budget": round(monthly_openrouter, 2),
            "honcho_usage": round(honcho_cost, 2),
            "electricity": round(power_cost, 2),
            "total": round(monthly_total, 2),
        },
        "first_year_cash_outlay": round(one_time_total + monthly_total * 12, 2),
        "notes": [
            "OpenRouter initial credits are a deposit, not recurring spend.",
            "Monthly usage budgets are planning caps, not guaranteed charges.",
            "Hardware ranges, taxes, shipping, labor, internet, and replacement risk may be separate.",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    one = result["one_time"]
    monthly = result["monthly"]
    lines = [
        f"# {result['name']}",
        "",
        "## One-time",
        f"- Base hardware/setup items: **${one['base_items']:.2f}**",
        f"- OpenRouter initial credits + purchase fee: **${one['openrouter_initial_credits_and_fee']:.2f}**",
        f"  - Fee portion: ${one['openrouter_purchase_fee']:.2f}",
        f"- **One-time total: ${one['total']:.2f}**",
        "",
        "## Monthly planning estimate",
        f"- Fixed items: **${monthly['fixed_items']:.2f}**",
        f"- OpenRouter usage cap: **${monthly['openrouter_usage_budget']:.2f}**",
        f"- Honcho metered estimate: **${monthly['honcho_usage']:.2f}**",
        f"- Electricity estimate: **${monthly['electricity']:.2f}**",
        f"- **Monthly total: ${monthly['total']:.2f}**",
        "",
        f"## First-year cash outlay: **${result['first_year_cash_outlay']:.2f}**",
        "",
        "### Notes",
    ]
    lines.extend(f"- {note}" for note in result["notes"])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Path to a JSON cost config")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    result = estimate(config)
    print(json.dumps(result, indent=2) if args.json else render_markdown(result))


if __name__ == "__main__":
    main()
