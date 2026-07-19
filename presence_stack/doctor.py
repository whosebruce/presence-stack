"""Secret-safe local readiness report for Presence Stack components."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    required: bool
    status: str
    detail: str


def _first_line(command: list[str], timeout: int = 15) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, type(exc).__name__
    output = (result.stdout or result.stderr).strip().splitlines()
    detail = output[0] if output else f"exit {result.returncode}"
    return result.returncode == 0, detail[:180]


def _env_names(env_path: Path) -> set[str]:
    if not env_path.is_file():
        return set()
    names: set[str] = set()
    for raw in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if value.strip():
            names.add(name.strip())
    return names


def collect_checks(home: Path | None = None) -> list[Check]:
    home = home or Path.home()
    hermes_home = Path(os.environ.get("HERMES_HOME", home / ".hermes"))
    configured_names = set(os.environ) | _env_names(hermes_home / ".env")

    commands = [
        ("python", "python3", True, ["python3", "--version"]),
        ("git", "git", True, ["git", "--version"]),
        ("hermes", "hermes", True, ["hermes", "--version"]),
        ("docker", "docker", False, ["docker", "--version"]),
        ("node", "node", False, ["node", "--version"]),
        ("claude-code", "claude", False, ["claude", "--version"]),
        ("codex-cli", "codex", False, ["codex", "--version"]),
        ("open-design", "od", False, ["od", "--help"]),
    ]

    checks: list[Check] = []
    for name, executable, required, version_command in commands:
        if not shutil.which(executable):
            checks.append(Check(name, required, "missing", "command not found"))
            continue
        ok, detail = _first_line(version_command)
        checks.append(Check(name, required, "ready" if ok else "error", detail))

    paths = [
        ("hermes-config", hermes_home / "config.yaml", True),
        ("hermes-soul", hermes_home / "SOUL.md", False),
        ("hermes-memory", hermes_home / "memories", False),
    ]
    for name, path, required in paths:
        checks.append(
            Check(name, required, "ready" if path.exists() else "missing", "present" if path.exists() else "not found")
        )

    env_checks = [
        ("openrouter", "OPENROUTER_API_KEY"),
        ("composio", "COMPOSIO_API_KEY"),
        ("searxng", "SEARXNG_URL"),
        ("firecrawl", "FIRECRAWL_API_URL"),
    ]
    for name, variable in env_checks:
        present = variable in configured_names
        checks.append(Check(name, False, "configured" if present else "not-configured", f"{variable} value is never displayed"))

    vault = os.environ.get("PRESENCE_VAULT_PATH", "").strip()
    if vault:
        path = Path(vault).expanduser()
        status = "ready" if path.is_dir() and os.access(path, os.R_OK) else "error"
        checks.append(Check("presence-vault", False, status, "configured path is readable" if status == "ready" else "configured path is not readable"))
    else:
        checks.append(Check("presence-vault", False, "not-configured", "PRESENCE_VAULT_PATH is unset"))

    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--strict", action="store_true", help="fail if a required check is not ready")
    args = parser.parse_args(argv)

    checks = collect_checks()
    if args.json:
        print(json.dumps([asdict(item) for item in checks], indent=2))
    else:
        print("Presence Stack readiness (secret values are never displayed)")
        for item in checks:
            marker = "REQ" if item.required else "OPT"
            print(f"[{marker}] {item.name:18} {item.status:14} {item.detail}")

    failed = [item for item in checks if item.required and item.status != "ready"]
    return 1 if args.strict and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
