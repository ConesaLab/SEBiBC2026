#!/usr/bin/env python
"""Build slides/SEBiBC26_TELLME_PaintOmicsAI_v2.pdf: the original deck with the practice turned
from "bring your own data" into "pick a paper whose data we ran".

    env/venv/bin/python scripts/slides/build_v2.py [--previews]

Reads slides/datasets.json (written by scripts/05_collect_jobs.py). Every edit is listed in
slides/CHANGES.md; this script is the edit itself.
"""
import json
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                    # noqa: E402
from deck import (BODY, CARD, INK, MUTED, ORANGE, ORANGE_INK, STRONG, TEAL, TEAL_DARK, WHITE, box, para, text, wipe, width)  # noqa: E402

SL = D.ROOT / "slides"
OUT = SL / "SEBiBC26_TELLME_PaintOmicsAI_v2.pdf"
DATASETS = json.loads((SL / "datasets.json").read_text()) if (SL / "datasets.json").exists() else []
QR = SL / "assets" / "qr"; QR.mkdir(parents=True, exist_ok=True)
FORM = "https://forms.gle/jQL8waXSd6BCAgJx6"


# ---------------------------------------------------------------- patched originals
def slide_title(out):
    p = D.from_original(out, 1)
    n = len([d for d in DATASETS if d.get("featured")])
    wipe(p, (60, 330, 790, 392), TEAL)
    text(p, 72, 350.9, [("PaintOmics AI", "Bold"), (", powered by TELLME: does the AI read the data the", "Regular")], 20.9, WHITE)
    text(p, 72, 379.4, "way its paper did?", 20.9, WHITE)
    wipe(p, (890, 448, 1345, 566), WHITE)
    text(p, 898, 468.0, [("Pick a paper:", "Bold", ORANGE_INK), (" we ran PaintOmics AI on the data", "Regular")], 17.8, STRONG)
    text(p, 898, 493.0, "of %s papers that used PaintOmics. Jobs: slide 29." % (n if n else "several"), 17.8, STRONG)
    text(p, 898, 528.5, [("While it loads:", "Bold", ORANGE_INK), (" open the paper beside it and", "Regular")], 17.8, STRONG)
    text(p, 898, 554.5, "read its abstract. Then mark what the AI wrote.", 17.8, STRONG)


def slide_who_judges(out):
    p = D.from_original(out, 22)
    wipe(p, (60, 590, 780, 622), WHITE)
    text(p, 71.5, 610.7, [("Today you stand in for the authors: judge it against the paper.", "Bold")], 18, TEAL_DARK)


def slide_two_questions(out):
    p = D.from_original(out, 24)
    wipe(p, (90, 147, 300, 176), CARD)
    text(p, 95.4, 165.7, [("In the paper?", "Bold")], 17.8, STRONG)
    wipe(p, (548, 146, 800, 176), WHITE)
    text(p, 551.5, 165.0, [("Beyond the paper:", "Bold")], 17.8, ORANGE_INK)
    wipe(p, (548, 181, 800, 208), WHITE)
    text(p, 551.5, 200.0, [("K", "Bold", ORANGE_INK), (" well known, left out", "Regular")], 17.8, STRONG)


def slide_your_turn(out):
    p = D.from_original(out, 28)
    # card 1: heading on two lines, as card 3 already is
    wipe(p, (120, 128, 378, 178), CARD)
    text(p, 124, 148.1, [("Pick a paper,", "Bold")], 17.2, STRONG)
    text(p, 124, 171.6, [("open its job", "Bold")], 17.2, STRONG)
    wipe(p, (85, 376, 376, 402), CARD)
    text(p, 89.5, 393.2, "QR codes on the next slide", 14.9, MUTED)
    # card 4
    wipe(p, (1106, 128, 1362, 160), CARD)
    text(p, 1109, 148.1, [("Then: beyond the paper", "Bold")], 17.2, STRONG)
    wipe(p, (1070, 376, 1350, 418), CARD)
    text(p, 1074.5, 393.2, "did it find something the paper", 14.95, MUTED)
    text(p, 1074.5, 412.7, "did not?", 14.95, MUTED)
    # footer
    wipe(p, (104, 608, 420, 638), WHITE)
    text(p, 107.5, 627.6, "The paper open beside the AI text", 15, "#484848")


def slide_your_examples(out):
    p = D.from_original(out, 31)
    wipe(p, (200, 400, 620, 434), WHITE)
    s = 262.5 / width([("One point beyond your paper", "Bold")], 1.0)
    text(p, 411.2, 408.5 + 0.76 * s, [("One point beyond the paper", "Bold")], s, ORANGE_INK, align="center")
    wipe(p, (570, 620, 950, 655), WHITE)
    s2 = 323.0 / width("Your own job, on the presenter laptop.", 1.0)
    text(p, 576.5, 628.5 + 0.76 * s2, "Your pick, on the presenter laptop.", s2, MUTED)


# ---------------------------------------------------------------- new slides
def card_grid(p, items, top=100, bottom=744, cols=3):
    """Dataset cards with a QR each. items: entries of datasets.json. Two rows of three, or three rows when there are more."""
    n = len(items)
    rows = max(2, (n + cols - 1) // cols)
    gx, gy, left, right = 22, 18, 72, 1368
    cw = (right - left - gx * (cols - 1)) / cols
    ch = (bottom - top - gy * (rows - 1)) / rows
    roomy = rows <= 2
    for i, d in enumerate(items):
        r, c = divmod(i, cols)
        x0, y0 = left + c * (cw + gx), top + r * (ch + gy)
        box(p, (x0, y0, x0 + cw, y0 + ch), fill=CARD, stroke="#e4e4e4", radius=12, lw=1)
        q = 138 if roomy else 124
        qx, qy = x0 + cw - q - 20, y0 + 20
        box(p, (qx - 7, qy - 7, qx + q + 7, qy + q + 7), fill=WHITE, radius=6)
        png = D.qr_png(d["url"], QR / (d["id"] + ".png"))
        p.insert_image(pymupdf.Rect(qx, qy, qx + q, qy + q), filename=str(png))
        tx = x0 + 22
        tw = qx - 7 - 14 - tx
        D.circle_number(p, tx + 12, y0 + 33, d["letter"], r=13, fill=TEAL, size=14)
        hs = min(18.5, 18.5 * (tw - 34) / width([(d["short"], "Bold")], 18.5))      # long names shrink to stay clear of the QR
        hx = text(p, tx + 34, y0 + 39.5, [(d["short"], "Bold")], hs, STRONG)
        if d.get("journal") and hx + 8 + width(d["journal"], 13) <= tx + tw:
            text(p, hx + 8, y0 + 39.5, d["journal"], 13, MUTED)
        y = para(p, tx, y0 + 60, d["topic"], 16.5 if roomy else 15.5, tw, color=STRONG, leading=1.3, max_lines=4 if roomy else 3)
        y = para(p, tx, y + 9, d["tag"], 14 if roomy else 13.5, tw, face="SemiBold", color=TEAL_DARK, leading=1.32, max_lines=3 if roomy else 2)
        # bottom line of the card: the job id and, if the text is held back, how to open it
        by = y0 + ch - 17
        jx = text(p, tx, by, [("Job ", "Regular", MUTED), (d["jobID"], "Mono", STRONG)], 13)
        if d.get("held_back"):
            room = x0 + cw - 20 - jx - 12          # the longest hint that leaves a gap after the job id
            hint = next((h for h in ("held back: click “Show the interpretation anyway”", "held back: “Show the interpretation anyway”",
                                     "held back: click “Show … anyway”") if width([(h, "SemiBold")], 11.5) <= room), "held back")
            text(p, x0 + cw - 20, by, [(hint, "SemiBold")], 11.5, ORANGE_INK, align="right")
        else:
            text(p, x0 + cw - 20, by, "doi.org/" + d["doi"], 11.5, MUTED, align="right")


def slide_pick_a_paper(out, items, number, part=None):
    title = "Pick a paper" + (" (%s)" % part if part else "")
    p = D.blank_content(out, like=29, title=title, number=number)
    text(p, 1220, 66, [("each QR opens a finished job: ", "Regular", MUTED), ("AI Interpret", "Bold", TEAL_DARK), (" is top right", "Regular", MUTED)], 14.5, align="right")
    card_grid(p, items, top=100, bottom=740)
    y = 770
    text(p, 72, y, [("Every one of these papers cites PaintOmics and used it on this data.", "Bold", TEAL_DARK)], 15)
    text(p, 1368, y, [("or the lab dataset, STATegra: ", "Regular", MUTED), ("paintomics.org/?jobID=jOT21M14SF", "SemiBold", STRONG)], 13.5, align="right")
    return p


# ---------------------------------------------------------------- assembly
PATCHED = {1: slide_title, 22: slide_who_judges, 24: slide_two_questions, 28: slide_your_turn, 31: slide_your_examples}


def build():
    out = pymupdf.open()
    featured = [d for d in DATASETS if d.get("featured")]
    pages = []                                  # (what, original page or None)
    for pno in range(1, len(D.orig()) + 1):
        if pno == 29 and featured:
            chunks = [featured[i:i + 9] for i in range(0, len(featured), 9)]
            for k, chunk in enumerate(chunks):
                slide_pick_a_paper(out, chunk, None, part="%d of %d" % (k + 1, len(chunks)) if len(chunks) > 1 else None)
                pages.append("pick-a-paper")
            continue                              # the old "No data with you?" slide goes; its lab job is in the footer
        if pno in PATCHED:
            PATCHED[pno](out)
        else:
            D.from_original(out, pno)
        pages.append("orig%d" % pno)
    # page numbers: the deck prints them on content slides only (not on title/section slides)
    numbered = {i for i in range(3, len(D.orig()) + 1)} - {5, 20, 26, 33, 25}
    for i, what in enumerate(pages, 1):
        o = int(what[4:]) if what.startswith("orig") else None
        if what == "pick-a-paper" or (o in numbered and i != o):
            D.renumber(out[i - 1], i)
    out.set_metadata({"title": "AI models to interpret system biology models: PaintOmics AI, powered by TELLME (SEBiBC 2026), v2",
                      "author": "Tianyuan Liu, Ana Conesa"})
    out.save(OUT, garbage=3, deflate=True)
    return pages


if __name__ == "__main__":
    pages = build()
    print("wrote", OUT, len(pages), "pages")
    if "--previews" in sys.argv:
        prev = SL / "work"; prev.mkdir(exist_ok=True)
        for i, what in enumerate(pages, 1):
            o = int(what[4:]) if what.startswith("orig") else None
            if what == "pick-a-paper" or o in PATCHED or o == 29:
                D.preview(OUT, i, prev / ("v2_p%02d.png" % i)); print("preview", i, what)
