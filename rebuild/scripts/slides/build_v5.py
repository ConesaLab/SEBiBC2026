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
import collections
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

# The AI readers of the 69 statements, in the order they are drawn on slide 29. Fable 5.2 is V3.EVAL (fable_eval.json, 10 Nov, extra-high
# effort). On 12 Nov Sonnet 5.5 marked the same statements (default effort, one subagent per paper) with the same rubric, the same packets and
# the same paper texts, and without seeing the Fable marks: analysis/ai_eval/<paper>/sonnet_eval.json.
# Opus (opus_eval.json, 12 Nov, default effort, one subagent per paper, saw neither the Fable nor the Sonnet marks) was Opus 5.5 on papers A, D, E and F.
# On B and C a safety classifier stopped the Opus 5.5 reader while it read the paper and Claude Code switched it to Opus 5 before any statement was
# marked, so those two files carry "model": "claude-opus-5" and the slides label those rows "Opus 5" (see ROW_LABEL and the footnote).
# On 12 Nov Gemini 4 Hydrogen (gemini_hydrogen_eval.json, extra-high effort, one subagent per paper), Gemini 4 Argon
# (gemini_argon_eval.json, default effort, four blind shards across the six papers) and Gemini 4 Carbon
# (gemini_carbon_eval.json, high effort, six blind shards plus an independent blind verifier) also marked all 69 statements independently.
# To add another reader, load its files the same way and append it here.
def _marks(name):
    return {d["id"]: json.loads((D.ROOT / "analysis" / "ai_eval" / d["id"] / name).read_text()) for d in V3.DATA}


EVAL_SONNET, EVAL_OPUS = _marks("sonnet_eval.json"), _marks("opus_eval.json")
EVAL_GEMINI, EVAL_ARGON = _marks("gemini_hydrogen_eval.json"), _marks("gemini_argon_eval.json")
EVAL_CARBON = _marks("gemini_carbon_eval.json")
READERS = [
    ("Fable 5.2", V3.EVAL),
    ("Sonnet 5.5", EVAL_SONNET),
    ("Opus", EVAL_OPUS),
    ("Gemini 4 Hydrogen", EVAL_GEMINI),
    ("Gemini 4 Argon", EVAL_ARGON),
    ("Gemini 4 Carbon", EVAL_CARBON),
]
EFFORT = {
    "Fable 5.2": "extra-high",
    "Sonnet 5.5": "default",
    "Opus": "default",
    "Gemini 4 Hydrogen": "extra-high",
    "Gemini 4 Argon": "default",
    "Gemini 4 Carbon": "high",
}
NUMWORD = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def row_label(name, ev, pid):
    """The short name drawn beside a bar: 'Opus 5' where the file says the reader was switched to Opus 5,
    'Hydrogen'/'Argon'/'Carbon' when multiple Gemini readers are shown, else the first word of the reader's name."""
    if ev[pid].get("model") == "claude-opus-5":
        return "Opus 5"
    if name.startswith("Gemini ") and sum(r.startswith("Gemini ") for r, _ in READERS) > 1:
        return name.split()[-1]
    return name.split()[0]


def reader_note():
    """One footnote line for slides 29 and 30 when Opus ran as two versions; empty otherwise."""
    five = [d["letter"] for d in V3.DATA if EVAL_OPUS[d["id"]].get("model") == "claude-opus-5"]
    if not five or not any(r == "Opus" for r, _ in READERS):
        return ""
    rest = [d["letter"] for d in V3.DATA if d["letter"] not in five]
    j = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
    return "Opus: 5.5 on %s; Opus 5 on %s (the system switched it after a safety-classifier stop, before it marked anything)" % (j(rest), j(five))


def plan(out):
    p = D.blank_content(out, like=29, title="The hour")
    cols = [("Why, and how it works", "10:00–10:30", ["One table, many stories: why reading a pathway analysis is the hard part", "PaintOmics: every omic painted on its pathways",
                                                      "TELLME: agents that walk the pathways and write; what it can and cannot do"]),
            ("Your turn", "10:30–10:47", ["Pick one of six published papers", "Read what the AI wrote about that paper's data", "Give every statement one of four marks"]),
            ("What the room found", "10:47–11:00", ["Your marks, live, statement by statement", "Next to the marks of %s AI readers" % NUMWORD[len(READERS)], "Your examples"])]
    w = (R - L - 2 * 24) / 3
    for i, (head, when, lines) in enumerate(cols):
        x = L + i * (w + 24)
        V3.card(p, x, 122, x + w, 392)
        D.circle_number(p, x + 37, 162, i + 1, r=14, fill=ORANGE, size=15)
        text(p, x + 60, 168.5, [(head, "Bold")], 19, STRONG)
        text(p, x + w - 22, 168, [(when, "Bold")], 14.5, ORANGE_INK, align="right")
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
    wipe(p, (1120, 215, 1358, 425), WHITE)
    V3.link_qr(p, V3.MATERIALS, "materials.png", 1163.5, 229, 142)
    gh = D.bare(V3.MATERIALS)                                       # the label is the address itself, like "paintomics.org" beside it
    text(p, 1234.5, 413.3, [(gh, "Bold")], min(15.2, 15.2 * 244 / width([(gh, "Bold")], 15.2)), STRONG, align="center")
    p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(1110, 222, 1358, 422), "uri": V3.MATERIALS})
    p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(928, 222, 1084, 422), "uri": "https://paintomics.org"})
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
    text(p, 1222, 65, [("10:30–10:47", "Bold")], 18, ORANGE_INK, align="right")
    V3.card(p, L, 118, 452, 566)
    cx = (L + 452) / 2
    text(p, cx, 164, [("One form per paper", "Bold")], 23, TEAL_DARK, align="center")
    text(p, cx, 192, "the QR code on the paper's card · no account", 14.5, MUTED, align="center")
    y = 240
    for d in V3.DATA:
        D.circle_number(p, L + 44, y - 5.5, d["letter"], r=13, fill=TEAL, size=14)
        text(p, L + 68, y, d["short"], 16.5, STRONG)
        text(p, 452 - 26, y, "%d statements" % FORMS[d["letter"]]["statements"], 14, MUTED, align="right")
        y += 44
    if V3.MATERIALS:
        text(p, cx, 546, [("slides: ", "Regular"), (D.bare(V3.MATERIALS), "SemiBold", TEAL_DARK)], 14, MUTED, align="center")
    steps = [("Pick a paper", "six papers, A to F: slide %d" % pick_no),
             ("Open its job page and read what the AI wrote", "its address is on the paper's card; AI Interpret is top right, with the evidence behind each statement"),
             ("Open the paper's form", "the QR code on its card, or its short link; every statement the AI wrote is there in full"),
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
    """Six cards, one per paper. The job on paintomics.org is given as its address, to click or type (no QR code:
    it is read on a laptop); the one QR code on a card is the paper's marking form."""
    p = D.blank_content(out, like=29, title="Pick a paper")
    text(p, 1232, 65, [("the job link opens what the AI wrote, with its evidence · ", "Regular", MUTED), ("the QR code is the form where you mark", "Bold", ORANGE_INK)], 13.5, align="right")
    top, bottom, cols, gx, gy = 100, 740, 3, 22, 18
    cw, ch = (R - L - gx * (cols - 1)) / cols, (bottom - top - gy) / 2
    q = 132
    for i, d in enumerate(V3.DATA):
        r, c = divmod(i, cols)
        x0, y0 = L + c * (cw + gx), top + r * (ch + gy)
        V3.card(p, x0, y0, x0 + cw, y0 + ch)
        form = FORMS[d["letter"]]["short"]
        qx, qy = x0 + cw - q - 20, y0 + 20                          # the form's QR code, with its caption and short link under it
        box(p, (qx - 7, qy - 7, qx + q + 7, qy + q + 7), fill=WHITE, radius=6)
        p.insert_image(pymupdf.Rect(qx, qy, qx + q, qy + q), filename=str(D.qr_png(form, V3.QR / ("form_%s.png" % d["letter"]))))
        text(p, qx + q / 2, qy + q + 27, [("Mark it here", "Bold")], 14.5, ORANGE_INK, align="center")
        lk = short(d["letter"])
        ls = min(11.5, 11.5 * (q + 14) / width([(lk, "Mono")], 11.5))
        text(p, qx + q / 2, qy + q + 45, [(lk, "Mono")], ls, STRONG, align="center")
        p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(qx - 7, qy - 7, qx + q + 7, qy + q + 50), "uri": form})
        tx = x0 + 22
        tw = qx - 7 - 14 - tx
        D.circle_number(p, tx + 12, y0 + 33, d["letter"], r=13, fill=TEAL, size=14)
        hs = min(18.5, 18.5 * (tw - 34) / width([(d["short"], "Bold")], 18.5))
        hx = text(p, tx + 34, y0 + 39.5, [(d["short"], "Bold")], hs, STRONG)
        if d.get("journal") and hx + 8 + width(d["journal"], 13) <= tx + tw:
            text(p, hx + 8, y0 + 39.5, d["journal"], 13, MUTED)
        y = para(p, tx, y0 + 60, d["topic"], 16.5, tw, color=STRONG, leading=1.3, max_lines=4)
        para(p, tx, y + 9, d["tag"], 14, tw, face="SemiBold", color=TEAL_DARK, leading=1.32, max_lines=3)
        jy = y0 + ch - 76                                           # the job: its address in full, clickable in the PDF
        p.draw_line((tx, jy - 22), (x0 + cw - 22, jy - 22), color=rgb("#dcdcdc"), width=1)
        text(p, tx, jy, [("Read what the AI wrote:", "Bold")], 13.5, TEAL_DARK)
        url = D.bare(d["url"])
        us = min(17, 17 * (cw - 44) / width([(url, "Mono")], 17))
        text(p, tx, jy + 25, [(url, "Mono")], us, STRONG)
        p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(tx, jy + 8, tx + width([(url, "Mono")], us), jy + 31), "uri": d["url"]})
        if d.get("held_back"):
            text(p, tx, y0 + ch - 17, [("held back on the page: click “Show the interpretation anyway”", "SemiBold")], 11.5, ORANGE_INK)
        else:
            text(p, tx, y0 + ch - 17, "the paper: doi.org/" + d["doi"], 11.5, MUTED)
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


MARK_WORDS = {"Makes sense": "make sense", "Especially good": "especially good", "Does not make sense": "do not make sense", "Can't judge": "can't judge"}


def _step(p, x, y, n, head, sub, w, fill=TEAL, head_size=19, sub_size=15.5):
    lines = []
    for part in head.split("\n"):
        lines.extend(D.wrap(part, "Bold", head_size, w - 38))
    if len(lines) == 1:
        return V3.step(p, x, y, n, lines[0], sub, w, fill=fill, head_size=head_size, sub_size=sub_size)
    D.circle_number(p, x + 13, y + 13, n, r=13, fill=fill, size=14)
    for idx, ln in enumerate(lines):
        text(p, x + 38, y + 20 + idx * 1.26 * head_size, [(ln, "Bold")], head_size, STRONG)
    sub_top = y + 32 + (len(lines) - 1) * 1.26 * head_size
    return para(p, x + 38, sub_top, sub, sub_size, w - 38, color=D.MUTED, leading=1.36) if sub else sub_top


def second_reader(out):
    """Slide 29: what each AI reader marked across all 69 statements, and how often they give the same mark.
    (V3.second_reader showed Fable 5.2 alone; five more independent readers were added on 12 Nov.)"""
    k = len(READERS)
    names = [r for r, _ in READERS]
    short_name = lambda r: r.split()[-1] if r.startswith("Gemini ") and sum(x.startswith("Gemini ") for x in names) > 1 else r.split()[0]
    join_names = lambda xs: (", ".join(xs[:-1]) + " and " + xs[-1]) if len(xs) > 1 else xs[0]
    n_all = sum(len(e["statements"]) for e in V3.EVAL.values())
    p = D.blank_content(out, like=29, title="%s AI readers mark the AI" % NUMWORD[k].capitalize())

    # Left card: four concise steps
    x_left_end = 546
    V3.card(p, L, 118, x_left_end, 600)
    by_effort = collections.OrderedDict()
    for r in names:
        by_effort.setdefault(EFFORT.get(r, "default"), []).append(short_name(r))
    effort_parts = ["%s at %s%s" % (join_names(v), e, " effort" if idx == 0 else "")
                    for idx, (e, v) in enumerate(by_effort.items())]
    steps = [
        ("%s models, one pass per paper" % NUMWORD[k].capitalize(), "; ".join(effort_parts)),
        ("The same %d statements" % n_all, "and the same four marks you used"),
        ("With the evidence open", "the paper's full text, the uploaded values, every cited passage"),
        ("Marked independently", "no reader saw another's marks: %s opinions to compare with yours, not an answer key" % NUMWORD[k]),
    ]
    y = 158
    for i, (h, s) in enumerate(steps):
        y = _step(p, L + 28, y, i + 1, h, s, x_left_end - L - 56, fill=TEAL) + 32

    # Right card: one stacked bar per AI reader across all statements
    x0 = 574
    V3.card(p, x0, 118, R, 600)
    text(p, x0 + 28, 160, [("What each reader marked", "Bold")], 18.5, STRONG)
    text(p, R - 28, 160, "%d statements across %d papers" % (n_all, len(V3.DATA)), 14, D.MUTED, align="right")
    tot = {r: collections.Counter(s["mark"] for d in V3.DATA for s in ev[d["id"]]["statements"]) for r, ev in READERS}
    seen = sum(tot.values(), collections.Counter())
    lx = x0 + 28
    for m in V3.ORDER:
        if not seen[m]:
            continue
        D.box(p, (lx, 181, lx + 13, 194), fill=V3.MARK[m], radius=3)
        lx = text(p, lx + 20, 193, m.lower(), 14, BODY) + 26

    lab_w = max(width([(r, "SemiBold")], 15) for r in names)
    bx0, bx1 = x0 + 28 + lab_w + 18, R - 28
    bar_w = bx1 - bx0
    bh = 28
    row_step = min(52, (532 - 222) / max(1, k))
    for j, (r, _) in enumerate(READERS):
        yy = 222 + j * row_step
        cy = yy + bh / 2
        text(p, bx0 - 14, cy + 5.5, [(r, "SemiBold")], 15, STRONG, align="right")
        segs = [(m, tot[r][m]) for m in V3.ORDER if tot[r][m]]
        min_slot = 20.0
        small = [(m, c) for m, c in segs if c / n_all * bar_w < min_slot]
        rem_w = bar_w - min_slot * len(small)
        rem_n = sum(c for m, c in segs if (m, c) not in small)
        x = bx0
        for m, c in segs:
            slot = min_slot if (m, c) in small else (c / rem_n * rem_w)
            wseg = slot - 2.5
            D.box(p, (x, yy, x + wseg, yy + bh), fill=V3.MARK[m], radius=4)
            nsz = 12.5 if wseg < 22 else 13.5
            text(p, x + wseg / 2, cy + 0.36 * nsz, [(str(c), "Bold")], nsz, STRONG if m == "Can't judge" else WHITE, align="center")
            x += slot

    marks = [{(d["id"], s["n"]): s["mark"] for d in V3.DATA for s in ev[d["id"]]["statements"]} for _, ev in READERS]
    same_all = sum(len({m[key] for m in marks}) == 1 for key in marks[0])
    p.draw_line((x0 + 28, 542), (R - 28, 542), color=rgb("#e0e0e0"), width=1)
    who = "Both readers" if k == 2 else "All %s readers" % NUMWORD[k]
    text(p, x0 + 28, 574, [("%s give the same mark to " % who, "Regular", BODY),
                           ("%d of %d statements" % (same_all, n_all), "Bold", STRONG)], 15.5)

    bottom_y = 644
    V3.bottom_line(p, "Where do you disagree with the AI readers, and where do they disagree with each other?", y=bottom_y)
    if reader_note():
        text(p, L, bottom_y + 28, reader_note(), 13.5, D.MUTED)
    return p


def ai_flagged(out):
    """Slide 30: the four errors flagged by Fable 5.2 (V3.FLAGS) with how many AI readers agree on each."""
    p = D.blank_content(out, like=29, title="What the AI readers flagged")
    by = {d["id"]: d for d in V3.DATA}
    reason = {"Data": "D", "Design": "X", "Citation": "C", "Biology": "B"}      # the letters of the rubric
    get = lambda ev, ds, n: next(s for s in ev[ds]["statements"] if s["n"] == n)
    w, h = (R - L - 24) / 2, 168
    for i, (kind, ds, n, said, flag) in enumerate(V3.FLAGS):
        fl = get(V3.EVAL, ds, n)                                                 # the card is Fable's flag ...
        assert fl["mark"] == "Does not make sense" and reason[kind] in fl["reasons"], (ds, n, fl["mark"], fl["reasons"])
        agree = sum(get(ev, ds, n)["mark"] == "Does not make sense" and reason[kind] in get(ev, ds, n)["reasons"] for _, ev in READERS)   # ... and who else marked it so
        tag = (("both agree" if len(READERS) == 2 else "all %s agree" % NUMWORD[len(READERS)]) if agree == len(READERS)
               else "%d of %d readers agree" % (agree, len(READERS)))
        x, y = L + (i % 2) * (w + 24), 112 + (i // 2) * (h + 18)
        V3.card(p, x, y, x + w, y + h)
        tw = D.width([(kind, "Bold")], 14.5) + 26
        D.box(p, (x + 24, y + 20, x + 24 + tw, y + 48), fill="#fde6dc", radius=13)
        text(p, x + 24 + tw / 2, y + 39.5, [(kind, "Bold")], 14.5, ORANGE_INK, align="center")
        text(p, x + 24 + tw + 14, y + 39.5, tag, 13.5, D.MUTED)
        text(p, x + w - 24, y + 39.5, "%s · %s · S%d" % (by[ds]["letter"], by[ds]["short"], n), 14, D.MUTED, align="right")
        V3.mark_icon(p, "Does not make sense", x + 37, y + 79, 11)
        yy = para(p, x + 60, y + 66, "The AI wrote: " + said, 16, w - 84, face="SemiBold", color=STRONG, leading=1.34)
        para(p, x + 60, yy + 8, flag, 15.5, w - 84, color=BODY, leading=1.38)
    ds, n, why = V3.STAR_EX
    assert get(V3.EVAL, ds, n)["mark"] == "Especially good", (ds, n)
    lab = lambda r, ev: "Opus 5" if ev[ds].get("model") == "claude-opus-5" else r    # "Opus 5" where that reader was switched to Opus 5
    others = " · ".join("%s: %s" % (lab(r, ev), get(ev, ds, n)["mark"].lower()) for r, ev in READERS[1:])
    y = 112 + 2 * (h + 18)
    left_head = [("And one Fable 5.2 marked especially good", "Bold", STRONG), ("   %s · %s · S%d" % (by[ds]["letter"], by[ds]["short"], n), "Regular", D.MUTED)]
    lw = D.width([(t, f) for t, f, _ in left_head], 15.5)
    ow = D.width(others, 14)
    if len(READERS) <= 3 and L + 70 + lw + 24 <= R - 26 - ow:
        V3.card(p, L, y, R, y + 84, fill="#ece9fb", stroke="#d5cff6")
        V3.mark_icon(p, "Especially good", L + 40, y + 42, 15)
        text(p, L + 70, y + 34, left_head, 15.5)
        text(p, R - 26, y + 34, others, 14, D.MUTED, align="right")
        para(p, L + 70, y + 44, why, 14.8, R - L - 96, color=BODY, leading=1.34)
        bottom_y = 618
    else:
        V3.card(p, L, y, R, y + 114, fill="#ece9fb", stroke="#d5cff6")
        V3.mark_icon(p, "Especially good", L + 40, y + 57, 15)
        text(p, L + 70, y + 32, left_head, 15.5)
        yy = para(p, L + 70, y + 42, why, 14.8, R - L - 96, color=BODY, leading=1.34)
        text(p, L + 70, yy + 17, others, 14, D.MUTED)
        bottom_y = 644
    V3.bottom_line(p, "Flags from %s AI readers. Are they right? You and the authors decide." % NUMWORD[len(READERS)], y=bottom_y)
    if reader_note():
        text(p, L, bottom_y + 28, reader_note(), 13.5, D.MUTED)
    return p


def reader_agreement(out):
    """Slide after the readers' marks: which AI readers think alike (pairwise kappa, closeness to the group, extra flags).
    Drawn by build_agreement.py from READERS, so it follows whichever readers are listed above."""
    import build_agreement as AG
    return AG.slide(out, READERS, V3.DATA)


def thank_you(out):
    """Thank you slide with aligned three-column grid (left cards + two symmetric QR cards)."""
    p = D.from_original(out, 32)
    wipe(p, (64, 130, 1380, 548), WHITE)
    top, bot, gap = 152, 502, 24
    xl1 = 732
    h_half = (bot - top - gap) / 2

    # Top-left card: acknowledgement + contact email
    V3.card(p, L, top, xl1, top + h_half)
    text(p, L + 28, top + 54, "We thank ELIXIR for supporting TELLME.", 19.5, STRONG)
    p.draw_line((L + 28, top + 82), (xl1 - 28, top + 82), color=rgb("#dcdcdc"), width=1)
    ex, ey = L + 28, top + 107
    p.draw_rect(pymupdf.Rect(ex, ey, ex + 22, ey + 15), color=rgb(TEAL_DARK), width=1.6)
    p.draw_polyline([(ex + 1, ey + 1), (ex + 11, ey + 9), (ex + 21, ey + 1)], color=rgb(TEAL_DARK), width=1.5)
    text(p, ex + 32, ey + 13.5, [("paintomicsai@gmail.com", "Bold")], 18, TEAL_DARK)
    p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(ex, ey - 4, ex + 310, ey + 20), "uri": "mailto:paintomicsai@gmail.com"})

    # Bottom-left card: PaintOmics web & open-source repository
    y2 = top + h_half + gap
    V3.card(p, L, y2, xl1, bot)
    text(p, L + 28, y2 + 48, [("Try PaintOmics AI on your own data", "Bold")], 18, STRONG)
    p.draw_line((L + 28, y2 + 72), (xl1 - 28, y2 + 72), color=rgb("#dcdcdc"), width=1)
    tx = text(p, L + 28, y2 + 106, [("Web:  ", "Regular", MUTED), ("paintomics.org", "Bold", TEAL_DARK)], 16)
    p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(L + 28, y2 + 88, tx, y2 + 112), "uri": "https://paintomics.org"})
    tx2 = text(p, L + 28, y2 + 134, [("Code:  ", "Regular", MUTED), ("github.com/ConesaLab/PaintOmics", "SemiBold", STRONG)], 15.5)
    p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(L + 28, y2 + 116, tx2, y2 + 140), "uri": "https://github.com/ConesaLab/PaintOmics"})

    # Two symmetric QR cards on the right
    pablo_url = "https://forms.gle/bUjZus6hCuVP7pDR7"
    qr_cards = [
        (xl1 + gap, xl1 + gap + 294, "All AI sessions: before you leave", pablo_url, "pablo_form.png", D.bare(pablo_url)),
    ]
    if V3.MATERIALS:
        qr_cards.append((xl1 + gap + 294 + gap, R, "Slides and materials", V3.MATERIALS, "materials.png", D.bare(V3.MATERIALS)))
    qsz = 204
    for cx0, cx1, head, url, png_name, label in qr_cards:
        V3.card(p, cx0, top, cx1, bot)
        mid = (cx0 + cx1) / 2
        text(p, mid, top + 38, [(head, "Bold")], 15, TEAL_DARK, align="center")
        V3.link_qr(p, url, png_name, mid - qsz / 2, top + 62, qsz)
        lsz = min(13.5, 13.5 * (cx1 - cx0 - 28) / width([(label, "Bold")], 13.5))
        text(p, mid, bot - 26, [(label, "Bold")], lsz, STRONG, align="center")
        p.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(cx0 + 12, top + 50, cx1 - 12, bot - 14), "uri": url})
    return p


def build():
    import build_clarity as CL
    out = pymupdf.open()
    O = lambda n, fn=None: ("orig", n, fn)
    P = lambda n: ("problem", n)                                    # slide n of the 11 Nov deck (docs/..._2026-11-11.pdf)
    seq = [O(1, "title"), ("new", plan),
           O(2), O(3), P(4), P(5), P(6),
           O(5), O(6), O(7), O(8), O(9), O(10), O(11), O(12), O(13, CL.where_it_runs), O(14), O(15, CL.picking_the_seeds), O(16), O(17), O(18), O(19),
           O(21, can_cannot),
           O(26, V4.practice_divider), ("new", V3.four_marks), ("new", "your_turn"), ("new", pick_a_paper),
           ("new", room_found), ("new", second_reader), ("new", reader_agreement), ("new", ai_flagged), O(31, V3.your_examples),
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
