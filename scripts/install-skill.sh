#!/usr/bin/env bash
# Install (or update) a skill from this repo into ~/.claude/skills/
# Usage: ./scripts/install-skill.sh <skill-name>
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <skill-name>"
  echo
  echo "Available skills:"
  for d in "$SKILLS_SRC"/*/; do
    [[ -f "$d/SKILL.md" ]] && echo "  - $(basename "$d")"
  done
  exit 1
fi

NAME="$1"
SRC="$SKILLS_SRC/$NAME"
DST="$SKILLS_DST/$NAME"

if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "No skill named '$NAME' in $SKILLS_SRC" >&2
  exit 1
fi

mkdir -p "$SKILLS_DST"
if [[ -d "$DST" ]]; then
  echo "Updating existing skill at $DST"
  rm -rf "$DST"
fi
cp -R "$SRC" "$DST"
find "$DST" -name "*.sh" -exec chmod +x {} \;
find "$DST" -name "*.py" -exec chmod +x {} \;

echo "Installed '$NAME' -> $DST"
if [[ -f "$DST/scripts/setup.sh" ]]; then
  echo
  echo "This skill has a one-time setup. Run it now with:"
  echo "  $DST/scripts/setup.sh"
fi
echo
echo "Start a new session (desktop app: sidebar → New session; CLI: restart claude) and type / to see it."
