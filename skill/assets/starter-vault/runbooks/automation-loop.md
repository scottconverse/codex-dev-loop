# Runbook: Automation Loop

## Trigger

Use when the user asks Codex to watch, monitor, check back, remind, or keep moving something later.

## Inputs

- Target source or URL
- Cadence
- Stop condition
- Approval boundary
- Expected output

## Steps

1. Read `automation-registry.md` to avoid duplicates.
2. Choose heartbeat for current-thread continuity or cron for detached workspace checks.
3. Create or propose the automation with the automation tool.
4. Record the automation in `automation-registry.md`.
5. On each wakeup, summarize changes, perform safe local work, and ask before irreversible actions.
6. Retire, pause, or reduce cadence when the stop condition is reached.

## Approval Points

Pause before posting, sending, pushing, merging, deploying, purchasing, or changing production settings.

