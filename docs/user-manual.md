# Codex Dev Loop User Manual

Version: 0.1.0

## 1. Purpose

Codex Dev Loop gives development work a durable home. Instead of restarting context every thread, a project gets a `.codex-loop/` vault with goals, decisions, open loops, approvals, runbooks, and review surfaces.

## 2. Install

Run the installer from the repository root.

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\installers\install.ps1
```

Bash:

```bash
bash installers/install.sh
```

By default, the skill installs to:

- Windows: `%USERPROFILE%\.codex\skills\codex-dev-loop`
- macOS/Linux: `$HOME/.codex/skills/codex-dev-loop`

You can override the destination:

```powershell
powershell -ExecutionPolicy Bypass -File .\installers\install.ps1 -Destination C:\path\to\skills\codex-dev-loop
```

```bash
bash installers/install.sh --destination /path/to/skills/codex-dev-loop
```

## 3. Start A Project Loop

Open a repo in Codex desktop and say:

```text
Use $codex-dev-loop for this repo. Initialize the dev loop vault.
```

Or run:

```powershell
python <skill-dir>\scripts\bootstrap_vault.py --target .
```

## 4. Work With Goals

For substantial work, create a goal card:

```powershell
python <skill-dir>\scripts\create_goal.py --target . --name "fix auth timeout" --objective "Users stay signed in across refreshes" --verification "Run auth tests and manual browser check"
```

A good goal includes:

- objective
- scope
- constraints
- verification
- approval gates
- status

## 5. Memory Files

Use the vault as reviewable memory:

- `project-brief.md`: product direction, architecture, repo conventions
- `preferences.md`: durable user preferences
- `decisions/`: dated technical and product decisions
- `open-loops.md`: blockers, follow-ups, waiting items
- `automation-registry.md`: recurring checks and wakeups
- `approval-queue.md`: actions waiting for user approval
- `inbox/`: raw transcripts, voice notes, and rough context

## 6. Approval Queue

Queue any action that changes external state:

```powershell
python <skill-dir>\scripts\queue_approval.py --target . --title "push branch" --action "Push local branch" --target-action "origin/feature-x"
```

Codex should not perform queued actions until the user approves the exact action and target.

## 7. Finalization Check

Before wrapping substantial work, run:

```powershell
python <skill-dir>\scripts\finalize_check.py --target .
```

This reports:

- active goals
- pending approvals
- missing required memory files

## 8. Dashboard

Generate a local HTML dashboard:

```powershell
python <skill-dir>\scripts\loop_status.py --target . --html
```

Open `.codex-loop/dashboard.html` to review current state.

## 9. Automations

Codex desktop supports real recurring automations. Use this system to define the target, cadence, stop condition, and approval boundary.

Example request:

```text
Use $codex-dev-loop. Watch PR 42 every 30 minutes until CI passes. Prepare fixes locally, but do not push or comment without approval.
```

Codex should record the automation in `automation-registry.md`.

## 10. Voice And Transcripts

Save rough notes:

```powershell
python <skill-dir>\scripts\ingest_transcript.py --target . --source notes.txt --title "release feedback"
```

Then distill the note into decisions, preferences, actions, and open loops.

## 11. Recommended Workflow

1. Use a pinned Codex thread per important project.
2. Initialize `.codex-loop/`.
3. Create a goal card for substantial work.
4. Let Codex implement and verify.
5. Record decisions and open loops.
6. Queue external actions for approval.
7. Run finalization check before closing.
