# Runbook: Finalize And Memory Enforcement

## Trigger

Use before the final response on substantial work in a project with `.codex-loop/`.

## Steps

1. Run `memory_check.py --target .`.
2. Update active goal status.
3. Record meaningful decisions.
4. Add unresolved follow-ups to `open-loops.md`.
5. Queue any external or irreversible proposed action in `approval-queue.md`.
6. Run `finalize_check.py --target .`.
7. Mention pending approvals and unresolved loops in the final response.

## Approval Points

Do not perform queued actions until the user approves the exact action and target.

