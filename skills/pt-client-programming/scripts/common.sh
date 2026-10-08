# shared helpers, sourced by the other scripts
PT_HOME="${PT_PROGRAMS_HOME:-$HOME/PT-Programs}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$PT_HOME/.venv/bin/python"
TODAY="$(date +%Y-%m-%d)"

need_workspace() {
  if [[ ! -d "$PT_HOME/clients" || ! -f "$PT_HOME/practice.conf" ]]; then
    echo "Workspace not set up at $PT_HOME. Run: $SKILL_DIR/scripts/setup.sh" >&2
    exit 2
  fi
}

client_dir() {
  local code="$1"
  local d="$PT_HOME/clients/$code"
  if [[ ! -d "$d" ]]; then
    echo "No client folder for '$code' at $d" >&2
    exit 3
  fi
  echo "$d"
}
