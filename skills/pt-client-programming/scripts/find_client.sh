#!/usr/bin/env bash
# Look up client codes by first name. Searches profile.md only.
# Usage: find_client.sh "<name>"
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
need_workspace
Q="${1:-}"; [[ -z "$Q" ]] && { echo "Usage: find_client.sh <name>" >&2; exit 1; }
hits=0
for p in "$PT_HOME"/clients/*/profile.md; do
  [[ -f "$p" ]] || continue
  if grep -qi "^first_name:.*$Q" "$p"; then
    code="$(basename "$(dirname "$p")")"
    echo "$code  ($(grep -i '^first_name:' "$p" | sed 's/first_name: *//'))"
    hits=$((hits+1))
  fi
done
[[ $hits -eq 0 ]] && { echo "No client with first name matching '$Q'."; exit 4; }
exit 0
