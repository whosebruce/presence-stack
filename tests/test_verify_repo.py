from __future__ import annotations

import unittest

import scripts.verify_repo as verify_repo


class VerifyRepoTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        existing = {
            str(path.relative_to(verify_repo.ROOT))
            for path in verify_repo.ROOT.rglob("*")
            if path.is_file()
        }
        self.assertFalse(verify_repo.REQUIRED - existing)

    def test_local_markdown_links_resolve(self) -> None:
        self.assertEqual(verify_repo.local_link_findings(), [])


if __name__ == "__main__":
    unittest.main()
