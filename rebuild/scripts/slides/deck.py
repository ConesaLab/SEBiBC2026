#!/usr/bin/env python
"""Drawing kit for the SEBiBC26 TELLME deck (1440 x 810 pt, Open Sans).

The original deck is a PDF whose pages are single raster images, so a slide is
changed by painting over the old line and writing the new one in the same face,
size and colour; new slides reuse the frame (bars, lab logo) of an original page.
"""
import pathlib

import numpy as np
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORIG = ROOT / "docs" / "SEBiBC26_TELLME_PaintOmicsAI.pdf"
FONTS = ROOT / "slides" / "assets" / "fonts"
W, H = 1440, 810

TEAL, TEAL_DARK, DARK_BG = "#009080", "#01695d", "#003b34"
INK, MUTED, CARD, RULE = "#404040", "#555555", "#f2f2f2", "#dddddd"     # INK is the slide-title grey
STRONG, BODY = "#1a1a1a", "#333333"                                   # card headings / running text
ORANGE, ORANGE_INK, YELLOW, WHITE = "#f08051", "#b85b36", "#f0c050", "#ffffff"

FACES = {"Light": "OpenSans-Light.ttf", "Regular": "OpenSans-Regular.ttf", "SemiBold": "OpenSans-SemiBold.ttf",
         "Bold": "OpenSans-Bold.ttf", "Italic": "OpenSans-Italic.ttf", "Mono": "JetBrainsMono-Bold.ttf"}
_font = {k: pymupdf.Font(fontfile=str(FONTS / v)) for k, v in FACES.items()}
ASC, DESC = 0.76, 0.24          # Open Sans: ascender and descender, in em


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def width(runs, size):
    """runs: [(text, face)] or a plain string (Regular)."""
    if isinstance(runs, str):
        runs = [(runs, "Regular")]
    return sum(_font[r[1]].text_length(r[0], size) for r in runs)


def text(page, x, baseline, runs, size, color=INK, align="left"):
    """One line. runs: str or [(text, face[, color])]. Returns the x after the last glyph."""
    if isinstance(runs, str):
        runs = [(runs, "Regular")]
    w = width([(r[0], r[1]) for r in runs], size)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    for r in runs:
        face, col = r[1], (r[2] if len(r) > 2 else color)
        page.insert_text((x, baseline), r[0], fontname="os" + face, fontfile=str(FONTS / FACES[face]),
                         fontsize=size, color=rgb(col))
        x += _font[face].text_length(r[0], size)
    return x


def wrap(s, face, size, maxw):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if _font[face].text_length(t, size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines


def para(page, x, top, s, size, maxw, face="Regular", color=INK, leading=1.38, max_lines=None):
    """Wrapped paragraph; `top` is the top of the first line's ascenders. Returns the y below the last line."""
    lines = wrap(s, face, size, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while _font[face].text_length(lines[-1] + "…", size) > maxw and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    y = top + ASC * size
    for ln in lines:
        text(page, x, y, [(ln, face)], size, color)
        y += leading * size
    return y - ASC * size


def box(page, rect, fill=None, stroke=None, radius=None, lw=1.0):
    r = pymupdf.Rect(rect)
    rad = None if not radius else min(0.5, radius / min(r.width, r.height))
    page.draw_rect(r, color=rgb(stroke) if stroke else None, fill=rgb(fill) if fill else None, width=lw if stroke else 0, radius=rad)


def wipe(page, rect, color):
    page.draw_rect(pymupdf.Rect(rect), color=None, fill=rgb(color), width=0)


def circle_number(page, cx, cy, n, r=11, fill=TEAL, size=12.5):
    page.draw_circle((cx, cy), r, color=None, fill=rgb(fill), width=0)
    text(page, cx, cy + 0.36 * size, [(str(n), "Bold")], size, WHITE, align="center")


# ------------------------------------------------------------------ original deck
_orig = None


def orig():
    global _orig
    if _orig is None:
        _orig = pymupdf.open(ORIG)
    return _orig


def page_image(pno, clip=None, zoom=None):
    """Pixels of an original slide (1-based), at the embedded image's own resolution by default."""
    z = zoom or 2560 / W
    return orig()[pno - 1].get_pixmap(matrix=pymupdf.Matrix(z, z), clip=pymupdf.Rect(clip) if clip else None)


def from_original(out, pno):
    """Append original slide `pno` to `out` unchanged and return the new page, ready to be drawn on."""
    out.insert_pdf(orig(), from_page=pno - 1, to_page=pno - 1)
    return out[-1]


def blank_content(out, like=29, title=None, number=None):
    """A content slide with the deck's frame (colour bars, lab logo) and nothing else."""
    page = from_original(out, like)
    wipe(page, (0, 12, 1235, 797), WHITE)        # everything left of the logo
    wipe(page, (1225, 100, W, 797), WHITE)       # below the logo (overlaps the first wipe: no seam)
    if title:
        text(page, 21, 68, [(title, "Bold")], 27.5, INK)
    if number is not None:
        text(page, 1417, 789, [(str(number), "SemiBold")], 11.5, TEAL, align="right")
    return page


def renumber(page, n):
    wipe(page, (1380, 774, 1432, 796), WHITE)
    text(page, 1417, 789, [(str(n), "SemiBold")], 11.5, TEAL, align="right")


def qr_png(url, path, scale=10, border=2, dark="#000000"):
    """QR code for `url`. Of the eight mask patterns, the first that two independent decoders
    (OpenCV and ZXing) both read back is used: OpenCV's detector fails on some valid codes, and a
    code that a weak decoder reads is the safer one to project in a lecture room."""
    import io
    import segno
    best = None
    try:
        import cv2
        import zxingcpp
        for mask in range(8):
            q = segno.make(url, error="m", mask=mask, boost_error=False)
            buf = io.BytesIO(); q.save(buf, kind="png", scale=scale, border=border)
            a = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
            if cv2.QRCodeDetector().detectAndDecode(a)[0] == url and any(r.text == url for r in zxingcpp.read_barcodes(a)):
                best = q; break
    except ImportError:
        pass
    (best or segno.make(url, error="m")).save(str(path), scale=scale, border=border, dark=dark, light="#ffffff")
    return path


def bare(url):
    """A link as written on a slide: without its scheme."""
    return url.split("://", 1)[-1]


def preview(pdf_path, pno, out_png, width_px=1400):
    d = pymupdf.open(pdf_path)
    p = d[pno - 1]
    z = width_px / p.rect.width
    p.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(str(out_png))
    return out_png
