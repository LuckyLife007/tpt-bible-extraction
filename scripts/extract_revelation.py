#!/usr/bin/env python3
"""
Extract TPT Revelation. Pages 2801-2933 (0-indexed, END exclusive).

Revelation renders most direct-speech quotations (Christ's letters to the
seven churches in ch. 2-3, plus scattered quotes elsewhere) in bold ~8.4pt —
the same style the shared parser normally treats as a section header (see
the Hebrews 10:5-9 defect documented in tpt-progress.md). Left unhandled,
this silently drops the quoted text (confirmed: it ate all of Rev 16:15 and
gutted parts of 2:1-3:22 and 22:6-20).

BOLD_OVERRIDES below is a manually-verified table (every page/line checked
against the actual PDF content — see tpt-progress.md's Revelation entry for
the full reasoning) telling the shared parser which bold ~8.4pt lines on
each affected page are genuine section headers (kept as headers) versus
quoted body text (reclassified so it isn't dropped). This is opt-in via the
bold_body_overrides parameter — it has zero effect on any other book.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import extract_book

_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_NAME   = "Revelation"
START_PAGE  = 2801
END_PAGE    = 2933
PDF_PATH    = os.path.join(_ROOT, "..", "The Passion Translation.pdf")
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_Revelation.json")

# Pages where ALL bold ~8.4pt content is quoted body text (no header on the page).
_ALL_BODY_PAGES = [2803, 2804, 2814, 2817, 2818, 2827, 2829, 2902, 2930]

# Pages with a MIX of a genuine header and quoted body text.
# Value = list of top-coordinates of the line(s) that are real headers;
# every other bold ~8.4pt line on that page is reclassified to body text.
_MIXED_PAGES = {
    2812: [193.2],                     # "Christ's Letter to Ephesus"
    2813: [285.7],                     # "Christ's Letter to Smyrna"
    2815: [36.6],                      # "Christ's Letter to Pergamum"
    2816: [126.6],                     # "Christ's Letter to Thyatira"
    2825: [145.2],                     # "Christ's Letter to Sardis"
    2826: [225.1],                     # "Christ's Letter to Philadelphia"
    2828: [81.6],                      # "Christ's Letter to Laodicea"
    2833: [174.0],                     # "John's Vision of the Throne Room"
    2928: [70.8, 145.2, 213.0],        # "The Testimony of the Angel/Jesus/John"
    2929: [114.6],                     # "Jesus' Final Words and John's Final Testimony"
}

BOLD_OVERRIDES = {p: 'all' for p in _ALL_BODY_PAGES}
BOLD_OVERRIDES.update(_MIXED_PAGES)

if __name__ == '__main__':
    print(f"Extracting {BOOK_NAME}…")
    extract_book(BOOK_NAME, START_PAGE, END_PAGE, PDF_PATH, OUTPUT_PATH,
                 bold_body_overrides=BOLD_OVERRIDES)
