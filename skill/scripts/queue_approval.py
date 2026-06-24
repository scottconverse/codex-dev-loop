import argparse
from datetime import date
from pathlib import Path


def clean_cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ").strip()


def ensure_table(path: Path) -> None:
    if path.exists() and path.read_text(encoding="utf-8").strip():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Approval Queue\n\n"
        "| Date | Title | Action | Target | Risk | Status | User Approval Needed |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Queue an action that requires user approval.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--target-action", default="", help="External system, file, branch, URL, or recipient.")
    parser.add_argument("--risk", default="External or irreversible action.")
    parser.add_argument("--approval-needed", default="User must approve the exact action and target.")
    args = parser.parse_args()

    vault = Path(args.target).resolve() / ".codex-loop"
    queue = vault / "approval-queue.md"
    ensure_table(queue)

    row = (
        f"| {date.today().isoformat()} | {clean_cell(args.title)} | {clean_cell(args.action)} | "
        f"{clean_cell(args.target_action)} | {clean_cell(args.risk)} | pending | "
        f"{clean_cell(args.approval_needed)} |\n"
    )
    with queue.open("a", encoding="utf-8") as handle:
        handle.write(row)
    print(queue)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

