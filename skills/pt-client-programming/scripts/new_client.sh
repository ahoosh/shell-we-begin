#!/usr/bin/env bash
# Create a client folder from templates.
# Usage: new_client.sh <CODE> "<First name>"
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
need_workspace

CODE="${1:-}"; FIRST="${2:-}"
if [[ -z "$CODE" || -z "$FIRST" ]]; then
  echo "Usage: new_client.sh <CODE> \"<First name>\"   e.g. new_client.sh C-0427 Sam" >&2; exit 1
fi
if [[ ! "$CODE" =~ ^[A-Za-z0-9][A-Za-z0-9_-]{1,31}$ ]]; then
  echo "Client code must be letters/digits/dashes, e.g. C-0427. Never a name." >&2; exit 1
fi
D="$PT_HOME/clients/$CODE"
if [[ -e "$D" ]]; then echo "Client $CODE already exists at $D" >&2; exit 1; fi

mkdir -p "$D"/{visits,drafts,drafts/archive,approved,adjuncts,images,exports}
for t in CURRENT_STATE.md intake.md profile.md CHANGELOG.md; do
  sed -e "s/{{CODE}}/$CODE/g" -e "s/{{DATE}}/$TODAY/g" -e "s/{{FIRST_NAME}}/$FIRST/g" \
    "$SKILL_DIR/templates/$t" > "$D/$t"
done
echo "Created client $CODE at $D"
find "$D" -maxdepth 1 | sort | sed 's|^|  |'
echo
echo "Next: fill $D/intake.md, then BUILD."
