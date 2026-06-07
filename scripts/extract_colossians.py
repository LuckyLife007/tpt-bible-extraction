#!/usr/bin/env python3
"""Extract TPT Colossians. Pages 2319-2343 (0-indexed)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import extract_book

_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_NAME   = "Colossians"
START_PAGE  = 2319
END_PAGE    = 2343
PDF_PATH    = os.path.join(_ROOT, "..", "The Passion Translation.pdf")
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_Colossians.json")

if __name__ == '__main__':
    print(f"Extracting {BOOK_NAME}…")
    extract_book(BOOK_NAME, START_PAGE, END_PAGE, PDF_PATH, OUTPUT_PATH)
