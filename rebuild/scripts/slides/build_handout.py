#!/usr/bin/env python
"""slides/practice_handout.pdf (A4, two papers per page) and slides/practice_datasets.html (links to
click instead of QR codes), both from slides/datasets.json.

    env/venv/bin/python scripts/slides/build_handout.py [--previews]
"""
import html
import json
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                                    # noqa: E402
from deck import BODY, CARD, MUTED, ORANGE_INK, STRONG, TEAL, TEAL_DARK, WHITE, box, para, text  # noqa: E402

SL = D.ROOT / "slides"
QR = SL / "assets" / "qr"; QR.mkdir(parents=True, exist_ok=True)
DATA = [d for d in json.loads((SL / "datasets.json").read_text()) if d.get("featured")]
PW, PH, M = 595, 842, 38
CFG = json.loads((SL / "config.json").read_text()) if (SL / "config.json").exists() else {}
SHEET = (CFG.get("marking_sheet_url") or "").strip()
MATERIALS = (CFG.get("materials_url") or "").strip()
FORMS = json.loads((SL / "marking_forms.json").read_text())["forms"]             # one marking form per paper (12 Nov)
FOOTER = [("Marking: ", "one form per paper, its link is on the paper's card")] + ([("Slides and materials: ", D.bare(MATERIALS))] if MATERIALS else [])
ORG = {"hsa": "human", "mmu": "mouse", "rno": "rat", "dme": "fruit fly", "ath": "Arabidopsis", "dre": "zebrafish", "sly": "tomato"}


def short_citation(c):
    """First three authors, then et al.; the title, journal and year are kept whole."""
    authors, sep, rest = c.partition(". ")
    names = [a.strip() for a in authors.split(",")]
    if sep and len(names) > 4 and "et al" not in authors:
        return ", ".join(names[:3]) + ", et al. " + rest
    return c


def header(p, n, total):
    box(p, (0, 0, PW, 8), fill=TEAL)
    text(p, M, 40, [("Pick a paper", "Bold")], 21, STRONG)
    text(p, PW - M, 40, "PaintOmics AI, powered by TELLME · SEBiBC 2026 · page %d of %d" % (n, total), 9.5, MUTED, align="right")
    if n > 1:
        return 56
    y = para(p, M, 50, "Each paper below cites PaintOmics and used it on this data. We ran the same data on paintomics.org, and "
             "PaintOmics AI wrote what it found as numbered statements. Pick a paper, open its form (the link on its card) and give every "
             "statement one of four marks: makes sense, does not make sense, especially good, can't judge. The job page shows "
             "the evidence behind each statement.", 10, PW - 2 * M, color=BODY, leading=1.42)
    return y + 10


def card(p, d, top, height=None):
    """Draw one paper. Without `height` this is the measuring pass (on a scratch page)."""
    x0, x1 = M, PW - M
    if height:
        box(p, (x0, top, x1, top + height), fill=CARD, stroke="#e2e2e2", radius=10)
    q = 82
    # two QR codes on the right: the job, and the paper
    for k, (label, url) in enumerate((("the job", d["url"]), ("the paper", "https://doi.org/" + d["doi"]))):
        qx, qy = x1 - 14 - q, top + 14 + k * (q + 30)
        box(p, (qx - 4, qy - 4, qx + q + 4, qy + q + 4), fill=WHITE, radius=4)
        png = D.qr_png(url, QR / ("%s_%s.png" % (d["id"], "job" if k == 0 else "paper")))
        p.insert_image(pymupdf.Rect(qx, qy, qx + q, qy + q), filename=str(png))
        text(p, qx + q / 2, qy + q + 14, [(label, "SemiBold")], 9, TEAL_DARK, align="center")
    text(p, x1 - 14 - q / 2, top + 14 + 2 * (q + 30) + 4, [(d["jobID"], "Mono")], 9, STRONG, align="center")
    tx, tw = x0 + 16, (x1 - x0) - q - 14 - 16 - 22
    D.circle_number(p, tx + 11, top + 25, d["letter"], r=12, fill=TEAL, size=13)
    text(p, tx + 31, top + 30, [(d["short"], "Bold"), ("  " + d.get("journal", ""), "Regular", MUTED)], 13.5, STRONG)
    y = para(p, tx, top + 44, d["topic"], 11.5, tw, face="SemiBold", color=STRONG, leading=1.32)
    y = para(p, tx, y + 4, short_citation(d["citation"]), 8.2, tw, color=MUTED, leading=1.36, max_lines=4)
    y = para(p, tx, y + 7, d["system"], 9.6, tw, color=BODY)
    y = para(p, tx, y + 2, d["omics"], 9.6, tw, face="SemiBold", color=TEAL_DARK)
    y = para(p, tx, y + 5, "In the paper: " + d["used_paintomics"], 9.2, tw, color=BODY, leading=1.34)
    text(p, tx, y + 16, [("The paper's main conclusions", "Bold")], 10, STRONG)
    text(p, tx + tw, y + 16, [("Mark it here: ", "Bold", ORANGE_INK), (D.bare(FORMS[d["letter"]]["short"]), "Mono", STRONG)], 9.5, align="right")
    y += 22
    for i, c in enumerate(d["conclusions"], 1):
        text(p, tx, y + 0.76 * 9.6, [("%d" % i, "Bold")], 9.6, TEAL_DARK)
        y = para(p, tx + 13, y, c, 9.4, tw - 13, color=BODY, leading=1.34) + 3.5
    if d.get("held_back"):
        y = para(p, tx, y + 3, "Held back on the job page by the \"not a graph artifact\" check: click \"Show the interpretation anyway\" "
                 "there. The paper's form lists its statements in full.",
                 9, tw, face="SemiBold", color=ORANGE_INK, leading=1.34)
    if d.get("note"):
        y = para(p, tx, y + 3, d["note"], 9, tw, face="Italic", color=MUTED)
    return max(y, top + 14 + 2 * (q + 30) + 10)


def build():
    scratch = pymupdf.open().new_page(width=PW, height=PH)
    more = len(FOOTER) - 1                                       # a second footer line takes 11 pt more of the margin, which the cards give up (5 pt each)
    heights = [card(scratch, d, 0) + 10 - 5 * more for d in DATA]   # content height + bottom padding
    GAP, FOOT = 8, 30 + 11 * more
    tops = {True: header(scratch, 1, 1), False: header(scratch, 2, 2)}       # first page / later pages
    pages, cur = [], []
    for d, h in zip(DATA, heights):
        avail = PH - tops[not pages] - FOOT
        if cur and sum(x[1] for x in cur) + GAP * len(cur) + h > avail + 0.5:
            pages.append(cur); cur = []
        cur.append((d, h))
    if cur:
        pages.append(cur)
    print("card heights:", [round(x) for x in heights], "| cards per page:", [len(c) for c in pages])
    doc = pymupdf.open()
    for n, chunk in enumerate(pages, 1):
        p = doc.new_page(width=PW, height=PH)
        top = header(p, n, len(pages))
        for d, h in chunk:
            card(p, d, top, h)
            top += h + GAP
        for k, (label, link) in enumerate(FOOTER):                # last line at PH - 16 as before; the first one moves up when there are two
            text(p, M, PH - 16 - 11 * (more - k), [(label, "Regular", MUTED), (link, "SemiBold", TEAL_DARK)], 8.5)
    out = SL / "practice_handout.pdf"
    doc.save(out, garbage=3, deflate=True)
    return out, len(pages)


def build_html():
    e = html.escape
    cards = []
    for d in DATA:
        held = ("<p class='held'>Held back by the “not a graph artifact” check: click <b>Show the interpretation anyway</b>, "
                "to read it on the job page. The paper's form lists its statements in full.</p>") if d.get("held_back") else ""
        cards.append("""<article><h2><span class="l">%s</span>%s</h2><p class="topic">%s</p>
<p class="btn"><a class="job" href="%s">Open the job <code>%s</code></a> <a href="https://doi.org/%s">Read the paper</a> <a href="%s">Mark the statements</a></p>
<p class="meta">%s<br><b>%s</b></p><p class="cite">%s</p><p><b>In the paper:</b> %s</p>
<p><b>The paper's main conclusions</b></p><ol>%s</ol>%s</article>""" % (
            e(d["letter"]), e(d["short"] + " · " + d.get("journal", "")), e(d["topic"]), e(d["url"]), e(d["jobID"]), e(d["doi"]), e(FORMS[d["letter"]]["short"]), e(d["system"]), e(d["omics"]),
            e(short_citation(d["citation"])), e(d["used_paintomics"]), "".join("<li>%s</li>" % e(c) for c in d["conclusions"]), held))
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pick a paper · PaintOmics AI practice</title><style>
:root{--teal:#009080;--dark:#01695d;--ink:#1a1a1a;--muted:#555;--card:#f2f2f2;--orange:#b85b36}
body{font:16px/1.5 "Open Sans",system-ui,sans-serif;color:var(--ink);margin:0;background:#fff}
header{background:var(--teal);color:#fff;padding:22px 16px}header h1{margin:0 0 6px;font-weight:300;font-size:28px}header p{margin:0;max-width:60em}
main{max-width:980px;margin:0 auto;padding:16px;display:grid;gap:16px}
article{background:var(--card);border-radius:12px;padding:16px 18px}h2{font-size:18px;margin:0 0 4px}
.l{display:inline-block;background:var(--teal);color:#fff;border-radius:50%%;width:1.6em;height:1.6em;line-height:1.6em;text-align:center;margin-right:.5em}
.topic{font-weight:600;margin:.2em 0 .6em}.meta{color:var(--muted);margin:.4em 0}.meta b{color:var(--dark)}.cite{font-size:13px;color:var(--muted)}
.btn a{display:inline-block;margin:0 8px 8px 0;padding:8px 14px;border-radius:8px;border:1px solid var(--teal);color:var(--dark);text-decoration:none;font-weight:600;background:#fff}
.btn a.job{background:var(--teal);color:#fff}.btn code{font-size:.9em}ol{margin:.3em 0 .3em 1.2em;padding:0}.held{color:var(--orange);font-weight:600}
footer{max-width:980px;margin:0 auto;padding:0 16px 32px;color:var(--muted)}a{color:var(--dark)}
</style></head><body><header><h1>Pick a paper</h1><p>PaintOmics AI, powered by TELLME · SEBiBC 2026. Each paper cites PaintOmics and used it on this data;
we ran the same data on paintomics.org and PaintOmics AI wrote what it found as numbered statements. Pick a paper, open its form (<b>Mark the statements</b>) and give every statement one of four marks. The job page (<b>AI Interpret</b>, top right) shows the evidence behind each statement.</p></header>
<main>%s</main><footer><p>%s</p></footer></body></html>""" % ("\n".join(cards), " · ".join(
        ["Marking: one form per paper, the button on each card"] + (['<a href="%s">Slides and materials</a>' % e(MATERIALS)] if MATERIALS else [])))
    out = SL / "practice_datasets.html"
    out.write_text(page)
    return out


if __name__ == "__main__":
    out, n = build()
    print("wrote", out, n, "pages;", build_html())
    if "--previews" in sys.argv:
        for i in range(1, n + 1):
            D.preview(out, i, SL / "work" / ("handout_p%d.png" % i), width_px=1000)
