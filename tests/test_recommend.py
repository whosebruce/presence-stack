from __future__ import annotations

import unittest

from presence_stack.recommend import recommend


class RecommendTests(unittest.TestCase):
    def test_under_8gb_is_upgrade_first(self) -> None:
        result = recommend({"ram_gb": 4, "cpu_threads": 4, "primary_goal": "combined"})
        self.assertEqual(result["architecture"], "upgrade-first")

    def test_8gb_media_with_quick_sync(self) -> None:
        result = recommend(
            {
                "ram_gb": 8,
                "cpu_threads": 4,
                "primary_goal": "media",
                "intel_quick_sync": True,
                "data_disk_count": 2,
                "wired_gigabit": True,
            }
        )
        self.assertEqual(result["architecture"], "single-purpose-bare-metal")
        self.assertIn("Jellyfin", result["verdict"])

    def test_16gb_combined_is_lean(self) -> None:
        result = recommend(
            {
                "ram_gb": 16,
                "cpu_threads": 8,
                "primary_goal": "combined",
                "intel_quick_sync": True,
                "data_disk_count": 2,
                "wired_gigabit": True,
            }
        )
        self.assertEqual(result["architecture"], "lean-linux-services")
        self.assertIn("Jellyfin", result["services_now"])
        self.assertIn("Hermes with hosted model", result["services_now"])

    def test_proxmox_warns_without_storage_passthrough(self) -> None:
        result = recommend(
            {
                "ram_gb": 32,
                "cpu_threads": 8,
                "primary_goal": "combined",
                "intel_quick_sync": True,
                "data_disk_count": 2,
                "storage_passthrough_possible": False,
                "wired_gigabit": True,
            }
        )
        self.assertEqual(result["architecture"], "separated-proxmox-guests")
        self.assertTrue(any("passthrough" in item for item in result["warnings"]))

    def test_invalid_goal(self) -> None:
        with self.assertRaises(ValueError):
            recommend({"ram_gb": 16, "primary_goal": "everything"})


if __name__ == "__main__":
    unittest.main()
