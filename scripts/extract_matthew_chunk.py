#!/usr/bin/env python3
"""
One-off helper: tokenize a sub-range of Matthew's pages and pickle the
result. Matthew (249 pages) is too large to tokenize in a single sandbox
call (~0.4s/page, exceeds the 45s per-call budget), so extract_matthew.py's
BOLD_OVERRIDES table is applied here in page-range chunks instead. Run
once per chunk, then extract_matthew_merge.py assembles the final JSON.
Temporary — not part of the standard per-book extraction pattern.

Usage: python3 extract_matthew_chunk.py <chunk_start> <chunk_end> <out.pkl>
"""
import os, sys, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import tokenize_pages
from extract_matthew import PDF_PATH, BOLD_OVERRIDES

chunk_start = int(sys.argv[1])
chunk_end   = int(sys.argv[2])
out_path    = sys.argv[3]

tokens, fn_words_seq, blue_sample = tokenize_pages(
    chunk_start, chunk_end, PDF_PATH, BOLD_OVERRIDES)

with open(out_path, 'wb') as f:
    pickle.dump((tokens, fn_words_seq, blue_sample), f)

print(f"chunk {chunk_start}-{chunk_end}: {len(tokens)} tokens, "
      f"{len(fn_words_seq)} fn words, {len(blue_sample)} blue samples -> {out_path}")
