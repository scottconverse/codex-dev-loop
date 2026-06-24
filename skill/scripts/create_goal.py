import argparse
import re
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return value.strip("-") or "goal"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Codex dev loop goal card.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    parser.add_argument("--name", required=True, help="Short goal name.")
    parser.add_argument("--objective", required=True, help="Concrete outcome.")
    parser.add_argument("--verification", default="", help="Verification command or criteria.")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    goals = root / ".codex-loop" / "goals"
    goals.mkdir(parents=True, exist_ok=True)
    path = goals / f"{date.today().isoformat()}-{slugify(args.name)}.md"
    if path.exists():
        raise SystemExit(f"goal already exists: {path}")

    content = f"""# Goal: {args.name}

## Objective

{args.objective}

## Scope

In bounds:

- 

Out of bounds:

- 

## Constraints

- Preserve unrelated user changes.
- Follow existing project conventions.

## Verification

- {args.verification or "Define and run the relevant checks before closing this goal."}

## Approval Gates

- Ask before publishing, deploying, merging, sending externally, deleting data, or changing production settings.

## Status

active
"""
    path.write_text(content, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

