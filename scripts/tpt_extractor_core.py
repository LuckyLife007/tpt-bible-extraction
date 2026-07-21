#!/usr/bin/env python3
"""
tpt_extractor_core.py  —  Shared extraction engine for all TPT books (v3 parser).

Usage from a book stub:
    from tpt_extractor_core import extract_book
    extract_book("Galatians", 2208, 2244, pdf_path, output_path)

Function signature:
    extract_book(book_name, start_page, end_page, pdf_path, output_path)
        book_name  : canonical book name, e.g. "1 Thessalonians"
        start_page : 0-indexed first page of the book's content
        end_page   : 0-indexed exclusive end page (first page after the book)
        pdf_path   : absolute path to "The Passion Translation.pdf"
        output_path: absolute path for the output JSON file
    Returns (result_dict, combined_log, blue_sample).
    Also saves the JSON and prints extraction stats automatically.
"""

import pdfplumber
import re
import json
import os


# ---------------------------------------------------------------------------
# Book abbreviation table  (expand as new abbreviations are encountered)
# ---------------------------------------------------------------------------

BOOK_ABBREV = {
    # --- Old Testament abbreviations ---
    'Gen.':              'Genesis',
    'Ex.':               'Exodus',
    'Exod.':             'Exodus',
    'Lev.':              'Leviticus',
    'Num.':              'Numbers',
    'Deut.':             'Deuteronomy',
    'Josh.':             'Joshua',
    'Judg.':             'Judges',
    '1 Sam.':            '1 Samuel',
    '2 Sam.':            '2 Samuel',
    '1 Kgs.':            '1 Kings',
    '2 Kgs.':            '2 Kings',
    '1 Chr.':            '1 Chronicles',
    '2 Chr.':            '2 Chronicles',
    'Neh.':              'Nehemiah',
    'Ps.':               'Psalms',
    'Pss.':              'Psalms',
    'Prov.':             'Proverbs',
    'Isa.':              'Isaiah',
    'Jer.':              'Jeremiah',
    'Ezek.':             'Ezekiel',
    'Dan.':              'Daniel',
    'Hos.':              'Hosea',
    'Joel':              'Joel',
    'Amos':              'Amos',
    'Obad.':             'Obadiah',
    'Jon.':              'Jonah',
    'Mic.':              'Micah',
    'Nah.':              'Nahum',
    'Hab.':              'Habakkuk',
    'Zeph.':             'Zephaniah',
    'Hag.':              'Haggai',
    'Zech.':             'Zechariah',
    'Mal.':              'Malachi',
    # --- New Testament abbreviations ---
    'Matt.':             'Matthew',
    'Mk.':               'Mark',
    'Lk.':               'Luke',
    'Jn.':               'John',
    'Acts':              'Acts',
    'Rom.':              'Romans',
    '1 Cor.':            '1 Corinthians',
    '2 Cor.':            '2 Corinthians',
    'Gal.':              'Galatians',
    'Eph.':              'Ephesians',
    'Phil.':             'Philippians',
    'Col.':              'Colossians',
    '1 Thess.':          '1 Thessalonians',
    '2 Thess.':          '2 Thessalonians',
    '1 Tim.':            '1 Timothy',
    '2 Tim.':            '2 Timothy',
    'Tit.':              'Titus',
    'Philem.':           'Philemon',
    'Heb.':              'Hebrews',
    'Jas.':              'James',
    '1 Pet.':            '1 Peter',
    '2 Pet.':            '2 Peter',
    '1 Jn.':             '1 John',
    '2 Jn.':             '2 John',
    '3 Jn.':             '3 John',
    'Jude':              'Jude',
    'Rev.':              'Revelation',
    'Song of Sol.':      'Song of Solomon',
    'Song.':             'Song of Solomon',
    'Song':              'Song of Solomon',
    # --- Full names (PDF sometimes uses these instead of abbreviations) ---
    'Genesis':           'Genesis',
    'Exodus':            'Exodus',
    'Leviticus':         'Leviticus',
    'Numbers':           'Numbers',
    'Deuteronomy':       'Deuteronomy',
    'Joshua':            'Joshua',
    'Judges':            'Judges',
    'Ruth':              'Ruth',
    '1 Samuel':          '1 Samuel',
    '2 Samuel':          '2 Samuel',
    '1 Kings':           '1 Kings',
    '2 Kings':           '2 Kings',
    '1 Chronicles':      '1 Chronicles',
    '2 Chronicles':      '2 Chronicles',
    'Ezra':              'Ezra',
    'Nehemiah':          'Nehemiah',
    'Esther':            'Esther',
    'Job':               'Job',
    'Psalms':            'Psalms',
    'Psalm':             'Psalms',
    'Proverbs':          'Proverbs',
    'Ecclesiastes':      'Ecclesiastes',
    'Isaiah':            'Isaiah',
    'Jeremiah':          'Jeremiah',
    'Lamentations':      'Lamentations',
    'Ezekiel':           'Ezekiel',
    'Daniel':            'Daniel',
    'Hosea':             'Hosea',
    'Obadiah':           'Obadiah',
    'Jonah':             'Jonah',
    'Micah':             'Micah',
    'Nahum':             'Nahum',
    'Habakkuk':          'Habakkuk',
    'Zephaniah':         'Zephaniah',
    'Haggai':            'Haggai',
    'Zechariah':         'Zechariah',
    'Malachi':           'Malachi',
    'Matthew':           'Matthew',
    'Mark':              'Mark',
    'Luke':              'Luke',
    'John':              'John',
    'Romans':            'Romans',
    '1 Corinthians':     '1 Corinthians',
    '2 Corinthians':     '2 Corinthians',
    'Galatians':         'Galatians',
    'Ephesians':         'Ephesians',
    'Philippians':       'Philippians',
    'Colossians':        'Colossians',
    '1 Thessalonians':   '1 Thessalonians',
    '2 Thessalonians':   '2 Thessalonians',
    '1 Timothy':         '1 Timothy',
    '2 Timothy':         '2 Timothy',
    'Titus':             'Titus',
    'Philemon':          'Philemon',
    'Hebrews':           'Hebrews',
    'James':             'James',
    '1 Peter':           '1 Peter',
    '2 Peter':           '2 Peter',
    '1 John':            '1 John',
    '2 John':            '2 John',
    '3 John':            '3 John',
    'Revelation':        'Revelation',
    'Song of Solomon':   'Song of Solomon',
}


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def is_blue_color(color):
    """
    Return True if the color represents the blue used for cross-reference
    hyperlinks in the TPT PDF.  pdfplumber may return color as:
      - int/float (indexed/grayscale) — compare to 238
      - 3-tuple of floats 0.0–1.0    — blue-dominant check
      - 3-tuple of ints 0–255        — blue-dominant check
    """
    if color is None:
        return False
    if isinstance(color, bool):
        return False
    if isinstance(color, (int, float)):
        return abs(color - 238) < 2
    if isinstance(color, (tuple, list)) and len(color) == 3:
        r, g, b = color
        # Float 0-1: strong blue, negligible red and green
        if isinstance(b, float) and b > 0.8 and r < 0.2 and g < 0.2:
            return True
        # Int 0-255
        if isinstance(b, (int, float)) and b > 180 and r < 50 and g < 50:
            return True
    return False


# ---------------------------------------------------------------------------
# Cross-reference span parser  (v3)
# ---------------------------------------------------------------------------

# Books with only one chapter — verse refs appear without a chapter number
SINGLE_CHAPTER_BOOKS = {'Obadiah', 'Philemon', '2 John', '3 John', 'Jude'}


def find_book_abbrev(text):
    """
    Try to find a book abbreviation at the start of text.
    Returns (canonical_name, remaining_text) or (None, text).
    Sorted longest-first so '1 Cor.' matches before 'Cor.'.
    """
    for abbrev in sorted(BOOK_ABBREV, key=len, reverse=True):
        if text == abbrev or text.startswith(abbrev + ' ') or text.startswith(abbrev + ','):
            rest = text[len(abbrev):].strip().lstrip(',').strip()
            return BOOK_ABBREV[abbrev], rest
    return None, text


def parse_cross_ref_span(span_text):
    """
    Parse the accumulated text of a blue cross-reference span into a list of
    cross_reference objects.  (v3 parser — handles all known TPT patterns.)

    Handles:
      'Gen. 1:2'                  → single reference
      '1 Tim. 1:2'                → book with number prefix
      'Gen. 1:2; 2:7'             → two chapters, same book (semicolon-separated)
      'Gen. 1:2, 7'               → comma-separated verse list within same chapter
      'Ps. 23:1-3'                → verse range
      'Acts 15:22-40 16:19-40'    → space-separated ch:verse refs, same book
      'Acts 17:4 14'              → bare verse following ch:verse (space-separated)
      'Acts 17:1- 16'             → line-break hyphen in verse range (PDF wrapping)
    """
    refs = []
    # Normalise dash characters
    span_text = span_text.replace('\u2013', '-').replace('\u2014', '-')
    # Fix PDF line-break hyphens in verse ranges: "17:1- 16" → "17:1-16"
    span_text = re.sub(r'-\s+(\d)', r'-\1', span_text)

    # Split by semicolons into logical segments
    segments = [s.strip() for s in span_text.split(';')]

    current_book    = None
    current_chapter = None

    for seg in segments:
        if not seg:
            continue

        # Try to find a book abbreviation at the start of this segment
        book, rest = find_book_abbrev(seg)
        if book:
            current_book    = book
            current_chapter = None   # reset chapter when book changes
        else:
            rest = seg

        if current_book is None:
            continue

        rest = rest.strip()

        # Walk through all tokens in `rest`, picking up every ch:verse or
        # bare-verse reference separated by spaces and/or commas.
        pos = 0
        while pos < len(rest):
            # Skip whitespace and commas
            while pos < len(rest) and rest[pos] in ' ,':
                pos += 1
            if pos >= len(rest):
                break

            # Try ch:verse[-verse] pattern  (e.g. "15:22-40")
            m = re.match(r'(\d+):(\d+)(?:-(\d+))?', rest[pos:])
            if m:
                current_chapter = int(m.group(1))
                v_start = int(m.group(2))
                v_end   = int(m.group(3)) if m.group(3) else v_start
                refs.append({
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse_start': v_start,
                    'verse_end': v_end,
                })
                pos += m.end()
                continue

            # Try single-chapter book bare verse (e.g. 'Philem. 10–12')
            if current_book in SINGLE_CHAPTER_BOOKS:
                m2 = re.match(r'(\d+)(?:-(\d+))?', rest[pos:])
                if m2:
                    v_start = int(m2.group(1))
                    v_end   = int(m2.group(2)) if m2.group(2) else v_start
                    refs.append({
                        'book': current_book,
                        'chapter': 1,
                        'verse_start': v_start,
                        'verse_end': v_end,
                    })
                    current_chapter = 1
                    pos += m2.end()
                    continue

            # Try bare verse number continuing same book + chapter (e.g. "14" after "17:4")
            if current_chapter is not None:
                m2 = re.match(r'(\d+)(?:-(\d+))?', rest[pos:])
                if m2:
                    v_start = int(m2.group(1))
                    v_end   = int(m2.group(2)) if m2.group(2) else v_start
                    refs.append({
                        'book': current_book,
                        'chapter': current_chapter,
                        'verse_start': v_start,
                        'verse_end': v_end,
                    })
                    pos += m2.end()
                    continue

            # Skip unrecognised token
            end = pos + 1
            while end < len(rest) and rest[end] not in ' ,':
                end += 1
            pos = end

    return refs


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def is_italic(fontname):
    return 'Italic' in fontname

def is_bold(fontname):
    return 'Bold' in fontname

def classify_word(w):
    """
    Returns one of:
      CHAPTER_NUM       – large bold digit (chapter heading)
      VERSE_NUM         – small non-italic digit(s) like '1', '3–4'
      FN_MARKER_INLINE  – small italic 1-3 lowercase letters (inline footnote marker)
      VERSE_TEXT        – regular ~8.4pt text (verse body)
      FN_MARKER_BLOCK   – small italic 1-3 lowercase letters at left margin (footnote marker)
      FN_XREF_SPAN      – blue ~7.2pt word that is part of a cross-reference link
      FN_CONTENT        – ~7.2pt text (footnote body)
      SKIP              – titles, section headers, etc.
    """
    size   = w['size']
    italic = is_italic(w['fontname'])
    bold   = is_bold(w['fontname'])
    text   = w['text'].strip()
    x0     = w['x0']
    color  = w.get('non_stroking_color')

    # Chapter number: large bold digit
    if size > 13 and bold and re.match(r'^\d+$', text):
        return 'CHAPTER_NUM'

    # Book/sub-titles and other large text
    if size > 10:
        return 'SKIP'

    # Section headers: ~8.4pt bold
    if abs(size - 8.4) < 0.5 and bold:
        return 'SKIP'

    # Small ~6.6pt text
    if abs(size - 6.6) < 0.4:
        if italic and re.match(r'^[a-z]{1,3}$', text):
            return 'FN_MARKER_INLINE'
        if not italic and re.match(r'^\d+[–—-]?\d*$', text):
            return 'VERSE_NUM'
        return 'SKIP'

    # Regular verse text: ~8.4pt
    if abs(size - 8.4) < 0.5:
        return 'VERSE_TEXT'

    # Footnote content: ~7.2pt
    if abs(size - 7.2) < 0.4:
        # Left-margin italic footnote block marker
        if italic and re.match(r'^[a-z]{1,3}$', text) and x0 < 45:
            return 'FN_MARKER_BLOCK'
        # Blue word → cross-reference link
        if is_blue_color(color):
            return 'FN_XREF_SPAN'
        return 'FN_CONTENT'

    return 'UNKNOWN'


# ---------------------------------------------------------------------------
# Line grouping
# ---------------------------------------------------------------------------

def group_into_lines(words, y_tol=3.0):
    """
    Group words into text lines.  Words within y_tol of each other vertically
    are treated as the same line; within each line they are sorted left-to-right.
    Handles superscript verse-numbers and footnote markers which sit slightly
    above the main text baseline.
    """
    if not words:
        return []

    lines    = []
    cur_line = []
    cur_y    = None

    for w in sorted(words, key=lambda w: (w['top'], w['x0'])):
        if cur_y is None or abs(w['top'] - cur_y) <= y_tol:
            cur_line.append(w)
            if cur_y is None:
                cur_y = w['top']
        else:
            lines.append(sorted(cur_line, key=lambda w: w['x0']))
            cur_line = [w]
            cur_y    = w['top']

    if cur_line:
        lines.append(sorted(cur_line, key=lambda w: w['x0']))

    return lines


# ---------------------------------------------------------------------------
# Verse-number parsing
# ---------------------------------------------------------------------------

def parse_verse_num(text):
    """
    Returns (start_verse, end_verse).
      '5'   → (5, 5)
      '3–4' → (3, 4)
    """
    text = text.strip()
    m = re.match(r'^(\d+)[–—-](\d+)$', text)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.match(r'^(\d+)$', text)
    if m:
        v = int(m.group(1))
        return v, v
    return None, None


# ---------------------------------------------------------------------------
# Footnote reference parsing
# ---------------------------------------------------------------------------

def parse_fn_ref(text):
    """
    Extracts (chapter, verse) from a reference like '1:1', '2:13', '1:1–2'.
    Returns (None, None) if not a reference.
    """
    m = re.match(r'^(\d+):(\d+)', text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def parse_fn_ref_verse_only(text):
    """
    For single-chapter books (e.g. Philemon) footnote bodies are prefixed with
    a verse-only reference ('9' or '1–2') instead of 'chapter:verse'. Treats the
    chapter as 1. Returns (1, start_verse) or (None, None).
    """
    m = re.match(r'^(\d+)[–—-]\d+$', text)
    if m:
        return 1, int(m.group(1))
    m = re.match(r'^(\d+)$', text)
    if m:
        return 1, int(m.group(1))
    return None, None


# ---------------------------------------------------------------------------
# Text builder and post-processor
# ---------------------------------------------------------------------------

def build_text(parts):
    """
    Build verse text from a list of ('text'|'marker', str) tuples.
    Markers are wrapped in curly brackets: {a}, {aa}, etc.
    """
    tokens = []
    for ptype, ptext in parts:
        if ptype == 'marker':
            tokens.append('{' + ptext + '}')
        else:
            tokens.append(ptext)
    text = ' '.join(tokens)
    return post_process(text)


def post_process(text):
    """
    Fix PDF extraction artefacts:
      - Remove spaces immediately before punctuation  (, . ; : ! ?)
      - Collapse line-break hyphens: "word- next" → "word-next"
      - Collapse multiple spaces
    """
    text = re.sub(r'-\s+([a-zA-Z])', r'-\1', text)
    text = re.sub(r'\s+([,\.;:!?\)])', r'\1', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


# ---------------------------------------------------------------------------
# Main extraction engine
# ---------------------------------------------------------------------------

def tokenize_pages(start_page, end_page, pdf_path, bold_body_overrides=None):
    """
    Phase 1 of extract_book: scan a page range and produce the raw token
    streams (all_verse_tokens, fn_words_seq, blue_sample) that the rest of
    the pipeline consumes. Split out from extract_book verbatim (no logic
    change) so a book's page range can be tokenized in smaller chunks
    across multiple calls — needed for very large books (e.g. Matthew,
    249 pages) where scanning the whole range in one process exceeds the
    sandbox's per-call time budget. See build_result_from_tokens() for
    phase 2, and extract_book() which simply chains the two for the
    normal single-call case (unchanged behavior for every existing book).

    Returns
    -------
    (all_verse_tokens, fn_words_seq, blue_sample)
    """
    bold_body_overrides = bold_body_overrides or {}

    all_verse_tokens = []
    fn_words_seq     = []
    blue_sample      = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in range(start_page, end_page):
            page  = pdf.pages[page_idx]
            words = page.extract_words(extra_attrs=['fontname', 'size', 'non_stroking_color'])

            verse_words = []
            cls_by_id   = {}
            page_override = bold_body_overrides.get(page_idx)

            for w in words:
                cls = classify_word(w)
                if cls == 'SKIP' and page_override is not None:
                    is_bold_84 = abs(w['size'] - 8.4) < 0.5 and is_bold(w['fontname'])
                    if is_bold_84:
                        if page_override == 'all':
                            cls = 'VERSE_TEXT'
                        elif not any(abs(w['top'] - t) < 3.0 for t in page_override):
                            cls = 'VERSE_TEXT'
                if cls in ('CHAPTER_NUM', 'VERSE_NUM', 'FN_MARKER_INLINE', 'VERSE_TEXT'):
                    verse_words.append(w)
                    cls_by_id[id(w)] = cls
                elif cls in ('FN_MARKER_BLOCK', 'FN_CONTENT', 'FN_XREF_SPAN'):
                    fn_words_seq.append((cls, w))
                    if cls == 'FN_XREF_SPAN' and len(blue_sample) < 20:
                        blue_sample.append({
                            'text':  w['text'],
                            'color': w.get('non_stroking_color'),
                            'page':  page_idx,
                        })

            lines = group_into_lines(verse_words, y_tol=3.0)
            for line in lines:
                for w in line:
                    cls  = cls_by_id[id(w)]
                    text = w['text'].strip()
                    if cls == 'CHAPTER_NUM':
                        all_verse_tokens.append(('CHAPTER_NUM', int(text)))
                    elif cls == 'VERSE_NUM':
                        s, e = parse_verse_num(text)
                        if s is not None:
                            all_verse_tokens.append(('VERSE_NUM', (s, e)))
                    elif cls == 'FN_MARKER_INLINE':
                        all_verse_tokens.append(('FN_MARKER', text))
                    elif cls == 'VERSE_TEXT':
                        all_verse_tokens.append(('TEXT', text))

    return all_verse_tokens, fn_words_seq, blue_sample


def build_result_from_tokens(book_name, all_verse_tokens, fn_words_seq, blue_sample, output_path):
    """
    Phase 2 of extract_book: consume the token streams produced by
    tokenize_pages() (concatenated across all chunks, in page order) and
    do everything extract_book used to do after tokenizing — chapter/verse
    parsing, footnote resolution, JSON assembly, save, and stats printing.
    Split out verbatim from extract_book (no logic change).

    Returns
    -------
    (result_dict, combined_log, blue_sample)
    """
    # -----------------------------------------------------------------------
    # Parse verse token stream → chapters / verses
    # -----------------------------------------------------------------------
    chapters        = []
    current_chapter = None
    current_verses  = []

    current_verse_num = None
    current_verse_max = None
    current_parts     = []
    pre_verse_parts   = []

    def flush_verse():
        nonlocal current_verse_num, current_verse_max, current_parts
        if current_verse_num is not None and current_parts:
            text    = build_text(current_parts)
            markers = [p[1] for p in current_parts if p[0] == 'marker']
            for vnum in range(current_verse_num, current_verse_max + 1):
                current_verses.append({
                    'verse_num': vnum,
                    'text':      text,
                    'markers':   markers,
                    'combined':  current_verse_max > current_verse_num
                })
        current_verse_num = None
        current_verse_max = None
        current_parts     = []

    def flush_chapter():
        nonlocal current_chapter, current_verses, pre_verse_parts
        if current_chapter is not None:
            flush_verse()
            if pre_verse_parts and not any(v['verse_num'] == 1 for v in current_verses):
                text    = build_text(pre_verse_parts)
                markers = [p[1] for p in pre_verse_parts if p[0] == 'marker']
                current_verses.insert(0, {
                    'verse_num': 1,
                    'text':      text,
                    'markers':   markers,
                    'combined':  False
                })
            chapters.append({'chapter': current_chapter, 'verses': current_verses[:]})
        current_verses  = []
        pre_verse_parts = []

    for (ttype, tdata) in all_verse_tokens:
        if ttype == 'CHAPTER_NUM':
            flush_chapter()
            current_chapter = tdata

        elif ttype == 'VERSE_NUM':
            # Single-chapter books (e.g. Philemon) have no printed chapter
            # number, so no CHAPTER_NUM token is ever emitted to set the
            # chapter. Default to chapter 1 on the first verse encountered.
            if current_chapter is None:
                current_chapter = 1
            start_v, end_v = tdata
            flush_verse()
            if pre_verse_parts and start_v > 1:
                text    = build_text(pre_verse_parts)
                markers = [p[1] for p in pre_verse_parts if p[0] == 'marker']
                for vnum in range(1, start_v):
                    current_verses.append({
                        'verse_num': vnum,
                        'text':      text,
                        'markers':   markers,
                        'combined':  False
                    })
                pre_verse_parts = []
            current_verse_num = start_v
            current_verse_max = end_v
            if pre_verse_parts:
                current_parts   = list(pre_verse_parts)
                pre_verse_parts = []
            else:
                current_parts = []

        elif ttype == 'FN_MARKER':
            target = current_parts if current_verse_num is not None else pre_verse_parts
            target.append(('marker', tdata))

        elif ttype == 'TEXT':
            target = current_parts if current_verse_num is not None else pre_verse_parts
            target.append(('text', tdata))

    flush_chapter()

    # -----------------------------------------------------------------------
    # Parse footnote word sequence → fn_map
    # fn_map: (chapter, verse, marker) → {'text': str, 'xrefs': list}
    # -----------------------------------------------------------------------
    fn_map = {}

    # Single-chapter books emit no CHAPTER_NUM token; their footnote bodies use
    # verse-only reference prefixes, so resolve those against chapter 1.
    is_single_chapter = not any(t[0] == 'CHAPTER_NUM' for t in all_verse_tokens)

    cur_fn_marker  = None
    cur_fn_chapter = None
    cur_fn_verse   = None
    cur_fn_parts   = []
    cur_xref_words = []
    cur_fn_xrefs   = []
    seen_ref       = False

    def flush_xref_span():
        nonlocal cur_xref_words
        if cur_xref_words:
            span_text = ' '.join(cur_xref_words)
            parsed    = parse_cross_ref_span(span_text)
            cur_fn_xrefs.extend(parsed)
            cur_xref_words = []

    def flush_fn():
        nonlocal cur_fn_marker, cur_fn_chapter, cur_fn_verse
        nonlocal cur_fn_parts, cur_xref_words, cur_fn_xrefs, seen_ref
        flush_xref_span()
        if cur_fn_marker and cur_fn_chapter is not None and cur_fn_verse is not None:
            text  = post_process(' '.join(cur_fn_parts))
            entry = {'text': text}
            if cur_fn_xrefs:
                entry['xrefs'] = list(cur_fn_xrefs)
            fn_map[(cur_fn_chapter, cur_fn_verse, cur_fn_marker)] = entry
        cur_fn_marker  = None
        cur_fn_chapter = None
        cur_fn_verse   = None
        cur_fn_parts   = []
        cur_xref_words = []
        cur_fn_xrefs   = []
        seen_ref       = False

    for (cls, w) in fn_words_seq:
        text = w['text'].strip()
        if cls == 'FN_MARKER_BLOCK':
            flush_fn()
            cur_fn_marker = text
        elif cls == 'FN_XREF_SPAN':
            if not seen_ref:
                seen_ref = True
            cur_xref_words.append(text)
            cur_fn_parts.append(text)
        elif cls == 'FN_CONTENT':
            # Semicolons and commas that sit between blue cross-reference words
            # are connectors, not terminators — keep accumulating the span.
            if cur_xref_words and text in (';', ','):
                cur_xref_words.append(text)
                cur_fn_parts.append(text)
                continue
            if cur_xref_words:
                flush_xref_span()
            if not seen_ref:
                ch, vs = parse_fn_ref(text)
                if ch is None and is_single_chapter:
                    ch, vs = parse_fn_ref_verse_only(text)
                if ch is not None:
                    cur_fn_chapter = ch
                    cur_fn_verse   = vs
                    seen_ref       = True
                    continue
                else:
                    seen_ref = True
            cur_fn_parts.append(text)

    flush_fn()

    # -----------------------------------------------------------------------
    # Assemble final JSON
    # -----------------------------------------------------------------------
    combined_log    = []
    result_chapters = []

    for chap_data in chapters:
        chap_num   = chap_data['chapter']
        verses_out = []

        for v in chap_data['verses']:
            vnum    = v['verse_num']
            text    = v['text']
            markers = v['markers']

            seen_markers = set()
            footnotes    = []
            for marker in markers:
                if marker in seen_markers:
                    continue
                seen_markers.add(marker)
                entry = fn_map.get((chap_num, vnum, marker))
                if entry is None:
                    for sv in range(max(1, vnum - 5), vnum + 1):
                        e = fn_map.get((chap_num, sv, marker))
                        if e:
                            entry = e
                            break
                if entry:
                    fn_obj = {'marker': marker, 'text': entry['text']}
                    if entry.get('xrefs'):
                        fn_obj['cross_references'] = entry['xrefs']
                    footnotes.append(fn_obj)

            verse_obj = {'verse': vnum, 'text': text}
            if footnotes:
                verse_obj['footnotes'] = footnotes
            verses_out.append(verse_obj)

        result_chapters.append({'chapter': chap_num, 'verses': verses_out})

    # Build combined-verse log for reporting
    for chap_data in chapters:
        chap_num = chap_data['chapter']
        text_to_vnums = {}
        for v in chap_data['verses']:
            if v['combined']:
                text_to_vnums.setdefault(v['text'], []).append(v['verse_num'])
        for text, vnums in text_to_vnums.items():
            if len(vnums) > 1:
                combined_log.append((chap_num, vnums, text))

    result = {'book': book_name, 'chapters': result_chapters}

    # -----------------------------------------------------------------------
    # Save to file
    # -----------------------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # -----------------------------------------------------------------------
    # Print stats
    # -----------------------------------------------------------------------
    total_verses   = sum(len(c['verses']) for c in result_chapters)
    total_fn       = sum(len(v.get('footnotes', [])) for c in result_chapters for v in c['verses'])
    total_xref_fns = sum(
        1 for c in result_chapters for v in c['verses']
        for fn in v.get('footnotes', []) if 'cross_references' in fn
    )
    total_xrefs = sum(
        len(fn['cross_references']) for c in result_chapters for v in c['verses']
        for fn in v.get('footnotes', []) if 'cross_references' in fn
    )

    print(f"Written → {output_path}")
    print(f"Chapters            : {len(result_chapters)}")
    print(f"Verses              : {total_verses}")
    print(f"Footnotes resolved  : {total_fn}")
    print(f"Footnotes with xrefs: {total_xref_fns}")
    print(f"Cross-references    : {total_xrefs}")
    for c in result_chapters:
        fn_count   = sum(len(v.get('footnotes', [])) for v in c['verses'])
        xref_count = sum(
            len(fn.get('cross_references', [])) for v in c['verses']
            for fn in v.get('footnotes', [])
        )
        print(f"  Chapter {c['chapter']}: {len(c['verses'])} verses, "
              f"{fn_count} footnotes, {xref_count} cross-references")

    if blue_sample:
        print("\n=== BLUE WORD SAMPLE (first 20 FN_XREF_SPAN detections) ===")
        for s in blue_sample:
            print(f"  page={s['page']}  color={s['color']}  text={s['text']!r}")
    else:
        print("\n=== NO BLUE (FN_XREF_SPAN) WORDS DETECTED ===")
        print("  Check non_stroking_color values if cross-references are expected.")

    print("\n=== COMBINED VERSES (need manual review) ===")
    if combined_log:
        for (chnum, vnums, text) in combined_log:
            print(f"  Ch{chnum}:{vnums}  →  \"{text[:80]}{'…' if len(text) > 80 else ''}\"")
    else:
        print("  None detected.")

    return result, combined_log, blue_sample


def extract_book(book_name, start_page, end_page, pdf_path, output_path,
                  bold_body_overrides=None):
    """
    Extract a single TPT book from the PDF and save to output_path as JSON.
    Thin wrapper chaining tokenize_pages() + build_result_from_tokens() —
    unchanged behavior/output from before this function was split into two
    phases (see tokenize_pages() for why: chunked tokenizing across
    multiple calls is needed for very large books).

    Parameters
    ----------
    book_name   : str  — e.g. "Galatians"
    start_page  : int  — 0-indexed first content page
    end_page    : int  — 0-indexed exclusive end (first page after this book)
    pdf_path    : str  — path to "The Passion Translation.pdf"
    output_path : str  — where to write the output JSON
    bold_body_overrides : dict, optional — OPT-IN ONLY, default None (no effect on
        any book that doesn't pass this). Some books render direct-speech quotations
        in bold ~8.4pt (the same font/size classify_word() normally treats as a
        section header and skips — see the Hebrews 10:5-9 defect in tpt-progress.md).
        This param lets a book script correct specific, manually-verified instances
        without changing default behavior for every other book.
        Keys are 0-indexed page numbers. Values are either:
          - the string 'all'  → every bold ~8.4pt run on this page is body text
            (reclassified VERSE_TEXT instead of SKIP)
          - a list of top-coordinates (floats) → these specific lines are KEPT as
            genuine section headers (SKIP); every other bold ~8.4pt line on this
            page is reclassified to VERSE_TEXT.
        Every page/line included here must be individually verified by reading the
        actual PDF content — this is a manually-curated override table, not a
        heuristic, precisely because a generic geometric rule proved unreliable
        (genuine headers and quote text sometimes share a page in this book).

    Returns
    -------
    (result_dict, combined_log, blue_sample)
    """
    all_verse_tokens, fn_words_seq, blue_sample = tokenize_pages(
        start_page, end_page, pdf_path, bold_body_overrides)
    return build_result_from_tokens(book_name, all_verse_tokens, fn_words_seq,
                                     blue_sample, output_path)
