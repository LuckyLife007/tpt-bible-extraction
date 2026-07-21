#!/usr/bin/env python3
"""
One-off helper: merge Matthew's pickled page-range chunks (produced by
extract_matthew_chunk.py) into the final TPT_Matthew.json, using the same
downstream logic (build_result_from_tokens) every other book's single-call
extract_book() uses. Temporary — not part of the standard per-book pattern.

Usage: python3 extract_matthew_merge.py <chunk1.pkl> <chunk2.pkl> ...
"""
import os, sys, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import build_result_from_tokens
from extract_matthew import BOOK_NAME, OUTPUT_PATH

all_tokens   = []
all_fn_words = []
all_blue     = []

for path in sys.argv[1:]:
    with open(path, 'rb') as f:
        tokens, fn_words_seq, blue_sample = pickle.load(f)
    all_tokens.extend(tokens)
    all_fn_words.extend(fn_words_seq)
    all_blue.extend(blue_sample)

build_result_from_tokens(BOOK_NAME, all_tokens, all_fn_words, all_blue, OUTPUT_PATH)
