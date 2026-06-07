# TPT Extraction Progress

## Status Summary

**Started:** March 2026
**Approach:** One book at a time — extract, review, split combined verses, confirm, move on.

---

## Completed

### Philippians ✅ Complete
- **Chapters:** 4
- **Verses:** 104
- **Footnotes resolved:** 80
- **Footnotes with cross_references:** 5
- **Total cross_references:** 8
- **Script:** `extract_philippians.py` (v2 — cross-reference support added March 2026)
- **Output:** `TPT/TPT_Philippians.json`
- **Cross-reference color:** `(0.0, 0.0, 0.933333)` = RGB float, blue channel ≈ 238/255. Confirmed working.
- **Note:** `Gen. 1:2` in Ch1:V6[d] is plain text (not hyperlinked) — correctly has no `cross_references`. Only blue hyperlinks are extracted structurally. The PDF also uses full book names (`Peter`, `John`, `1 Peter`, `1 John`) alongside standard abbreviations — both forms now covered in BOOK_ABBREV.

**Combined verses found and split:**
| Original | Split into | Notes |
|----------|------------|-------|
| Ch1: 1–2 | V1, V2 | User split manually (first example) |
| Ch1: 3–4 | V3, V4 | Split at sentence boundary |
| Ch1: 22–24 | V22, V23, V24 | Three-way split; footnote {y} assigned to V23 |
| Ch4: 12–13 | V12, V13 | Clean split; {k} stays V12, {l} moved to V13 |

All split verses carry a `combined_source` field in the JSON indicating the original combined range.

> **Correction (June 2026):** These four splits had been *documented* but were never actually applied to `TPT_Philippians.json` — the committed file still held the raw combined blocks duplicated across each verse number, with no `combined_source` fields. The splits were applied and verified June 2026 (boundaries reviewed against KJV and approved one-by-one): V1/V2 at the grace-and-peace greeting; V3/V4 at the sentence break; V22/V23/V24 three-way ({y}→V23); V12/V13 at "in hunger." ({k}→V12, {l}→V13). All inline markers now match their footnotes, and `{a}`'s 1 Timothy 1:2 cross-reference is intact.

---

### Ephesians ✅ Complete
- **Chapters:** 6
- **Verses:** 155
- **Footnotes resolved:** 105 (post-split deduplication; 114 pre-split)
- **Footnotes with cross_references:** 10
- **Total cross_references:** 11 (after splits)
- **Script:** `extract_ephesians.py` (v3 parser)
- **Output:** `TPT/TPT_Ephesians.json`
- **New abbreviation found:** `Song.` = Song of Solomon — added to BOOK_ABBREV in template

**Combined verses — split applied:**
| Chapter | Original | Split point |
|---------|----------|-------------|
| 1 | 5–6 | V5 ends "…through our union with Jesus, the Anointed One," / V6 begins "so that his tremendous love…" — {g}→V5, {i}→V6 |
| 2 | 11–12 | V11 ends "…(circumcision itself is just a work of man's hands);" / V12 begins "you had none of the Jewish covenants…" — {h}→V12 |
| 3 | 7–8 | V7 ends "…by the gift of grace that works through me." / V8 begins "Even though I am the least significant…" — {a}→V8 |
| 3 | 18–19 | V18 ends "…the astonishing love of Christ in all its dimensions." / V19 begins "How deeply intimate…" — {f}→V18 |
| 5 | 15–16 | V15 ends "…for we are living in evil times." / V16 = "Take full advantage of every day…" — no footnotes |
| 6 | 17–18 | V17 ends "…the mighty razor-sharp Spirit-sword {r} of the spoken Word of God." / V18 begins "Pray passionately {s}…" — {r}→V17, {s}→V18 |
| 6 | 21–22 | V21 ends "…will inform you of how I am getting along." / V22 = "And he will also prophesy over you {u}…" — {t}→V21, {u}→V22 |

---

### 2 Thessalonians ✅ Complete
- **Chapters:** 3
- **Verses:** 47
- **Footnotes resolved:** 59
- **Footnotes with cross_references:** 11
- **Total cross_references:** 28
- **Script:** `extract_2thessalonians.py` (v3 parser)
- **Output:** `TPT/TPT_2_Thessalonians.json`
- **Note:** Ch1:V1 footnotes [a], [b], [c] each reference 1 Thess 1:1 — correct (companion letter). Ch3:V3 [c] self-references 2 Thess 3:3 — handled gracefully. Combined verse manually split.

**Combined verses — split applied:**
| Chapter | Original | Split point |
|---------|----------|-------------|
| 3 | 17–18 | V17 = "So now, in my own handwriting, I add these words: Loving greetings to each of you." / V18 = "And may the grace of our Lord Jesus Christ be with you all. Paul The above is my signature and the token of authenticity in every letter I write. {o}" |

---

### 1 Thessalonians ✅ Complete
- **Chapters:** 5
- **Verses:** 89
- **Footnotes resolved:** 71
- **Footnotes with cross_references:** 12
- **Total cross_references:** 27
- **Script:** `extract_1thessalonians.py` (v3 — improved cross-reference parser)
- **Output:** `TPT/TPT_1_Thessalonians.json`
- **Combined verses:** None — no splits required.
- **Parser improvements in v3 (applies to all future scripts):**
  - Fixed line-break hyphen in verse ranges: `"17:1– 16"` → `"17:1–16"` (digits now included in hyphen-collapse regex)
  - Space-separated ch:verse refs within one blue span now all captured (walker loop replaces single-regex approach)
  - Non-blue `;` and `,` between blue reference words are now treated as connectors (span not flushed), so `"Acts 15:22–40; 16:19–40; 17:1–16"` is parsed as one unit with book context preserved across semicolon segments

---

### Galatians ✅ Complete
<!-- Footnote count corrected June 2026: log previously recorded the pre-split raw count (110); committed JSON has 96 after combined-verse deduplication. No data lost. -->

- **Chapters:** 6
- **Verses:** 149
- **Footnotes resolved:** 96 (post-split deduplication; 110 pre-split)
- **Footnotes with cross_references:** 4
- **Total cross_references:** 4
- **Script:** `extract_galatians.py` (v3 parser)
- **Output:** `TPT/TPT_Galatians.json`
- **Note:** Pages 2208–2244. No new abbreviations encountered.

**Combined verses — split applied:**
| Chapter | Original | Split point |
|---------|----------|-------------|
| 1 | 3–4 | V3 ends "…from the Lord Jesus. {f}" / V4 begins "He's the Anointed Messiah…" — {e},{f}→V3, {g}→V4 |
| 3 | 17–18 | V17 ends "…the royal proclamation was given before the law. {o}" / V18 begins "If that were the case…" — {n},{o}→V17, V18 no footnotes |
| 4 | 21–22 | V21 ends "…what the law really says?" / V22 begins "Have you forgotten…" — {k}→V22 |
| 5 | 22–23 | V22 ends "…faith that prevails," / V23 begins "gentleness of heart, and strength of spirit. {r}…" — {l},{m},{n},{o},{p},{q}→V22, {r},{s}→V23 |

---

### Colossians ✅ Complete
- **Chapters:** 4
- **Verses:** 95
- **Footnotes resolved:** 65 (post-split deduplication; 70 pre-split)
- **Footnotes with cross_references:** 5
- **Total cross_references:** 5
- **Script:** `extract_colossians.py`
- **Output:** `TPT/TPT_Colossians.json`
- **Note:** Single-chapter-book parser fix applied (Philemon verse-only refs like `Philem. 10–12` correctly emit `chapter: 1`). All 7 combined verse pairs manually split and verified.

**Combined verses — split applied:**
| Chapter | Original | Split point |
|---------|----------|-------------|
| 1 | 1–2 | V1 ends "…send this letter" / V2 begins "to all the holy believers…" (mid-sentence, per KJV boundary) |
| 1 | 21–22 | V21 ends "…reconnected you back to himself." / V22 begins "He released his supernatural peace…" |
| 1 | 28–29 | V28 ends "…full understanding of truth." / V29 begins "It has become my inspiration…" |
| 3 | 7–8 | V7 ends "…evil deeds." / V8 begins "But now it's time…" |
| 4 | 7–8 | V7 = "Tychicus will tell you…" (one sentence) / V8 = "I have sent him…For he is a beloved brother…" |
| 4 | 10–11 | V10 ends "…receive him warmly." / V11 begins "These three men…" |
| 4 | 12–13 | V12 ends "…God's plan for your lives." / V13 begins "Epaphras has such great zeal…" |

---

### 1 Timothy ✅ Complete
- **Chapters:** 6
- **Verses:** 113 (matches standard KJV chapter breakdown: 20/15/16/16/25/21)
- **Footnotes resolved:** 87
- **Footnotes with cross_references:** 5
- **Total cross_references:** 5
- **Script:** `extract_1timothy.py` (v3 parser; pages 2402–2430, END exclusive)
- **Output:** `TPT/TPT_1_Timothy.json`
- **Cross-references:** 1:20[n]→2 Tim. 2:17; 2:11[h]→1 Tim. 2:9–15; 3:1[b]→Eph. 4:11; 3:11[m]→Rom. 16:1; 5:13[j]→Acts 19:19. All parsed and verified.
- **Note:** No new abbreviations encountered. Schema and footnote-marker continuity clean (no gaps). Extracted June 2026.

**Combined verses — split applied:**
| Chapter | Original | Split point |
|---------|----------|-------------|
| 1 | 18–19 | V18 ends "…by faith and with a clean conscience." / V19 = "For there are many who reject these virtues and are now destitute of the true faith," — no footnotes either side |

---

### 2 Timothy ✅ Complete
- **Chapters:** 4
- **Verses:** 83 (matches standard KJV chapter breakdown: 18/26/17/22)
- **Footnotes resolved:** 50
- **Footnotes with cross_references:** 2
- **Total cross_references:** 6
- **Script:** `extract_2timothy.py` (v3 parser; pages 2435–2455, END exclusive)
- **Output:** `TPT/TPT_2_Timothy.json`
- **Cross-references:** 2:17[k]→1 Tim. 1:20; 4:19[n]→Acts 18:2, Acts 18:18, Acts 18:26, Rom. 16:3, 1 Cor. 16:19 (five-part reference, all captured). All parsed and verified.
- **Note:** No combined verses — no splits required. No new abbreviations. Schema and footnote-marker continuity clean. Extracted June 2026.

---

### Titus ✅ Complete
- **Chapters:** 3
- **Verses:** 46 (matches standard KJV chapter breakdown: 16/15/15)
- **Footnotes resolved:** 51
- **Footnotes with cross_references:** 5
- **Total cross_references:** 13
- **Script:** `extract_titus.py` (v3 parser; pages 2463–2477, END exclusive)
- **Output:** `TPT/TPT_Titus.json`
- **Cross-references:** 1:5[e]→Acts 27:7–12; 1:5[g]→1 Tim. 5:2; 3:9[j]→Heb. 13:9; 3:12[l]→Acts 20:4, Eph. 6:21, Col. 4:7, 2 Tim. 4:12; 3:13[o]→Acts 18:24, 1 Cor. 1:12, 1 Cor. 3:4–6, 1 Cor. 3:22, 1 Cor. 4:6, 1 Cor. 16:12. All parsed and verified.
- **Note:** No combined verses — no splits required. No new abbreviations. Schema and footnote-marker continuity clean. Extracted June 2026.

---

### Philemon ✅ Complete
- **Chapters:** 1 (single-chapter book)
- **Verses:** 25 (matches KJV; single chapter)
- **Footnotes resolved:** 19 (markers a–s, continuous)
- **Footnotes with cross_references:** present (e.g. {c}→Col. 4:17)
- **Script:** `extract_philemon.py` (v3 parser; pages 2484–2490, END exclusive)
- **Output:** `TPT/TPT_Philemon.json`
- **⚠ Required two core-parser fixes** (see Notes & Concerns) before it would extract at all:
  1. Single-chapter books emit no chapter-number token → parser now defaults to chapter 1 on the first verse.
  2. Single-chapter footnote bodies use verse-only reference prefixes (e.g. `1–2`, `9`) → new `parse_fn_ref_verse_only()` resolves these against chapter 1 (guarded to single-chapter books so multi-chapter extraction is unaffected; regression-tested against 1 Timothy — identical output).
- **PDF glitch — verse 5:** the verse number "5" was rendered at body-text size (8.40 pt) instead of the usual 6.60 pt, so it was misread as text and absorbed into verse 4. Recovered manually by splitting at the stray "5" (KJV-confirmed boundary). v4/v5 are NOT marked `combined_source` — they were never a combined range, just a misread number.

**Combined verses — split applied:**
| Original | Split point |
|----------|-------------|
| 1–2 | V1 ends "…companion in this work," ({a},{b}) / V2 = "and to the church…Archippus. {c}" |
| 4–5 | (recovery, not a true combine) V4 = "…as I remember you in my prayers" / V5 = "because I'm hearing reports…" |
| 9–10 | V9 ends "…making my loving appeal to you." ({e}) / V10 = "It is on behalf of my child…Onesimus. {g}" ({f},{g}) |

---

## Remaining Books

Books to extract (New Testament + Psalms, Proverbs, Song of Solomon):

### New Testament
- [ ] Matthew
- [ ] Mark
- [ ] Luke
- [ ] John
- [ ] Acts
- [ ] Romans
- [ ] 1 Corinthians
- [ ] 2 Corinthians
- [x] **Galatians** ✅
- [x] **Ephesians** ✅
- [ ] Colossians
- [x] **1 Thessalonians** ✅
- [x] **2 Thessalonians** ✅
- [x] **1 Timothy** ✅
- [x] **2 Timothy** ✅
- [x] **Titus** ✅
- [x] **Philemon** ✅
- [x] **Colossians** ✅
- [x] **Philippians** ✅
- [ ] Hebrews
- [ ] James
- [ ] 1 Peter
- [ ] 2 Peter
- [ ] 1 John
- [ ] 2 John
- [ ] 3 John
- [ ] Jude
- [ ] Revelation

### Old Testament (selected)
- [ ] Psalms
- [ ] Proverbs
- [ ] Song of Solomon

---

## Next Steps

**Immediate priority — start here next session:**
1. Pastoral epistles complete (1 & 2 Timothy, Titus, Philemon). Next batch: the remaining NT books and the OT selections (Psalms, Proverbs, Song of Solomon).
   - Suggested next: Hebrews, James, 1–2 Peter, 1–3 John, Jude, Revelation; then the Gospels/Acts/Romans/Corinthians; then OT.
   - Single-chapter support is now in the core (chapter defaults to 1; verse-only footnote refs resolved) — no other single-chapter books remain in the NT, but Obadiah/2–3 John-style books would now work if ever added.

**For future new books** — standard workflow:
- Copy any stub in `scripts/` (e.g. `scripts/extract_galatians.py`) — they are all 15 lines
- Update `BOOK_NAME`, `START_PAGE`, `END_PAGE` only — everything else is inherited from `scripts/tpt_extractor_core.py`
- To fix a parser bug or add a new book abbreviation: edit `scripts/tpt_extractor_core.py` once; all books benefit automatically
- Font taxonomy is consistent across NT books — no inspection step needed unless a book shows unexpected results

---

## Notes & Concerns

- The extraction script is robust to double-letter footnote markers (`{aa}`, `{ab}`, etc.)
- **Single-chapter book support (added June 2026, in `tpt_extractor_core.py`):** (1) a verse encountered with no chapter set now defaults to chapter 1; (2) `parse_fn_ref_verse_only()` resolves verse-only footnote prefixes against chapter 1, guarded by `is_single_chapter` so multi-chapter books are untouched. Regression-tested against 1 Timothy (identical output).
- **⚠ Verse-number font glitches:** verse numbers are normally ~6.6 pt. In Philemon, verse "5" was rendered at 8.40 pt and got misread as body text (absorbing verse 5 into verse 4). If a future book comes up short by a verse, check for a stray digit mid-text and split manually at it. A general parser fix was deliberately NOT made (8.40 pt is also the verse-text size, so reclassifying all 8.4 pt digits as verse numbers would risk corrupting legitimate numerals in prose).
- Psalms and Proverbs are long books — extra testing will be needed before committing to the full extraction
- Song of Solomon may have unusual formatting; inspect carefully before running
- ✅ KJV reference files in `KJV/` are present (30 files) — verified June 2026. Earlier "missing in session" warning is resolved.
- ℹ Ephesians ch.1 footnote markers run `…f, g, i…` (no `h`). Verified against the source PDF (raw re-extraction also has no `h`) — this is faithful to the TPT source, not a dropped footnote.
- **Cross-reference parsing — known patterns (all handled as of v3):**
  - Verse lists within the same chapter (e.g. `Gen. 1:2, 7`) — each verse number is a separate object
  - Multiple references separated by semicolons (e.g. `Gen. 1:2; 2:7`) — one object per reference
  - Multiple ch:verse references space-separated in one blue span (`Acts 15:22–40 16:19–40 17:1–16`) — all captured
  - Non-blue `;` and `,` sitting between blue words within one reference cluster — treated as connectors, span not flushed
  - Line-break hyphen in verse ranges (`17:1–` wraps to `16` on next line) — normalized before parsing
  - Bare verse following ch:verse in same span (`Acts 17:4 14`) — captured as Acts 17:14
  - `v. N` intra-chapter verse references — blue but no book prefix; currently not emitted as cross_references (no chapter context available); ignored gracefully
  - Unparseable or ambiguous spans — left as plain text in `text` only, no partial object emitted
  - The abbreviation normalisation table in `tpt-extraction-guide.md` is a starter set; expand it as new abbreviations are encountered
