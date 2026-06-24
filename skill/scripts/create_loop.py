import argparse
from datetime import date
from pathlib import Path

from loop_utils import slugify


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Codex dev loop contract.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    parser.add_argument("--name", required=True, help="Loop name.")
    parser.add_argument("--description", default="", help="What repeated task this loop handles.")
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--scope", default="Define exact queues, labels, files, URLs, or systems in bounds.")
    parser.add_argument("--action", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--stop-condition", required=True)
    parser.add_argument("--escalation", default="Ask before external or irreversible actions.")
    parser.add_argument("--max-attempts", default="3")
    parser.add_argument("--max-minutes", default="30")
    parser.add_argument("--max-files-changed", default="10")
    parser.add_argument("--max-consecutive-failures", default="2")
    parser.add_argument("--status", default="proposed")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    loops = root / ".codex-loop" / "loops"
    loops.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.name)
    path = loops / f"{date.today().isoformat()}-{slug}.yaml"
    if path.exists():
        raise SystemExit(f"loop already exists: {path}")

    content = f"""name: {slug}
description: {args.description or args.name}
trigger: {args.trigger}
scope: {args.scope}
action: {args.action}
verifier: {args.verifier}
budget:
  max_attempts: {args.max_attempts}
  max_minutes: {args.max_minutes}
  max_files_changed: {args.max_files_changed}
  max_consecutive_failures: {args.max_consecutive_failures}
stop_condition: {args.stop_condition}
escalation: {args.escalation}
status: {args.status}
"""
    path.write_text(content, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

