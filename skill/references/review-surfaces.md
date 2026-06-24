# Review Surfaces

Use this when Codex should make work inspectable inside the thread or side panel.

## Choose A Surface

- Frontend app: run the dev server and inspect with browser screenshots.
- Static review: create a single `index.html` with embedded CSS/JS.
- Project status: generate `.codex-loop/dashboard.html` with `loop_status.py --html`.
- Docs/data: create Markdown, PDF, spreadsheet, or CSV artifacts in `outputs/`.
- Visual change: produce before/after screenshots and note viewport sizes.

## Expectations

- Show the actual artifact, not a marketing placeholder.
- Keep review surfaces local and reversible.
- Include verification status and known gaps.
- Treat comments or user feedback on the artifact as new instructions.

## Dashboard Pattern

The `.codex-loop` dashboard should show:

- active goals
- open loops
- recent decisions
- approval gates
- automation registry
- stale items or missing files

