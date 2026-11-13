#!/usr/bin/env python
"""Clear vector redraws of Slide 16 ('Where it runs') and Slide 18 ('Picking the seeds') for v5."""
import math
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                    # noqa: E402
from deck import (BODY, CARD, MUTED, ORANGE, ORANGE_INK, STRONG, TEAL, TEAL_DARK, WHITE,
                  box, circle_number, para, rgb, text, width)       # noqa: E402
import build_v3 as V3                                               # noqa: E402

L, R = V3.L, V3.R


def _arrow_h(p, x0, x1, y, col=TEAL, lw=2.2, head=7):
    p.draw_line((x0, y), (x1, y), color=rgb(col), width=lw)
    s = 1 if x1 >= x0 else -1
    p.draw_polyline([(x1 - s * head, y - 0.62 * head), (x1, y), (x1 - s * head, y + 0.62 * head)],
                    color=rgb(col), width=lw, lineCap=1, lineJoin=1)


def _arrow_v(p, x, y0, y1, col=TEAL, lw=2.2, head=7):
    p.draw_line((x, y0), (x, y1), color=rgb(col), width=lw)
    s = 1 if y1 >= y0 else -1
    p.draw_polyline([(x - 0.62 * head, y1 - s * head), (x, y1), (x + 0.62 * head, y1 - s * head)],
                    color=rgb(col), width=lw, lineCap=1, lineJoin=1)


def _pill(p, x, y, label, fill, ink, sz=12.5, face="Mono", pad_x=10, h=24):
    w = width([(label, face)], sz) + 2 * pad_x
    box(p, (x, y, x + w, y + h), fill=fill, radius=6)
    text(p, x + w / 2, y + h / 2 + 0.36 * sz, [(label, face)], sz, ink, align="center")
    return w


def _bullet(p, x, y, lead, rest, maxw, sz=14, col_lead=STRONG, col_rest=BODY, dot_col=TEAL):
    p.draw_circle((x + 4, y + 0.52 * sz), 3, color=None, fill=rgb(dot_col), width=0)
    # Wrap combined text using Regular metrics, then draw bold prefix on line 1
    full = (lead + " " + rest).strip() if lead else rest
    lines = D.wrap(full, "Regular", sz, maxw - 16)
    yy = y + D.ASC * sz
    rem_lead = len(lead)
    for ln in lines:
        if rem_lead > 0:
            part_b = ln[:rem_lead]
            part_r = ln[rem_lead:]
            runs = []
            if part_b:
                runs.append((part_b, "Bold", col_lead))
            if part_r:
                runs.append((part_r, "Regular", col_rest))
            text(p, x + 16, yy, runs, sz)
            rem_lead = max(0, rem_lead - len(ln) - 1)
        else:
            text(p, x + 16, yy, [(ln, "Regular", col_rest)], sz)
        yy += 1.36 * sz
    return yy - D.ASC * sz


def where_it_runs(out):
    """Slide 16: clean 4-stage top architecture pipeline + aligned Literature & Privacy bottom cards."""
    p = D.blank_content(out, like=29, title="Where it runs")
    text(p, 1222, 65, "all server & LLM calls stay inside CSIC infrastructure in Spain", 13.5, MUTED, align="right")

    top1, bot1 = 112, 378
    cy = (top1 + bot1) / 2
    gap_arr = 32

    # 4 top boxes: Browser | PaintOmics Server | LLM Gateway | Pinned Model
    x_b0, x_b1 = L, L + 172
    x_s0, x_s1 = x_b1 + gap_arr, 696
    x_g0, x_g1 = x_s1 + gap_arr, 1020
    x_m0, x_m1 = x_g1 + gap_arr, R

    # 1. Your browser
    box(p, (x_b0, top1, x_b1, bot1), fill=WHITE, stroke="#cfcfcf", radius=12, lw=1.4)
    mx = (x_b0 + x_b1) / 2
    # Clean laptop icon
    p.draw_rect(pymupdf.Rect(mx - 22, top1 + 48, mx + 22, top1 + 78), color=rgb(TEAL_DARK), width=2, radius=0.1)
    p.draw_line((mx - 30, top1 + 83), (mx + 30, top1 + 83), color=rgb(TEAL_DARK), width=2.4)
    text(p, mx, top1 + 114, [("Your browser", "Bold")], 17.5, STRONG, align="center")
    _pill(p, mx - width([("paintomics.org", "Mono")], 12) / 2 - 10, top1 + 128, "paintomics.org", "#e8f4f2", TEAL_DARK, sz=12)
    for k, ln in enumerate(("Upload data or", "open a job link;", "view pathways &", "AI interpretation")):
        text(p, mx, top1 + 176 + k * 19, ln, 13.5, MUTED, align="center")

    _arrow_h(p, x_b1 + 5, x_s0 - 5, cy, col="#777777")

    # 2. PaintOmics server (Drago, CSIC)
    V3.card(p, x_s0, top1, x_s1, bot1)
    circle_number(p, x_s0 + 30, top1 + 32, 1, r=12, fill=TEAL, size=13)
    text(p, x_s0 + 50, top1 + 37, [("PaintOmics server", "Bold")], 18, STRONG)
    text(p, x_s0 + 50, top1 + 57, "Supercomputador Drago (CSIC)", 13.5, MUTED)

    sq0, sq1 = x_s0 + 18, x_s0 + 188
    sa0, sa1 = sq1 + 26, x_s1 - 18
    sy0, sy1 = top1 + 76, bot1 - 18
    box(p, (sq0, sy0, sq1, sy1), fill=WHITE, stroke="#d4d4d4", radius=10, lw=1.2)
    text(p, sq0 + 16, sy0 + 32, [("Job queue", "Bold")], 16, STRONG)
    para(p, sq0 + 16, sy0 + 46, "Walk runs on the server alongside pathway analysis", 13.5, sq1 - sq0 - 32, color=BODY, leading=1.36)

    _arrow_h(p, sq1 + 4, sa0 - 4, (sy0 + sy1) / 2, col="#777777", lw=1.8, head=5.5)

    box(p, (sa0, sy0, sa1, sy1), fill=WHITE, stroke=TEAL, radius=10, lw=1.6)
    text(p, sa0 + 16, sy0 + 32, [("AI agents", "Bold")], 16, TEAL_DARK)
    para(p, sa0 + 16, sy0 + 46, "Walk the graph, fetch papers, write & check (next slide)", 13.5, sa1 - sa0 - 32, color=BODY, leading=1.36)

    _arrow_h(p, x_s1 + 5, x_g0 - 5, cy, col=TEAL)

    # 3. LLM gateway (llm.iiia.es)
    box(p, (x_g0, top1, x_g1, bot1), fill=WHITE, stroke=TEAL, radius=12, lw=1.6)
    circle_number(p, x_g0 + 30, top1 + 32, 2, r=12, fill=TEAL, size=13)
    text(p, x_g0 + 50, top1 + 37, [("CSIC LLM gateway", "Bold")], 17.5, STRONG)
    _pill(p, x_g0 + 20, top1 + 52, "llm.iiia.es", "#e8f4f2", TEAL_DARK, sz=12.5)
    yg = top1 + 92
    for lead, rest in (("IIIA-CSIC:", "AI Research Institute of CSIC (hardware in Spain)"),
                       ("Interface:", "OpenAI-compatible API"),
                       ("Shared pace:", "54 req/min across callers (60/min key limit)")):
        yg = _bullet(p, x_g0 + 20, yg, lead, rest, x_g1 - x_g0 - 38, sz=13.5) + 9

    _arrow_h(p, x_g1 + 5, x_m0 - 5, cy, col=TEAL)

    # 4. Pinned Model
    box(p, (x_m0, top1, x_m1, bot1), fill=WHITE, stroke=TEAL, radius=12, lw=1.6)
    circle_number(p, x_m0 + 30, top1 + 32, 3, r=12, fill=TEAL, size=13)
    text(p, x_m0 + 50, top1 + 37, [("Pinned model", "Bold")], 17.5, STRONG)
    _pill(p, x_m0 + 20, top1 + 52, "DeepSeek-V4-Flash-0731", "#e8f4f2", TEAL_DARK, sz=12.5)
    ym = top1 + 92
    for lead, rest in (("Reproducible:", "pinned, dated model snapshot"),
                       ("Fallback:", "gateway alias default/llm only if pinned snapshot is offline"),
                       ("Auditable:", "every result records the exact model that answered")):
        ym = _bullet(p, x_m0 + 20, ym, lead, rest, x_m1 - x_m0 - 38, sz=13.5) + 9

    # Vertical arrow from AI agents down to Literature card
    ax_mid = (sa0 + sa1) / 2
    top2, bot2 = 418, 616
    _arrow_v(p, ax_mid, bot1 + 4, top2 - 5, col=TEAL)

    # Bottom-left card: Literature lookup (aligned L..x_s1)
    V3.card(p, L, top2, x_s1, bot2)
    text(p, L + 24, top2 + 36, [("Literature lookup", "Bold")], 18, STRONG)
    text(p, x_s1 - 24, top2 + 36, "queried by the paper & walker agents", 13.5, MUTED, align="right")
    lx0, lx1 = L + 20, L + 252
    rx0, rx1 = lx1 + 16, x_s1 - 20
    box(p, (lx0, top2 + 54, lx1, bot2 - 18), fill=WHITE, stroke="#dcdcdc", radius=8, lw=1)
    text(p, lx0 + 16, top2 + 84, [("NCBI PubMed", "Bold")], 15.5, STRONG)
    para(p, lx0 + 16, top2 + 96, "Search in best-match order for candidate papers", 13.5, lx1 - lx0 - 32, color=BODY, leading=1.36)

    box(p, (rx0, top2 + 54, rx1, bot2 - 18), fill=WHITE, stroke="#dcdcdc", radius=8, lw=1)
    text(p, rx0 + 16, top2 + 84, [("Europe PMC / PubMed Central", "Bold")], 15.5, STRONG)
    para(p, rx0 + 16, top2 + 96, "Full text (Introduction, Results, Discussion) when open-access; otherwise the abstract",
         13.5, rx1 - rx0 - 32, color=BODY, leading=1.36)

    # Bottom-right card: Data & privacy (aligned x_g0..R)
    V3.card(p, x_g0, top2, R, bot2)
    text(p, x_g0 + 24, top2 + 36, [("What leaves the PaintOmics server", "Bold")], 18, STRONG)
    text(p, R - 24, top2 + 36, "sent only to llm.iiia.es", 13.5, MUTED, align="right")

    box(p, (x_g0 + 20, top2 + 54, R - 20, top2 + 124), fill=WHITE, stroke="#dcdcdc", radius=8, lw=1)
    pw1 = _pill(p, x_g0 + 32, top2 + 66, "Sent", "#e3f3f0", TEAL_DARK, sz=12.5, face="Bold", pad_x=12, h=24)
    para(p, x_g0 + 32 + pw1 + 12, top2 + 64,
         "Feature names, values & column labels of the nodes walked or shown, and the experiment description",
         13.5, R - 34 - (x_g0 + 32 + pw1 + 12), color=BODY, leading=1.34)

    box(p, (x_g0 + 20, top2 + 134, R - 20, bot2 - 18), fill="#fdf3ee", stroke="#f3d2c3", radius=8, lw=1)
    pw2 = _pill(p, x_g0 + 32, top2 + 144, "Never", "#fde2d4", ORANGE_INK, sz=12.5, face="Bold", pad_x=12, h=24)
    text(p, x_g0 + 32 + pw2 + 12, top2 + 161,
         [("Your raw uploaded files, unmapped features, or user account data", "SemiBold")], 14, STRONG)

    V3.bottom_line(p, "End-to-end on public CSIC infrastructure in Spain, with a pinned model snapshot for reproducibility.", y=664)
    return p


def _draw_star(p, cx, cy, k, sig_idx, hot=False):
    """Draw a clean node neighbourhood diagram: `sig_idx` neighbours are filled coral (significant)."""
    r = 76 if hot else 82
    pts = [(cx + r * math.cos(2 * math.pi * i / k - math.pi / 2 + 0.28),
            cy + r * math.sin(2 * math.pi * i / k - math.pi / 2 + 0.28)) for i in range(k)]
    for x, y in pts:
        p.draw_line((cx, cy), (x, y), color=rgb("#cccccc"), width=1.6)
    for i, (x, y) in enumerate(pts):
        is_sig = i in sig_idx
        box(p, (x - 15, y - 9.5, x + 15, y + 9.5),
            fill="#f79b74" if is_sig else "#efefef",
            stroke=ORANGE_INK if is_sig else "#bdbdbd", radius=4, lw=1.5 if is_sig else 1.1)
    if hot:
        box(p, (cx - 31, cy - 21, cx + 31, cy + 21), fill="#e3f3f0", stroke=TEAL, radius=9, lw=2.8)
    box(p, (cx - 23, cy - 14, cx + 23, cy + 14),
        fill="#f79b74", stroke=ORANGE_INK, radius=5, lw=1.8)


def picking_the_seeds(out):
    """Slide 18: clear visual explanation of Heat (hub vs specific node) + 3-step seed selection rules."""
    p = D.blank_content(out, like=29, title="Picking the seeds")
    text(p, 1222, 65, "where the walk starts: enriched local peaks on a cleaned pathway graph", 13.5, MUTED, align="right")

    top, bot = 108, 620
    xl1 = 668
    xr0 = 694

    # ---------------- Left Card: Heat ----------------
    V3.card(p, L, top, xl1, bot)
    text(p, L + 26, top + 38, [("Heat: enrichment among neighbours", "Bold")], 18.5, STRONG)

    # Clear color legend right at top of Left Card
    lx = L + 26
    box(p, (lx, top + 52, lx + 18, top + 64), fill="#f79b74", stroke=ORANGE_INK, radius=3, lw=1.2)
    lx = text(p, lx + 24, top + 62.5, [("significant feature", "SemiBold", STRONG), (" (in your data)    ", "Regular", MUTED)], 12.5)
    box(p, (lx, top + 52, lx + 18, top + 64), fill="#efefef", stroke="#bdbdbd", radius=3, lw=1.0)
    text(p, lx + 24, top + 62.5, "other neighbour", 12.5, MUTED)

    # Crisp white inner diagram canvas
    dx0, dx1, dy0, dy1 = L + 22, xl1 - 22, top + 78, top + 368
    box(p, (dx0, dy0, dx1, dy1), fill=WHITE, stroke="#e2e2e2", radius=10, lw=1)
    dmid = (dx0 + dx1) / 2
    p.draw_line((dmid, dy0 + 18), (dmid, dy1 - 18), color=rgb("#ebebeb"), width=1)

    c1x, c2x, cy = (dx0 + dmid) / 2, (dmid + dx1) / 2, dy0 + 100
    _draw_star(p, c1x, cy, 12, {0, 6}, hot=False)
    _draw_star(p, c2x, cy, 4, {0, 1, 2}, hot=True)

    # Labels under Hub vs Focused node
    text(p, c1x, dy0 + 218, [("A hub node", "Bold")], 16, STRONG, align="center")
    text(p, c1x, dy0 + 238, "2 of 12 neighbours significant", 13.5, MUTED, align="center")
    w_cool = _pill(p, 0, -100, "Cool · expected by chance", "#ededed", MUTED, sz=12.5, face="Bold", pad_x=12, h=25)
    _pill(p, c1x - w_cool / 2, dy0 + 250, "Cool · expected by chance", "#ededed", MUTED, sz=12.5, face="Bold", pad_x=12, h=25)

    text(p, c2x, dy0 + 218, [("A focused node", "Bold")], 16, STRONG, align="center")
    text(p, c2x, dy0 + 238, "3 of 4 neighbours significant", 13.5, MUTED, align="center")
    w_hot = _pill(p, 0, -100, "Hot · strong seed", "#e3f3f0", TEAL_DARK, sz=12.5, face="Bold", pad_x=14, h=25)
    _pill(p, c2x - w_hot / 2, dy0 + 250, "Hot · strong seed", "#e3f3f0", TEAL_DARK, sz=12.5, face="Bold", pad_x=14, h=25)

    yh = dy1 + 20
    yh = para(p, L + 26, yh,
              "Hypergeometric test: measures how surprising the number of significant neighbours is, given how many total neighbours the node has.",
              14.8, xl1 - L - 52, color=BODY, leading=1.38)
    text(p, L + 26, bot - 24, [("So a hub gene is not hot just for being a hub.", "Bold")], 16.5, TEAL_DARK)

    # ---------------- Right Column: 3 Step Cards ----------------
    # Card 1: Clean the graph (What a node is)
    c1_top, c1_bot = top, top + 178
    V3.card(p, xr0, c1_top, R, c1_bot)
    circle_number(p, xr0 + 30, c1_top + 31, 1, r=12, fill=TEAL, size=13)
    text(p, xr0 + 50, c1_top + 36, [("What counts as a node (clean graph)", "Bold")], 17.5, STRONG)
    yy = c1_top + 52
    for lead, rest in (
        ("Nodes:", "genes, metabolites (compounds), and your miRNAs."),
        ("No currency shortcuts:", "ATP, ADP, phosphate, NAD, water… are never walked and never a seed — no walk joins two pathways through water."),
        ("Complexes:", "Reactome complexes expand to member proteins; reactions joining >36 pairs are skipped."),
    ):
        yy = _bullet(p, xr0 + 24, yy, lead, rest, R - xr0 - 48, sz=13.5) + 6

    # Card 2: Seed candidates (Local peaks)
    c2_top, c2_bot = c1_bot + 16, c1_bot + 16 + 120
    V3.card(p, xr0, c2_top, R, c2_bot)
    circle_number(p, xr0 + 30, c2_top + 31, 2, r=12, fill=TEAL, size=13)
    text(p, xr0 + 50, c2_top + 36, [("Seed candidates (one per local peak)", "Bold")], 17.5, STRONG)
    yy = c2_top + 54
    _bullet(p, xr0 + 24, yy,
            "Local maxima only:",
            "significant nodes that are not adjacent to an even hotter candidate — avoids picking multiple seeds in the same cluster.",
            R - xr0 - 48, sz=14)

    # Card 3: Anchored to the perturbation
    c3_top, c3_bot = c2_bot + 16, bot
    V3.card(p, xr0, c3_top, R, c3_bot)
    circle_number(p, xr0 + 30, c3_top + 31, 3, r=12, fill=TEAL, size=13)
    text(p, xr0 + 50, c3_top + 36, [("Anchored to the perturbation (when known)", "Bold")], 17.5, STRONG)
    yy = c3_top + 52
    for lead, rest in (
        ("TF–target edges:", "when the design card names a perturbed gene, its known targets (CollecTRI, TRRUST) are added as edges."),
        ("Nearest first:", "seeds come first from within 2 steps of the perturbed gene (hottest first; first seed must be among the nearest)."),
    ):
        yy = _bullet(p, xr0 + 24, yy, lead, rest, R - xr0 - 48, sz=13.5) + 6
    text(p, xr0 + 40, c3_bot - 16, "Example: STATegra network walk anchored on Ikzf1 (shown on 'What you will see')", 12.5, MUTED)

    V3.bottom_line(p, "Clean graph + degree-corrected heat + local peaks = starting points grounded in your data.", y=664)
    return p
