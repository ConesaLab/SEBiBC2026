"""Add a hidden tab "AI evaluation Gemini 4 Hydrogen" to statement_marks.xlsx without rewriting any existing part.

The new sheet is a copy of the "AI evaluation" sheet (xl/worksheets/sheet9.xml: same styles, frozen panes, colour
rules and per-paper count formulas) populated with Gemini 4 Hydrogen's marks, plus two comparison columns: Fable 5.2's
mark (a live reference to 'AI evaluation'!D) and whether the two readers agree. Every other zip entry is copied byte
for byte, except workbook.xml, its rels, [Content_Types].xml (one new sheet each), and sheet1.xml (the "Start here"
presenter note listing hidden tabs).

usage: python3 -I add_gemini_tab.py <in.xlsx> <out.xlsx> <rebuild/analysis/gemini_eval>
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
EVD = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT_DIR / "rebuild" / "analysis" / "gemini_eval"

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ET.register_namespace("", NS)
q = lambda t: "{%s}%s" % (NS, t)

TAB = "AI evaluation Gemini 4 Hydrogen"
assert len(TAB) <= 31, f"Excel tab name exceeds 31 chars: {len(TAB)}"

PAPERS = [
    ("A", "A_hernandez_2017.json"),
    ("B", "B_wang_2019.json"),
    ("C", "C_jimenez_2021.json"),
    ("D", "D_balzano_2021.json"),
    ("E", "E_rubio_2021.json"),
    ("F", "F_fabregas_2018.json"),
]

OVERALL_COMMENTS = {
    "A": (
        "Seven of eight statements are numerically and contrast-accurate, recovering Cxcl2 (Fig 5a-c) and identifying "
        "Axl (S4, Especially good: novel biphasic C5aR1 pattern in MOESM8 Cluster 2), Ccl6, Hck, Stat5a, and Tlr2/Cd14 "
        "cleanly. Only S7 fails (X, D): it cites non-Arctic C5aR1KO_vs_WT as 'partial restoration' of Cx3cr1 while "
        "ArcticC5aR1KO_vs_Arctic is negative/flat and Cluster 3 showed no rescue difference."
    ),
    "B": (
        "Only S2 and S6 hold up and S5 is Especially good (uncovering a 12.2-fold post-transcriptional collapse of DAB2 "
        "in DBDmut omitted by Wang 2019). Five fail: S1 and S8 wrongly treat HNF1A mRNA as unchanged despite Fig. 2C "
        "qPCR loss (p < 0.0001) and S8 conflates HNF4A DBD loss with HNF1A transactivation; S3 and S4 misstate "
        "non-significant/below-cutoff CDH1 and ITGB5 contrasts; S7 is generic background with no experiment data."
    ),
    "C": (
        "Shared IL6/NFKB2/ISGF3 claims (S1, S2, S7, S11, S15) hold up, and S16 is Especially good (actionable "
        "Lbp-induced CXCL10/CXCL11 -> CXCR3 T-cell link absent from Paper C). Ten fail: legs hallucinate unmeasured "
        "C1QA/B/C/C4A_2 and non-DEG PGGT1B/CASP4 (S3, S4, S10, S12), misread single-arm DEGs as dual-arm (S5, S9, "
        "S13), deny Lbp's Type I IFN signature (S8), reverse receptor-less BAFF->NFKB2 or pro-IL-1beta logic (S6, S14), "
        "and confuse Lbp with Gram-negative LbpB (S12)."
    ),
    "D": (
        "S1, S7, S10, and S13 are accurate on values, IDs, and longitudinal contrasts. Ten fail, six from a systematic "
        "design error (X): treating 12mo_before_SC Case-vs-Control differences as an untreated baseline (S4, S5, S6, "
        "S8, S9, S11). S2, S3, and S12 invert ACOT4/ACOT2 free-fatty-acid and GALR3/GAL ligand directions, and S14 "
        "substitutes mis-mapped APC2 (WNT pathway) for APOC2 while triglyceride values drop."
    ),
    "E": (
        "IL4/IL6 transcript-protein discordance claims (S2-S5) and HOXA9-MEIS1-FLT3 (S7) hold up, and S1 is "
        "Especially good (linking induced IL4 mRNA to CD36/PPARgamma via human macrophage evidence while noting flat "
        "serum IL-4). Four fail: S6 misreads non-significant IFNG (+0.33, FDR=0.211) and cites type I IFN liver work "
        "as IFN-gamma; S8 and S10 apply liver/fibrosis or germline studies to cirrhotic blood cells and leak inverted "
        "'noMHE' labels; S9 misclassifies LIPA as a cholesterol-synthesis enzyme."
    ),
    "F": (
        "Only S7 (MAPKKK18), S8 (LOX3), and S10 (SUS3) are fully accurate. Ten fail on biology, citations, data, or "
        "contrasts: S1 merges FAH1 with non-relevant CYP84A4; S2 denies trehalose's further drought rise and calls "
        "vacuolar ATBETAFRUCT4 cell-wall; S3-S6 and S9 conflate HKL1/AtHXK1, BGLU24/BGLU18, ABA attenuation vs "
        "readout, SnRK2 subclasses, and catalytically inactive TPS7 (citing Morus alba); S11 puts 9-LOX LOX5 at the "
        "head of JA synthesis; S12 cites r=0 TPS1 noise; S13 inverts sucrose cleavage."
    ),
}

with zipfile.ZipFile(SRC) as zin:
    infos = zin.infolist()
    parts = {i.filename: zin.read(i.filename) for i in infos}

wb_str = parts["xl/workbook.xml"].decode()
rels_str = parts["xl/_rels/workbook.xml.rels"].decode()
ct_str = parts["[Content_Types].xml"].decode()

assert "xl/worksheets/sheet10.xml" in parts, "expected sheet10.xml (AI evaluation Opus) to exist first"
assert "xl/worksheets/sheet11.xml" not in parts and TAB.encode() not in parts["xl/workbook.xml"], "tab already there"
assert 'sheetId="11"' not in wb_str and 'rId13"' not in wb_str and 'rId13"' not in rels_str, "sheetId/rId already used"

ev = {L: json.loads((EVD / fname).read_text()) for L, fname in PAPERS}
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

put("A1", "Independent evaluation by a third AI reader: Gemini 4 Hydrogen")
put(
    "A2",
    'Marked on 2026-11-12 at extra-high (XHigh) effort by six independent readers (one per paper), blind to Fable '
    '5.2\'s and Opus\'s marks, using the paper\'s full text, cited references, PaintOmics AI walk JSON, and uploaded '
    'job values on the same rubric and scale as the "AI evaluation" tab, and independently verified per statement. '
    "One more reader's opinion, not an answer key.",
)
for i, (L, _) in enumerate(PAPERS):
    put(f"G{6 + i}", OVERALL_COMMENTS[L])

accept = {"Makes sense", "Especially good"}
counts = collections.Counter()
r = 14
for L, _ in PAPERS:
    for s in ev[L]["statements"]:
        fa, fn, fmark = fable_rows[r]
        assert (fa, fn) == (L, s["id"]), (r, fa, fn, L, s["id"])
        ck = s["checks"]
        put(f"D{r}", s["mark"])
        put(f"E{r}", ", ".join(s["reason_codes"]))
        put(f"F{r}", s["in_paper"])
        put(f"G{r}", "")
        put(f"H{r}", "")
        for col, v in zip(
            "IJKLMN",
            [ck["data"], ck["design"], ck["citation"], ck["biology"], s["summary_reason"], s["evidence"]],
        ):
            put(f"{col}{r}", v, style=10)
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

# headers, column widths, merges, dimension, and conditional formatting for the two Fable comparison columns
hdr = {c.get("r"): c.get("s") for c in rows[13].findall(q("c"))}
put("I13", "Data", style=hdr["I13"])
put("M13", "Summary reason", style=hdr["M13"])
put("N13", "Evidence", style=hdr["N13"])
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
col_widths = {"9": "42", "10": "42", "11": "42", "12": "42", "14": "48"}
for col_el in cols.findall(q("col")):
    if col_el.get("min") == col_el.get("max") and col_el.get("min") in col_widths:
        col_el.set("width", col_widths[col_el.get("min")])
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

sheet11 = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(
    root, encoding="utf-8", xml_declaration=False
)

wb = wb_str.replace(
    "</sheets>",
    f'<sheet name="{TAB}" sheetId="11" state="hidden" r:id="rId13" /></sheets>',
    1,
)
rels = rels_str.replace(
    "</Relationships>",
    '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="/xl/worksheets/sheet11.xml" Id="rId13" /></Relationships>',
    1,
)
ct = ct_str.replace(
    '<Override PartName="/xl/workbook.xml"',
    '<Override PartName="/xl/worksheets/sheet11.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml" />'
    '<Override PartName="/xl/workbook.xml"',
    1,
)

s1 = parts["xl/worksheets/sheet1.xml"].decode()
old = 'the tabs "Results", "AI evaluation" (Fable 5.2) and "AI evaluation Opus" are hidden while people mark.'
assert s1.count(old) == 1, f"expected 1 Start-here note match, found {s1.count(old)}"
s1 = s1.replace(
    old,
    'the tabs "Results", "AI evaluation" (Fable 5.2), "AI evaluation Opus" and "AI evaluation Gemini 4 Hydrogen" '
    "are hidden while people mark.",
)

for a, b in ((wb, "rId13"), (rels, "sheet11.xml"), (ct, "sheet11.xml")):
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
        if info.filename == "xl/worksheets/sheet10.xml":
            zi = zipfile.ZipInfo("xl/worksheets/sheet11.xml", date_time=info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, sheet11)

os.replace(tmp_dst, DST)
print("wrote", DST, "counts", dict(collections.Counter(m for (_, m), n in counts.items() for _ in range(n))))
