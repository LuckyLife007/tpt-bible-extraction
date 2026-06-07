# TPT Bible Extraction

A project to extract **The Passion Translation (TPT)** Bible from its source PDF into structured JSON files, one per book, for use in church display software.

## What's in this repo

| Path | Description |
|---|---|
| `The Passion Translation.pdf` | Source PDF (not committed — place in the **parent** folder of this repo) |
| `tpt-extraction-guide.md` | Full extraction specification: JSON schema, font taxonomy, cross-reference rules, workflows |
| `tpt-progress.md` | Book-by-book progress log and next steps |
| `scripts/tpt_extractor_core.py` | Shared extraction engine (v3 parser) — all logic lives here |
| `scripts/extract_<book>.py` | One 15-line stub per book — only page range and output path |
| `scripts/apply_*_splits.py` | One-off scripts used to apply combined-verse splits after extraction |
| `TPT/` | Output JSON files (one per completed book) |
| `KJV/` | KJV reference JSONs used for splitting combined verses |

## Quick start

1. Place `The Passion Translation.pdf` in the **parent** folder of this repo (one level up — not committed to git)
2. Install dependencies: `pip install pdfplumber`
3. Read `tpt-progress.md` for current status and the immediate next step
4. Read `tpt-extraction-guide.md` for the full extraction spec before writing or modifying any script

## Adding a new book

Copy any existing stub in `scripts/` and update 3 values:

```python
BOOK_NAME   = "1 Timothy"
START_PAGE  = 2404   # 0-indexed
END_PAGE    = 2422   # 0-indexed exclusive
```

All extraction logic is in `scripts/tpt_extractor_core.py` — never edit the stubs for logic changes.

## Current status

6 books extracted and committed (March 2026):

| Book | Chapters | Verses | Script |
|------|----------|--------|--------|
| Philippians | 4 | 104 | `scripts/extract_philippians.py` |
| Colossians | 4 | 95 | `scripts/extract_colossians.py` |
| 1 Thessalonians | 5 | 89 | `scripts/extract_1thessalonians.py` |
| 2 Thessalonians | 3 | 47 | `scripts/extract_2thessalonians.py` |
| Ephesians | 6 | 155 | `scripts/extract_ephesians.py` |
| Galatians | 6 | 149 | `scripts/extract_galatians.py` |

See `tpt-progress.md` for the full extraction log, split decisions, and next steps.

## Output format (summary)

```json
{
  "book": "Philippians",
  "chapters": [
    {
      "chapter": 1,
      "verses": [
        {
          "verse": 1,
          "text": "Dear friends in Philippi... {a}",
          "footnotes": [
            {
              "marker": "a",
              "text": "Timothy was Paul's convert... See 1 Tim. 1:2.",
              "cross_references": [
                { "book": "1 Timothy", "chapter": 1, "verse_start": 2, "verse_end": 2 }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

See `tpt-extraction-guide.md` for the complete schema and all extraction rules.
