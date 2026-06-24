# Changelog

## 0.2.0 - 2026-06-24

Adds first-class loop engineering primitives.

- Added `.codex-loop/loops/` loop contracts with trigger, action, verifier, budget, stop condition, escalation, and status.
- Added `.codex-loop/runs/` execution logs.
- Added loop templates for PR babysitting, CI health clustering, deploy verification, feedback clustering, docs freshness, and release readiness.
- Added `create_loop.py`, `record_loop_run.py`, and `run_loop_check.py`.
- Dashboard now shows active loops, stalled loops, recent loop specs, and recent run logs.
- Finalization check now reports stalled loops.
- Docs now describe loop engineering, budgets, verifiers, stall detection, and when not to loop.

## 0.1.0 - 2026-06-24

Initial public release.

- Installable `$codex-dev-loop` Codex skill.
- Starter `.codex-loop/` project memory vault.
- Goal cards, approval gates, approval queue, open loops, automation registry, and runbooks.
- Helper scripts for vault bootstrap, goal creation, memory checks, finalization checks, transcript intake, approval queueing, and dashboard generation.
- Desktop Codex workflow documentation, user manual, landing page, and discussion seed posts.
