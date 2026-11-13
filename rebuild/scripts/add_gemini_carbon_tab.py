"""Add a hidden tab "AI evaluation Gemini 4 Carbon" to statement_marks.xlsx without rewriting any existing part.

The new sheet is a copy of the "AI evaluation" sheet (xl/worksheets/sheet9.xml: same styles, frozen panes, colour
rules and per-paper count formulas) populated with Gemini 4 Carbon's marks, plus two comparison columns: Fable 5.2's
mark (a live reference to 'AI evaluation'!D) and whether the two readers agree. Every other zip entry is copied byte
for byte, except workbook.xml, its rels, [Content_Types].xml (one new sheet each), and sheet1.xml (the "Start here"
presenter note listing hidden tabs).

usage: python3 -I add_gemini_carbon_tab.py [in.xlsx] [out.xlsx] [rebuild/analysis/ai_eval]
"""
import collections
import copy
import json
import os
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT_DIR = pathlib.Path(__file__).resolve().parents[2]
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT_DIR / "statement_marks.xlsx"
DST = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT_DIR / "statement_marks.xlsx"
EVD = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT_DIR / "rebuild" / "analysis" / "ai_eval"

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ET.register_namespace("", NS)
q = lambda t: "{%s}%s" % (NS, t)

TAB = "AI evaluation Gemini 4 Carbon"
assert len(TAB) <= 31, f"Excel tab name exceeds 31 chars: {len(TAB)}"

PAPERS = [
    ("A", "hernandez2017_c5ar1_microglia"),
    ("B", "wang2019_hnf4a_hpsc"),
    ("C", "jimenez2021_hbmec_lbp"),
    ("D", "balzano2021_teddy"),
    ("E", "rubio2021_mhe"),
    ("F", "fabregas2018_brl3_drought"),
]

with zipfile.ZipFile(SRC) as zin:
    infos = zin.infolist()
    parts = {i.filename: zin.read(i.filename) for i in infos}

wb_str = parts["xl/workbook.xml"].decode()
rels_str = parts["xl/_rels/workbook.xml.rels"].decode()
ct_str = parts["[Content_Types].xml"].decode()

assert "xl/worksheets/sheet12.xml" in parts, "expected sheet12.xml (AI evaluation Gemini 4 Argon) to exist first"
assert "xl/worksheets/sheet13.xml" not in parts and TAB.encode() not in parts["xl/workbook.xml"], "tab already there"
assert 'sheetId="13"' not in wb_str and 'rId15"' not in wb_str and 'rId15"' not in rels_str, "sheetId/rId already used"

ev = {L: json.loads((EVD / pid / "gemini_carbon_eval.json").read_text()) for L, pid in PAPERS}
root = ET.fromstring(parts["xl/worksheets/sheet9.xml"])
sd = root.find(q("sheetData"))
rows = {int(r.get("r")): r for r in sd.findall(q("row"))}


def cell(row, ref):
    c = next((c for c in row.findall(q("c")) if c.get("r") == ref), None)
    if c is None:
        c = ET.SubElement(row, q("c"), {"r": ref})
    return c


def put(ref, value, style=None, formula=None, cached=None):
    r = int(re.sub(r"[A-Z]", "", ref))
    c = cell(rows[r], ref)
    for ch in list(c):
        c.remove(ch)
    for a in ("t",):
        c.attrib.pop(a, None)
    if style is not None:
        c.set("s", str(style))
    if formula is not None:
        ET.SubElement(c, q("f")).text = formula
        if isinstance(cached, (int, float)):
            ET.SubElement(c, q("v")).text = str(cached)
        elif cached is not None:
            c.set("t", "str")
            ET.SubElement(c, q("v")).text = cached
        return
    if value in (None, ""):
        return
    c.set("t", "inlineStr")
    t = ET.SubElement(ET.SubElement(c, q("is")), q("t"))
    t.text = str(value)
    if t.text != t.text.strip():
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


# Fable's marks, only to fill the cached values of the comparison formulas (the formulas read the "AI evaluation" tab).
fable_rows = {}
for r in range(14, 83):
    row = rows[r]

    def txt(col, _row=row, _r=r):
        c = next((c for c in _row.findall(q("c")) if c.get("r") == f"{col}{_r}"), None)
        t = c.find(f"{q('is')}/{q('t')}") if c is not None else None
        return t.text if t is not None else ""

    fable_rows[r] = (txt("A"), txt("B"), txt("D"))

put("A1", "Independent evaluation by another AI reader: Gemini 4 Carbon")
put(
    "A2",
    "Marked on 2026-11-12 at high effort by six blind Gemini 4 Carbon readers (sharded across the papers) and checked "
    "per statement by an independent blind verifier, each given only its papers' blind evaluation packet (the "
    "statements, the cited passages, the walk legs, the uploaded values) and the papers' full text, with the same "
    'rubric and scale as the "AI evaluation" tab. Neither the readers nor the verifier ever saw Fable 5.2\'s marks or '
    "any other reader's. One more reader's opinion, not an answer key; no person has checked it.",
)
for i, (L, _) in enumerate(PAPERS):
    put(f"G{6 + i}", ev[L]["overall"]["comment"])

accept = {"Makes sense", "Especially good"}
counts = collections.Counter()
r = 14
for L, _ in PAPERS:
    for s in ev[L]["statements"]:
        fa, fn, fmark = fable_rows[r]
        assert (fa, fn) == (L, f"S{s['n']}"), (r, fa, fn, L, s["n"])
        ck = s["checks"]
        for col, v in zip(
            "DEFGHIJKLMN",
            [
                s["mark"],
                ", ".join(s["reasons"]),
                s["in_paper"],
                s.get("beyond", ""),
                s["confidence"],
                ck["numbers"],
                ck["design"],
                ck["citation"],
                ck["biology"],
                s["justification"],
                s.get("in_paper_where", ""),
            ],
        ):
            put(f"{col}{r}", v)
        put(f"O{r}", None, style=37, formula=f"'AI evaluation'!D{r}", cached=fmark)
        same = (
            "same mark"
            if s["mark"] == fmark
            else "same verdict"
            if s["mark"] in accept and fmark in accept
            else "differs"
        )
        put(
            f"P{r}",
            None,
            style=37,
            formula=(
                f'IF(D{r}=O{r},"same mark",IF(AND(OR(D{r}="Makes sense",D{r}="Especially good"),'
                f'OR(O{r}="Makes sense",O{r}="Especially good")),"same verdict","differs"))'
            ),
            cached=same,
        )
        counts[(L, s["mark"])] += 1
        r += 1
assert r == 83

# cached values of the per-paper count formulas (C6:F11), so a reader that does not recalculate still sees numbers
for i, (L, _) in enumerate(PAPERS):
    for col, m in zip("CDEF", ["Especially good", "Makes sense", "Can't judge", "Does not make sense"]):
        c = cell(rows[6 + i], f"{col}{6 + i}")
        v = c.find(q("v"))
        if v is None:
            v = ET.SubElement(c, q("v"))
        v.text = str(counts[(L, m)])

# headers of the two new columns, the title merges widened to P, widths, dimension
hdr = {c.get("r"): c.get("s") for c in rows[13].findall(q("c"))}
put("O13", "Fable 5.2's mark", style=hdr["N13"])
put("P13", "Same as Fable 5.2?", style=hdr["N13"])

for row in rows.values():  # keep cells of every row in column order
    cs = row.findall(q("c"))
    key = lambda c: (len(re.sub(r"\d", "", c.get("r"))), re.sub(r"\d", "", c.get("r")))
    for c in cs:
        row.remove(c)
    for c in sorted(cs, key=key):
        row.append(c)
    if row.get("spans"):
        row.attrib.pop("spans")

root.find(q("dimension")).set("ref", "A1:P82")
cols = root.find(q("cols"))
for n, w in ((15, 20), (16, 16)):
    ET.SubElement(cols, q("col"), {"width": str(w), "customWidth": "1", "min": str(n), "max": str(n)})

for mc in root.find(q("mergeCells")).findall(q("mergeCell")):
    if mc.get("ref") in ("A2:N2", "A3:N3"):
        mc.set("ref", mc.get("ref").replace("N", "P"))

cfs = root.findall(q("conditionalFormatting"))
cf2 = copy.deepcopy(cfs[0])
cf2.set("sqref", "O14:O82")
for i, rule in enumerate(cf2.findall(q("cfRule"))):
    rule.set("priority", str(5 + i))
root.insert(list(root).index(cfs[0]) + 1, cf2)

sheet13 = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(
    root, encoding="utf-8", xml_declaration=False
)

wb = wb_str.replace(
    "</sheets>",
    f'<sheet name="{TAB}" sheetId="13" state="hidden" r:id="rId15" /></sheets>',
    1,
)
rels = rels_str.replace(
    "</Relationships>",
    '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="/xl/worksheets/sheet13.xml" Id="rId15" /></Relationships>',
    1,
)
ct = ct_str.replace(
    '<Override PartName="/xl/workbook.xml"',
    '<Override PartName="/xl/worksheets/sheet13.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml" />'
    '<Override PartName="/xl/workbook.xml"',
    1,
)

s1 = parts["xl/worksheets/sheet1.xml"].decode()
old = (
    'the tabs "Results", "AI evaluation" (Fable 5.2), "AI evaluation Opus", '
    '"AI evaluation Gemini 4 Hydrogen" and "AI evaluation Gemini 4 Argon" are hidden while people mark.'
)
assert s1.count(old) == 1, f"expected 1 Start-here note match, found {s1.count(old)}"
s1 = s1.replace(
    old,
    'the tabs "Results", "AI evaluation" (Fable 5.2), "AI evaluation Opus", '
    '"AI evaluation Gemini 4 Hydrogen", "AI evaluation Gemini 4 Argon" and "AI evaluation Gemini 4 Carbon" '
    "are hidden while people mark.",
)

for a, b in ((wb, "rId15"), (rels, "sheet13.xml"), (ct, "sheet13.xml")):
    assert b in a

new = {
    "xl/workbook.xml": wb.encode(),
    "xl/_rels/workbook.xml.rels": rels.encode(),
    "[Content_Types].xml": ct.encode(),
    "xl/worksheets/sheet1.xml": s1.encode(),
}

tmp_dst = DST.with_suffix(".xlsx.tmp")
with zipfile.ZipFile(tmp_dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for info in infos:
        data = new.get(info.filename, parts[info.filename])
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zout.writestr(zi, data)
        if info.filename == "xl/worksheets/sheet12.xml":
            zi = zipfile.ZipInfo("xl/worksheets/sheet13.xml", date_time=info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, sheet13)

os.replace(tmp_dst, DST)
print("wrote", DST, "counts", dict(collections.Counter(m for (_, m), n in counts.items() for _ in range(n))))
