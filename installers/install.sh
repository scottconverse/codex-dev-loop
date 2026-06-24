#!/usr/bin/env bash
set -euo pipefail

DESTINATION=""
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --destination)
      DESTINATION="$2"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="$REPO_ROOT/skill"

if [[ ! -d "$SOURCE" ]]; then
  echo "Could not find skill source at $SOURCE" >&2
  exit 1
fi

if [[ -z "$DESTINATION" ]]; then
  CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
  DESTINATION="$CODEX_HOME/skills/codex-dev-loop"
fi

if [[ -e "$DESTINATION" && "$FORCE" != "true" ]]; then
  echo "Destination already exists: $DESTINATION" >&2
  echo "Use --force to replace it." >&2
  exit 1
fi

rm -rf "$DESTINATION"
mkdir -p "$(dirname "$DESTINATION")"
cp -R "$SOURCE" "$DESTINATION"

echo "Installed codex-dev-loop skill to:"
echo "$DESTINATION"
echo
echo 'In Codex desktop, start a new thread or reload context, then say:'
echo 'Use $codex-dev-loop for this repo.'
