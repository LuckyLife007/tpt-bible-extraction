#!/usr/bin/env python3
"""Extract TPT Ephesians. Pages 2250-2283 (0-indexed)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import extract_book

_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_NAME   = "Ephesians"
START_PAGE  = 2250
END_PAGE    = 2283
PDF_PATH    = os.path.join(_ROOT, "..", "The Passion Translation.pdf")
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_Ephesians.json")

if __name__ == '__main__':
    print(f"Extracting {BOOK_NAME}…")
    extract_book(BOOK_NAME, START_PAGE, END_PAGE, PDF_PATH, OUTPUT_PATH)
