#!/usr/bin/env python
"""Prove that a draft changed only what was asked.

Usage: patch_check.py <baseline.md> <draft.md> [--no-diff] [--strict]

Prints: line counts (added/removed/changed), which headed sections were
touched, leftover [[CONFIRM]]/[[MISSING]] markers, whether every exercise named
in a phase/ladder/routine table has a row in the Exercise menu, then the
unified diff. --strict exits 1 when markers remain.
"""
import difflib, re, sys, argparse

MARKER_RE = re.compile(r"\[\[(CONFIRM|MISSING)[^\]]*\]\]")
HEAD_RE = re.compile(r"^(#{1,2})\s+(.*)")


def sections_for(lines):
    cur = "(front matter)"; out = []
    for l in lines:
        m = HEAD_RE.match(l)
        if m:
            cur = m.group(2).strip()
        out.append(cur)
    return out


def norm(name):
    name = re.sub(r"\*\*|__", "", name)
    name = re.sub(r"^\s*\d+\s+", "", name)          # "3 Feet-supported active hang"
    name = re.sub(r"^(optional fourth|companion)\s*:?\s*", "", name, flags=re.I)
    name = re.sub(r"\s*\(.*?\)", "", name)
    name = re.sub(r"\s+(or|/)\s+.*$", "", name, flags=re.I)  # "Forward OR side step-up" → forward
    return re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()


def table_first_cells(lines):
    """Yield (section, first-cell) for body rows of every pipe table."""
    sec = sections_for(lines)
    in_table = False; header_seen = False
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not in_table:
                in_table = True; header_seen = False; continue        # header row
            if not header_seen and re.match(r"^\|?\s*:?-{2,}", s):
                header_seen = True; continue                           # separator
            if cells and cells[0]:
                yield sec[i], cells[0]
        else:
            in_table = False


def menu_check(lines):
    phase_ex, menu_ex = [], set()
    for sec, cell in table_first_cells(lines):
        sl = sec.lower()
        if "exercise menu" in sl:
            menu_ex.add(norm(cell))
        elif any(k in sl for k in ("phase", "ladder", "routine", "reset", "strength", "control")):
            n = norm(cell)
            if n and not re.match(r"^(plan and baseline|weekly dose|walking|e-bike|longer days|use the ladder|strength a|strength b|level|step|stage)", n):
                phase_ex.append((sec, cell, n))
    if not menu_ex:
        return "menu check: no Exercise menu table found (fine for TABLE ONLY exports)"
    missing = []
    for sec, cell, n in phase_ex:
        if n in menu_ex or any(n in m or m in n for m in menu_ex if len(n) > 4):
            continue
        missing.append(f"{cell}  (in {sec})")
    if not missing:
        return "menu check: all phase/ladder exercises present in Exercise menu"
    return "menu check: NOT in Exercise menu →\n    " + "\n    ".join(dict.fromkeys(missing))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline"); ap.add_argument("draft")
    ap.add_argument("--no-diff", action="store_true"); ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    b = open(a.baseline, encoding="utf-8").read().splitlines()
    d = open(a.draft, encoding="utf-8").read().splitlines()
    sb, sd = sections_for(b), sections_for(d)
    added = removed = changed = 0; touched = []
    sm = difflib.SequenceMatcher(a=b, b=d, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if op == "insert":
            added += j2 - j1
        elif op == "delete":
            removed += i2 - i1
        else:
            changed += max(i2 - i1, j2 - j1)
        for s in sd[j1:j2] or sb[i1:i2]:
            if s not in touched:
                touched.append(s)
    markers = [l.strip() for l in d if MARKER_RE.search(l)]
    print("PATCH CHECK")
    print(f"baseline: {a.baseline}\ndraft:    {a.draft}")
    print(f"lines: +{added}  -{removed}  ~{changed}   (added / removed / changed)")
    print("sections touched: " + (" · ".join(touched) if touched else "none (files identical)"))
    print(f"markers in draft: {len(markers)}")
    for m in markers:
        print("    " + m[:120])
    print(menu_check(d))
    if not a.no_diff and (added or removed or changed):
        print("\n--- unified diff ---")
        sys.stdout.writelines(l + ("\n" if not l.endswith("\n") else "") for l in
                              difflib.unified_diff(b, d, a.baseline, a.draft, lineterm="", n=1))
    if a.strict and markers:
        sys.exit(1)


if __name__ == "__main__":
    main()
