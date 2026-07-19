"""Validate repository shape and local Markdown links."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "AGENTS.md",
    "AGENT_README.md",
    "INSTALL_PROMPT.md",
    "docs/BUILD_ORDER.md",
    "docs/REFERENCE_STACK.md",
    "docs/REQUIREMENTS.md",
    "docs/HERMES_SUPERCHARGE.md",
    "docs/WEB_RESEARCH.md",
    "docs/MEMORY_HONCHO.md",
    "docs/OBSIDIAN_SMB.md",
    "docs/COMPOSIO_GOOGLE.md",
    "docs/OPEN_DESIGN_CODING_AGENTS.md",
    "docs/PERSONALITIES_PROFILES.md",
    "docs/VERIFICATION.md",
    "config/hermes-sanitized.yaml.example",
    "templates/SOUL.md.example",
    "deploy/searxng/compose.yaml",
    "scripts/privacy_scan.py",
}
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PROHIBITED_TRACKED = {".env", "auth.json", "honcho.json", "state.db"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "build", "dist"}


def repository_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in SKIP_PARTS or part.endswith(".egg-info") for part in path.relative_to(ROOT).parts)
    )


def markdown_files() -> list[Path]:
    return [path for path in repository_files() if path.suffix.lower() == ".md"]


def local_link_findings() -> list[str]:
    findings: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = (path.parent / unquote(target)).resolve()
            try:
                target_path.relative_to(ROOT.resolve())
            except ValueError:
                findings.append(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not target_path.exists():
                findings.append(f"missing link: {path.relative_to(ROOT)} -> {target}")
    return findings


def main() -> int:
    findings: list[str] = []
    existing = {str(path.relative_to(ROOT)) for path in repository_files()}
    for required in sorted(REQUIRED - existing):
        findings.append(f"missing required file: {required}")
    for path in sorted(existing):
        if Path(path).name in PROHIBITED_TRACKED and path != ".env.example":
            findings.append(f"prohibited repository file: {path}")
    findings.extend(local_link_findings())

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "https://github.com/whosebruce/presence-stack" not in readme:
        findings.append("README is missing the canonical repository URL")

    if findings:
        print(f"FAIL: {len(findings)} repository finding(s)")
        for item in findings:
            print(f"- {item}")
        return 1
    print(f"PASS: {len(existing)} files checked; {len(markdown_files())} Markdown files; 0 missing local links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
