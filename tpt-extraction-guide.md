# TPT Bible Extraction Guide

## Overview

This project extracts text from **The Passion Translation (TPT)** PDF Bible into structured JSON files, one per book, intended for use in church display software. The extraction covers the New Testament plus Psalms, Proverbs, and Song of Solomon.

The primary tool is a Python script using `pdfplumber` for rich word-level metadata extraction (font name, size, position). Each book gets its own extraction script and its own output JSON file.

---

## Scope

Books to extract:
- **New Testament** (Matthew through Revelation)
- **Psalms**
- **Proverbs**
- **Song of Solomon**

---

## Output Format

### File Naming and Location

- One JSON file per book, saved to the `TPT/` subfolder
- File naming: `TPT_{BookName}.json`
  - Examples: `TPT_Philippians.json`, `TPT_1_Corinthians.json`, `TPT_Song_of_Solomon.json`

### JSON Structure

```json
{
  "book": "Philippians",
  "chapters": [
    {
      "chapter": 1,
      "verses": [
        {
          "verse": 1,
          "text": "Dear friends in Philippi, My name is Paul...",
          "footnotes": [
            { "marker": "a", "text": "Timothy was Paul's convert, coworker, and spiritual son. See 1 Tim. 1:2.",
              "cross_references": [
                { "book": "1 Timothy", "chapter": 1, "verse_start": 2, "verse_end": 2 }
              ]
            },
            { "marker": "b", "text": "Or 'guardians,' as translated..." }
          ]
        },
        {
          "verse": 2,
          "text": "May the blessings of divine grace..."
        }
      ]
    }
  ]
}
```

**Rules:**
- No `"version"` field anywhere in the JSON
- `"verse"` is always an integer
- `"chapter"` is always an integer
- `"text"` is always a string
- `"footnotes"` is an array — **omit the field entirely** if the verse has no footnotes
- `"cross_references"` is an optional array within each footnote — **omit entirely** if the footnote has no cross-references (do not write an empty array)
- `"combined_source"` is an optional array — see Combined Verses section below
- All chapters and verses are in ascending order

---

## Inline Footnote Markers

Footnote markers appear inline within verse text. They must be wrapped in **curly brackets** in the output:

```
{a}  {b}  {aa}  {ab}
```

Example verse text:
> "My name is Paul and I'm joined by Timothy, {a} both of us servants of Jesus..."

This makes markers visually distinguishable in the display software without interfering with the reading flow.

**Do not** use bare letters (`a`, `b`) — always use `{a}`, `{b}`, etc.

---

## Footnote Text Rules

Each footnote entry has:
- `"marker"` — the letter(s) matching the inline marker in the verse text
- `"text"` — the footnote body

**Strip the verse-reference prefix** from the footnote body. The PDF encodes each footnote with a chapter:verse reference at the start (e.g. `1:6`). This reference must be removed from the output text.

Example: PDF footnote content reads: `1:6 Timothy was Paul's convert, coworker...`
→ Output: `"text": "Timothy was Paul's convert, coworker..."`

**Marker reset:** Footnote markers reset to `a` at the start of each chapter. A marker key is therefore `(chapter, verse, letter)`.

---

## Combined Verses

The TPT sometimes merges two or more consecutive verse numbers into a single paragraph. For example, a passage might be labelled `3–4` in the PDF, with one block of text covering both verses.

### Extraction Behaviour

The script duplicates the combined text under each verse number in the range. So `3–4` produces two entries, both with the same text, for verses 3 and 4.

### Manual Review and Splitting

After extraction, all combined verses are **reported to the operator** for manual review. Using the corresponding KJV JSON file (in the `KJV/` folder) as a verse-boundary reference, the text is split so each verse number receives its own distinct text.

Splitting rules:
1. Cross-reference the KJV version to determine the verse boundaries
2. Find the nearest natural sentence or clause break in the TPT text that corresponds to the KJV boundary
3. Each resulting verse gets only its portion of the text
4. Footnote markers stay with whichever verse they naturally appear in after the split
5. If a split is uncertain, document the KJV and TPT side-by-side and flag for operator review

### `combined_source` Field

After splitting, **every verse that originated from a combined passage** receives a `combined_source` field listing all the verse numbers in the original combined range:

```json
{
  "verse": 22,
  "text": "So here's my dilemma: Each day I live...",
  "combined_source": [22, 23, 24]
}
```

This field is present on **all** verses from the original group, not just the first. It allows the display software to know that these were originally one passage in the source text.

---

## PDF Font Taxonomy

The TPT PDF uses consistent font sizes across all books. Classification by size and style:

| Font size | Style | Color | Classification |
|-----------|-------|-------|----------------|
| ~16.8pt | Bold | Any | Chapter number |
| >10pt | Any | Any | Skip (book titles, sub-headers) |
| ~8.4pt | Bold | Any | Skip (section headers within chapters) |
| ~8.4pt | Regular or Italic | Any | Verse text |
| ~6.6pt | Non-italic, digits | Any | Verse number (may be a range like `3–4`) |
| ~6.6pt | Italic, a-z letters | Any | Inline footnote marker |
| ~7.2pt | Italic, a-z, left margin | Any | Footnote block marker |
| ~7.2pt | Any | `color=238` (blue), **single character** | Footnote cross-reference marker (same as footnote block marker — treat identically) |
| ~7.2pt | Any | `color=238` (blue), **multi-character** | Cross-reference link (e.g. `Gen. 1:2`, `1 Tim. 1:2`) — extract structurally |
| ~7.2pt | Any other | Any | Footnote body text |

All size comparisons use a ±0.4–0.5pt tolerance to account for minor PDF rendering variation.

**Key distinction for cross-references:** Within the footnote body, blue (`color=238`) spans at ~7.2pt are cross-reference links. A **single-character** blue span is a footnote marker (treat as normal). A **multi-character** blue span is a scripture cross-reference that must be extracted structurally into the `cross_references` array.

---

## Line Grouping

Superscript verse numbers and inline footnote markers sit slightly **above** the main text baseline (typically 1–2pt higher). If words are sorted purely by their `top` coordinate, markers and verse numbers appear out of order relative to surrounding text.

**Fix:** Group words into lines using a `y_tolerance = 3.0pt` window. Words within 3pt of each other vertically are treated as the same line; within a line they are sorted left-to-right by `x0`.

---

## Post-Processing

PDF word extraction introduces spacing artefacts. A post-processing pass is applied to all verse and footnote text:

1. **Space before punctuation** — `"for you ,"` → `"for you,"`
   `re.sub(r'\s+([,\.;:!?\)])', r'\1', text)`
2. **Hyphenated line breaks** — `"servant- leaders"` → `"servant-leaders"`
   `re.sub(r'-\s+([a-zA-Z])', r'-\1', text)`
3. **Space after opening parenthesis** — `"( word"` → `"(word"`
   `re.sub(r'\(\s+', '(', text)`
4. **Multiple spaces** — collapse to single space

---

## Pre-Verse-1 Text

Some chapters begin with verse content immediately following the chapter number, with no visible `1` superscript (the `1` is omitted from the PDF layout). The script accumulates text that appears before the first explicit verse number into `pre_verse_parts`. If the first explicit verse number seen is greater than `1`, the accumulated text is assigned to verse 1.

---

## Workflow

### Book-by-Book Approach

Books are extracted **one at a time**. Before running on any new book:

1. Locate the book's page range in the PDF using `pdftotext` and form-feed character counting
2. Inspect a sample page with `pdfplumber` to confirm the font taxonomy holds
3. Check whether the current script needs modification (some books may have structural differences)
4. Run the extraction script
5. Review the output JSON for quality
6. Review and split any combined verses reported by the script
7. Confirm the output is satisfactory before proceeding to the next book

### Script Retention

Each book's extraction script is **kept in the working folder** (`/Extraction/`). This ensures:
- The script is accessible across sessions
- Any book can be re-extracted if needed
- Script variations between books are preserved for reference

---

## File Organisation

```
Extraction/
├── The Passion Translation.pdf        ← Source PDF
├── tpt-extraction-guide.md            ← This document
├── tpt-progress.md                    ← Progress log
├── extract_philippians.py             ← Per-book extraction scripts
├── extract_<bookname>.py
├── TPT/                               ← Output JSON files
│   ├── TPT_Philippians.json
│   └── TPT_<BookName>.json
└── KJV/                               ← KJV reference JSONs (for combined-verse splitting)
    ├── KJV_Philippians.json
    └── KJV_<BookName>.json
```

---

## Cross-Reference Extraction

### What it is

Some footnotes contain hyperlinked scripture references — e.g. `"See 1 Tim. 1:2."` — where the reference text is rendered in blue in the PDF. These must be extracted not just as plain text (they already appear in the footnote `text` field) but also as structured metadata in a `cross_references` array.

### Schema

```json
{
  "marker": "d",
  "text": "Or \"good [worthwhile] work.\" Paul uses language here that sounds similar to Gen. 1:2...",
  "cross_references": [
    { "book": "Genesis", "chapter": 1, "verse_start": 2, "verse_end": 2 }
  ]
}
```

Each object in `cross_references` has:
- `"book"` — full canonical name (never an abbreviation)
- `"chapter"` — integer
- `"verse_start"` — integer (first verse in range)
- `"verse_end"` — integer (equals `verse_start` for single-verse references)

### Parsing rules

| PDF text | Output |
|---|---|
| `Gen. 1:2` | `{ "book": "Genesis", "chapter": 1, "verse_start": 2, "verse_end": 2 }` |
| `1 Tim. 1:2` | `{ "book": "1 Timothy", "chapter": 1, "verse_start": 2, "verse_end": 2 }` |
| `Ps. 23:1-3` | `{ "book": "Psalms", "chapter": 23, "verse_start": 1, "verse_end": 3 }` |
| `John 3:16` | `{ "book": "John", "chapter": 3, "verse_start": 16, "verse_end": 16 }` |

- For a range (`23:1-3`), `verse_start` is the first number, `verse_end` the last.
- If a span contains multiple references separated by punctuation (e.g. `Gen. 1:2; 2:7`), emit one object per reference.
- **⚠ Watch for:** verse lists within the same chapter (e.g. `Gen. 1:2, 7`) — treat each verse number as a separate object with its own `verse_start`/`verse_end`.
- If a span cannot be confidently parsed, leave the reference as plain text in `text` only — do not emit a partial or guessed cross-reference object.

### Book name normalisation

| Abbreviation | Canonical name |
|---|---|
| `Gen.` | `Genesis` |
| `Ex.` / `Exod.` | `Exodus` |
| `Lev.` | `Leviticus` |
| `Num.` | `Numbers` |
| `Deut.` | `Deuteronomy` |
| `Ps.` / `Pss.` | `Psalms` |
| `Prov.` | `Proverbs` |
| `Isa.` | `Isaiah` |
| `Jer.` | `Jeremiah` |
| `Ezek.` | `Ezekiel` |
| `Dan.` | `Daniel` |
| `Hos.` | `Hosea` |
| `Matt.` | `Matthew` |
| `Mk.` | `Mark` |
| `Lk.` | `Luke` |
| `Jn.` | `John` |
| `Acts` | `Acts` |
| `Rom.` | `Romans` |
| `1 Cor.` | `1 Corinthians` |
| `2 Cor.` | `2 Corinthians` |
| `Gal.` | `Galatians` |
| `Eph.` | `Ephesians` |
| `Phil.` | `Philippians` |
| `Col.` | `Colossians` |
| `1 Thess.` | `1 Thessalonians` |
| `2 Thess.` | `2 Thessalonians` |
| `1 Tim.` | `1 Timothy` |
| `2 Tim.` | `2 Timothy` |
| `Tit.` | `Titus` |
| `Philem.` | `Philemon` |
| `Heb.` | `Hebrews` |
| `Jas.` | `James` |
| `1 Pet.` | `1 Peter` |
| `2 Pet.` | `2 Peter` |
| `1 Jn.` | `1 John` |
| `2 Jn.` | `2 John` |
| `3 Jn.` | `3 John` |
| `Jude` | `Jude` |
| `Rev.` | `Revelation` |
| `Song` / `Song of Sol.` | `Song of Solomon` |

Expand this table as new abbreviations are encountered in the PDF.

---

## Quality Checklist

After each book extraction, verify:

- [ ] Correct number of chapters
- [ ] All expected verses present (cross-check against KJV verse counts)
- [ ] No `"version"` field present anywhere
- [ ] Inline markers are in `{curly brackets}`
- [ ] Footnote verse-reference prefixes are stripped
- [ ] `"footnotes"` field omitted where there are no footnotes
- [ ] Combined verses reported and reviewed
- [ ] `"combined_source"` field added to all split verses
- [ ] Post-processing applied (no leading/trailing spaces before punctuation)
- [ ] Blue multi-character spans in footnote bodies extracted into `cross_references` array
- [ ] All book names in `cross_references` are full canonical names (no abbreviations)
- [ ] `cross_references` field omitted on footnotes with no cross-references (no empty arrays)
- [ ] Verse ranges parsed correctly (`verse_start` / `verse_end`)

---

## KJV Reference Files

KJV JSON files are stored in `KJV/` and used exclusively as **verse-boundary references** when splitting combined TPT verses. They are not part of the output.

KJV file naming: `KJV_{BookName}.json`

KJV structure:
```json
{
  "book": "Philippians",
  "chapters": [
    {
      "chapter": 1,
      "verses": [
        { "verse": 1, "text": "Paul and Timotheus, the servants of Jesus Christ..." }
      ]
    }
  ]
}
```

---

## Dependencies

```
pdfplumber    # PDF text extraction with font metadata
```

Install: `pip install pdfplumber`
