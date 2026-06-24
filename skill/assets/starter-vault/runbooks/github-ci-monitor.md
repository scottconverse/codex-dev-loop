# Runbook: GitHub CI Monitor

## Trigger

Use when the user asks Codex to watch a PR, branch, workflow run, or preview deployment.

## Inputs

- Repo and branch or PR URL
- Desired cadence
- Stop condition

## Steps

1. Record the target in an active goal card.
2. Check PR status, checks, review comments, and deployment state.
3. If failing, inspect logs and identify the smallest likely fix.
4. Implement local fixes when safe and verify them.
5. Report exactly what changed and what still requires approval.
6. Do not push, comment, merge, or deploy without approval.

## Verification

- Relevant tests or build command
- CI/check status summary
- Preview URL or screenshot when applicable

