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

Copy any existing stub in `scripts/` and update its values (page ranges are 0-indexed; `END_PAGE` is exclusive — the first page of the next book's intro):

```python
BOOK_NAME   = "1 Timothy"
START_PAGE  = 2402   # scripture-start page (after the "AT A GLANCE" intro pages)
END_PAGE    = 2430   # exclusive — next book's intro page
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_1_Timothy.json")  # underscore for numbered books
```

All extraction logic is in `scripts/tpt_extractor_core.py` — never edit the stubs for logic changes. To find a book's page range, scan the PDF for its title heading; `START_PAGE` is the page where verse 1 appears (not the introduction pages).

## Current status

10 books extracted (6 committed March 2026; 1 & 2 Timothy, Titus, Philemon added June 2026) — 906 verses total:

| Book | Chapters | Verses | Script |
|------|----------|--------|--------|
| Galatians | 6 | 149 | `scripts/extract_galatians.py` |
| Ephesians | 6 | 155 | `scripts/extract_ephesians.py` |
| Philippians | 4 | 104 | `scripts/extract_philippians.py` |
| Colossians | 4 | 95 | `scripts/extract_colossians.py` |
| 1 Thessalonians | 5 | 89 | `scripts/extract_1thessalonians.py` |
| 2 Thessalonians | 3 | 47 | `scripts/extract_2thessalonians.py` |
| 1 Timothy | 6 | 113 | `scripts/extract_1timothy.py` |
| 2 Timothy | 4 | 83 | `scripts/extract_2timothy.py` |
| Titus | 3 | 46 | `scripts/extract_titus.py` |
| Philemon | 1 | 25 | `scripts/extract_philemon.py` |

Output files use the underscore naming convention for numbered books (e.g. `TPT/TPT_1_Timothy.json`).

The core engine supports single-chapter books (e.g. Philemon): it defaults to chapter 1 when no chapter number is present and resolves verse-only footnote references.

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
