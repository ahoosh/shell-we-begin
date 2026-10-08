#!/usr/bin/env python
"""Build a client handout (.docx) from a markdown program file.

Usage:
  build_handout.py program.md --out program.docx [--practice practice.conf]
                   [--table-only] [--strict]

Steps: substitute {{tokens}} from practice.conf -> pandoc markdown->docx ->
add header (schedule link + page numbers), footer (contact line), table
borders, base font -> reopen the file and print a verification report.

Exit codes: 0 ok (warnings allowed), 1 missing images or (with --strict)
leftover [[CONFIRM]]/[[MISSING]] markers, 2 usage/tool error.
"""
import argparse, os, re, subprocess, sys, tempfile, shutil

try:
    import docx
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
except ImportError:
    sys.exit("python-docx missing. Run scripts/setup.sh (or use the workspace .venv python).")

MARKER_RE = re.compile(r"\[\[(CONFIRM|MISSING)[^\]]*\]\]")


def read_conf(path):
    conf = {}
    if path and os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
                continue
            k, v = line.split(":", 1)
            conf[k.strip()] = v.strip()
    return conf


def fill(text, conf):
    def rep(m):
        return conf.get(m.group(1), "")
    return re.sub(r"\{(\w+)\}", rep, text)


def add_hyperlink(paragraph, url, text, size=None):
    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    st = OxmlElement("w:rStyle"); st.set(qn("w:val"), "Hyperlink"); rpr.append(st)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rpr.append(u)
    c = OxmlElement("w:color"); c.set(qn("w:val"), "1155CC"); rpr.append(c)
    if size:
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t"); t.text = text; t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); paragraph._p.append(h)


def add_field(paragraph, instr):
    r = paragraph.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    r._r.append(f1); r._r.append(it); r._r.append(f2)


def write_line(paragraph, text, conf, size):
    """Write text into a paragraph; schedule_text and bare URLs become links."""
    sched_t, sched_u = conf.get("schedule_text", ""), conf.get("schedule_url", "")
    tokens = re.split(r"(https?://\S+)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("http"):
            add_hyperlink(paragraph, tok, tok.replace("https://", "").replace("http://", "").rstrip("/"), size)
        elif sched_t and sched_u and sched_t in tok:
            pre, post = tok.split(sched_t, 1)
            if pre:
                paragraph.add_run(pre).font.size = Pt(size)
            add_hyperlink(paragraph, sched_u, sched_t, size)
            if post:
                paragraph.add_run(post).font.size = Pt(size)
        else:
            paragraph.add_run(tok).font.size = Pt(size)


def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0"); el.set(qn("w:color"), "999999")
        borders.append(el)
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    tblPr.append(borders)
    # light shading + bold on header row
    if table.rows:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "EFEFEF")
            tcPr.append(shd)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.bold = True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--practice", default=os.path.join(os.environ.get("PT_PROGRAMS_HOME", os.path.expanduser("~/PT-Programs")), "practice.conf"))
    ap.add_argument("--table-only", action="store_true", help="no header/footer; for pasting into an existing document")
    ap.add_argument("--strict", action="store_true", help="fail on leftover [[CONFIRM]]/[[MISSING]] markers")
    a = ap.parse_args()

    if not shutil.which("pandoc"):
        sys.exit("pandoc not found. Run scripts/setup.sh")
    if not os.path.exists(a.source):
        sys.exit(f"source not found: {a.source}")

    conf = read_conf(a.practice)
    src_dir = os.path.dirname(os.path.abspath(a.source))
    # images are referenced relative to the client folder (images/x.png); the
    # source may sit in drafts/, approved/ or exports/, so search both.
    resource_path = os.pathsep.join([src_dir, os.path.dirname(src_dir), os.getcwd()])
    text = open(a.source, encoding="utf-8").read()
    markers = MARKER_RE.findall(text)
    marker_lines = [l.strip() for l in text.splitlines() if MARKER_RE.search(l)]
    # {{clinician_first_name}} style tokens from practice.conf
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: conf.get(m.group(1), m.group(0)), text)

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8", dir=src_dir) as tmp:
        tmp.write(text); tmp_path = tmp.name
    try:
        proc = subprocess.run(
            ["pandoc", tmp_path, "-o", a.out, "--from", "markdown", "--to", "docx", "--resource-path", resource_path],
            capture_output=True, text=True)
    finally:
        os.unlink(tmp_path)
    if proc.returncode != 0:
        sys.exit(f"pandoc failed:\n{proc.stderr}")
    missing_images = [m.rstrip(":.,") for m in re.findall(r"Could not fetch resource (\S+)", proc.stderr)]

    d = docx.Document(a.out)
    # base font
    normal = d.styles["Normal"]
    normal.font.name = conf.get("font_name", "Calibri")
    try:
        normal.font.size = Pt(float(conf.get("font_size", "11")))
    except ValueError:
        pass
    for t in d.tables:
        set_table_borders(t)

    if not a.table_only:
        sec = d.sections[0]
        sec.different_first_page_header_footer = False
        h = sec.header; h.is_linked_to_previous = False
        hp = h.paragraphs[0] if h.paragraphs else h.add_paragraph()
        hp.text = ""
        write_line(hp, fill(conf.get("header_text", ""), conf), conf, 9)
        hp2 = h.add_paragraph(); hp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = hp2.add_run("Page "); r.font.size = Pt(9)
        add_field(hp2, "PAGE")
        r = hp2.add_run(" of "); r.font.size = Pt(9)
        add_field(hp2, "NUMPAGES")
        for run in hp2.runs:
            run.font.size = Pt(9)
        f = sec.footer; f.is_linked_to_previous = False
        first = True
        for line in re.split(r"\s+//\s+", fill(conf.get("footer_text", ""), conf)):
            line = " | ".join(x.strip() for x in line.split("|") if x.strip())
            if not line:
                continue
            fp = (f.paragraphs[0] if first and f.paragraphs else f.add_paragraph())
            fp.text = ""; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            write_line(fp, line, conf, 9)
            first = False
    d.save(a.out)

    # ---- verification: reopen and read back
    v = docx.Document(a.out)
    h1 = sum(1 for p in v.paragraphs if p.style.name == "Heading 1")
    h2 = sum(1 for p in v.paragraphs if p.style.name == "Heading 2")
    title = next((p.text for p in v.paragraphs if p.style.name == "Title"), "")
    rows = sum(len(t.rows) for t in v.tables)
    body_text = "\n".join(p.text for p in v.paragraphs) + "\n".join(c.text for t in v.tables for r in t.rows for c in r.cells)
    leftover = MARKER_RE.findall(body_text)
    size_kb = os.path.getsize(a.out) // 1024
    print("BUILD REPORT")
    print(f"source:   {a.source}")
    print(f"output:   {a.out}  ({size_kb} KB)")
    print(f"title:    {title or '(none)'}")
    print(f"headings: {h1} (H1) · {h2} (H2)")
    print(f"tables:   {len(v.tables)}   rows: {rows}")
    print(f"images:   {len(v.inline_shapes)} embedded, {len(missing_images)} missing" + (": " + ", ".join(missing_images) if missing_images else ""))
    print("header:   " + ("none (table-only)" if a.table_only else f"\"{fill(conf.get('header_text',''), conf)}\" + page numbers"))
    print("footer:   " + ("none (table-only)" if a.table_only else "practice contact line"))
    print(f"markers:  {len(leftover)}" + ("" if not leftover else " ← unresolved:"))
    for l in marker_lines[:20]:
        print("          " + l[:120])
    print("Google Docs: upload the .docx to Drive, right-click → Open with → Google Docs.")
    if missing_images:
        sys.exit(1)
    if a.strict and leftover:
        sys.exit(1)


if __name__ == "__main__":
    main()
