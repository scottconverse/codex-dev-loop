# Loop Engineering With Codex Dev Loop

Version: 0.2.0

Loop engineering means designing the system that prompts, checks, and re-prompts an agent until a measurable condition is met or the loop stops itself.

Codex Dev Loop treats a loop as a contract plus a run log:

- the contract lives in `.codex-loop/loops/`
- each pass lives in `.codex-loop/runs/`

## Loop Contract

Create one with:

```powershell
python <skill-dir>\scripts\create_loop.py --target . --name "pr babysitter" --trigger "Every 15 minutes" --scope "Open PRs labeled agent-watch" --action "Inspect CI and attempt one deterministic fix" --verifier "CI green and no blocking review comments" --stop-condition "CI green or budget exhausted"
```

The contract includes:

- trigger
- scope
- action
- verifier
- budget
- stop condition
- escalation
- status

## Run Log

Record a pass with:

```powershell
python <skill-dir>\scripts\record_loop_run.py --target . --loop pr-babysitter --observed "CI red on auth tests" --action "Prepared one deterministic fix" --verifier-result failed --failure-signature "auth timeout test still failing" --next-step "Ask user before push"
```

## Health Check

```powershell
python <skill-dir>\scripts\run_loop_check.py --target .
```

This reports active loops, stalled loops, missing fields, and recent run state.

## Good Loops

- PR babysitter
- CI health clustering
- deploy verification
- feedback clustering
- docs freshness
- release readiness

## Bad Loops

- "make the code better"
- "figure out why users churn"
- "improve the design until it feels right"
- any task with no verifier or no budget

## Safety Rules

- Independent verifier for risky work.
- Max attempts and max wall-clock time.
- Max files changed.
- Max consecutive failures.
- Escalate before pushing, merging, deploying, posting, deleting, spending, or changing production.

