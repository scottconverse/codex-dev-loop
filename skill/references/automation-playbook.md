# Automation Playbook

Use this when the user wants Codex to check back, monitor something, create a reminder, or run a recurring workflow.

## Automation Choice

- Use a heartbeat attached to the current thread when the work should continue this conversation.
- Use a cron/workspace automation when the task is detached from this thread and tied to one or more workspace directories.
- Use suggested create/update when the automation needs a worktree environment setup for user review.

## Required Fields To Decide

- Target: PR, branch, CI run, deploy URL, inbox, Slack thread, open-loop list, or other source.
- Cadence: every N minutes, hourly, daily, weekly, or until condition.
- Stop condition: checks pass, PR merged, user approves, date reached, no changes after N checks.
- Approval boundary: what Codex may do automatically and what requires approval.
- Output: summary only, draft fix, local patch, screenshots, dashboard, or explicit question.

## Standard Prompts

### PR/CI Monitor

Check the target PR or branch status. Summarize new failures, review comments, and deployment state. If a safe local fix is available, prepare it and report verification. Do not merge, deploy, post comments, or push without approval.

### Open Loop Review

Review `.codex-loop/open-loops.md` and active goals. Identify stale items, completed loops, blocked loops, and suggested next actions. Update only local memory files unless the user approves external action.

### Deploy Watch

Check the target deployment or preview. Report readiness, errors, screenshots if useful, and the next decision. Do not publish or promote anything without approval.

### Message Drafting

Check approved message sources for items needing attention. Gather context and draft replies. Do not send, post, or react without approval.

## Registry Entry

Add or update this in `.codex-loop/automation-registry.md`:

```markdown
| Date | Name | Target | Cadence | Status | Stop Condition | Approval Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | PR CI Monitor | PR URL | Every 30 min | proposed | Checks pass | No pushes/comments/merges without approval |
```

