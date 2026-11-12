#!/usr/bin/env python
"""Build slides/SEBiBC26_TELLME_PaintOmicsAI_v5.pdf: the deck as a tutorial that teaches how to use and read TELLME.

    the problem -> PaintOmics and TELLME (how it works, what you will see, what it can and cannot do)
    -> practice: read a real AI interpretation and give each statement one of four marks
    -> what the room found, next to a second AI reader

Compared with v4 (build_v4.py): "What TELLME can and cannot do" is back, as the last slide before the practice,
with a closing line that leads into it; "What next: the authors' panel" is gone (it asked authors for datasets and
recorded conversations). Still gone, as in v4: the section "What we can do, what we can't, and your help" (its
divider, "Who can judge an interpretation?", the six-papers funnel) and the STATegra worked example.

Since 11 Nov the problem is told in three slides: "How experts read it: limits and biases" (original 4, six cards
without sources) is replaced by Problem 1, 2 and 3 of the 11 Nov deck (docs/SEBiBC26_TELLME_PaintOmicsAI_2026-11-11.pdf,
its slides 4 to 6), each with three cards of published evidence. The deck has 37 slides.

    python scripts/slides/build_v5.py [--previews]

The marking sheet's link is read from slides/config.json ("marking_sheet_url"). Until it is set, the places where
its QR code goes show a dashed placeholder. The optional "materials_url" (the public repository with the slides, the
handout and the marking workbook) adds one card with its QR code to the Thank you slide. slides/deck_map.json records
which slides carry the two codes (scripts/slides/check_qr.py reads it).
"""
import json
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                    # noqa: E402
from deck import BODY, ORANGE, ORANGE_INK, STRONG, TEAL, WHITE, para, rgb, text, wipe  # noqa: E402
import build_v3 as V3                                               # noqa: E402
import build_v4 as V4                                               # noqa: E402

NAME = "SEBiBC26_TELLME_PaintOmicsAI_v5.pdf"
OUT = D.ROOT / "slides" / NAME
L, R = V3.L, V3.R


def plan(out):
    p = D.blank_content(out, like=29, title="The hour")
    cols = [("Why, and how it works", "from 10:00", ["One table, many stories: why reading a pathway analysis is the hard part", "PaintOmics: every omic painted on its pathways",
                                                      "TELLME: agents that walk the pathways and write; what it can and cannot do"]),
            ("Your turn", "until 10:47", ["Pick one of six published papers", "Read what the AI wrote about that paper's data", "Give every statement one of four marks"]),
            ("What the room found", "to 11:00", ["Your marks, live, statement by statement", "Next to the marks of a second AI reader", "Your examples"])]
    w = (R - L - 2 * 24) / 3
    for i, (head, when, lines) in enumerate(cols):
        x = L + i * (w + 24)
        V3.card(p, x, 122, x + w, 392)
        D.circle_number(p, x + 37, 162, i + 1, r=14, fill=ORANGE, size=15)
        text(p, x + 62, 169, [(head, "Bold")], 20, STRONG)
        text(p, x + w - 24, 168, [(when, "Bold")], 15, ORANGE_INK, align="right")
        y = 212
        for ln in lines:
            p.draw_circle((x + 30, y + 9), 3, color=None, fill=rgb(TEAL), width=0)
            y = para(p, x + 46, y, ln, 16.5, w - 46 - 26, color=BODY, leading=1.36) + 14
    V3.bottom_line(p, "By 11:00 you will have read, and judged, a real AI interpretation yourself.", y=452)
    return p


def can_cannot(out):
    """Original 21 without its "Today" strip (it was about attendees running their own jobs), and with a closing
    line that hands over to the practice."""
    p = D.from_original(out, 21)
    wipe(p, (60, 490, 1380, 560), WHITE)
    V3.bottom_line(p, "TELLME writes the draft; the judgement is yours. Next, you try it on a published dataset.", y=540)
    return p


# ---------------------------------------------------------------- the marking forms (12 Nov, evening)
# The room marks in six Google Forms, one per paper: every statement in full, one of the four marks each. Their
# answers land in one spreadsheet whose tab "Results" counts them live, next to the second reader's marks. slides/marking_forms.json holds the links (written by scripts/forms/marking_forms.gs, tab "Links").
# (For a few hours on 12 Nov the marking was on Slido, slides/slido.json; the free plan could not ask one question
# per statement, so it was dropped.)
import build_v2 as V2                                               # noqa: E402
from deck import MUTED, TEAL_DARK, box, width                       # noqa: E402
FORMS = json.loads((D.ROOT / "slides" / "marking_forms.json").read_text())["forms"]


def short(letter):
    return D.bare(FORMS[letter]["short"])


def title_slide(out, pick_no):
    """V3.title_slide with the materials' QR in the place of the marking sheet's: each paper now has its own form."""
    p = D.from_original(out, 1)
    wipe(p, (60, 330, 790, 392), TEAL)
    text(p, 72, 350.9, [("PaintOmics AI", "Bold"), (", powered by TELLME: does the AI read the data the", "Regular")], 20.9, WHITE)
    text(p, 72, 379.4, "way its paper did?", 20.9, WHITE)
    wipe(p, (1150, 215, 1325, 425), WHITE)
    V3.link_qr(p, V3.MATERIALS, "materials.png", 1163.5, 229, 142)
    text(p, 1234.5, 413.3, [("Slides and materials", "Bold")], 15.2, STRONG, align="center")
    wipe(p, (890, 448, 1345, 566), WHITE)
    box(p, (873, 540, 1368, 642.5), fill=WHITE, radius=12)
    text(p, 898, 468.0, [("Pick a paper:", "Bold", ORANGE_INK), (" six published datasets, already", "Regular")], 17.8, STRONG)
    text(p, 898, 493.0, "run on paintomics.org. They are on slide %d." % pick_no, 17.8, STRONG)
    text(p, 898, 528.5, [("Then mark:", "Bold", ORANGE_INK), (" in the paper's form, give each", "Regular")], 17.8, STRONG)
    text(p, 898, 554.5, "statement the AI wrote one of four marks.", 17.8, STRONG)
    text(p, 898, 590.0, [("Each paper has its own form:", "Bold", ORANGE_INK), (" its QR code", "Regular")], 17.8, STRONG)
    text(p, 898, 616.0, "and a short link are on slide %d, on the paper's card." % pick_no, 17.8, STRONG)
    return p


def your_turn(out, pick_no):
    p = D.blank_content(out, like=29, title="Your turn")
    text(p, 1232, 65, [("until 10:47", "Bold")], 18, ORANGE_INK, align="right")
    V3.card(p, L, 118, 452, 566)
    cx = (L + 452) / 2
    text(p, cx, 164, [("One form per paper", "Bold")], 23, TEAL_DARK, align="center")
    text(p, cx, 192, "the bottom QR on the paper's card · no account", 14.5, MUTED, align="center")
    y = 240
    for d in V3.DATA:
        D.circle_number(p, L + 44, y - 5.5, d["letter"], r=13, fill=TEAL, size=14)
        text(p, L + 68, y, d["short"], 16.5, STRONG)
        text(p, 452 - 26, y, "%d statements" % FORMS[d["letter"]]["statements"], 14, MUTED, align="right")
        y += 44
    if V3.MATERIALS:
        text(p, cx, 546, [("slides: ", "Regular"), (D.bare(V3.MATERIALS), "SemiBold", TEAL_DARK)], 14, MUTED, align="center")
    steps = [("Pick a paper", "six papers, A to F: slide %d" % pick_no),
             ("Open its job page and read what the AI wrote", "the top QR on the paper's card; AI Interpret is top right, with the evidence behind each statement"),
             ("Open the paper's form", "the bottom QR on its card, or its short link; every statement the AI wrote is there in full"),
             ("Give each statement one mark, then press Submit", "makes sense, does not make sense, especially good, can't judge. None is required: skip what you do not reach")]
    y = 118
    for i, (h, s) in enumerate(steps):
        V3.card(p, 482, y, R, y + 100)
        V3.step(p, 506, y + 24, i + 1, h, s, R - 482 - 48)
        y += 100 + 16
    for i, s in enumerate(["Your marks count only after Submit: press it by 10:45", "After Submit you can still edit your answers", "Time up? Stop, rather than skip around"]):
        x = L + (0, 470, 880)[i]
        p.draw_circle((x + 6, 625), 4, color=None, fill=rgb(TEAL), width=0)
        text(p, x + 22, 630.5, s, 15.5, "#484848")
    return p


def pick_a_paper(out):
    """The six cards of V2.card_grid, each with a second QR code under the job's: the paper's marking form."""
    p = D.blank_content(out, like=29, title="Pick a paper")
    text(p, 1232, 65, [("top QR: the job, with the walk and the cited passages · ", "Regular", MUTED), ("bottom QR: the form where you mark", "Bold", ORANGE_INK)], 13.5, align="right")
    top, bottom, cols, gx, gy = 100, 740, 3, 22, 18                 # the geometry of V2.card_grid
    V2.card_grid(p, V3.DATA, top=top, bottom=bottom)
    cw, ch = (R - L - gx * (cols - 1)) / cols, (bottom - top - gy) / 2
    q = 100
    for i, d in enumerate(V3.DATA):
        r, c = divmod(i, cols)
        x0, y0 = L + c * (cw + gx), top + r * (ch + gy)
        qx, qy = x0 + cw - q - 20, y0 + 178
        box(p, (qx - 6, qy - 6, qx + q + 6, qy + q + 6), fill=WHITE, radius=6)
        p.insert_image(pymupdf.Rect(qx, qy, qx + q, qy + q), filename=str(D.qr_png(FORMS[d["letter"]]["short"], V3.QR / ("form_%s.png" % d["letter"]))))
        tx = qx - 20
        text(p, tx, y0 + 230, [("Mark it here", "Bold")], 15, ORANGE_INK, align="right")
        lk = short(d["letter"])
        text(p, tx, y0 + 254, [(lk, "Mono")], min(14.5, 14.5 * (tx - x0 - 22) / width([(lk, "Mono")], 14.5)), STRONG, align="right")
    text(p, L, 770, [("Every one of these papers cites PaintOmics and used it on this data.", "Bold", TEAL_DARK),
                     ("  We ran the same data again, with the AI.", "Regular", BODY)], 15)
    return p


def room_found(out):
    p = D.blank_content(out, like=29, title="What the room found")
    V3.card(p, L, 132, 852, 612)
    items = [("Each statement", "how many of you chose each mark"), ("Agreement", "where the room agrees, and where it splits"),
             ("The doubtful ones", "the statements most of you marked “does not make sense”")]
    for i, (h, s) in enumerate(items):
        y = 132 + i * 160
        if i:
            p.draw_line((L + 28, y), (852 - 28, y), color=rgb("#dcdcdc"), width=1)
        text(p, L + 28, y + 88, [("%02d" % (i + 1), "Mono")], 17, ORANGE)
        text(p, L + 86, y + 78, [(h, "Bold")], 19, STRONG)
        text(p, L + 86, y + 104, s, 16.5, BODY)
    box(p, (888, 132, R, 612), fill=TEAL, radius=12)
    text(p, 1128, 232, [("Live from the six forms", "Bold")], 22, WHITE, align="center")
    text(p, 1128, 266, "every answer lands in one sheet as it is submitted", 16, WHITE, align="center")
    text(p, 1128, 360, [("Tab “Results”", "Bold")], 21, WHITE, align="center")
    for i, s in enumerate(["every statement with its four counts,", "a coloured bar of the room's marks,", "and the second reader's mark beside it"]):
        text(p, 1128, 394 + i * 26, s, 16, WHITE, align="center")
    text(p, 1128, 560, "shown from the presenter's laptop", 14.5, WHITE, align="center")
    return p


def thank_you(out):
    """V3.thank_you without the tile of the old marking sheet (the room marks in the forms now)."""
    keep, V3.SHEET = V3.SHEET, ""
    try:
        return V3.thank_you(out)
    finally:
        V3.SHEET = keep


def build():
    out = pymupdf.open()
    O = lambda n, fn=None: ("orig", n, fn)
    P = lambda n: ("problem", n)                                    # slide n of the 11 Nov deck (docs/..._2026-11-11.pdf)
    seq = [O(1, "title"), ("new", plan),
           O(2), O(3), P(4), P(5), P(6),
           O(5), O(6), O(7), O(8), O(9), O(10), O(11), O(12), O(13), O(14), O(15), O(16), O(17), O(18), O(19),
           O(21, can_cannot),
           O(26, V4.practice_divider), ("new", V3.four_marks), ("new", "your_turn"), ("new", pick_a_paper),
           ("new", room_found), ("new", V3.second_reader), ("new", V3.ai_flagged), O(31, V3.your_examples),
           O(32, thank_you),                                     # to bring "What next" back, put O(25), before this line
           O(33), O(34), O(36), O(37), ("new", V3.backup_papers)]
    where = lambda what: 1 + next(i for i, s in enumerate(seq) if what in s)
    pick_no = where(pick_a_paper)
    unnumbered = {1, 2, 5, 20, 26, 33}                              # title, section dividers, backup divider
    log = []
    for i, s in enumerate(seq, 1):
        if s[0] == "orig":
            _, n, fn = s
            if fn == "title":
                title_slide(out, pick_no)
            elif fn:
                fn(out)
            else:
                D.from_original(out, n)
            page = out[-1]
            if n not in unnumbered and n != i:
                if n == 25:                                         # "What next" is a teal page with a white number
                    wipe(page, (1380, 774, 1432, 796), TEAL)
                    text(page, 1417, 789, [(str(i), "SemiBold")], 11.5, WHITE, align="right")
                else:
                    D.renumber(page, i)
            log.append((i, "original %d%s" % (n, " (edited)" if fn else "")))
        elif s[0] == "problem":
            page = D.from_problems(out, s[1])
            D.renumber(page, i)
            log.append((i, "11 Nov deck %d (Problem %d)" % (s[1], s[1] - 3)))
        else:
            fn = s[1]
            page = your_turn(out, pick_no) if fn == "your_turn" else fn(out)
            D.renumber(page, i)
            log.append((i, "new: " + (fn if isinstance(fn, str) else fn.__name__)))
    out.set_metadata({"title": "AI models to interpret system biology models: PaintOmics AI, powered by TELLME (SEBiBC 2026)",
                      "author": "Tianyuan Liu, Ana Conesa"})
    out.save(OUT, garbage=3, deflate=True)
    deck_map = {"deck": NAME, "slides": len(seq), "pick_a_paper": pick_no,
                "sheet_qr_slides": [],
                "form_qr_slides": [pick_no],
                "materials_qr_slides": [1, where(thank_you)] if V3.MATERIALS else [],
                "materials_text_slides": [where("your_turn"), where(thank_you)] if V3.MATERIALS else []}   # where its address is printed, to type
    (D.ROOT / "slides" / "deck_map.json").write_text(json.dumps(deck_map, indent=1) + "\n")
    return log, deck_map


if __name__ == "__main__":
    log, deck_map = build()
    print("wrote", OUT, len(log), "pages | marking sheet link:", V3.SHEET or "NOT SET (placeholders drawn)")
    print("marking sheet QR on slides", deck_map["sheet_qr_slides"], "| materials link:", V3.MATERIALS or "not set", "| QR on slides", deck_map["materials_qr_slides"],
          "| pick a paper: slide", deck_map["pick_a_paper"])
    for i, what in log:
        print("  %2d  %s" % (i, what))
    if "--previews" in sys.argv:
        prev = D.ROOT / "slides" / "work"; prev.mkdir(exist_ok=True)
        for i, what in log:
            if "new" in what or "edited" in what:
                D.preview(OUT, i, prev / ("v5_p%02d.png" % i))
