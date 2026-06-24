import argparse
from pathlib import Path


REQUIRED = [
    "project-brief.md",
    "preferences.md",
    "approval-gates.md",
    "open-loops.md",
    "automation-ideas.md",
    "automation-registry.md",
    "approval-queue.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Codex dev loop vault for missing or stale-looking memory.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    args = parser.parse_args()

    vault = Path(args.target).resolve() / ".codex-loop"
    if not vault.exists():
        raise SystemExit(f"missing vault: {vault}")

    issues: list[str] = []
    for rel in REQUIRED:
        path = vault / rel
        if not path.exists():
            issues.append(f"missing file: {rel}")
        elif not path.read_text(encoding="utf-8").strip():
            issues.append(f"empty file: {rel}")

    for rel in ["goals", "loops", "runs", "decisions", "runbooks", "inbox"]:
        path = vault / rel
        if not path.exists():
            issues.append(f"missing directory: {rel}")

    goals = list((vault / "goals").glob("*.md")) if (vault / "goals").exists() else []
    active_goals = []
    for goal in goals:
        text = goal.read_text(encoding="utf-8", errors="ignore").lower()
        if "active" in text and "template" not in goal.name.lower():
            active_goals.append(goal.name)

    print(f"vault: {vault}")
    print(f"active_goals: {len(active_goals)}")
    for name in active_goals:
        print(f"- {name}")

    if issues:
        print("issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("memory_check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
