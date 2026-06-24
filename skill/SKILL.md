---
name: codex-dev-loop
description: Build and operate a durable Codex development workflow for a repo or project. Use when the user wants smoother development with Codex, persistent project memory, reusable runbooks, approval gates, automation loops, goal cards, release/readiness checks, or a Codex operating system inspired by long-running threads and reviewable memory.
---

# Codex Dev Loop

Use this skill to make Codex collaboration durable, reviewable, and testable across a development project.

## Core Loop

1. Locate or create a project memory vault. Prefer `.codex-loop/` in the repo. In projectless threads, use `outputs/codex-dev-loop-system/` for user-facing setup.
2. Read the current project brief, open loops, decisions, preferences, and runbooks before making broad changes.
3. Convert vague requests into a goal card with done criteria and verification.
4. Work normally, but update memory when decisions, preferences, blockers, or open loops change.
5. Before final response, report verification, changed files, unresolved loops, and memory updates.

## Vault Shape

Use this directory shape unless the repo already has a comparable system:

```text
.codex-loop/
  project-brief.md
  preferences.md
  approval-gates.md
  goals/
  decisions/
  inbox/
  open-loops.md
  runbooks/
  automation-ideas.md
  automation-registry.md
  approval-queue.md
```

If a vault exists, preserve local conventions and add only missing pieces.

To initialize a vault, run:

```powershell
python <skill-dir>\scripts\bootstrap_vault.py --target .
```

Use `--force` only when the user explicitly wants starter templates to overwrite existing vault files.

Useful helper scripts:

```powershell
python <skill-dir>\scripts\create_goal.py --target . --name "short name" --objective "verified outcome"
python <skill-dir>\scripts\loop_status.py --target . --html
python <skill-dir>\scripts\memory_check.py --target .
python <skill-dir>\scripts\finalize_check.py --target .
python <skill-dir>\scripts\ingest_transcript.py --target . --source notes.txt
python <skill-dir>\scripts\queue_approval.py --target . --title "push branch" --action "Push branch feature-x"
```

## Goal Cards

Create a goal card for substantial work in `goals/YYYY-MM-DD-short-name.md`.

Include:

- Objective: concrete user-visible outcome.
- Scope: files, systems, or behaviors in bounds.
- Constraints: things to preserve or avoid.
- Verification: commands, screenshots, manual checks, or acceptance criteria.
- Approval gates: actions that require user consent.
- Status: active, blocked, ready for review, complete.

Prefer strong goals that Codex can verify. Example: "Refactor auth middleware while keeping the public API compatible; done when existing auth tests pass and changed behavior is documented."

## Memory Rules

Record durable facts only. Do not store noisy transcripts, guesses, secrets, credentials, or private content unrelated to the project.

Update:

- `project-brief.md` when product direction, architecture, or repo conventions become clear.
- `preferences.md` when the user states durable working preferences.
- `decisions/` when a meaningful technical or product decision is made.
- `open-loops.md` when something is waiting, blocked, delegated, or needs follow-up.
- `runbooks/` when a repeatable workflow emerges.
- `automation-registry.md` when a recurring check is proposed, active, paused, or retired.
- `approval-queue.md` when Codex needs user approval for an external or irreversible action.
- `inbox/` for raw voice notes, transcripts, screenshots, and rough context that still needs distillation.

Keep entries dated, concise, and reviewable. If memory is uncertain, mark it as tentative.

Before finishing substantial work, run `finalize_check.py` when a vault exists and update any stale active goal, open loop, decision record, or pending approval.

## Approval Gates

Default to asking before:

- sending messages or emails
- publishing, deploying, merging, or releasing
- deleting user data or destructive filesystem operations
- changing production configuration
- spending money or making purchases
- taking action in authenticated external systems on the user's behalf

Drafts, local edits, tests, screenshots, summaries, and local preview work usually do not need approval unless the project vault says otherwise.

## Runbooks

Create runbooks for repeated workflows. Keep them short and executable.

Good runbooks include:

- trigger: when to use it
- inputs: what Codex needs
- steps: the reliable sequence
- verification: how to know it worked
- approval points: where to pause
- memory updates: what to record afterward

Read `references/loop-patterns.md` when designing a new loop or automation.
Read `references/automation-playbook.md` when creating or updating recurring wakeups.
Read `references/review-surfaces.md` when building side-panel artifacts, previews, dashboards, or screenshot review flows.
Read `references/voice-and-transcripts.md` when the user provides raw spoken notes, meeting transcripts, or messy feedback.

## Automations

When the user asks for recurring checks or wakeups, use the available automation tools rather than writing raw scheduling text. Attach the automation to the durable thread when possible.

Useful automation loops:

- Check PR/CI status and summarize blockers.
- Monitor review comments and prepare fixes.
- Watch deploy/preview status and report when ready.
- Review open loops daily or weekly.
- Draft follow-ups from issue trackers, Slack, or email, without sending.

Keep irreversible actions behind explicit approval.

Record every live or proposed automation in `.codex-loop/automation-registry.md` with owner, cadence, status, stop condition, and approval boundary.

## Durable Thread Setup

For important workstreams, use a pinned thread as the home thread. When thread tools are available:

1. Find the current or target thread with thread search/list tools.
2. Rename it to a durable, project-specific title.
3. Pin it.
4. Record the thread role in `project-brief.md` or `open-loops.md`.

Do not hand off the current thread to another host unless the user explicitly asks for remote execution.

## Approval Queue

Use `.codex-loop/approval-queue.md` to queue actions that need user consent.

Queue approval for:

- external messages, comments, replies, or posts
- pushes, merges, releases, deploys, or production changes
- destructive filesystem or data actions
- purchases or paid actions
- authenticated third-party actions on the user's behalf

Include title, exact action, target, risk, status, and the exact user approval needed. Do not perform queued actions until the user approves them.

## Side-Panel Review

When visual or artifact review matters, create a small review surface rather than relying on prose alone. Good options:

- local app preview with screenshots
- generated HTML dashboard
- Markdown/PDF/spreadsheet artifact in `outputs/`
- before/after image set
- test or CI summary

Use `loop_status.py --html` to generate a status dashboard for the vault.

## Final Response Checklist

When this skill is used, close with:

- what was set up or changed
- where the vault or skill lives
- what verification ran
- any open loops or approval gates still active

Run `finalize_check.py` first when a vault exists. If it reports pending approvals or stale active goals, mention them plainly.
