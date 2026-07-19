"""Recommend an initial Presence Stack layout from sanitized hardware facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VALID_GOALS = {"agent", "media", "combined"}


def recommend(config: dict[str, Any]) -> dict[str, Any]:
    ram = float(config.get("ram_gb", 0))
    threads = int(config.get("cpu_threads", 0))
    quick_sync = bool(config.get("intel_quick_sync", False))
    dedicated_gpu = bool(config.get("dedicated_gpu", False))
    disks = int(config.get("data_disk_count", 0))
    passthrough = bool(config.get("storage_passthrough_possible", False))
    wired = bool(config.get("wired_gigabit", False))
    local_llm = bool(config.get("local_llm_required", False))
    transcodes = int(config.get("expected_4k_transcodes", 0))
    goal = str(config.get("primary_goal", "combined")).lower()
    if goal not in VALID_GOALS:
        raise ValueError(f"primary_goal must be one of {sorted(VALID_GOALS)}")

    warnings: list[str] = []
    deferred: list[str] = []

    if ram < 8:
        architecture = "upgrade-first"
        verdict = "Do not install the full stack. Upgrade RAM or run one tiny service directly on Linux."
    elif ram < 16:
        architecture = "single-purpose-bare-metal"
        if goal == "media" and (quick_sync or dedicated_gpu):
            verdict = "Start with Jellyfin on Debian/Ubuntu; use hardware acceleration and defer Proxmox/TrueNAS."
        else:
            verdict = "Start with hosted-model Hermes on Debian/Ubuntu; add Jellyfin only after measuring headroom."
        deferred.extend(["Proxmox + virtualized TrueNAS", "local LLM"])
    elif ram < 32:
        architecture = "lean-linux-services"
        verdict = "Run Debian/Ubuntu with isolated services. A combined hosted-model Hermes + Jellyfin stack is feasible but tight."
        deferred.append("virtualized TrueNAS unless storage passthrough and memory headroom are proven")
    else:
        architecture = "separated-proxmox-guests"
        verdict = "A separated Proxmox layout is reasonable: storage, Jellyfin, Hermes, and services in distinct guests."

    if threads < 4:
        warnings.append("Fewer than four CPU threads will constrain simultaneous tools/transcodes.")
    if not wired:
        warnings.append("Use wired gigabit Ethernet; Wi-Fi is a weak server foundation.")
    if goal in {"media", "combined"} and not (quick_sync or dedicated_gpu):
        warnings.append("No hardware transcoding path is declared; prefer direct play or upgrade before remote/4K use.")
    if transcodes > 0 and not (quick_sync or dedicated_gpu):
        warnings.append("Requested 4K transcodes conflict with the declared lack of GPU/iGPU acceleration.")
    if disks < 2:
        warnings.append("Fewer than two data disks: no redundant TrueNAS pool. A separate backup is still required either way.")
    if architecture == "separated-proxmox-guests" and disks >= 2 and not passthrough:
        warnings.append("Do not place an important TrueNAS pool on ordinary virtual disks; storage passthrough is unproven.")
    if local_llm:
        warnings.append("Local LLM requested: RAM/VRAM, model, quantization, and 64K context must be benchmarked separately.")

    services_now = ["Hermes with hosted model"]
    if goal in {"media", "combined"} and ram >= 8:
        services_now.append("Jellyfin" if (quick_sync or dedicated_gpu) else "Jellyfin direct-play only")
    if goal == "media" and "Hermes with hosted model" in services_now:
        services_now.remove("Hermes with hosted model")
    if goal == "agent" and ram < 16:
        deferred.append("Jellyfin until agent baseline is stable")

    return {
        "name": config.get("name", "Candidate hardware"),
        "architecture": architecture,
        "verdict": verdict,
        "services_now": services_now,
        "defer": sorted(set(deferred)),
        "warnings": warnings,
        "next_checks": [
            "Record exact CPU model and Intel media capabilities.",
            "Record disk models, SMART health, controller, and backup target.",
            "Run one direct-play and one forced-transcode Jellyfin test.",
            "Run one Hermes tool call and session-resume test.",
            "Retest both workloads simultaneously, then reboot and verify recovery.",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['name']}",
        "",
        f"**Architecture:** `{result['architecture']}`",
        "",
        result["verdict"],
        "",
        "## Start now",
    ]
    lines.extend(f"- {item}" for item in result["services_now"])
    lines.append("\n## Defer")
    lines.extend(f"- {item}" for item in result["defer"] or ["Nothing identified by the basic rules."])
    lines.append("\n## Warnings")
    lines.extend(f"- {item}" for item in result["warnings"] or ["No basic warning; detailed inventory is still required."])
    lines.append("\n## Next checks")
    lines.extend(f"- {item}" for item in result["next_checks"])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Path to a sanitized JSON hardware file")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    result = recommend(config)
    print(json.dumps(result, indent=2) if args.json else render_markdown(result))


if __name__ == "__main__":
    main()
