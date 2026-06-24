import argparse
import shutil
from pathlib import Path


def copy_tree(src: Path, dst: Path, force: bool) -> list[str]:
    written: list[str] = []
    for source in src.rglob("*"):
        relative = source.relative_to(src)
        target = dst / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        written.append(str(target))
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Codex development loop vault.")
    parser.add_argument("--target", default=".", help="Project directory where .codex-loop should be created.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing starter files.")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    starter = skill_dir / "assets" / "starter-vault"
    target_dir = Path(args.target).resolve()
    vault = target_dir / ".codex-loop"

    if not starter.exists():
        raise SystemExit(f"starter vault not found: {starter}")

    written = copy_tree(starter, vault, args.force)
    print(f"vault: {vault}")
    print(f"files_written: {len(written)}")
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
