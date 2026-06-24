# Codex Dev Loop

Codex Dev Loop is a lightweight operating system for long-running development work with the Codex desktop app.

It packages a reusable Codex skill, a project memory vault, approval gates, goal cards, automation runbooks, and local helper scripts so Codex can keep context, verify work, and ask for approval at the right moments.

Version: **0.1.0**

## What It Gives You

- A local Codex skill: `$codex-dev-loop`
- A repo-local `.codex-loop/` memory vault
- Goal cards with done criteria and verification
- Approval gates for external or irreversible actions
- Approval queue for pushes, deploys, messages, merges, and production changes
- Open-loop tracking
- Automation registry and runbooks
- Voice/transcript intake workflow
- HTML status dashboard
- GitHub/CI monitoring runbook
- Side-panel review workflow

## Quick Install

Clone the repo, then run the installer for your shell.

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\installers\install.ps1
```

Bash:

```bash
bash installers/install.sh
```

The installer copies `skill/` into your Codex skills directory as `codex-dev-loop`.

## Use In Codex Desktop

In a project thread, say:

```text
Use $codex-dev-loop for this repo.
```

Then ask Codex to initialize the vault:

```text
Initialize the dev loop vault here.
```

Or run it yourself from the project root:

```powershell
python $HOME\.codex\skills\codex-dev-loop\scripts\bootstrap_vault.py --target .
```

## Project Vault

The default vault shape:

```text
.codex-loop/
  project-brief.md
  preferences.md
  approval-gates.md
  approval-queue.md
  goals/
  decisions/
  inbox/
  open-loops.md
  runbooks/
  automation-ideas.md
  automation-registry.md
```

## Helper Scripts

```powershell
python <skill-dir>\scripts\bootstrap_vault.py --target .
python <skill-dir>\scripts\create_goal.py --target . --name "first goal" --objective "verified outcome"
python <skill-dir>\scripts\memory_check.py --target .
python <skill-dir>\scripts\finalize_check.py --target .
python <skill-dir>\scripts\loop_status.py --target . --html
python <skill-dir>\scripts\queue_approval.py --target . --title "push branch" --action "Push branch feature-x"
python <skill-dir>\scripts\ingest_transcript.py --target . --source notes.txt
```

## Documentation

- [User manual](docs/user-manual.md)
- [Landing page](docs/index.html)
- [Discussion seed posts](discussion-seeds/)

## Safety Model

Codex may normally proceed with local reads, local edits, tests, local dashboards, and drafts.

Codex must ask before:

- sending messages, comments, or emails
- pushing, merging, deploying, publishing, or releasing
- deleting data or running destructive operations
- changing production configuration
- spending money
- taking authenticated third-party actions on your behalf

## Repository Status

This is an early 0.1.0 system. It intentionally starts simple: files, scripts, and a Codex skill. The next layer is real project adoption and live Codex desktop heartbeats for specific PRs, CI runs, deployments, and review loops.
