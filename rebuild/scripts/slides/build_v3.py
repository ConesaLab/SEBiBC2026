#!/usr/bin/env python
"""Build slides/SEBiBC26_TELLME_PaintOmicsAI_v3.pdf: the deck reorganised around the workshop as it now runs.

    talk (problem, PaintOmics, TELLME, limits)  ->  six published papers  ->  four marks in one shared sheet
    ->  what the room found, next to a second AI reader  ->  what next

    env/venv/bin/python scripts/slides/build_v3.py [--previews]

Original pages are reused untouched or with single lines repainted; new pages are drawn on the deck's own frame.
The marking sheet's link is read from slides/config.json ("marking_sheet_url"); until it is set, the places where
its QR code goes show a marked placeholder. slides/CHANGES.md lists every change.
"""
import collections
import json
import math
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                    # noqa: E402
from deck import (BODY, CARD, INK, MUTED, ORANGE, ORANGE_INK, STRONG, TEAL, TEAL_DARK, WHITE, box, para, rgb, text, wipe, width)  # noqa: E402
import build_v2 as V2                                               # noqa: E402  (card grid of the Pick a paper slide, two line patches)

SL = D.ROOT / "slides"
OUT = SL / "SEBiBC26_TELLME_PaintOmicsAI_v3.pdf"
CFG = json.loads((SL / "config.json").read_text()) if (SL / "config.json").exists() else {}
SHEET = (CFG.get("marking_sheet_url") or "").strip()
MATERIALS = (CFG.get("materials_url") or "").strip()                 # public repository: slides, handout, marking workbook
DATA = [d for d in json.loads((SL / "datasets.json").read_text()) if d.get("featured")]
QR = SL / "assets" / "qr"; QR.mkdir(parents=True, exist_ok=True)
EVAL = {d["id"]: json.loads((D.ROOT / "analysis" / "ai_eval" / d["id"] / "fable_eval.json").read_text()) for d in DATA}

GOOD, BAD, STAR, UNK = "#1baf7a", "#eb6834", "#6250d6", "#c3c2b7"      # the four marks, as in the sheet's charts
MARK = {"Makes sense": GOOD, "Does not make sense": BAD, "Especially good": STAR, "Can't judge": UNK}
ORDER = ["Especially good", "Makes sense", "Can't judge", "Does not make sense"]
L, R = 72, 1368                                                        # content margins of the deck


# ---------------------------------------------------------------- small parts
def card(p, x0, y0, x1, y1, fill=CARD, stroke="#e4e4e4", r=12):
    box(p, (x0, y0, x1, y1), fill=fill, stroke=stroke, radius=r, lw=1)


def bottom_line(p, s, y=668):
    text(p, L, y, [(s, "Bold")], 18, TEAL_DARK)


def mark_icon(p, kind, cx, cy, r):
    """One of the four marks as a filled circle with its sign, drawn (the deck's font has no such glyphs)."""
    col = MARK[kind]
    p.draw_circle((cx, cy), r, color=None, fill=rgb(col), width=0)
    w, ink = max(1.6, 0.17 * r), rgb(WHITE)
    if kind == "Makes sense":
        p.draw_polyline([(cx - 0.46 * r, cy + 0.04 * r), (cx - 0.13 * r, cy + 0.37 * r), (cx + 0.48 * r, cy - 0.33 * r)], color=ink, width=w, lineCap=1, lineJoin=1)
    elif kind == "Does not make sense":
        for s in (1, -1):
            p.draw_line((cx - 0.36 * r, cy - s * 0.36 * r), (cx + 0.36 * r, cy + s * 0.36 * r), color=ink, width=w, lineCap=1)
    elif kind == "Especially good":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = (0.6 if i % 2 == 0 else 0.25) * r
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        p.draw_polyline(pts + [pts[0]], color=ink, fill=ink, width=0.5, closePath=True)
    else:
        text(p, cx, cy + 0.42 * r, [("?", "Bold")], 1.2 * r, STRONG, align="center")


def step(p, x, y, n, head, sub, w, fill=ORANGE, head_size=19, sub_size=15.5):
    D.circle_number(p, x + 13, y + 13, n, r=13, fill=fill, size=14)
    text(p, x + 38, y + 20, [(head, "Bold")], head_size, STRONG)
    return para(p, x + 38, y + 32, sub, sub_size, w - 38, color=MUTED, leading=1.36) if sub else y + 30


def qr_tile(p, x, y, size):
    box(p, (x - 8, y - 8, x + size + 8, y + size + 8), fill=WHITE, radius=8)


def link_qr(p, url, png_name, x, y, size):
    """The QR of `url` (a code that both decoders read, see D.qr_png) in a white tile, `size` pt square."""
    qr_tile(p, x, y, size)
    p.insert_image(pymupdf.Rect(x, y, x + size, y + size), filename=str(D.qr_png(url, QR / png_name)))


def sheet_qr(p, x, y, size, label=True):
    """The marking sheet's QR in a white tile, or a marked placeholder while the sheet has no link."""
    if SHEET:
        link_qr(p, SHEET, "marking_sheet.png", x, y, size)
    else:
        qr_tile(p, x, y, size)
        p.draw_rect(pymupdf.Rect(x, y, x + size, y + size), color=rgb(ORANGE), width=1.5, dashes="[6 5] 0")
        s = min(15, size / 11)
        for i, ln in enumerate(("QR of the", "marking sheet", "(link not set yet)")):
            text(p, x + size / 2, y + size / 2 + (i - 1) * 1.45 * s + 0.35 * s, [(ln, "SemiBold")], s, ORANGE_INK, align="center")


# ---------------------------------------------------------------- patched originals
def title_slide(out, pick_no):
    p = D.from_original(out, 1)
    wipe(p, (60, 330, 790, 392), TEAL)
    text(p, 72, 350.9, [("PaintOmics AI", "Bold"), (", powered by TELLME: does the AI read the data the", "Regular")], 20.9, WHITE)
    text(p, 72, 379.4, "way its paper did?", 20.9, WHITE)
    wipe(p, (1150, 215, 1325, 425), WHITE)                         # the old form QR and its label
    sheet_qr(p, 1163.5, 229, 142)
    text(p, 1234.5, 413.3, [("Marking sheet", "Bold")], 15.2, STRONG, align="center")
    wipe(p, (890, 448, 1345, 566), WHITE)
    if MATERIALS:                                                  # the card grows by one paragraph; 873, 1368 and 12 are the original card's edges and corner radius
        box(p, (873, 540, 1368, 642.5), fill=WHITE, radius=12)
    text(p, 898, 468.0, [("Pick a paper:", "Bold", ORANGE_INK), (" six published datasets, already", "Regular")], 17.8, STRONG)
    text(p, 898, 493.0, "run on paintomics.org. They are on slide %d." % pick_no, 17.8, STRONG)
    text(p, 898, 528.5, [("Then mark:", "Bold", ORANGE_INK), (" in the marking sheet, give each", "Regular")], 17.8, STRONG)
    text(p, 898, 554.5, "statement the AI wrote one of four marks.", 17.8, STRONG)
    if MATERIALS:                                                  # for people on a laptop: an address short enough to type
        text(p, 898, 590.0, [("On a laptop:", "Bold", ORANGE_INK), (" " + D.bare(MATERIALS), "SemiBold")], 17.8, STRONG)
        text(p, 898, 616.0, "the marking sheet is linked at the top of that page.", 17.8, STRONG)


def can_cannot(out):
    p = D.from_original(out, 21)
    wipe(p, (60, 490, 1380, 560), WHITE)                           # the "Today" strip was about attendees running their own jobs
    return p


def who_judges(out):
    V2.slide_who_judges(out)
    return out[-1]


def worked_example(out):
    p = D.from_original(out, 27)
    for x0 in (95.5, 536.5, 977.5):                                # "In the paper? yes / partly / no" is no longer asked
        wipe(p, (x0 - 5, 526, x0 + 300, 561), CARD)
        text(p, x0, 549, "Ana's mark", 15, MUTED)
    wipe(p, (60, 632, 950, 668), WHITE)
    text(p, 71.5, 654.2, [("Ana marks each one: makes sense, does not make sense, especially good, or can't judge.", "Bold")], 18, ORANGE_INK)
    return p


def your_examples(out):
    p = D.from_original(out, 31)
    s = 262.5 / width([("One point beyond your paper", "Bold")], 1.0)
    wipe(p, (200, 400, 620, 434), WHITE)
    text(p, 411.2, 410 + 0.76 * s, [("One you marked especially good", "Bold")], s, ORANGE_INK, align="center")
    wipe(p, (850, 400, 1300, 436), WHITE)
    text(p, 1029, 410 + 0.76 * s, [("One that does not make sense, and why", "Bold")], s, ORANGE_INK, align="center")
    for cx, kind in ((411.2, "Especially good"), (1029, "Does not make sense")):       # the icons become the two marks
        wipe(p, (cx - 56, 282, cx + 56, 394), WHITE)
        mark_icon(p, kind, cx, 338, 34)
    wipe(p, (570, 620, 950, 655), WHITE)
    s2 = 323.0 / width("Your own job, on the presenter laptop.", 1.0)
    text(p, 576.5, 628.5 + 0.76 * s2, "Your pick, on the presenter laptop.", s2, MUTED)
    return p


def thank_you(out):
    p = D.from_original(out, 32)
    if SHEET:                                                      # second tile: the form's QR becomes the sheet's
        wipe(p, (1085, 160, 1360, 195), CARD)
        text(p, 1221.5, 181.5, [("Marking sheet", "Bold")], 15.2, TEAL_DARK, align="center")
        wipe(p, (1100, 203, 1345, 447), CARD)
        sheet_qr(p, 1108, 212, 226)
    else:
        wipe(p, (1066, 134, 1380, 470), WHITE)                     # no link yet: drop the tile rather than keep the old form
    if MATERIALS:                                                  # new card under the ELIXIR one, same edges: where to download everything
        y0, y1 = 379, 527
        card(p, 72.5, y0, 716.75, y1)
        link_qr(p, MATERIALS, "materials.png", 96, (y0 + y1) / 2 - 50, 100)
        text(p, 228, (y0 + y1) / 2 - 8, [("Slides and materials", "Bold")], 15.2, TEAL_DARK)
        link = D.bare(MATERIALS)
        text(p, 228, (y0 + y1) / 2 + 15, link, min(13.5, 460 / width(link, 1.0)), BODY)
    return p


# ---------------------------------------------------------------- new slides
def plan(out):
    p = D.blank_content(out, like=29, title="The hour")
    cols = [("Why, and how it works", "from 10:00", ["One table, many stories: why reading a pathway analysis is the hard part", "PaintOmics, and TELLME: agents that walk the pathways and write", "What it can and cannot do"]),
            ("Your turn", "until 10:47", ["Pick one of six published papers", "Read what the AI wrote about that paper's data", "Give every statement one of four marks"]),
            ("What the room found", "to 11:00", ["Your marks, live, statement by statement", "Next to the marks of a second AI reader", "Your examples, and what comes next"])]
    w = (R - L - 2 * 24) / 3
    for i, (head, when, lines) in enumerate(cols):
        x = L + i * (w + 24)
        card(p, x, 122, x + w, 392)
        D.circle_number(p, x + 37, 162, i + 1, r=14, fill=ORANGE, size=15)
        text(p, x + 62, 169, [(head, "Bold")], 20, STRONG)
        text(p, x + w - 24, 168, [(when, "Bold")], 15, ORANGE_INK, align="right")
        y = 212
        for ln in lines:
            p.draw_circle((x + 30, y + 9), 3, color=None, fill=rgb(TEAL), width=0)
            y = para(p, x + 46, y, ln, 16.5, w - 46 - 26, color=BODY, leading=1.36) + 14
    bottom_line(p, "The question for today: does the AI read the data the way its paper did?", y=452)
    return p


def six_papers(out):
    p = D.blank_content(out, like=29, title="The data: six papers that used PaintOmics")
    cites = len(json.loads((D.ROOT / "analysis/literature/epmc_citing_paintomics.json").read_text()))
    tri = json.loads((D.ROOT / "analysis/literature/epmc_triage.json").read_text())
    used = sum(1 for r in tri if not r.get("note") and not any("review" in t.lower() for t in r.get("pubtype", []))
               and (set(r["where"]) & {"methods", "results"} or r.get("n_po_mentions", 0) >= 2))
    run = len(list((D.ROOT / "analysis" / "jobs").glob("*/ai_report.json")))
    n_st = [len(EVAL[d["id"]]["statements"]) for d in DATA]
    rows = [(cites, "papers cite PaintOmics"), (used, "open-access research papers use it in their methods or results"),
            (run, "had enough public data to run again this week"), (len(DATA), "with the full measured background: today's papers")]
    y = 122
    for i, (n, lab) in enumerate(rows):
        w = 640 - i * 62
        last = i == len(rows) - 1
        card(p, L, y, L + w, y + 96, fill="#e3f3f0" if last else CARD, stroke=TEAL if last else "#e4e4e4")
        text(p, L + 26, y + 61, [(str(n), "Bold")], 36, TEAL_DARK)
        para(p, L + 122, y + (38 if width(lab, 16.5) <= w - 148 else 27), lab, 16.5, w - 148, color=STRONG if last else BODY, face="SemiBold" if last else "Regular", leading=1.3)
        y += 96 + 14
    x = 760
    card(p, x, 122, R, 548)
    text(p, x + 28, 166, [("What we did with each paper", "Bold")], 19, STRONG)
    yy = 196
    for i, (h, s) in enumerate([("Took the paper's own tables", "the authors' fold changes and their significant features, from the supplement or the public repository"),
                                ("Ran PaintOmics AI on paintomics.org", "one finished job per paper, open to anyone with the link"),
                                ("Collected what it wrote", "%d to %d statements per paper, %d in all" % (min(n_st), max(n_st), sum(n_st)))]):
        yy = step(p, x + 28, yy, i + 1, h, s, R - x - 56, fill=TEAL) + 22
    bottom_line(p, "The AI was told the experiment, not the paper's conclusions.", y=620)
    return p


def four_marks(out):
    p = D.blank_content(out, like=29, title="How you mark: four marks")
    marks = [("Makes sense", "Consistent with the data and with what you know. You would accept it from a colleague. It may be well known."),
             ("Does not make sense", "Something in it is wrong or empty. One wrong part is enough."),
             ("Especially good", "Correct, and it adds something: a link the paper did not make, or a clearer mechanism."),
             ("Can't judge", "You cannot tell without more work. Better than a guess.")]
    w = (R - L - 3 * 22) / 4
    for i, (m, why) in enumerate(marks):
        x = L + i * (w + 22)
        card(p, x, 118, x + w, 372)
        mark_icon(p, m, x + 46, 168, 22)
        text(p, x + 24, 228, [(m, "Bold")], 19.5, STRONG)
        para(p, x + 24, 246, why, 15.5, w - 48, color=BODY, leading=1.38)
    card(p, L, 396, R, 590)
    text(p, L + 26, 436, [("What can be wrong", "Bold")], 18, STRONG)
    text(p, L + 26 + width([("What can be wrong", "Bold")], 18) + 14, 436, "things to check before you choose “does not make sense”", 15, MUTED)
    wrong = [("Data", "a value, a direction or a significance is not what the data shows"), ("Citation", "the cited paper does not say this, or is about something else"),
             ("Biology", "wrong as biology, against the consensus"), ("Design", "misreads the experiment: the contrast, the baseline, the time point"),
             ("Generic", "true, but says nothing about this experiment")]
    cw = (R - L - 52) / 5
    for i, (h, s) in enumerate(wrong):
        x = L + 26 + i * cw
        text(p, x, 480, [(h, "Bold")], 16.5, ORANGE_INK)
        para(p, x, 492, s, 14.5, cw - 22, color=BODY, leading=1.36)
    bottom_line(p, "Judge each statement against the paper and what you know. One mark per statement.", y=648)
    return p


def your_turn(out, pick_no):
    p = D.blank_content(out, like=29, title="Your turn")
    text(p, 1232, 65, [("until 10:47", "Bold")], 18, ORANGE_INK, align="right")
    card(p, L, 118, 452, 566)
    up = 6 if MATERIALS else 0                                     # the code and its lines move up to make room for one more line
    sheet_qr(p, L + 60, 160 - up, 260)
    text(p, L + 190, 470 - up, [("The marking sheet", "Bold")], 19, STRONG, align="center")
    text(p, L + 190, 496 - up, "one tab per paper, every statement on it", 15, MUTED, align="center")
    text(p, L + 190, 520 - up, "no account needed", 15, MUTED, align="center")
    if MATERIALS:                                                  # the address to type, for people who cannot scan
        text(p, L + 190, 544 - up, [("on a laptop: ", "Regular"), (D.bare(MATERIALS), "SemiBold", TEAL_DARK)], 15, MUTED, align="center")
    steps = [("Pick a paper", "six papers, A to F: slide %d" % pick_no),
             ("Open the marking sheet and go to your paper's tab", "every statement the AI wrote about that paper's data is listed there"),
             ("Take the first free Rater column", "your initials or a nickname go in its yellow cell"),
             ("Give each statement one mark", "from the list in your column: makes sense, does not make sense, especially good, can't judge")]
    y = 118
    for i, (h, s) in enumerate(steps):
        card(p, 482, y, R, y + 100)
        step(p, 506, y + 24, i + 1, h, s, R - 482 - 48)
        y += 100 + 16
    for i, s in enumerate(["The paper and the job page are linked on your tab", "Mark first, then look at your neighbours' columns", "Time up? Stop, rather than skip around"]):
        x = L + i * 440
        p.draw_circle((x + 6, 625), 4, color=None, fill=rgb(TEAL), width=0)
        text(p, x + 22, 630.5, s, 15.5, "#484848")
    return p


def pick_a_paper(out):
    p = D.blank_content(out, like=29, title="Pick a paper")
    text(p, 1232, 65, [("your letter is your tab in the marking sheet · the QR opens the job: the walk and the cited passages", "Regular")], 13.5, MUTED, align="right")
    V2.card_grid(p, DATA, top=100, bottom=740)
    text(p, L, 770, [("Every one of these papers cites PaintOmics and used it on this data.", "Bold", TEAL_DARK)], 15)
    text(p, R, 770, [("or the lab dataset, STATegra: ", "Regular", MUTED), ("paintomics.org/?jobID=jOT21M14SF", "SemiBold", STRONG)], 13.5, align="right")
    return p


def room_found(out):
    p = D.blank_content(out, like=29, title="What the room found")
    card(p, L, 132, 852, 612)
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
    text(p, 1128, 196, [("Live from the marking sheet", "Bold")], 18, WHITE, align="center")
    sheet_qr(p, 1128 - 115, 232, 230)
    text(p, 1128, 520, "Tab “Results”, hidden until now:", 16, WHITE, align="center")
    text(p, 1128, 545, [("View > Hidden sheets > Results", "SemiBold")], 16, WHITE, align="center")
    return p


def second_reader(out):
    p = D.blank_content(out, like=29, title="A second reader: an AI marks the AI")
    card(p, L, 118, 556, 600)
    y = 150
    n_all = sum(len(e["statements"]) for e in EVAL.values())
    for i, (h, s) in enumerate([("Claude Fable 5.2", "run at its extra-high effort setting, one pass per paper"),
                                ("The same %d statements" % n_all, "and the same four marks you used"),
                                ("With the evidence open", "the paper's full text, the uploaded values, every cited passage"),
                                ("One more reader", "an opinion to compare with yours, not an answer key")]):
        y = step(p, L + 28, y, i + 1, h, s, 556 - L - 56, fill=TEAL) + 24
    x0 = 586
    card(p, x0, 118, R, 600)
    text(p, x0 + 28, 160, [("What it marked, paper by paper", "Bold")], 18, STRONG)
    counts = {d["id"]: collections.Counter(s["mark"] for s in EVAL[d["id"]]["statements"]) for d in DATA}
    tot = sum(counts.values(), collections.Counter())
    lx = x0 + 28
    for m in ORDER:                                           # legend: always there, in the order of the segments
        if not tot[m]:
            continue
        box(p, (lx, 181, lx + 13, 194), fill=MARK[m], radius=3)
        lx = text(p, lx + 20, 193, m.lower(), 14, BODY) + 26
    bx, unit, bh = x0 + 262, (R - 60 - (x0 + 262)) / max(sum(c.values()) for c in counts.values()), 26
    for i, d in enumerate(DATA):
        y = 224 + i * 54
        D.circle_number(p, x0 + 40, y + bh / 2, d["letter"], r=12, fill=TEAL, size=13)
        text(p, x0 + 62, y + bh / 2 + 5.5, d["short"], 15.5, STRONG)
        x = bx
        for m in ORDER:
            k = counts[d["id"]][m]
            if not k:
                continue
            wseg = k * unit - 2
            box(p, (x, y, x + wseg, y + bh), fill=MARK[m], radius=4)
            text(p, x + wseg / 2, y + bh / 2 + 5, [(str(k), "Bold")], 14, STRONG if m == "Can't judge" else WHITE, align="center")
            x += k * unit
        text(p, x + 8, y + bh / 2 + 5, "%d" % sum(counts[d["id"]].values()), 14, MUTED)
    parts = ["%d %s" % (tot[m], {"Makes sense": "make sense", "Especially good": "especially good", "Does not make sense": "do not make sense", "Can't judge": "can't judge"}[m])
             for m in ("Makes sense", "Especially good", "Does not make sense") if tot[m]]
    text(p, x0 + 28, 572, [("Of %d statements: " % n_all, "Regular", MUTED), (" · ".join(parts), "Bold", STRONG)], 16)
    bottom_line(p, "Where do you and the second reader disagree? The Results tab shows both.", y=656)
    return p


FLAGS = [   # one example per kind of error, from analysis/ai_eval/*/fable_eval.json (wording shortened, facts as written there)
    ("Data", "balzano2021_teddy", 14, "A dip in APOC2 means less triglyceride clearance.",
     "The value belongs to APC2, another gene, matched to APOC2 through an old alias. APOC2 itself is not in the signature."),
    ("Design", "hernandez2017_c5ar1_microglia", 7, "Cx3cr1 is partially restored by the C5aR1 knockout.",
     "Read from knockout against wild type: mice without the transgene. The right contrast, Arctic/knockout against Arctic, shows nothing."),
    ("Citation", "jimenez2021_hbmec_lbp", 12, "Lbp alone is enough to trigger complement and NF-κB.",
     "The cited paper is about lactoferrin-binding proteins of other bacteria. Here Lbp is the pneumococcal laminin binding protein."),
    ("Biology", "jimenez2021_hbmec_lbp", 4, "GBP2 to CASP4 is the route to the IL1B seen with pneumococcus.",
     "Caspase-4 senses cytosolic LPS, which a Gram-positive bacterium does not have."),
]
STAR_EX = ("jimenez2021_hbmec_lbp", 14, "IL1B rises only with live pneumococcus, which fits inflammasome activation by its toxin pneumolysin: "
           "something the adhesin alone cannot supply. The paper leaves that contrast unexplained.")


def ai_flagged(out):
    p = D.blank_content(out, like=29, title="What the second reader flagged")
    by = {d["id"]: d for d in DATA}
    w, h = (R - L - 24) / 2, 168
    for i, (kind, ds, n, said, flag) in enumerate(FLAGS):
        ev = next(s for s in EVAL[ds]["statements"] if s["n"] == n)
        assert ev["mark"] == "Does not make sense" and kind[0] in ev["reasons"], (ds, n, ev["mark"], ev["reasons"])
        x, y = L + (i % 2) * (w + 24), 112 + (i // 2) * (h + 18)
        card(p, x, y, x + w, y + h)
        tw = width([(kind, "Bold")], 14.5) + 26
        box(p, (x + 24, y + 20, x + 24 + tw, y + 48), fill="#fde6dc", radius=13)
        text(p, x + 24 + tw / 2, y + 39.5, [(kind, "Bold")], 14.5, ORANGE_INK, align="center")
        text(p, x + w - 24, y + 39.5, "%s · %s · S%d" % (by[ds]["letter"], by[ds]["short"], n), 14, MUTED, align="right")
        mark_icon(p, "Does not make sense", x + 37, y + 79, 11)
        yy = para(p, x + 60, y + 66, "The AI wrote: " + said, 16, w - 84, face="SemiBold", color=STRONG, leading=1.34)
        para(p, x + 60, yy + 8, flag, 15.5, w - 84, color=BODY, leading=1.38)
    ds, n, why = STAR_EX
    ev = next(s for s in EVAL[ds]["statements"] if s["n"] == n)
    assert ev["mark"] == "Especially good", (ds, n, ev["mark"])
    y = 112 + 2 * (h + 18)
    card(p, L, y, R, y + 84, fill="#ece9fb", stroke="#d5cff6")
    mark_icon(p, "Especially good", L + 40, y + 42, 15)
    text(p, L + 70, y + 34, [("And one it marked especially good", "Bold", STRONG), ("   %s · %s · S%d" % (by[ds]["letter"], by[ds]["short"], n), "Regular", MUTED)], 15.5)
    para(p, L + 70, y + 44, why, 14.8, R - L - 96, color=BODY, leading=1.34)
    bottom_line(p, "Flags from one AI reader. Are they right? You and the authors decide.", y=618)
    return p


def backup_papers(out):
    p = D.blank_content(out, like=29, title="The six papers")
    cols = [("", 46), ("Paper", 190), ("What was measured", 330), ("How the paper used PaintOmics", 470), ("AI text on the job page", 200)]
    x = L
    xs = []
    for h, w in cols:
        xs.append(x); x += w + 12
    box(p, (L, 108, R, 140), fill=TEAL_DARK, radius=6)
    for (h, w), x in zip(cols, xs):
        text(p, x + 10, 130, [(h, "Bold")], 14, WHITE)
    y = 150
    for i, d in enumerate(DATA):
        hrow = 92
        if i % 2 == 0:
            box(p, (L, y - 4, R, y + hrow - 8), fill=CARD, radius=6)
        D.circle_number(p, xs[0] + 24, y + 22, d["letter"], r=13, fill=TEAL, size=14)
        text(p, xs[1] + 10, y + 22, [(d["short"], "Bold")], 15, STRONG)
        text(p, xs[1] + 10, y + 42, d.get("journal", ""), 13, MUTED)
        para(p, xs[2] + 10, y + 8, d["system"], 13, cols[2][1] - 12, color=BODY, leading=1.32, max_lines=3)
        para(p, xs[2] + 10, y + 62, d["omics"], 12.5, cols[2][1] - 12, face="SemiBold", color=TEAL_DARK, max_lines=1)
        para(p, xs[3] + 10, y + 8, d["used_paintomics"], 13, cols[3][1] - 12, color=BODY, leading=1.32, max_lines=4)
        held = d.get("held_back")
        para(p, xs[4] + 10, y + 8, "held back by the graph-artifact check; one click shows it" if held else "shown", 13, cols[4][1] - 12,
             face="SemiBold", color=ORANGE_INK if held else TEAL_DARK, leading=1.32)
        y += hrow
    text(p, L, 722, "Two more papers were run but are not in the practice, because their public data is incomplete: Khurana 2023 and Lopez-Ortiz 2022.", 13.5, MUTED)
    return p


# ---------------------------------------------------------------- assembly
def build():
    out = pymupdf.open()
    O = lambda n, fn=None: ("orig", n, fn)
    seq = [O(1, "title"), ("new", plan),
           O(2), O(3), O(4),
           O(5), O(6), O(7), O(8), O(9), O(10), O(11), O(12), O(13), O(14), O(15), O(16), O(17), O(18), O(19),
           O(20), O(21, can_cannot), O(22, who_judges), ("new", six_papers), ("new", four_marks),
           O(26), O(27, worked_example), ("new", "your_turn"), ("new", pick_a_paper), ("new", room_found), ("new", second_reader), ("new", ai_flagged),
           O(31, your_examples), O(25), O(32, thank_you),
           O(33), O(34), O(36), O(37), ("new", backup_papers)]
    pick_no = 1 + next(i for i, s in enumerate(seq) if s[1] is pick_a_paper)
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
        else:
            fn = s[1]
            page = your_turn(out, pick_no) if fn == "your_turn" else fn(out)
            D.renumber(page, i)
            log.append((i, "new: " + (fn if isinstance(fn, str) else fn.__name__)))
    out.set_metadata({"title": "AI models to interpret system biology models: PaintOmics AI, powered by TELLME (SEBiBC 2026), v3",
                      "author": "Tianyuan Liu, Ana Conesa"})
    out.save(OUT, garbage=3, deflate=True)
    return log


if __name__ == "__main__":
    log = build()
    print("wrote", OUT, len(log), "pages | marking sheet link:", SHEET or "NOT SET (placeholders drawn)")
    for i, what in log:
        if "new" in what or "edited" in what:
            print("  %2d  %s" % (i, what))
    if "--previews" in sys.argv:
        prev = SL / "work"; prev.mkdir(exist_ok=True)
        for i, what in log:
            if "new" in what or "edited" in what or "original 25" in what:
                D.preview(OUT, i, prev / ("v3_p%02d.png" % i))
