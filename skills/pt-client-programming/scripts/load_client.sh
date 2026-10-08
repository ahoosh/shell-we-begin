#!/usr/bin/env bash
# Print the retrieval report for one client. Never reads other clients.
# Usage: load_client.sh <CODE>
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
need_workspace
CODE="${1:-}"; [[ -z "$CODE" ]] && { echo "Usage: load_client.sh <CODE>" >&2; exit 1; }
D="$(client_dir "$CODE")"

first="$(grep -i '^first_name:' "$D/profile.md" 2>/dev/null | sed 's/first_name: *//' || true)"
ver="$(grep '^approved_version:' "$D/CURRENT_STATE.md" | sed 's/approved_version: *//')"
file="$(grep '^approved_file:' "$D/CURRENT_STATE.md" | sed 's/approved_file: *//')"
adate="$(grep '^approved_date:' "$D/CURRENT_STATE.md" | sed 's/approved_date: *//')"
status="$(grep '^status:' "$D/CURRENT_STATE.md" | sed 's/status: *//')"
nextv="$(grep '^next_visit:' "$D/CURRENT_STATE.md" | sed 's/next_visit: *//')"

echo "RETRIEVAL REPORT — $CODE (${first:-no first name})"
if [[ "$ver" == "none" || -z "$ver" ]]; then
  echo "approved:   NONE — no approved program yet. Anything produced is a first draft."
else
  if [[ -f "$D/$file" ]]; then
    echo "approved:   $file   ($adate)  ← authoritative, $(wc -l < "$D/$file" | tr -d ' ') lines"
    docx="${file%.md}.docx"
    [[ -f "$D/$docx" ]] && echo "            docx: present" || echo "            docx: MISSING (run EXPORT)"
    m=$(grep -c '\[\[\(CONFIRM\|MISSING\)' "$D/$file" || true)
    echo "markers:    $m in approved $([[ $m -gt 0 ]] && echo '← PROBLEM: approved files must have none')"
  else
    echo "approved:   $file — FILE NOT FOUND. CURRENT_STATE is inconsistent. Contents of approved/:"
    ls -1 "$D/approved" 2>/dev/null | sed 's|^|              |' || echo "              (empty)"
  fi
fi
nd=$(ls -1 "$D/drafts"/*.md 2>/dev/null | wc -l | tr -d ' ')
if [[ "$nd" == "0" ]]; then echo "drafts:     none"; else
  echo "drafts:     $nd"; ls -1t "$D/drafts"/*.md | sed 's|.*/|              |'; fi
nv=$(ls -1 "$D/visits"/*.md 2>/dev/null | wc -l | tr -d ' ')
if [[ "$nv" == "0" ]]; then echo "visits:     none"; else
  echo "visits:     latest $(ls -1t "$D/visits"/*.md | head -1 | xargs basename) ($nv notes)"; fi
na=$(ls -1 "$D/adjuncts"/*.md 2>/dev/null | wc -l | tr -d ' ')
if [[ "$na" == "0" ]]; then echo "adjuncts:   none"; else
  echo "adjuncts:   $(ls -1 "$D/adjuncts"/*.md | xargs -n1 basename | tr '\n' ' ')"; fi
ni=$(ls -1 "$D/images" 2>/dev/null | wc -l | tr -d ' ')
echo "images:     $ni files"
echo "status:     ${status:-?}${nextv:+ — next visit $nextv}"
echo "approved versions on disk: $(ls -1 "$D/approved"/v*.md 2>/dev/null | xargs -n1 basename 2>/dev/null | tr '\n' ' ')"
echo
echo "--- CURRENT_STATE.md ---"
cat "$D/CURRENT_STATE.md"
