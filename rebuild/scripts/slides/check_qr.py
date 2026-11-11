#!/usr/bin/env python
"""After a build: read every QR code back from the rendered deck and handout and say where each one leads.

    python scripts/slides/check_qr.py

The marking sheet's link (slides/config.json) must be found on the slides that slides/deck_map.json names (written
by build_v5.py: title, Your turn, What the room found, Thank you), and so must the materials link, if one is set
(the Thank you slide); if a link is set and one of its slides does not carry it, the script exits with status 1.
It needs the optional package zxing-cpp; without it the script says so and exits 0 (scan the slides with a phone instead).
"""
import json
import pathlib
import sys

import numpy as np
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAP = json.loads((ROOT / "slides" / "deck_map.json").read_text())
DECK = ROOT / "slides" / MAP["deck"]
HANDOUT = ROOT / "slides" / "practice_handout.pdf"
SHEET_SLIDES = MAP["sheet_qr_slides"]
MATERIALS_SLIDES = MAP.get("materials_qr_slides", [])


def names(slides):
    return ", ".join(map(str, slides[:-1])) + (" and " if len(slides) > 1 else "") + str(slides[-1])


NAMES = names(SHEET_SLIDES)

try:
    import zxingcpp
except ImportError:
    print("QR check skipped: the optional package zxing-cpp is not installed. Scan slides %s with a phone instead." % names(sorted(set(SHEET_SLIDES + MATERIALS_SLIDES))))
    sys.exit(0)


def codes(pdf):
    out = {}
    for i, page in enumerate(pymupdf.open(pdf), 1):
        found = set()
        for zoom in (2, 3):                                         # small codes on the handout need the larger render
            pm = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), colorspace=pymupdf.csRGB, alpha=False)
            a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, 3)
            found |= {r.text for r in zxingcpp.read_barcodes(a, formats=zxingcpp.BarcodeFormat.QRCode) if r.text}
        if found:
            out[i] = sorted(found)
    return out


CFG = json.loads((ROOT / "slides" / "config.json").read_text())
sheet, materials = (CFG.get("marking_sheet_url") or "").strip(), (CFG.get("materials_url") or "").strip()
deck = codes(DECK)
print("QR codes read back from", DECK.name)
for i, found in deck.items():
    for url in found:
        print("  slide %2d  %s%s" % (i, url, "   <- marking sheet" if sheet and url == sheet else "   <- materials" if materials and url == materials else ""))
if HANDOUT.exists():
    print("QR codes read back from", HANDOUT.name)
    for i, found in codes(HANDOUT).items():
        print("  page %d   %d codes%s" % (i, len(found), ", marking sheet among them" if sheet and sheet in found else ""))

failed = False
if not sheet:
    print("RESULT: no marking sheet link is set (slides/config.json); slides %s show the dashed placeholder." % ", ".join(map(str, SHEET_SLIDES[:-1])))
else:
    missing = [i for i in SHEET_SLIDES if sheet not in deck.get(i, [])]
    if missing:
        print("RESULT: PROBLEM. The marking sheet's code was not read on slide(s) %s." % ", ".join(map(str, missing)))
        failed = True
    else:
        print("RESULT: ok. The marking sheet's code is on slides %s and leads to" % NAMES, sheet)
if not materials:
    print("RESULT: no materials link is set (slides/config.json); the Thank you slide has no card for it.")
elif not MATERIALS_SLIDES:
    print("RESULT: PROBLEM. The materials link is set but slides/deck_map.json names no slide for its code: rebuild the deck.")
    failed = True
else:
    missing = [i for i in MATERIALS_SLIDES if materials not in deck.get(i, [])]
    if missing:
        print("RESULT: PROBLEM. The materials code was not read on slide(s) %s." % ", ".join(map(str, missing)))
        failed = True
    else:
        print("RESULT: ok. The materials code is on slide%s %s and leads to" % ("s" if len(MATERIALS_SLIDES) > 1 else "", names(MATERIALS_SLIDES)), materials)
sys.exit(1 if failed else 0)
