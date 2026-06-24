# Loop Engineering

Use this when a task should repeat without the user manually prompting each turn.

## Fit Check

Create a loop only when all are true:

- The task repeats.
- The scope can be bounded.
- A verifier can cheaply say met/not met.
- A budget can cap cost and blast radius.
- A stop condition and escalation path are clear.

Do not loop one-shot edits, broad discovery, subjective taste work, or tasks without a cheap verifier.

## Contract Fields

- `name`: stable id, hyphen-case.
- `trigger`: schedule, webhook, label, file change, or manual.
- `scope`: exact queue, repo, files, URLs, labels, or systems in bounds.
- `action`: what Codex can attempt.
- `verifier`: objective check, command, API status, count, or artifact condition.
- `budget`: `max_attempts`, `max_minutes`, `max_files_changed`, `max_consecutive_failures`.
- `stop_condition`: success or exhaustion condition.
- `escalation`: when to ask the user.
- `status`: proposed, active, paused, stalled, complete, retired.

## Roles

Keep executor and verifier separate in the workflow description when the risk warrants it. The executor changes things. The verifier judges evidence. A loop that grades its own vague work is not trustworthy.

## Run Log

Every pass should record:

- observed state
- action taken
- verifier result: passed, failed, blocked, skipped
- failure signature when failed
- budget used
- next step

Stall when the same failure signature repeats or the max consecutive failures budget is reached.

