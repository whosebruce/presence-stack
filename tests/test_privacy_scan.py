from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import privacy_scan


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


class PrivacyScanTests(unittest.TestCase):
    def make_repo(self) -> Path:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        root = Path(self.tempdir.name)
        git(root, "init", "-q")
        git(root, "config", "user.name", "Synthetic Tester")
        git(root, "config", "user.email", "tester@example.com")
        return root

    def test_index_scan_reads_staged_blob_not_worktree(self) -> None:
        root = self.make_repo()
        path = root / "sample.txt"
        staged_value = "API_" + "KEY=" + ("Z" * 24)
        path.write_text(staged_value + "\n", encoding="utf-8")
        git(root, "add", "sample.txt")
        path.write_text("safe worktree\n", encoding="utf-8")

        findings, counts = privacy_scan.scan(root, ["index"])
        self.assertEqual(counts["index"], 1)
        self.assertTrue(any(item.category == "secret-looking assignment" for item in findings))

    def test_history_scan_catches_removed_content(self) -> None:
        root = self.make_repo()
        path = root / "sample.txt"
        private_address = "192" + ".168.50.25"
        path.write_text(private_address + "\n", encoding="utf-8")
        git(root, "add", "sample.txt")
        git(root, "commit", "-q", "-m", "synthetic private fixture")
        path.write_text("safe replacement\n", encoding="utf-8")
        git(root, "add", "sample.txt")
        git(root, "commit", "-q", "-m", "remove synthetic fixture")

        findings, counts = privacy_scan.scan(root, ["tree", "history"])
        self.assertFalse(any(item.surface == "tree" for item in findings))
        self.assertGreaterEqual(counts["history"], 2)
        self.assertTrue(any(item.surface == "history" and item.category == "private IPv4" for item in findings))

    def test_gitignored_local_patterns_catch_operator_literal(self) -> None:
        root = self.make_repo()
        marker = "private" + "-fixture-label"
        (root / ".gitignore").write_text("local-patterns.txt\n", encoding="utf-8")
        (root / "local-patterns.txt").write_text(marker + "\n", encoding="utf-8")
        (root / "note.txt").write_text("contains " + marker + "\n", encoding="utf-8")

        findings, _ = privacy_scan.scan(root, ["tree"])
        self.assertTrue(any(item.category == "operator-specific marker" for item in findings))
        self.assertFalse(any(item.path == "local-patterns.txt" for item in findings))


if __name__ == "__main__":
    unittest.main()
