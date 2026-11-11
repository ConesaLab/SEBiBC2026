#!/usr/bin/env python
"""After the workshop: turn the filled-in sheet into one page that shows, for every statement, what the room chose
and what the AI evaluation (Claude Fable 5.2) chose.

    1. In Google Sheets: File > Download > Microsoft Excel (.xlsx)
    2. env/venv/bin/python scripts/10_ratings_report.py <downloaded.xlsx> [sheets/ratings_report.html]

Reads the paper tabs (rater columns) and the "AI evaluation" tab; needs nothing else.
"""
import html
import pathlib
import sys

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = ["Especially good", "Makes sense", "Can't judge", "Does not make sense"]            # best to worst
COLOR = {"Makes sense": "#1baf7a", "Does not make sense": "#eb6834", "Especially good": "#6250d6", "Can't judge": "#c3c2b7"}
POSITIVE = {"Especially good", "Makes sense"}
e = html.escape


def read(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ai = {}
    if "AI evaluation" in wb.sheetnames:
        ws = wb["AI evaluation"]
        for r in ws.iter_rows(values_only=True):
            if r and r[0] and r[1] and str(r[1]).startswith("S") and len(str(r[0])) == 1:
                ai[(str(r[0]), str(r[1]))] = dict(mark=r[3], reasons=r[4] or "", in_paper=r[5] or "", why=r[12] or "")
            elif r and r[0] and len(str(r[0])) == 1 and r[1] and not str(r[1]).startswith("S") and len(r) > 6 and r[6]:
                ai[(str(r[0]), "overall")] = dict(comment=r[6])                    # the per-paper row: counts in C to F, comment in G
    papers = []
    for ws in wb.worksheets:
        if len(ws.title) < 3 or ws.title[1] != " " or not ws.title[0].isalpha() or ws.title in ("Start here",):
            continue
        letter = ws.title[0]
        rows = list(ws.iter_rows(values_only=True))
        st = []
        for r in rows:
            if r and r[0] and str(r[0]).startswith("S") and str(r[0])[1:].isdigit():
                marks = [str(v).strip() for v in r[3:] if v is not None and str(v).strip() in COLOR]
                st.append(dict(n=str(r[0]), tier=r[1] or "", text=r[2] or "", marks=marks, ai=ai.get((letter, str(r[0])))))
        papers.append(dict(letter=letter, name=ws.title[2:], title=str(rows[0][0] or ws.title), st=st, ai_overall=ai.get((letter, "overall"))))
    return papers


def bar(marks):
    n = len(marks)
    if not n:
        return '<div class="bar empty">no marks yet</div>'
    segs = []
    for m in ORDER:
        k = marks.count(m)
        if k:
            segs.append('<span class="seg" style="flex:%d;background:%s" title="%s: %d of %d raters">%s</span>' % (
                k, COLOR[m], e(m), k, n, '<b class="%s">%d</b>' % ("dark" if m == "Can't judge" else "", k)))
    return '<div class="bar" role="img" aria-label="%s">%s</div>' % (e(", ".join("%s %d" % (m, marks.count(m)) for m in ORDER)), "".join(segs))


def chip(mark):
    if not mark:
        return '<span class="chip none">not evaluated</span>'
    return '<span class="chip"><i style="background:%s"></i>%s</span>' % (COLOR.get(mark, "#999"), e(mark))


def page(papers, src):
    out = []
    tot_marks = sum(len(s["marks"]) for p in papers for s in p["st"])
    for p in papers:
        marks = [m for s in p["st"] for m in s["marks"]]
        raters = max([len(s["marks"]) for s in p["st"]] or [0])
        agree = sum(s["marks"].count(s["ai"]["mark"]) for s in p["st"] if s["ai"] and s["ai"]["mark"])
        judged = sum(len(s["marks"]) for s in p["st"] if s["ai"] and s["ai"]["mark"])
        ai_pos = sum(1 for s in p["st"] if s["ai"] and s["ai"]["mark"] in POSITIVE)
        ai_n = sum(1 for s in p["st"] if s["ai"] and s["ai"]["mark"])
        tiles = [("Raters", str(raters)), ("Marks", str(len(marks))),
                 ("Room: makes sense or better", "%d%%" % round(100 * sum(m in POSITIVE for m in marks) / len(marks)) if marks else "–"),
                 ("AI: makes sense or better", "%d of %d" % (ai_pos, ai_n) if ai_n else "–"),
                 ("Room: does not make sense", "%d%%" % round(100 * marks.count("Does not make sense") / len(marks)) if marks else "–"),
                 ("AI: does not make sense", "%d of %d" % (sum(1 for s in p["st"] if s["ai"] and s["ai"]["mark"] == "Does not make sense"), ai_n) if ai_n else "–"),
                 ("Marks equal to the AI's", "%d%%" % round(100 * agree / judged) if judged else "–")]
        rows = []
        for s in p["st"]:
            a = s["ai"] or {}
            n = len(s["marks"])
            same = s["marks"].count(a.get("mark")) if a.get("mark") else 0
            top = max(ORDER, key=lambda m: (s["marks"].count(m), -ORDER.index(m))) if n else ""
            differ = bool(n and a.get("mark") and top != a["mark"] and ((top in POSITIVE) != (a["mark"] in POSITIVE)))
            rows.append("""<tr class="%s"><th scope="row">%s</th><td class="txt"><details><summary>%s</summary>%s</details></td>
<td class="barcell">%s<div class="counts">%s</div></td><td>%s%s</td><td class="num">%s</td></tr>""" % (
                "differ" if differ else "", e(s["n"]), e(s["text"][:150] + ("…" if len(s["text"]) > 150 else "")),
                ("<p>%s</p>" % e(s["text"])) + ("<p class='why'><b>AI evaluation:</b> %s%s %s</p>" % (e(a.get("mark") or ""), (" (" + e(a["reasons"]) + ")") if a.get("reasons") else "", e(a.get("why") or "")) if a else ""),
                bar(s["marks"]), e(" · ".join("%s %d" % (m, s["marks"].count(m)) for m in ORDER if s["marks"].count(m))) or "&nbsp;",
                chip(a.get("mark")), ('<div class="counts">%s</div>' % e(a["reasons"])) if a.get("reasons") else "",
                ("%d of %d" % (same, n)) if n and a.get("mark") else "–"))
        out.append("""<section><h2><span class="l">%s</span>%s</h2><p class="sub">%s</p><div class="tiles">%s</div><div class="allbar"><span>All marks of the room</span>%s</div>
<table><thead><tr><th>No.</th><th>Statement</th><th>What the room chose</th><th>AI evaluation</th><th>Same as AI</th></tr></thead><tbody>%s</tbody></table>%s</section>""" % (
            e(p["letter"]), e(p["name"]), e(p["title"]), "".join('<div class="tile"><b>%s</b><span>%s</span></div>' % (v, e(k)) for k, v in tiles), bar(marks), "".join(rows),
            ('<p class="sub"><b>AI evaluation, overall:</b> %s</p>' % e(p["ai_overall"]["comment"])) if p["ai_overall"] and p["ai_overall"].get("comment") else ""))
    legend = "".join('<span class="chip"><i style="background:%s"></i>%s</span>' % (COLOR[m], e(m)) for m in ORDER)
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Statement marks: the room and the AI</title><style>
:root{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--line:#e1e0d9;--card:#f4f4f1;--flag:#fff4e0}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--line:#2c2c2a;--card:#242422;--flag:#3a2f1a}}
:root[data-theme=dark]{--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--line:#2c2c2a;--card:#242422;--flag:#3a2f1a}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,"Open Sans",Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:20px 16px 48px}h1{font-size:26px;font-weight:600;margin:0 0 4px}
h2{font-size:19px;margin:34px 0 2px}.l{display:inline-block;width:1.7em;height:1.7em;line-height:1.7em;text-align:center;border-radius:50%%;background:#01695d;color:#fff;margin-right:.5em;font-size:.85em}
.sub{color:var(--ink2);margin:4px 0 10px}.legend{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0 0}
.chip{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}.chip i{width:11px;height:11px;border-radius:3px;display:inline-block}.chip.none{color:var(--muted)}
.tiles{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 12px}.tile{background:var(--card);border-radius:8px;padding:8px 12px;min-width:104px}
.allbar{display:grid;grid-template-columns:170px 1fr;gap:10px;align-items:center;max-width:720px;margin:0 0 14px;color:var(--ink2);font-size:13px}
.tile b{display:block;font-size:20px;font-weight:600}.tile span{color:var(--ink2);font-size:12px}
table{border-collapse:collapse;width:100%%}th,td{padding:7px 8px;border-top:1px solid var(--line);vertical-align:top;text-align:left}
thead th{font-size:12px;color:var(--ink2);font-weight:600;border-top:0}tbody th{white-space:nowrap}td.num{white-space:nowrap}
td.txt{width:42%%}td.barcell{width:30%%;min-width:220px}summary{cursor:pointer}details p{color:var(--ink2);margin:6px 0}.why{font-size:13px}
.bar{display:flex;gap:2px;height:20px}.bar.empty{color:var(--muted);font-size:12px;align-items:center}
.seg{display:flex;align-items:center;justify-content:center;min-width:14px;border-radius:4px}.seg b{color:#fff;font-size:11px;font-weight:600}.seg b.dark{color:#0b0b0b}
.seg:hover{outline:2px solid var(--ink);outline-offset:1px}.counts{color:var(--muted);font-size:12px;margin-top:3px}
tr.differ{background:var(--flag)}.note{color:var(--muted);font-size:12px;margin-top:28px}
@media (max-width:760px){td.txt{width:auto}thead{display:none}tr{display:block;padding:6px 0}td,tbody th{display:block;border:0;padding:3px 8px}}
</style></head><body><main><h1>Statement marks: the room and the AI</h1>
<p class="sub">PaintOmics AI, powered by TELLME · SEBiBC 2026. %d marks on %d statements of %d papers. Bars show how many raters chose each mark; the AI evaluation is
by Claude Fable 5.2 at extra-high effort. Shaded rows: the room's most common mark and the AI's fall on opposite sides (makes sense or better, against does not make sense or can't judge).</p>
<div class="legend">%s</div>%s<p class="note">Built from %s.</p></main></body></html>""" % (
        tot_marks, sum(len(p["st"]) for p in papers), len(papers), legend, "".join(out), e(pathlib.Path(src).name))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    papers = read(sys.argv[1])
    dest = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "sheets" / "ratings_report.html"
    dest.write_text(page(papers, sys.argv[1]))
    print("wrote", dest, "|", "; ".join("%s: %d statements, %d marks" % (p["letter"], len(p["st"]), sum(len(s["marks"]) for s in p["st"])) for p in papers))
