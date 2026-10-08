#!/usr/bin/env bash
# Scan the repo for things that must never be published: phone numbers,
# emails, personal names you list in .pii-denylist, Google Doc links, etc.
# Usage: ./scripts/pii-scan.sh   (exit 1 if anything is found)
# Denylist: a file of words/names, one per line, at .pii-denylist (gitignored) or $PII_DENYLIST
set -uo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"
found=0
echo "== phone numbers"
grep -rnE '\b\(?[0-9]{3}\)?[-. ][0-9]{3}[-. ][0-9]{4}\b' --include='*.md' --include='*.py' --include='*.sh' --include='*.conf' --include='*.txt' . | grep -v 'pii-scan.sh' && found=1
echo "== email addresses"
grep -rnE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' --include='*.md' --include='*.py' --include='*.sh' --include='*.conf' --include='*.txt' . | grep -vE 'example\.com|pii-scan.sh|noreply@anthropic|<noreply' && found=1
echo "== google docs / drive links"
grep -rnE 'docs\.google\.com|drive\.google\.com' . --include='*.md' --include='*.py' --include='*.sh' | grep -v 'pii-scan.sh' && found=1
echo "== denylist words (.pii-denylist, one per line, case-insensitive)"
DENY="${PII_DENYLIST:-.pii-denylist}"
if [[ -f "$DENY" ]]; then
  while IFS= read -r w; do
    [[ -z "$w" || "$w" == \#* ]] && continue
    grep -rniw --include='*.md' --include='*.py' --include='*.sh' --include='*.conf' --include='*.txt' -- "$w" . | grep -v 'pii-denylist' && found=1
  done < "$DENY"
fi
if [[ $found -eq 0 ]]; then echo "clean"; else echo; echo "FOUND possible personal data above. Fix before publishing."; fi
exit $found
