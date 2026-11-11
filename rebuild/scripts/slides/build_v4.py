#!/usr/bin/env python
"""Build slides/SEBiBC26_TELLME_PaintOmicsAI_v4.pdf: the deck as a tutorial.

    the problem -> PaintOmics and TELLME (how it works, what you will see) -> practice: read a real AI
    interpretation and give each statement one of four marks -> what the room found, next to a second AI reader

Compared with v3 (build_v3.py, whose slide functions are reused here): the section "What we can do, what we
can't, and your help" is gone with its three slides (can and cannot, who can judge, the six-papers funnel), and
so is the STATegra worked example. The workshop teaches how to use and read TELLME; it does not ask for help.

    python scripts/slides/build_v4.py [--previews]

The marking sheet's link is read from slides/config.json ("marking_sheet_url"). Until it is set, the places where
its QR code goes show a dashed placeholder.
"""
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                    # noqa: E402
from deck import BODY, MUTED, ORANGE, ORANGE_INK, STRONG, TEAL, TEAL_DARK, WHITE, para, rgb, text, wipe  # noqa: E402
import build_v2 as V2                                               # noqa: E402
import build_v3 as V3                                               # noqa: E402

OUT = D.ROOT / "slides" / "SEBiBC26_TELLME_PaintOmicsAI_v4.pdf"
L, R = V3.L, V3.R


def plan(out):
    p = D.blank_content(out, like=29, title="The hour")
    cols = [("Why, and how it works", "from 10:00", ["One table, many stories: why reading a pathway analysis is the hard part", "PaintOmics: every omic painted on its pathways",
                                                      "TELLME: agents that walk the pathways and write, and what you will see on the page"]),
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


def practice_divider(out):
    """The Practice section is now the third, not the fourth."""
    p = D.from_original(out, 26)
    wipe(p, (80, 533, 114, 558), D.DARK_BG)
    text(p, 85, 552.6, [("03", "Mono")], 17.5, "#fb8351")
    return p


def pick_a_paper(out):
    p = D.blank_content(out, like=29, title="Pick a paper")
    text(p, 1232, 65, [("your letter is your tab in the marking sheet · the QR opens the job: the walk and the cited passages", "Regular")], 13.5, MUTED, align="right")
    V2.card_grid(p, V3.DATA, top=100, bottom=740)
    text(p, L, 770, [("Every one of these papers cites PaintOmics and used it on this data.", "Bold", TEAL_DARK),
                     ("  We ran the same data again, with the AI.", "Regular", BODY)], 15)
    return p


def build():
    out = pymupdf.open()
    O = lambda n, fn=None: ("orig", n, fn)
    seq = [O(1, "title"), ("new", plan),
           O(2), O(3), O(4),
           O(5), O(6), O(7), O(8), O(9), O(10), O(11), O(12), O(13), O(14), O(15), O(16), O(17), O(18), O(19),
           O(26, practice_divider), ("new", V3.four_marks), ("new", "your_turn"), ("new", pick_a_paper),
           ("new", V3.room_found), ("new", V3.second_reader), ("new", V3.ai_flagged), O(31, V3.your_examples),
           O(25), O(32, V3.thank_you),
           O(33), O(34), O(36), O(37), ("new", V3.backup_papers)]
    pick_no = 1 + next(i for i, s in enumerate(seq) if s[1] is pick_a_paper)
    unnumbered = {1, 2, 5, 20, 26, 33}                              # title, section dividers, backup divider
    log = []
    for i, s in enumerate(seq, 1):
        if s[0] == "orig":
            _, n, fn = s
            if fn == "title":
                V3.title_slide(out, pick_no)
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
        else:
            fn = s[1]
            page = V3.your_turn(out, pick_no) if fn == "your_turn" else fn(out)
            D.renumber(page, i)
            log.append((i, "new: " + (fn if isinstance(fn, str) else fn.__name__)))
    out.set_metadata({"title": "AI models to interpret system biology models: PaintOmics AI, powered by TELLME (SEBiBC 2026)",
                      "author": "Tianyuan Liu, Ana Conesa"})
    out.save(OUT, garbage=3, deflate=True)
    return log


if __name__ == "__main__":
    log = build()
    print("wrote", OUT, len(log), "pages | marking sheet link:", V3.SHEET or "NOT SET (placeholders drawn)")
    for i, what in log:
        print("  %2d  %s" % (i, what))
    if "--previews" in sys.argv:
        prev = D.ROOT / "slides" / "work"; prev.mkdir(exist_ok=True)
        for i, what in log:
            if "new" in what or "edited" in what:
                D.preview(OUT, i, prev / ("v4_p%02d.png" % i))
