import argparse
from datetime import datetime
from pathlib import Path

from loop_utils import slugify


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a Codex dev loop run.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    parser.add_argument("--loop", required=True, help="Loop name or id.")
    parser.add_argument("--observed", required=True, help="Observed state.")
    parser.add_argument("--action", required=True, help="Action taken.")
    parser.add_argument("--verifier-result", choices=["passed", "failed", "blocked", "skipped"], required=True)
    parser.add_argument("--failure-signature", default="", help="Stable signature for repeated failures.")
    parser.add_argument("--budget-used", default="", help="Attempts/minutes/files used.")
    parser.add_argument("--next-step", default="", help="Next step or escalation.")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    runs = root / ".codex-loop" / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S-%f")
    slug = slugify(args.loop)
    path = runs / f"{timestamp}-{slug}.md"

    content = f"""# Run: {args.loop}

- Captured: {datetime.now().isoformat(timespec="seconds")}
- Loop: {slug}
- Observed: {args.observed}
- Action: {args.action}
- Verifier Result: {args.verifier_result}
- Failure Signature: {args.failure_signature or "n/a"}
- Budget Used: {args.budget_used or "n/a"}
- Next Step: {args.next_step or "n/a"}
"""
    path.write_text(content, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
