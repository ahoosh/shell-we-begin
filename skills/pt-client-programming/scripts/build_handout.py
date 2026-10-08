#!/usr/bin/env python
"""Build client handouts from a markdown program file.

Usage:
  build_handout.py program.md --out program.docx [--pdf] [--html] [--all]
                   [--practice practice.conf] [--table-only] [--strict]

Outputs (same base name as --out):
  .docx  editable handout: header (schedule link + page numbers), footer
         (practice contact line), bordered tables, embedded images.
         Upload to Google Drive -> Open with Google Docs for an editable Doc.
  .pdf   client-facing copy, converted from the .docx by LibreOffice when it is
         installed (brew install --cask libreoffice); otherwise from the HTML
         version with headless Google Chrome; otherwise skipped with a note.
  .html  single-file, phone-friendly version (traffic-light rows coloured,
         images embedded). Clients can open it from a text message or email.

Images are referenced as images/<file> and resolved against the client folder
and the shared library/images folder.

Exit codes: 0 ok (warnings allowed), 1 missing images or (with --strict)
leftover [[CONFIRM]]/[[MISSING]] markers, 2 usage/tool error.
"""
import argparse, html, os, re, shutil, subprocess, sys, tempfile

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
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PT_HOME = os.environ.get("PT_PROGRAMS_HOME", os.path.expanduser("~/PT-Programs"))
SOFFICE_CANDIDATES = ["soffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"]
CHROME_CANDIDATES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium"]


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
    return re.sub(r"\{(\w+)\}", lambda m: conf.get(m.group(1), ""), text)


def find_exe(cands):
    for c in cands:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        p = shutil.which(c)
        if p:
            return p
    return None


# ---------- docx helpers
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
    r = paragraph.add_run(); r.font.size = Pt(9)
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    r._r.append(f1); r._r.append(it); r._r.append(f2)


def write_line(paragraph, text, conf, size):
    """Write text into a paragraph; schedule_text and bare URLs become links."""
    sched_t, sched_u = conf.get("schedule_text", ""), conf.get("schedule_url", "")
    for tok in re.split(r"(https?://\S+)", text):
        if not tok:
            continue
        if tok.startswith("http"):
            add_hyperlink(paragraph, tok, re.sub(r"^https?://", "", tok).rstrip("/"), size)
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
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0"); el.set(qn("w:color"), "999999")
        borders.append(el)
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    tblPr.append(borders)
    if table.rows:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "EFEFEF")
            tcPr.append(shd)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.bold = True
    # traffic-light cells
    for row in table.rows[1:]:
        first = row.cells[0].text.strip().upper()
        fill_hex = {"GREEN": "E3F6E8", "YELLOW": "FFF6D6", "RED": "FDE2E1"}.get(first.split(" ")[0].strip("*—-:"), None)
        if fill_hex and len(first) < 40:
            tcPr = row.cells[0]._tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), fill_hex)
            tcPr.append(shd)


# ---------- html helpers
def footer_lines(conf):
    out = []
    for line in re.split(r"\s+//\s+", fill(conf.get("footer_text", ""), conf)):
        line = " | ".join(x.strip() for x in line.split("|") if x.strip())
        if line:
            out.append(line)
    return out


def linkify_html(text, conf):
    sched_t, sched_u = conf.get("schedule_text", ""), conf.get("schedule_url", "")
    parts = []
    for tok in re.split(r"(https?://\S+)", text):
        if not tok:
            continue
        if tok.startswith("http"):
            parts.append(f'<a href="{html.escape(tok)}">{html.escape(re.sub(r"^https?://", "", tok).rstrip("/"))}</a>')
        elif sched_t and sched_u and sched_t in tok:
            pre, post = tok.split(sched_t, 1)
            parts.append(html.escape(pre) + f'<a href="{html.escape(sched_u)}">{html.escape(sched_t)}</a>' + html.escape(post))
        else:
            parts.append(html.escape(tok))
    return "".join(parts)


def colour_zone_rows(h):
    def rep(m):
        row = m.group(0)
        cell = re.search(r"<td[^>]*>(.*?)</td>", row, re.S)
        if not cell:
            return row
        txt = re.sub(r"<[^>]+>", "", cell.group(1)).strip().upper()
        for zone in ("GREEN", "YELLOW", "RED"):
            if txt.startswith(zone) and len(txt) < 40:
                return row.replace("<tr", f'<tr class="zone-{zone.lower()}"', 1)
        return row
    return re.sub(r"<tr[^>]*>.*?</tr>", rep, h, flags=re.S)


def build_html(src_md, out_html, conf, resource_path, src_dir):
    css = os.path.join(SKILL_DIR, "assets", "handout.css")
    header = f'<div class="practice-header">{linkify_html(fill(conf.get("header_text", ""), conf), conf)}</div>\n<div class="page-body">\n'
    footer = "</div>\n<div class=\"practice-footer\">" + "<br>".join(linkify_html(l, conf) for l in footer_lines(conf)) + "</div>\n"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as hb, \
         tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as ha:
        hb.write(header); ha.write(footer); hb_path, ha_path = hb.name, ha.name
    try:
        proc = subprocess.run(["pandoc", src_md, "-o", out_html, "--from", "markdown", "--to", "html5",
                               "--standalone", "--embed-resources", "--css", css,
                               "--include-before-body", hb_path, "--include-after-body", ha_path,
                               "--resource-path", resource_path, "--metadata", "lang=en"],
                              capture_output=True, text=True, cwd=src_dir)
    finally:
        os.unlink(hb_path); os.unlink(ha_path)
    if proc.returncode != 0:
        return False, proc.stderr
    h = open(out_html, encoding="utf-8").read()
    h = colour_zone_rows(h)
    h = h.replace('<meta name="viewport"', '<meta name="viewport"', 1)
    if "viewport" not in h:
        h = h.replace("<head>", '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">', 1)
    open(out_html, "w", encoding="utf-8").write(h)
    return True, proc.stderr


def build_pdf(out_docx, out_html, out_pdf):
    """Return (method, note). Prefers LibreOffice (keeps Word header/footer/page numbers)."""
    soffice = find_exe(SOFFICE_CANDIDATES)
    if soffice:
        outdir = os.path.dirname(os.path.abspath(out_pdf))
        proc = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", outdir, out_docx],
                              capture_output=True, text=True, timeout=180)
        produced = os.path.join(outdir, os.path.splitext(os.path.basename(out_docx))[0] + ".pdf")
        if proc.returncode == 0 and os.path.exists(produced):
            if os.path.abspath(produced) != os.path.abspath(out_pdf):
                shutil.move(produced, out_pdf)
            return "LibreOffice (from .docx)", ""
        return None, f"LibreOffice failed: {proc.stderr.strip()[:200]}"
    chrome = find_exe(CHROME_CANDIDATES)
    if chrome and out_html and os.path.exists(out_html):
        proc = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                               f"--print-to-pdf={os.path.abspath(out_pdf)}", "file://" + os.path.abspath(out_html)],
                              capture_output=True, text=True, timeout=120)
        if os.path.exists(out_pdf):
            return "Google Chrome (from .html; no page numbers)", ""
        return None, f"Chrome failed: {proc.stderr.strip()[:200]}"
    return None, "no converter found. For best results: brew install --cask libreoffice"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True, help="path of the .docx; .pdf/.html use the same base name")
    ap.add_argument("--practice", default=os.path.join(PT_HOME, "practice.conf"))
    ap.add_argument("--pdf", action="store_true"); ap.add_argument("--html", action="store_true")
    ap.add_argument("--all", action="store_true", help="docx + pdf + html")
    ap.add_argument("--table-only", action="store_true", help="no header/footer; for pasting into an existing document")
    ap.add_argument("--strict", action="store_true", help="fail on leftover [[CONFIRM]]/[[MISSING]] markers")
    a = ap.parse_args()
    if a.all:
        a.pdf = a.html = True
    if not shutil.which("pandoc"):
        sys.exit("pandoc not found. Run scripts/setup.sh")
    if not os.path.exists(a.source):
        sys.exit(f"source not found: {a.source}")

    conf = read_conf(a.practice)
    src_dir = os.path.dirname(os.path.abspath(a.source))
    client_dir = os.path.dirname(src_dir)
    resource_path = os.pathsep.join([src_dir, client_dir, os.path.join(PT_HOME, "library"), os.getcwd()])
    text = open(a.source, encoding="utf-8").read()
    marker_lines = [l.strip() for l in text.splitlines() if MARKER_RE.search(l)]
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: conf.get(m.group(1), m.group(0)), text)

    base = os.path.splitext(a.out)[0]
    out_docx, out_pdf, out_html = base + ".docx", base + ".pdf", base + ".html"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8", dir=src_dir) as tmp:
        tmp.write(text); tmp_path = tmp.name
    try:
        proc = subprocess.run(["pandoc", tmp_path, "-o", out_docx, "--from", "markdown", "--to", "docx",
                               "--resource-path", resource_path], capture_output=True, text=True)
        if proc.returncode != 0:
            sys.exit(f"pandoc failed:\n{proc.stderr}")
        missing_images = [m.rstrip(":.,") for m in re.findall(r"Could not fetch resource (\S+)", proc.stderr)]
        html_ok, html_err = (None, "")
        if a.html or a.pdf:
            html_ok, html_err = build_html(tmp_path, out_html, conf, resource_path, src_dir)
    finally:
        os.unlink(tmp_path)

    d = docx.Document(out_docx)
    normal = d.styles["Normal"]
    normal.font.name = conf.get("font_name", "Calibri")
    try:
        normal.font.size = Pt(float(conf.get("font_size", "11")))
    except ValueError:
        pass
    for sname in ("Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3"):
        try:
            d.styles[sname].font.name = conf.get("font_name", "Calibri")
        except KeyError:
            pass
    for t in d.tables:
        set_table_borders(t)
    if not a.table_only:
        sec = d.sections[0]
        h = sec.header; h.is_linked_to_previous = False
        hp = h.paragraphs[0] if h.paragraphs else h.add_paragraph()
        hp.text = ""
        write_line(hp, fill(conf.get("header_text", ""), conf), conf, 9)
        hp2 = h.add_paragraph(); hp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp2.add_run("Page ").font.size = Pt(9); add_field(hp2, "PAGE")
        hp2.add_run(" of ").font.size = Pt(9); add_field(hp2, "NUMPAGES")
        f = sec.footer; f.is_linked_to_previous = False
        first = True
        for line in footer_lines(conf):
            fp = (f.paragraphs[0] if first and f.paragraphs else f.add_paragraph())
            fp.text = ""; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            write_line(fp, line, conf, 9); first = False
    d.save(out_docx)

    pdf_method, pdf_note = (None, "")
    if a.pdf:
        pdf_method, pdf_note = build_pdf(out_docx, out_html if html_ok else None, out_pdf)
    if a.pdf and not a.html and os.path.exists(out_html):
        os.unlink(out_html)

    # ---- verification: reopen and read back
    v = docx.Document(out_docx)
    h1 = sum(1 for p in v.paragraphs if p.style.name == "Heading 1")
    h2 = sum(1 for p in v.paragraphs if p.style.name == "Heading 2")
    title = next((p.text for p in v.paragraphs if p.style.name == "Title"), "")
    rows = sum(len(t.rows) for t in v.tables)
    body_text = "\n".join(p.text for p in v.paragraphs) + "\n".join(c.text for t in v.tables for r in t.rows for c in r.cells)
    leftover = MARKER_RE.findall(body_text)
    kb = lambda p: f"{os.path.getsize(p) // 1024} KB" if os.path.exists(p) else "missing"
    print("BUILD REPORT")
    print(f"source:   {a.source}")
    print(f"docx:     {out_docx}  ({kb(out_docx)})")
    if a.pdf:
        print(f"pdf:      {out_pdf}  ({kb(out_pdf)})  via {pdf_method}" if pdf_method else f"pdf:      SKIPPED — {pdf_note}")
    if a.html:
        print(f"html:     {out_html}  ({kb(out_html)})" if html_ok else f"html:     FAILED — {html_err.strip()[:200]}")
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
