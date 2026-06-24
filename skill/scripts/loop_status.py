import argparse
import html
import re
from datetime import datetime
from pathlib import Path


def read(path: Path) -> str:
    if not path.exists():
        return "_Missing_"
    return path.read_text(encoding="utf-8", errors="ignore").strip() or "_Empty_"


def list_md(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)


def md_to_html(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = html.escape(raw)
        if line.startswith("# "):
            lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("- "):
            lines.append(f"<li>{line[2:]}</li>")
        elif line.strip():
            lines.append(f"<p>{line}</p>")
    return "\n".join(lines)


def section(title: str, body: str) -> str:
    return f"<section class='panel'><h2>{html.escape(title)}</h2>{md_to_html(body)}</section>"


def count_active_goals(paths: list[Path]) -> int:
    count = 0
    for path in paths:
        if "template" in path.name.lower():
            continue
        text = read(path).lower()
        if re.search(r"## status\s+active\b", text):
            count += 1
    return count


def count_pending_approvals(vault: Path) -> int:
    text = read(vault / "approval-queue.md").lower()
    return sum(1 for line in text.splitlines() if line.startswith("|") and "pending" in line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a Codex dev loop vault.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    parser.add_argument("--html", action="store_true", help="Write .codex-loop/dashboard.html.")
    args = parser.parse_args()

    vault = Path(args.target).resolve() / ".codex-loop"
    if not vault.exists():
        raise SystemExit(f"missing vault: {vault}")

    goals = list_md(vault / "goals")
    decisions = list_md(vault / "decisions")
    runbooks = list_md(vault / "runbooks")

    summary = {
        "vault": str(vault),
        "goals": len([p for p in goals if "template" not in p.name.lower()]),
        "active_goals": count_active_goals(goals),
        "decisions": len([p for p in decisions if "template" not in p.name.lower()]),
        "runbooks": len(runbooks),
        "pending_approvals": count_pending_approvals(vault),
    }

    for key, value in summary.items():
        print(f"{key}: {value}")

    if args.html:
        parts = [
            "<!doctype html><html><head><meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1'>",
            "<title>Codex Dev Loop Dashboard</title>",
            "<style>body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f6f7f9;color:#15171a}header{background:#111827;color:white;padding:24px 32px}main{max-width:1180px;margin:0 auto;padding:24px;display:grid;gap:16px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.metric,.panel{background:white;border:1px solid #d8dde6;border-radius:8px;padding:18px}.metric strong{display:block;font-size:32px}.metric span{color:#5b6472}h1,h2{margin-top:0}p,li{line-height:1.45}code{background:#eef1f5;padding:2px 4px;border-radius:4px}.meta{color:#cbd5e1}.warn{border-color:#f59e0b}.ok{border-color:#10b981}</style>",
            "</head><body>",
            f"<header><h1>Codex Dev Loop Dashboard</h1><div class='meta'>{html.escape(datetime.now().isoformat(timespec='seconds'))}</div></header><main>",
            "<div class='grid'>",
            f"<div class='metric {'warn' if summary['active_goals'] else 'ok'}'><strong>{summary['active_goals']}</strong><span>Active goals</span></div>",
            f"<div class='metric {'warn' if summary['pending_approvals'] else 'ok'}'><strong>{summary['pending_approvals']}</strong><span>Pending approvals</span></div>",
            f"<div class='metric'><strong>{summary['decisions']}</strong><span>Decisions</span></div>",
            f"<div class='metric'><strong>{summary['runbooks']}</strong><span>Runbooks</span></div>",
            "</div>",
            section("Project Brief", read(vault / "project-brief.md")),
            section("Open Loops", read(vault / "open-loops.md")),
            section("Approval Queue", read(vault / "approval-queue.md")),
            section("Approval Gates", read(vault / "approval-gates.md")),
            section("Automation Registry", read(vault / "automation-registry.md")),
            "<section class='panel'><h2>Recent Goals</h2><ul>",
        ]
        for path in goals[:8]:
            parts.append(f"<li><code>{html.escape(path.name)}</code></li>")
        parts.append("</ul></section><section class='panel'><h2>Recent Decisions</h2><ul>")
        for path in decisions[:8]:
            parts.append(f"<li><code>{html.escape(path.name)}</code></li>")
        parts.append("</ul></section><section class='panel'><h2>Runbooks</h2><ul>")
        for path in runbooks:
            parts.append(f"<li><code>{html.escape(path.name)}</code></li>")
        parts.append("</ul></section></main></body></html>")
        out = vault / "dashboard.html"
        out.write_text("\n".join(parts), encoding="utf-8")
        print(f"dashboard: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
