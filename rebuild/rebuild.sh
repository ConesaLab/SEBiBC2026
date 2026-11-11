#!/bin/sh
# Regenerate the deck, the handout and the web page, with the marking sheet's and the materials' QR codes, and copy them one folder up.
#   ./rebuild.sh "<marking sheet link>" ["<materials link>"]
#   ./rebuild.sh "https://docs.google.com/spreadsheets/d/XXXX/edit?usp=sharing" "https://github.com/ORG/REPO"
# The links are kept in slides/config.json ("marking_sheet_url", "materials_url"; the materials link is the public
# repository with the slides, the handout and the marking workbook). An argument you leave out, or pass as "", keeps
# the value already in the file, so ./rebuild.sh "" "<materials link>" sets only the second one. Without arguments it
# rebuilds with whatever is in the file (an empty sheet link = placeholders; an empty materials link = no card for it).
set -e
cd "$(dirname "$0")"
[ $# -le 2 ] || { echo "usage: $0 [\"<marking sheet link>\" [\"<materials link>\"]]" >&2; exit 2; }
python3 - "$1" "$2" <<'PY'
import json, os, sys
f = "slides/config.json"
c = json.load(open(f)) if os.path.exists(f) else {}
new = dict(zip(("marking_sheet_url", "materials_url"), sys.argv[1:]))
for k in ("marking_sheet_url", "materials_url"):
    c[k] = new.get(k, "").strip() or c.get(k) or ""
open(f, "w").write(json.dumps(c, indent=1) + "\n")
PY
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt
pip install -q -r requirements-optional.txt || echo "note: optional QR-check packages not installed; the QR codes are still valid, scan them with a phone"
python scripts/slides/build_v5.py
python scripts/slides/build_handout.py
cp slides/SEBiBC26_TELLME_PaintOmicsAI_v5.pdf slides/practice_handout.pdf slides/practice_datasets.html ..
echo "done: deck, handout and web page copied to $(cd .. && pwd)"
python scripts/slides/check_qr.py
