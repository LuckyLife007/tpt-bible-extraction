#!/usr/bin/env python3
"""Extract TPT 3 John. Pages 2756-2762 (0-indexed, END exclusive). Single-chapter book."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import extract_book

_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_NAME   = "3 John"
START_PAGE  = 2756
END_PAGE    = 2762
PDF_PATH    = os.path.join(_ROOT, "..", "The Passion Translation.pdf")
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_3_John.json")

if __name__ == '__main__':
    print(f"Extracting {BOOK_NAME}…")
    extract_book(BOOK_NAME, START_PAGE, END_PAGE, PDF_PATH, OUTPUT_PATH)
