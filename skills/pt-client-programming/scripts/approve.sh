#!/usr/bin/env bash
# Promote a draft to the next approved version.
# Usage: approve.sh <CODE> <path/to/draft.md> "<one-line change summary>"
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
need_workspace
CODE="${1:-}"; DRAFT="${2:-}"; MSG="${3:-}"
[[ -z "$CODE" || -z "$DRAFT" || -z "$MSG" ]] && { echo "Usage: approve.sh <CODE> <draft.md> \"<summary>\"" >&2; exit 1; }
D="$(client_dir "$CODE")"
[[ -f "$DRAFT" ]] || DRAFT="$D/drafts/$(basename "$DRAFT")"
[[ -f "$DRAFT" ]] || { echo "Draft not found: $DRAFT" >&2; exit 1; }

if grep -q '\[\[\(CONFIRM\|MISSING\)' "$DRAFT"; then
  echo "REFUSED: unresolved markers in draft:"; grep -n '\[\[\(CONFIRM\|MISSING\)' "$DRAFT"; exit 5
fi

last=$(ls -1 "$D/approved"/v[0-9][0-9][0-9]_*.md 2>/dev/null | sed -E 's/.*\/v([0-9]{3})_.*/\1/' | sort -n | tail -1 || true)
next=$(printf "%03d" $(( ${last:-0} + 1 )))
NEW="$D/approved/v${next}_${TODAY}.md"
cp "$DRAFT" "$NEW"

# title → slug for the client copy
title=$(grep -m1 '^title:' "$NEW" | sed -E 's/^title: *"?//; s/"? *$//' || true)
slug=$(echo "${title:-program}" | tr -cs '[:alnum:]' '-' | sed 's/^-//; s/-$//' | cut -c1-40)
CLIENT_COPY="$D/approved/${CODE}_${slug}_v${next}.docx"

if ! "$PY" "$SKILL_DIR/scripts/build_handout.py" "$NEW" --out "${NEW%.md}.docx" --all --strict; then
  rm -f "$NEW" "${NEW%.md}.docx"
  echo; echo "REFUSED: handout build failed (see report above). Nothing was approved; draft left in place."; exit 6
fi
cp "${NEW%.md}.docx" "$CLIENT_COPY"
[[ -f "${NEW%.md}.pdf" ]] && cp "${NEW%.md}.pdf" "${CLIENT_COPY%.docx}.pdf"
[[ -f "${NEW%.md}.html" ]] && cp "${NEW%.md}.html" "${CLIENT_COPY%.docx}.html"

# what changed since the previous approved version (for the clinician and for an "Updates this visit" note)
prev=$(ls -1 "$D/approved"/v[0-9][0-9][0-9]_*.md 2>/dev/null | grep -v "$(basename "$NEW")" | sort | tail -1 || true)
if [[ -n "$prev" ]]; then
  "$PY" "$SKILL_DIR/scripts/patch_check.py" "$prev" "$NEW" > "${NEW%.md}_changes.txt" || true
else
  echo "First approved version — no previous version to compare." > "${NEW%.md}_changes.txt"
fi

# update state
sed -i '' -e "s|^approved_version:.*|approved_version: v${next}|" \
          -e "s|^approved_file:.*|approved_file: approved/$(basename "$NEW")|" \
          -e "s|^approved_date:.*|approved_date: ${TODAY}|" \
          -e "s|^status:.*|status: active|" "$D/CURRENT_STATE.md"
echo "| v${next} | ${TODAY} | ${MSG} |" >> "$D/CHANGELOG.md"
mkdir -p "$D/drafts/archive"; mv "$DRAFT" "$D/drafts/archive/"
[[ -f "${DRAFT%.md}_REVIEW.docx" ]] && mv "${DRAFT%.md}_REVIEW.docx" "$D/drafts/archive/" || true

cat <<MSG

APPROVED — $CODE
new version:  approved/$(basename "$NEW")
handout:      approved/$(basename "${NEW%.md}.docx")$([[ -f "${NEW%.md}.pdf" ]] && echo " + .pdf")$([[ -f "${NEW%.md}.html" ]] && echo " + .html")
client copy:  approved/$(basename "$CLIENT_COPY")$([[ -f "${CLIENT_COPY%.docx}.pdf" ]] && echo " (+ .pdf, .html)")
changes:      approved/$(basename "${NEW%.md}_changes.txt")  (diff vs previous version)
CURRENT_STATE.md updated (approved_version: v${next}, approved_date: ${TODAY})
CHANGELOG.md appended: ${MSG}
draft archived: drafts/archive/$(basename "$DRAFT")
MSG
