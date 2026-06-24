import argparse
from pathlib import Path

from loop_utils import loop_files, loop_status, parse_run, read_loop, required_loop_fields, run_files


def int_budget(value: object, key: str, default: int) -> int:
    if not isinstance(value, dict):
        return default
    try:
        return int(str(value.get(key, default)).strip())
    except ValueError:
        return default


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Codex dev loop contracts and recent run logs.")
    parser.add_argument("--target", default=".", help="Project directory containing .codex-loop.")
    args = parser.parse_args()

    vault = Path(args.target).resolve() / ".codex-loop"
    if not vault.exists():
        raise SystemExit(f"missing vault: {vault}")

    loops = loop_files(vault)
    issues: list[str] = []
    active: list[str] = []
    stalled: list[str] = []

    for path in loops:
        data = read_loop(path)
        missing = [field for field in required_loop_fields() if not data.get(field)]
        if missing:
            issues.append(f"{path.name}: missing {', '.join(missing)}")
        status = loop_status(data)
        if status == "active":
            active.append(path.name)
        if status == "stalled":
            stalled.append(path.name)

        budget = data.get("budget", {})
        max_failures = int_budget(budget, "max_consecutive_failures", 2)
        recent = [parse_run(p) for p in run_files(vault, str(data.get("name", path.stem)))[:max_failures]]
        if len(recent) >= max_failures and all(r.get("verifier_result") == "failed" for r in recent):
            signatures = [r.get("failure_signature", "") for r in recent]
            if signatures and len(set(signatures)) == 1 and signatures[0] not in ("", "n/a"):
                stalled.append(path.name)
                issues.append(f"{path.name}: stalled on repeated failure signature '{signatures[0]}'")

    print(f"vault: {vault}")
    print(f"loops: {len(loops)}")
    print(f"active_loops: {len(active)}")
    for item in active:
        print(f"- active: {item}")
    print(f"stalled_loops: {len(set(stalled))}")
    for item in sorted(set(stalled)):
        print(f"- stalled: {item}")

    if issues:
        print("issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("run_loop_check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

