import argparse
import re
from pathlib import Path

from loop_utils import loop_files, loop_status, parse_run, read_loop, run_files


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def active_goals(vault: Path) -> list[str]:
    found = []
    goals = vault / "goals"
    if not goals.exists():
        return found
    for path in goals.glob("*.md"):
        if "template" in path.name.lower():
            continue
        text = read(path).lower()
        if re.search(r"## status\s+active\b", text):
            found.append(path.name)
    return found


def pending_approvals(vault: Path) -> list[str]:
    text = read(vault / "approval-queue.md")
    pending = []
    for line in text.splitlines():
        if line.startswith("|") and "pending" in line.lower():
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 6 and cells[0].lower() != "date":
                pending.append(cells[1])
    return pending


def stalled_loops(vault: Path) -> list[str]:
    found: list[str] = []
    for path in loop_files(vault):
        data = read_loop(path)
        if loop_status(data) == "stalled":
            found.append(path.name)
            continue
        budget = data.get("budget", {})
        max_failures = 2
        if isinstance(budget, dict):
            try:
                max_failures = int(str(budget.get("max_consecutive_failures", 2)))
            except ValueError:
                max_failures = 2
        recent = [parse_run(p) for p in run_files(vault, str(data.get("name", path.stem)))[:max_failures]]
        if len(recent) >= max_failures and all(r.get("verifier_result") == "failed" for r in recent):
            signatures = [r.get("failure_signature", "") for r in recent]
            if signatures and len(set(signatures)) == 1 and signatures[0] not in ("", "n/a"):
                found.append(path.name)
    return sorted(set(found))


def main() -> int:
    parser = argparse.ArgumentParser(description="Final pre-response check for Codex dev loop memory.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    args = parser.parse_args()

    vault = Path(args.target).resolve() / ".codex-loop"
    if not vault.exists():
        raise SystemExit(f"missing vault: {vault}")

    issues = []
    for rel in ["project-brief.md", "open-loops.md", "approval-gates.md", "approval-queue.md"]:
        if not (vault / rel).exists():
            issues.append(f"missing {rel}")

    active = active_goals(vault)
    pending = pending_approvals(vault)
    stalled = stalled_loops(vault)

    print(f"vault: {vault}")
    print(f"active_goals: {len(active)}")
    for goal in active:
        print(f"- {goal}")
    print(f"pending_approvals: {len(pending)}")
    for approval in pending:
        print(f"- {approval}")
    print(f"stalled_loops: {len(stalled)}")
    for loop in stalled:
        print(f"- {loop}")

    if issues:
        print("issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("finalize_check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
