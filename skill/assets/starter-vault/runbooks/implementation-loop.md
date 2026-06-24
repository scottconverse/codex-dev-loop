# Runbook: Implementation Loop

## Trigger

Use when the user asks Codex to build, fix, or refactor code.

## Inputs

- User request
- Relevant goal card
- Current repo state
- Test/build commands

## Steps

1. Read project brief, preferences, approval gates, and relevant memory.
2. Inspect files before editing.
3. Create or update a goal card for substantial work.
4. Implement scoped changes.
5. Run verification.
6. Update decisions or open loops if anything durable changed.
7. Final response: changed files, verification, unresolved loops.

## Approval Points

Pause before publishing, deploying, merging, deleting, or sending externally.

