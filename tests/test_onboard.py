from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from presence_stack.onboard import build_plan, render_markdown


class OnboardingTests(unittest.TestCase):
    def test_starts_where_owner_already_lives(self) -> None:
        plan = build_plan(
            {
                "current_channel": "telegram",
                "audience": "community",
                "organized_projects": True,
                "future_channel": "discord",
            }
        )
        self.assertEqual(plan["primary_channel"], "telegram")
        self.assertEqual(plan["future_channel"], "discord")
        self.assertTrue(plan["migration_steps"])

    def test_no_current_channel_solo_simple_prefers_telegram(self) -> None:
        plan = build_plan(
            {
                "current_channel": "none",
                "audience": "solo",
                "simplest_start": True,
            }
        )
        self.assertEqual(plan["primary_channel"], "telegram")

    def test_existing_slack_team_stays_slack(self) -> None:
        plan = build_plan(
            {
                "current_channel": "slack",
                "audience": "team",
                "organized_projects": True,
            }
        )
        self.assertEqual(plan["primary_channel"], "slack")

    def test_apple_native_can_recommend_imessage(self) -> None:
        plan = build_plan(
            {
                "current_channel": "none",
                "audience": "solo",
                "apple_native": True,
                "simplest_start": False,
            }
        )
        self.assertEqual(plan["primary_channel"], "imessage")

    def test_public_audience_requires_boundary(self) -> None:
        plan = build_plan({"current_channel": "discord", "audience": "public"})
        self.assertTrue(plan["public_boundary_required"])
        self.assertIn("tool-isolated", render_markdown(plan))

    def test_invalid_channel(self) -> None:
        with self.assertRaises(ValueError):
            build_plan({"current_channel": "fax", "audience": "solo"})

    def test_render_can_be_written_to_private_temp_dir(self) -> None:
        plan = build_plan({"current_channel": "cli", "audience": "solo"})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PLAN.md"
            path.write_text(render_markdown(plan), encoding="utf-8")
            self.assertIn("CLI / Desktop", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
