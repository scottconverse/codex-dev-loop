import argparse
import re
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return value.strip("-") or "transcript"


def main() -> int:
    parser = argparse.ArgumentParser(description="Save raw spoken/transcript context into the Codex dev loop inbox.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    parser.add_argument("--source", required=True, help="Text file to ingest.")
    parser.add_argument("--title", default="", help="Optional title.")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f"missing source: {source}")

    vault = Path(args.target).resolve() / ".codex-loop"
    inbox = vault / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    title = args.title or source.stem
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    out = inbox / f"{timestamp}-{slugify(title)}.md"
    raw = source.read_text(encoding="utf-8", errors="ignore")
    content = f"""# Inbox: {title}

Source: `{source}`
Captured: {datetime.now().isoformat(timespec="seconds")}

## Raw

{raw}

## Distillation

- Decisions:
- Preferences:
- Actions:
- Open loops:
- Questions:
"""
    out.write_text(content, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

