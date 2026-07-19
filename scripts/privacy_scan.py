"""Scan working tree, exact Git index, and reachable history for privacy risks.

The scanner prints only category, file, and line. It never prints matched values.
Operator-specific literals belong in gitignored local-patterns.txt, one literal per line.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    "",
    ".md",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
    ".csv",
    ".sh",
    ".ini",
    ".example",
}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "build", "dist"}
SKIP_NAMES = {"local-patterns.txt"}

PATTERNS = {
    "absolute user home": re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+/"),
    "non-example email": re.compile(
        r"\b[A-Z0-9._%+-]+@(?!example\.(?:com|org|net)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I
    ),
    "phone-like number": re.compile(r"(?<!\d)(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?!\d)"),
    "platform-like numeric id": re.compile(r"(?<!\d)\d{17,22}(?!\d)"),
    "private IPv4": re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
    ),
    "secret-looking assignment": re.compile(
        r"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{16,}"
    ),
    "common token prefix": re.compile(
        r"\b(?:sk-(?:or-|proj-)?|gh[opusr]_|github_pat_|xox[baprs]-|AKIA)[A-Za-z0-9_-]{12,}\b"
    ),
    "private key header": re.compile("-----BEGIN " + "(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


@dataclass(frozen=True)
class Finding:
    surface: str
    category: str
    path: str
    line: int


def _git(root: Path, args: list[str], *, text: bool = True) -> str | bytes:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=text, stderr=subprocess.DEVNULL
    )


def is_git_repo(root: Path) -> bool:
    try:
        return str(_git(root, ["rev-parse", "--is-inside-work-tree"])).strip() == "true"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _eligible(path: str) -> bool:
    candidate = Path(path)
    return (
        candidate.name not in SKIP_NAMES
        and candidate.suffix.lower() in TEXT_SUFFIXES
        and not any(part in SKIP_PARTS for part in candidate.parts)
    )


def _operator_patterns(root: Path) -> list[re.Pattern[str]]:
    path = root / "local-patterns.txt"
    if not path.is_file():
        return []
    patterns: list[re.Pattern[str]] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        literal = raw.strip()
        if literal and not literal.startswith("#"):
            patterns.append(re.compile(re.escape(literal), re.I))
    return patterns


def _scan_text(surface: str, path: str, text: str, operator: list[re.Pattern[str]]) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for category, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(Finding(surface, category, path, line_number))
        for pattern in operator:
            if pattern.search(line):
                findings.append(Finding(surface, "operator-specific marker", path, line_number))
    return findings


def tree_documents(root: Path) -> list[tuple[str, str]]:
    if is_git_repo(root):
        output = str(_git(root, ["ls-files", "--cached", "--others", "--exclude-standard"]))
        paths = [root / line for line in output.splitlines() if line]
    else:
        paths = [path for path in root.rglob("*") if path.is_file()]
    documents: list[tuple[str, str]] = []
    for path in sorted(paths):
        rel = str(path.relative_to(root))
        if not path.is_file() or not _eligible(rel):
            continue
        try:
            documents.append((rel, path.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            continue
    return documents


def index_documents(root: Path) -> list[tuple[str, str]]:
    if not is_git_repo(root):
        return []
    output = str(_git(root, ["ls-files", "--cached"]))
    documents: list[tuple[str, str]] = []
    for path in output.splitlines():
        if not _eligible(path):
            continue
        try:
            blob = _git(root, ["show", f":{path}"], text=False)
            documents.append((path, bytes(blob).decode("utf-8")))
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            continue
    return documents


def history_documents(root: Path) -> list[tuple[str, str]]:
    if not is_git_repo(root):
        return []
    try:
        commits = str(_git(root, ["rev-list", "--all"])).splitlines()
    except subprocess.CalledProcessError:
        return []
    seen: set[str] = set()
    documents: list[tuple[str, str]] = []
    for commit in commits:
        tree = str(_git(root, ["ls-tree", "-r", commit]))
        for row in tree.splitlines():
            metadata, path = row.split("\t", 1)
            parts = metadata.split()
            if len(parts) < 3 or parts[1] != "blob" or not _eligible(path):
                continue
            blob_id = parts[2]
            if blob_id in seen:
                continue
            seen.add(blob_id)
            try:
                blob = _git(root, ["cat-file", "blob", blob_id], text=False)
                documents.append((f"{path}@{blob_id[:12]}", bytes(blob).decode("utf-8")))
            except (subprocess.CalledProcessError, UnicodeDecodeError):
                continue
    return documents


def scan(root: Path = ROOT, surfaces: list[str] | None = None) -> tuple[list[Finding], dict[str, int]]:
    surfaces = surfaces or ["tree", "index", "history"]
    operator = _operator_patterns(root)
    readers = {
        "tree": tree_documents,
        "index": index_documents,
        "history": history_documents,
    }
    findings: list[Finding] = []
    counts: dict[str, int] = {}
    for surface in surfaces:
        documents = readers[surface](root)
        counts[surface] = len(documents)
        for path, text in documents:
            findings.extend(_scan_text(surface, path, text, operator))
    return findings, counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--surface",
        action="append",
        choices=["tree", "index", "history"],
        help="surface to scan; repeat for multiple (default: all available)",
    )
    args = parser.parse_args(argv)
    findings, counts = scan(surfaces=args.surface)
    if findings:
        print(f"FAIL: {len(findings)} potential privacy/secret finding(s)")
        for item in findings:
            print(f"- {item.surface}: {item.category}: {item.path}:{item.line}")
        return 1
    summary = ", ".join(f"{surface}={count}" for surface, count in counts.items())
    print(f"PASS: {summary}; 0 privacy/secret findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
