from __future__ import annotations

import re
from pathlib import Path


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return value.strip("-") or "loop"


def read_loop(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current_parent: str | None = None
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") and current_parent and ":" in raw:
            key, value = raw.strip().split(":", 1)
            parent = data.setdefault(current_parent, {})
            if isinstance(parent, dict):
                parent[key.strip()] = value.strip()
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = value
                current_parent = None
            else:
                data[key] = {}
                current_parent = key
    return data


def loop_files(vault: Path) -> list[Path]:
    loops = vault / "loops"
    if not loops.exists():
        return []
    return sorted([p for p in loops.glob("*.yaml") if "template" not in p.name.lower()])


def run_files(vault: Path, loop_name: str | None = None) -> list[Path]:
    runs = vault / "runs"
    if not runs.exists():
        return []
    paths = sorted(
        [p for p in runs.glob("*.md") if p.name.lower() != "readme.md" and "template" not in p.name.lower()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if loop_name is None:
        return paths
    slug = slugify(loop_name)
    return [p for p in paths if f"-{slug}-" in p.name or p.name.endswith(f"-{slug}.md")]


def parse_run(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if raw.startswith("- ") and ":" in raw:
            key, value = raw[2:].split(":", 1)
            data[key.strip().lower().replace(" ", "_")] = value.strip()
    return data


def loop_status(data: dict[str, object]) -> str:
    value = str(data.get("status", "")).strip().lower()
    return value or "unknown"


def required_loop_fields() -> list[str]:
    return [
        "name",
        "trigger",
        "scope",
        "action",
        "verifier",
        "budget",
        "stop_condition",
        "escalation",
        "status",
    ]
