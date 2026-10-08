#!/usr/bin/env bash
# One-time setup. Safe to re-run. No Homebrew required (used if present).
#   setup.sh              tools + workspace + seed library + practice.conf
#   setup.sh --with-pdf   also installs LibreOffice (~400 MB) for PDFs that match the Word file
# Honors PT_PROGRAMS_HOME (default ~/PT-Programs).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
TOOLS="$PT_HOME/.tools"; mkdir -p "$TOOLS/bin" "$PT_HOME"
ARCH="$(uname -m)"   # arm64 (Apple silicon) or x86_64 (Intel)

echo "== pt-client-programming setup"
echo "workspace: $PT_HOME"

# 1. Python 3 (ships with Apple's Command Line Tools). Try the CLT copy directly first,
#    because the /usr/bin/python3 shim can misbehave when an old Xcode is around.
PYBIN=""
for cand in /Library/Developer/CommandLineTools/usr/bin/python3 "$(command -v python3 || true)" /usr/bin/python3; do
  [[ -n "$cand" && -x "$cand" ]] || continue
  if "$cand" -c 'import venv, sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then PYBIN="$cand"; break; fi
done
if [[ -z "$PYBIN" ]]; then
  cat <<MSG
Python is not available yet. macOS installs it with Apple's Command Line Tools.
A dialog may have appeared asking to install them: click "Install", wait for it to finish
(a few minutes), then run this setup again. If no dialog appeared, run:  xcode-select --install
MSG
  exit 1
fi
echo "-- python: $("$PYBIN" --version 2>&1) ($PYBIN)"

# 2. pandoc: use an existing one, else download the official release binary (no admin password)
if ! command -v pandoc >/dev/null 2>&1 && [[ ! -x "$TOOLS/bin/pandoc" ]]; then
  if command -v brew >/dev/null 2>&1; then
    echo "-- installing pandoc with Homebrew"; brew install pandoc
  else
    echo "-- downloading pandoc"
    tag="$(curl -sI https://github.com/jgm/pandoc/releases/latest | grep -i '^location:' | sed -E 's#.*/tag/##' | tr -d '\r\n')"
    [[ -z "$tag" ]] && tag="3.12.1"
    url="https://github.com/jgm/pandoc/releases/download/${tag}/pandoc-${tag}-${ARCH}-macOS.zip"
    tmp="$(mktemp -d)"; curl -sL -o "$tmp/pandoc.zip" "$url"
    (cd "$tmp" && unzip -q pandoc.zip)
    cp "$(find "$tmp" -type f -name pandoc -path '*/bin/*' | head -1)" "$TOOLS/bin/pandoc"; chmod +x "$TOOLS/bin/pandoc"
    rm -rf "$tmp"
  fi
fi
PANDOC="$(command -v pandoc || echo "$TOOLS/bin/pandoc")"
echo "-- pandoc: $("$PANDOC" --version | head -1)"

# 3. Python environment with python-docx
if [[ ! -x "$PY" ]]; then
  echo "-- creating Python environment"
  "$PYBIN" -m venv "$PT_HOME/.venv"
fi
"$PY" -m pip install --quiet --upgrade pip >/dev/null
"$PY" -m pip install --quiet "python-docx>=1.1" >/dev/null
echo "-- python-docx: $("$PY" -c 'import importlib.metadata as m; print(m.version("python-docx"))')"

# 4. folders
mkdir -p "$PT_HOME/clients" "$PT_HOME/library/images"

# 5. seed library (never overwrite an existing copy)
for pair in "exercise-library.md:exercises.md" "language-blocks.md:language.md"; do
  src="${pair%%:*}"; dst="${pair##*:}"
  if [[ ! -f "$PT_HOME/library/$dst" ]]; then
    cp "$SKILL_DIR/references/$src" "$PT_HOME/library/$dst"; echo "-- seeded library/$dst"
  fi
done

# 6. practice.conf
if [[ ! -f "$PT_HOME/practice.conf" ]]; then
  cp "$SKILL_DIR/templates/practice.conf.example" "$PT_HOME/practice.conf"
  echo "-- created practice.conf (EDIT THIS: your name, practice, links)"
fi

# 7. PDF converter (optional). LibreOffice turns the .docx into a PDF with identical header/footer/page numbers.
have_soffice() { [[ -x /Applications/LibreOffice.app/Contents/MacOS/soffice || -x "$HOME/Applications/LibreOffice.app/Contents/MacOS/soffice" ]] || command -v soffice >/dev/null 2>&1; }
if [[ "${1:-}" == "--with-pdf" ]] && ! have_soffice; then
  if command -v brew >/dev/null 2>&1; then
    echo "-- installing LibreOffice with Homebrew (large download)"; brew install --cask libreoffice
  else
    echo "-- downloading LibreOffice (large download, a few minutes)"
    ver="$(curl -s https://download.documentfoundation.org/libreoffice/stable/ | grep -oE 'href="[0-9]+\.[0-9]+\.[0-9]+/"' | grep -oE '[0-9.]+' | sort -V | tail -1)"
    [[ "$ARCH" == "arm64" ]] && la="aarch64" && lf="aarch64" || { la="x86_64"; lf="x86-64"; }
    url="https://download.documentfoundation.org/libreoffice/stable/${ver}/mac/${la}/LibreOffice_${ver}_MacOS_${lf}.dmg"
    tmp="$(mktemp -d)"; curl -L -o "$tmp/lo.dmg" "$url"
    mnt="$(hdiutil attach -nobrowse -readonly "$tmp/lo.dmg" | grep -oE '/Volumes/.*$' | tail -1)"
    mkdir -p "$HOME/Applications"; rm -rf "$HOME/Applications/LibreOffice.app"
    cp -R "$mnt/LibreOffice.app" "$HOME/Applications/LibreOffice.app"
    hdiutil detach "$mnt" -quiet; rm -rf "$tmp"
    xattr -dr com.apple.quarantine "$HOME/Applications/LibreOffice.app" 2>/dev/null || true
    echo "-- LibreOffice installed to ~/Applications"
  fi
fi
if have_soffice; then echo "-- PDF export: LibreOffice available"
else
  echo "-- PDF export: LibreOffice not installed. PDFs will use Google Chrome if present (no page numbers)."
  echo "   For full-quality PDFs run:  $SKILL_DIR/scripts/setup.sh --with-pdf"
fi

cat <<MSG

Setup complete.

Next:
  1. Fill in $PT_HOME/practice.conf (your name, credentials, practice, links).
     Open it with:  open -e "$PT_HOME/practice.conf"
  2. Then say:  new client C-0001, first name Sam, ...

Workspace layout:
  $PT_HOME/practice.conf
  $PT_HOME/library/exercises.md
  $PT_HOME/library/language.md
  $PT_HOME/library/images/        shared exercise photos, reused across clients by file name
  $PT_HOME/clients/<CODE>/...
MSG
