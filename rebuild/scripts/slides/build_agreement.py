#!/usr/bin/env python
"""One slide: which AI readers think alike (12 Nov).

Three panels, all on one binary question (did the reader mark the statement "Does not make sense", or not):
  1. Cohen's kappa for every pair of readers, ordered by group agreement so the 4-reader cluster sits top-left;
  2. each reader's kappa and raw agreement against the majority of the other readers, on the exact same row grid;
  3. share of the others' flags this reader also flags vs extra flags it adds on statements the others accept.

`slide(out, readers, data)` takes the reader list of build_v5.py (`READERS`: [(name, {paper id: evaluation})]) and
V3.DATA, so the slide follows whichever readers the deck shows. No reader is an answer key: this is agreement,
not accuracy.
"""
import itertools
import pathlib
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deck as D                                                    # noqa: E402
from deck import BODY, MUTED, STRONG, TEAL, TEAL_DARK, WHITE, box, rgb, text, width  # noqa: E402
import build_v3 as V3                                               # noqa: E402

L, R = 72, 1368
NUMWORD = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}
FLAG = "Does not make sense"


def short(name):
    """'Fable 5.2' -> 'Fable', 'Gemini 4 Hydrogen' -> 'Hydrogen', 'Opus' -> 'Opus'."""
    return name.split()[-1] if name.startswith("Gemini ") else name.split()[0]


def stats(readers, data):
    """Everything the slide draws, from the readers' marks."""
    keys = [(d["id"], s["n"]) for d in data for s in readers[0][1][d["id"]]["statements"]]
    F = []                                                          # F[i][k]: reader i flags statement k
    for _, ev in readers:
        m = {(d["id"], s["n"]): s["mark"] == FLAG for d in data for s in ev[d["id"]]["statements"]}
        assert set(m) == set(keys), "the readers did not mark the same statements"
        F.append([m[k] for k in keys])
    n, N = len(readers), len(keys)

    def kappa(a, b):
        po = sum(x == y for x, y in zip(a, b)) / N
        pa, pb = sum(a) / N, sum(b) / N
        pe = pa * pb + (1 - pa) * (1 - pb)
        return (po - pe) / (1 - pe) if pe < 1 else 1.0

    K = [[kappa(F[i], F[j]) for j in range(n)] for i in range(n)]
    dis = [[sum(x != y for x, y in zip(F[i], F[j])) / N for j in range(n)] for i in range(n)]
    clusters = [[i] for i in range(n)]
    link = lambda a, b: sum(dis[i][j] for i in a for j in b) / (len(a) * len(b))
    while len(clusters) > 1:
        a, b = min(itertools.combinations(range(len(clusters)), 2), key=lambda ab: link(clusters[ab[0]], clusters[ab[1]]))
        merged = clusters[a] + clusters[b]
        clusters = [c for k, c in enumerate(clusters) if k not in (a, b)] + [merged]
    loo = []
    for i in range(n):                                              # reader i against the majority of the others (more than half of them flag)
        maj = [sum(F[j][k] for j in range(n) if j != i) * 2 > (n - 1) for k in range(N)]
        hit = sum(F[i][k] and maj[k] for k in range(N))
        extra = sum(F[i][k] and not maj[k] for k in range(N))
        loo.append({"kappa": kappa(F[i], maj), "agree": sum(F[i][k] == maj[k] for k in range(N)),
                    "hit": hit, "majflag": sum(maj), "extra": extra, "majok": N - sum(maj), "flags": sum(F[i])})
    rank = sorted(range(n), key=lambda i: (-loo[i]["kappa"], -loo[i]["agree"], i))
    per = [sum(F[i][k] for i in range(n)) for k in range(N)]
    P = sum((x * x + (n - x) ** 2 - n) / (n * (n - 1)) for x in per) / N
    p = sum(per) / (N * n)
    Pe = p * p + (1 - p) ** 2
    return {"n": n, "N": N, "K": K, "order": rank, "loo": loo, "fleiss": (P - Pe) / (1 - Pe),
            "all": sum(x == n for x in per), "none": sum(x == 0 for x in per)}


def _mix(a, b, t):
    ca, cb = rgb(a), rgb(b)
    return "#%02x%02x%02x" % tuple(round(255 * (ca[i] + (cb[i] - ca[i]) * t)) for i in range(3))


def _card(p, x0, y0, x1, y1):
    box(p, (x0, y0, x1, y1), fill=D.CARD, stroke="#e4e4e4", radius=12, lw=1)


def slide(out, readers, data):
    S = stats(readers, data)
    n, N, names = S["n"], S["N"], [short(r) for r, _ in readers]
    order = S["order"]
    p = D.blank_content(out, like=29, title="Which AI readers think alike")

    # Top-right binary key so "flag" is defined before reading any panel
    r1 = [("Binary check (69 statements):  ", "SemiBold")]
    r2 = [("flagged", "Bold", STRONG), (" = does not make sense   ", "Regular", MUTED)]
    r3 = [("accepted", "Bold", STRONG), (" = other marks", "Regular", MUTED)]
    pw = 14 + width(r1, 12.5) + 16 + width([(t, f) for t, f, _ in r2], 12.5) + 16 + width([(t, f) for t, f, _ in r3], 12.5) + 14
    kx = 1222 - pw
    box(p, (kx, 48, kx + pw, 76), fill="#f6f6f6", stroke="#e4e4e4", radius=6, lw=1)
    lx = text(p, kx + 14, 66.5, r1, 12.5, BODY)
    box(p, (lx, 55.5, lx + 11, 66.5), fill=V3.BAD, radius=2.5)
    lx = text(p, lx + 16, 66.5, r2, 12.5)
    box(p, (lx, 55.5, lx + 11, 66.5), fill=V3.GOOD, radius=2.5)
    text(p, lx + 16, 66.5, r3, 12.5)

    top, bot = 108, 608
    gap = 20
    w1, w2 = 456, 376
    x1, x2, x3 = L, L + w1 + gap, L + w1 + gap + w2 + gap

    lab_w = max(width([(s, "SemiBold")], 13) for s in names) + 10
    gy0 = top + 114
    cell = min((x1 + w1 - 24 - (x1 + 22 + lab_w)) / n, (bot - 58 - gy0) / n)

    # ---------------------------------------------------------------- 1. the pairwise matrix
    _card(p, x1, top, x1 + w1, bot)
    text(p, x1 + 22, top + 36, [("1. Pairwise agreement", "Bold")], 18, STRONG)
    text(p, x1 + 22, top + 58, "Cohen's kappa: 0 = chance, 1 = identical", 13.5, MUTED)
    gx0 = x1 + 22 + lab_w
    box(p, (gx0 - 4, gy0 - 28, gx0 + n * cell + 4, gy0 + n * cell + 4), fill=WHITE, radius=8)
    col_sz = min(12.0, 12.0 * (cell - 4) / max(width([(s, "SemiBold")], 12.0) for s in names))
    for a, i in enumerate(order):
        cy_mid = gy0 + (a + 0.5) * cell
        text(p, gx0 + (a + 0.5) * cell, gy0 - 9, [(names[i], "SemiBold")], col_sz, STRONG, align="center")
        text(p, gx0 - 10, cy_mid + 4.5, [(names[i], "SemiBold")], 13, STRONG, align="right")
        for b, j in enumerate(order):
            cx, cy = gx0 + b * cell, gy0 + a * cell
            if i == j:
                box(p, (cx + 1.5, cy + 1.5, cx + cell - 1.5, cy + cell - 1.5), fill="#eeeeee", radius=4)
                text(p, cx + cell / 2, cy_mid + 4, "—", 12, MUTED, align="center")
                continue
            k = S["K"][i][j]
            t = max(0.0, min(1.0, (k - 0.10) / 0.68))
            box(p, (cx + 1.5, cy + 1.5, cx + cell - 1.5, cy + cell - 1.5), fill=_mix("#ebf5f3", TEAL_DARK, t), radius=4)
            text(p, cx + cell / 2, cy_mid + 5, [("%.2f" % k, "Bold")], 14.5, WHITE if t > 0.50 else STRONG, align="center")
    text(p, x1 + 22, bot - 20, [("All %s readers together: " % NUMWORD.get(n, str(n)).lower(), "Regular", MUTED),
                                ("Fleiss' kappa %.2f" % S["fleiss"], "Bold", STRONG), (" (moderate)", "Regular", MUTED)], 13.5)

    # ---------------------------------------------------------------- 2. each reader against the majority of the others
    _card(p, x2, top, x2 + w2, bot)
    text(p, x2 + 22, top + 36, [("2. Closest to the group", "Bold")], 18, STRONG)
    text(p, x2 + 22, top + 58, "vs. majority vote of the other five readers", 13.5, MUTED)
    bx0 = x2 + 22 + lab_w
    bx1 = x2 + w2 - 118
    box(p, (bx0 - 6, gy0 - 28, x2 + w2 - 18, gy0 + n * cell + 4), fill=WHITE, radius=8)
    text(p, bx1 + 22, gy0 - 9, [("kappa", "SemiBold")], 11.5, MUTED, align="center")
    text(p, x2 + w2 - 44, gy0 - 9, [("agree", "SemiBold")], 11.5, MUTED, align="center")
    for a, i in enumerate(order):
        cy_mid = gy0 + (a + 0.5) * cell
        k = S["loo"][i]["kappa"]
        text(p, bx0 - 10, cy_mid + 4.5, [(names[i], "SemiBold")], 13, STRONG, align="right")
        box(p, (bx0 + 2, cy_mid - 10, bx1, cy_mid + 10), fill="#ececec", radius=4)
        if k > 0:
            box(p, (bx0 + 2, cy_mid - 10, bx0 + 2 + max(8, k * (bx1 - bx0 - 2)), cy_mid + 10), fill=TEAL, radius=4)
        text(p, bx1 + 22, cy_mid + 5, [("%.2f" % k, "Bold")], 14.5, STRONG, align="center")
        text(p, x2 + w2 - 44, cy_mid + 4.5, "%d/%d" % (S["loo"][i]["agree"], N), 12.5, MUTED, align="center")
    text(p, x2 + 22, bot - 20, [("agree", "SemiBold", STRONG), (" = statements matching the other five's majority", "Regular", MUTED)], 13)

    # ---------------------------------------------------------------- 3. catches the group's flags vs adds its own
    _card(p, x3, top, R, bot)
    text(p, x3 + 22, top + 36, [("3. Same flags, or extra ones?", "Bold")], 18, STRONG)
    text(p, x3 + 22, top + 58, "each dot is one reader vs. the other five's majority", 13.5, MUTED)
    box(p, (x3 + 18, gy0 - 28, R - 18, gy0 + n * cell + 4), fill=WHITE, radius=8)
    px0, px1, py0, py1 = x3 + 68, R - 34, gy0 + 2, gy0 + n * cell - 46
    pts = []
    for i in range(n):
        lo = S["loo"][i]
        pts.append((100 * lo["extra"] / max(1, lo["majok"]), 100 * lo["hit"] / max(1, lo["majflag"])))
    xmax = max(60, 10 * (int(max(x for x, _ in pts) / 10) + 1))
    X = lambda v: px0 + v / xmax * (px1 - px0)
    Y = lambda v: py1 - v / 100 * (py1 - py0)
    text(p, px0 - 38, gy0 - 11, [("Group's flags caught (%)", "SemiBold")], 12, BODY)
    for v in range(0, xmax + 1, 20):
        p.draw_line((X(v), py0), (X(v), py1), color=rgb("#e5e5e5"), width=1)
        text(p, X(v), py1 + 16, "%d%%" % v, 11.5, MUTED, align="center")
    for v in (0, 25, 50, 75, 100):
        p.draw_line((px0, Y(v)), (px1, Y(v)), color=rgb("#e5e5e5"), width=1)
        text(p, px0 - 8, Y(v) + 4, "%d%%" % v, 11.5, MUTED, align="right")
    p.draw_rect(pymupdf.Rect(px0, py0, px1, py1), color=rgb("#cccccc"), width=1)
    text(p, (px0 + px1) / 2, py1 + 36, [("Extra flags added (% of non-flagged)", "SemiBold")], 12, BODY, align="center")

    placed = [(X(x) - 8, Y(y) - 8, X(x) + 8, Y(y) + 8) for x, y in pts]
    hits = lambda r: any(not (r[2] <= q[0] or r[0] >= q[2] or r[3] <= q[1] or r[1] >= q[3]) for q in placed)
    for i, (x, y) in enumerate(pts):
        cx, cy = X(x), Y(y)
        lw = width([(names[i], "Bold")], 13)
        for dx, dy, al in ((10, 4.5, "left"), (-10, 4.5, "right"), (0, -11, "center"), (0, 20, "center"),
                           (10, -9, "left"), (10, 18, "left"), (-10, 18, "right"), (-10, -9, "right")):
            x0 = cx + dx - (lw if al == "right" else lw / 2 if al == "center" else 0)
            r = (x0 - 2, cy + dy - 13, x0 + lw + 2, cy + dy + 4)
            if not hits(r) and r[0] >= px0 + 2 and r[2] <= px1 - 2 and r[1] >= py0 - 12:
                break
        placed.append(r)
        text(p, cx + dx, cy + dy, [(names[i], "Bold")], 13, STRONG, align=al)
    for x, y in pts:
        p.draw_circle((X(x), Y(y)), 6.5, color=rgb(WHITE), fill=rgb(TEAL), width=1.8)
    text(p, x3 + 22, bot - 20, [("Top-left", "Bold", STRONG), (" = catches group flags, adds few extras · ", "Regular", MUTED),
                                ("Right", "Bold", STRONG), (" = stricter", "Regular", MUTED)], 12.5)

    text(p, L, bot + 40, [("Agreement is not accuracy: no reader is an answer key. Which reader is closest to you?", "Bold")], 18, TEAL_DARK)
    text(p, L, bot + 68, "%d of %d statements are flagged by all %s readers, and %d by none."
         % (S["all"], N, NUMWORD.get(n, str(n)).lower(), S["none"]), 14, MUTED)
    return p
