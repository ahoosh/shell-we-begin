#!/usr/bin/env bash
# One-time setup: tools, workspace, seed library, practice.conf.
# Safe to re-run. Honors PT_PROGRAMS_HOME (default ~/PT-Programs).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

echo "== pt-client-programming setup"
echo "workspace: $PT_HOME"

# 1. pandoc
if ! command -v pandoc >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "-- installing pandoc with Homebrew"
    brew install pandoc
  else
    echo "pandoc is missing and Homebrew is not installed. Install Homebrew first (see the main guide, step 1)." >&2
    exit 1
  fi
fi
echo "-- pandoc: $(pandoc --version | head -1)"

# 2. python venv with python-docx
mkdir -p "$PT_HOME"
if [[ ! -x "$PY" ]]; then
  echo "-- creating Python environment"
  python3 -m venv "$PT_HOME/.venv"
fi
"$PY" -m pip install --quiet --upgrade pip >/dev/null
"$PY" -m pip install --quiet "python-docx>=1.1" >/dev/null
echo "-- python-docx: $("$PY" -c 'import docx, importlib.metadata as m; print(m.version("python-docx"))')"

# 3. folders
mkdir -p "$PT_HOME/clients" "$PT_HOME/library" "$PT_HOME/library/images"

# 3b. PDF converter (optional, ~500 MB). LibreOffice turns the .docx into a PDF
#     with identical header, footer and page numbers. Run: setup.sh --with-pdf
if [[ "${1:-}" == "--with-pdf" ]]; then
  if [[ ! -x /Applications/LibreOffice.app/Contents/MacOS/soffice ]] && ! command -v soffice >/dev/null 2>&1; then
    echo "-- installing LibreOffice for PDF export (large download)"
    brew install --cask libreoffice
  fi
  echo "-- PDF export: LibreOffice available"
else
  if [[ -x /Applications/LibreOffice.app/Contents/MacOS/soffice ]] || command -v soffice >/dev/null 2>&1; then
    echo "-- PDF export: LibreOffice available"
  else
    echo "-- PDF export: LibreOffice not installed. PDFs will use Google Chrome if present (no page numbers)."
    echo "   For full-quality PDFs run:  $SKILL_DIR/scripts/setup.sh --with-pdf"
  fi
fi

# 4. seed library (never overwrite an existing copy)
for pair in "exercise-library.md:exercises.md" "language-blocks.md:language.md"; do
  src="${pair%%:*}"; dst="${pair##*:}"
  if [[ ! -f "$PT_HOME/library/$dst" ]]; then
    cp "$SKILL_DIR/references/$src" "$PT_HOME/library/$dst"
    echo "-- seeded library/$dst"
  fi
done

# 5. practice.conf
if [[ ! -f "$PT_HOME/practice.conf" ]]; then
  cp "$SKILL_DIR/templates/practice.conf.example" "$PT_HOME/practice.conf"
  echo "-- created practice.conf (EDIT THIS: your name, practice, links)"
fi

cat <<MSG

Setup complete.

Next:
  1. Edit $PT_HOME/practice.conf with your name, credentials, practice and links.
     (open it with:  open -e "$PT_HOME/practice.conf")
  2. In Claude Code, say:  new client C-0001, first name Sam, ...

Workspace layout:
  $PT_HOME/practice.conf
  $PT_HOME/library/exercises.md
  $PT_HOME/library/language.md
  $PT_HOME/library/images/        shared exercise photos, reused across clients by file name
  $PT_HOME/clients/<CODE>/...
MSG
