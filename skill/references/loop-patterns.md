# Loop Patterns

Use these patterns to design durable Codex workflows.

## Development Implementation Loop

Trigger: user asks Codex to build, fix, or refactor.

Flow:

1. Read project brief, preferences, approval gates, and relevant runbook.
2. Create or update a goal card.
3. Inspect repo state and tests.
4. Implement scoped changes.
5. Run verification.
6. Update decisions and open loops.
7. Finalize with changed files, test results, and next decision.

## PR/CI Monitoring Loop

Trigger: user wants Codex to watch a pull request, CI run, or deployment.

Flow:

1. Record target URL, branch, or PR number in an active goal.
2. On each wakeup, check status and recent comments/logs.
3. If failing, summarize cause and implement a local fix when safe.
4. If action requires approval, draft the exact proposed action.
5. Stop or reduce cadence when checks pass or the user closes the loop.

## Review Feedback Loop

Trigger: user asks Codex to address review comments.

Flow:

1. Gather unresolved review threads and changed-file context.
2. Group comments into actionable fixes, questions, and non-actions.
3. Implement small, testable fixes first.
4. Report any comment that needs product judgment.
5. Update open loops with remaining review items.

## Release Readiness Loop

Trigger: user asks whether a feature, sprint, or release is ready.

Flow:

1. Define readiness criteria and approval gates.
2. Run tests, lint, build, and targeted manual checks.
3. Inspect docs, migration notes, and user-visible changes.
4. Produce a concise readiness result: pass, risk, blocker.
5. Record release decisions and unresolved risks.

## Chief-of-Staff Loop

Trigger: user wants Codex to monitor messages, inboxes, or issue trackers.

Flow:

1. Search only approved sources.
2. Summarize items needing attention.
3. Gather context before drafting replies.
4. Draft, but do not send without approval.
5. Record follow-ups in open loops.

