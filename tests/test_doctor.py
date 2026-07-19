from __future__ import annotations

import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from presence_stack import doctor


class DoctorTests(unittest.TestCase):
    def test_env_parser_returns_names_not_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            name = "OPENROUTER_" + "API_KEY"
            value = "synthetic-" + "secret-value"
            path.write_text(f"{name}={value}\nEMPTY=\n", encoding="utf-8")
            self.assertEqual(doctor._env_names(path), {name})

    def test_collect_checks_never_includes_env_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            hermes_home = home / ".hermes"
            hermes_home.mkdir()
            name = "OPENROUTER_" + "API_KEY"
            value = "synthetic-" + "secret-value"
            (hermes_home / ".env").write_text(
                f"{name}={value}\n", encoding="utf-8"
            )
            with mock.patch.dict(os.environ, {"HERMES_HOME": str(hermes_home)}, clear=False):
                checks = doctor.collect_checks(home)
            rendered = "\n".join(item.detail for item in checks)
            self.assertNotIn(value, rendered)
            self.assertIn(f"{name} value is never displayed", rendered)

    def test_main_non_strict_returns_zero(self) -> None:
        with mock.patch.object(doctor, "collect_checks", return_value=[]):
            with redirect_stdout(StringIO()):
                self.assertEqual(doctor.main(["--json"]), 0)


if __name__ == "__main__":
    unittest.main()
