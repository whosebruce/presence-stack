from __future__ import annotations

import unittest

from presence_stack.estimate import (
    HOURS_PER_MONTH,
    estimate,
    honcho_monthly_cost,
    openrouter_purchase_charge,
    power_monthly_cost,
)


class EstimateTests(unittest.TestCase):
    def test_openrouter_50_credit_fee(self) -> None:
        charge, fee = openrouter_purchase_charge(
            {"initial_credits": 50, "credit_purchase_fee_rate": 0.055, "minimum_purchase_fee": 0.80}
        )
        self.assertAlmostEqual(fee, 2.75)
        self.assertAlmostEqual(charge, 52.75)

    def test_openrouter_minimum_fee(self) -> None:
        charge, fee = openrouter_purchase_charge(
            {"initial_credits": 10, "credit_purchase_fee_rate": 0.055, "minimum_purchase_fee": 0.80}
        )
        self.assertAlmostEqual(fee, 0.80)
        self.assertAlmostEqual(charge, 10.80)

    def test_honcho_metering(self) -> None:
        value = honcho_monthly_cost(
            {
                "ingestion_million_tokens_per_month": 2,
                "ingestion_cost_per_million": 2,
                "reasoning_queries_per_month": {"minimal": 100, "low": 10},
                "reasoning_cost_per_query": {"minimal": 0.001, "low": 0.01},
            }
        )
        self.assertAlmostEqual(value, 4.20)

    def test_power(self) -> None:
        value = power_monthly_cost(
            {"average_watts": 100, "electricity_usd_per_kwh": 0.25, "uptime_fraction": 1}
        )
        self.assertAlmostEqual(value, 0.1 * HOURS_PER_MONTH * 0.25)

    def test_full_estimate(self) -> None:
        result = estimate(
            {
                "one_time": {"hardware": 100},
                "monthly_fixed": {"subscription": 20},
                "openrouter": {
                    "initial_credits": 50,
                    "credit_purchase_fee_rate": 0.055,
                    "minimum_purchase_fee": 0.8,
                    "monthly_usage_budget": 10,
                },
                "honcho": {},
                "power": {},
            }
        )
        self.assertEqual(result["one_time"]["total"], 152.75)
        self.assertEqual(result["monthly"]["total"], 30.00)
        self.assertEqual(result["first_year_cash_outlay"], 512.75)

    def test_invalid_uptime(self) -> None:
        with self.assertRaises(ValueError):
            power_monthly_cost({"average_watts": 10, "electricity_usd_per_kwh": 0.2, "uptime_fraction": 2})


if __name__ == "__main__":
    unittest.main()
