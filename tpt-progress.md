# TPT Extraction Progress

## Status Summary

**Started:** March 2026
**Approach:** One book at a time — extract, review, split combined verses, confirm, move on.

---

## Completed

### Matthew ✅ Complete
- **Chapters:** 28
- **Verses:** 1070 (KJV has 1071 — see versification note below)
- **Footnotes resolved:** 669
- **Footnotes with cross_references:** 98
- **Total cross_references:** 149
- **Script:** `extract_matthew.py` (v3 parser; pages 761–1010, END exclusive — the largest book yet, 249 pages, nearly double Revelation's 132)
- **Output:** `TPT/TPT_Matthew.json`
- **Versification note (Matt 11:4/5):** the printed PDF has no separate verse-5 number at all — it jumps straight from "4" to "6". TPT folds KJV v5's content ("the blind receive their sight...") into v4's quoted text. Confirmed genuine (not a defect) via the footnote apparatus: footnote `a` is explicitly labeled "11:5" even though no verse 5 exists as a separate printed entry. Footnote `a` was manually attached to v4 since that's where its content now lives.
- **⚠ Extraction required a new technique — chunked tokenize/build split:** at 249 pages (~0.4s/page to tokenize), a single-call extraction exceeds the sandbox's ~45s per-command budget, and background processes don't survive between tool calls here. `tpt_extractor_core.py`'s `extract_book()` was split into two pure phases — `tokenize_pages()` (page-range → raw token streams) and `build_result_from_tokens()` (token streams → parsed JSON + stats) — with `extract_book()` now just chaining them, unchanged behavior. This let Matthew's page range be tokenized in 5 chunks (pickled to disk) and merged in one final build step. Regression-verified byte-identical output against the already-completed Jude before trusting it. One-off helper scripts `extract_matthew_chunk.py` / `extract_matthew_merge.py` are not part of the standard per-book pattern — future very-large books (Mark, Luke, John, Acts are all sizeable) may need the same approach; smaller books should keep using `extract_book()` directly in one call.

**⚠ Bold-quote defect — confirmed at even larger scale than Revelation, fixed via the same opt-in mechanism:**
Per the user's explicit instruction to prioritize accuracy over speed, the entire 249-page range was scanned and every bold ~8.4pt line-group manually read and classified (not a geometric heuristic) before any extraction was run. Roughly two-thirds of Matthew's chapters contain extended bold discourse (Sermon on the Mount, Mission Discourse, Parables, Community Discourse, Woes to the Pharisees, Olivet Discourse, Last Supper/Gethsemane) — essentially any time Jesus speaks at length in the text. See `extract_matthew.py`'s `BOLD_OVERRIDES` table and header comment for the full page-by-page table and methodology.
- **Confirmed edge case:** page 823 has only a single bold line-group ("go!") — normally a strong single-line signal for "genuine header" — but it's actually the tail end of a quote spanning from the previous page. Proves the "1 line = header" shortcut cannot be trusted even when it holds everywhere else in the same book; every page still needs individual verification.
- **⚠ Real defect caught during verification, not before:** despite the exhaustive manual review, page 783 was initially omitted from the override table entirely, silently dropping the "Go away, enemy!... Kneel before the Lord your God and worship only him." rebuke quote from 4:10 (left as a truncated "But Jesus said,"). Caught by the short-verse-text scan (part of the standard checklist since Revelation), then confirmed by re-reading the page's bold content directly. This is a reminder that even a careful manual process needs the downstream automated checks as a backstop — added a further systematic check (does every page with any bold ~8.4pt content appear in the override table at all?) across the full 249-page range afterward, which found no further omissions.
- **Combined-verse detection gap found:** the parser's automatic `combined` flag only fires when the PDF prints a merged verse-number token like "17–19". Matthew 7:1–2 has no printed verse-1 or verse-2 number at all (paragraph starts right after the chapter heading; the first printed digit is "3") — the parser's fallback still assigns identical text to both implied verses but never marks them `combined`, so it didn't show up in the automatic combined-verse report. Found by additionally scanning for *any* group of verses in a chapter with byte-identical text, not just parser-flagged ones — now a standard step, see [[feedback-combined-verse-splits]].

**Combined verses — 8 found, all split (3 clean/auto-applied, 5 flagged as unclear and split per the user's explicit decisions — the user rejected "leave unsplit" as an option for any of them):**
| Verses | KJV | TPT combined | Split applied |
|--------|-----|---------------|----------------|
| 6:17–18 | v17 "wash thy face"; v18 "Father...seeth in secret...reward thee openly" | "When you fast, don't let it be obvious, but instead, wash your face {p} and groom yourself and realize that your Father in the secret place is the one who is watching all that you do in secret and will continue to reward you openly."" | v17 = "...wash your face {p} and groom yourself" / v18 = "and realize that your Father...reward you openly."" — clean, auto-applied |
| 7:1–2 | v1 "Judge not..."; v2 "For with what judgment..." | "Refuse to be a critic full of bias toward others, and judgment {a} will not be passed on you. For you'll be judged by the same standard that you've used to judge others. The measurement you use on them will be used on you. {b}" | v1 = "...judgment {a} will not be passed on you." / v2 = "For you'll be judged...used on you. {b}" — clean, auto-applied |
| 7:17–19 | v17 good/corrupt tree good/evil fruit; v18 good tree cannot bear evil (and vice versa); v19 unfruitful tree hewn down, cast into fire | "So if the tree is good, it will produce good fruit; but if the tree is bad, it will bear only rotten fruit and it deserves to be cut down and burned." | No clean 3-way boundary (TPT compresses 3 KJV verses into 1 sentence) — user-specified: v17 = "So if the tree is good, it will produce good fruit;" / v18 = "but if the tree is bad, it will bear only rotten fruit" / v19 = "and it deserves to be cut down and burned." |
| 8:8–9 | v8 centurion "not worthy...speak the word only"; v9 "for I am a man under authority..." | "But the Roman officer interjected, "Lord, who am I to have you come into my house? I understand your authority, for I too am a man who walks under authority and have authority over soldiers who serve under me. I can tell one to go and he'll go, and another to come and he'll come. I order my servants and they'll do whatever I ask. So I know that all you need to do is to stand here and command healing over my son and he will be instantly healed."" | TPT reorders — v8's "speak the word only" content moved to the *end*, after v9's "under authority" content. User-specified: v8 = "...Lord, who am I to have you come into my house?" / v9 = everything else ("I understand your authority..." through "...instantly healed."") |
| 10:30–31 | v30 "hairs of your head numbered"; v31 "fear not...more value than sparrows" | "So don't worry. For your Father cares deeply about even the smallest detail of your life. {y}" | Too compressed/paraphrased to map cleanly. User-specified: v30 = "So don't worry." / v31 = "For your Father cares deeply about even the smallest detail of your life. {y}" |
| 25:2–4 | v2 "five wise, five foolish"; v3 foolish took no oil; v4 wise took oil | "Five of them were foolish and ill-prepared, for they took no extra oil {b} for their lamps. Five of them were wise and sensible, for they took flasks of olive oil with their lamps." | No clean 3-way boundary (v2's framing folded into both sentences). User-specified: v2 = "Five of them were foolish and ill-prepared," / v3 = "for they took no extra oil {b} for their lamps." / v4 = "Five of them were wise and sensible, for they took flasks of olive oil with their lamps." |
| 26:6–7 | v6 "Jesus was in Bethany, house of Simon leper"; v7 "woman with alabaster box of ointment" | "Then Jesus went to Bethany, to the home of Simon, a man Jesus had healed of leprosy. A woman came into the house, holding an alabaster flask {c} filled with fragrant and expensive oil. {d} She walked right up to Jesus, and in a lavish gesture of devotion, she poured out the costly oil, and it cascaded over his head as he was at the table." | v6 = "...healed of leprosy." / v7 = "A woman came into the house..." (rest, with footnotes c/d) — clean, auto-applied |
| 28:2–4 | v2 earthquake, angel descends, rolls back stone, sits on it; v3 countenance like lightning, raiment white; v4 keepers shook, became as dead men | "Suddenly, the earth shook violently beneath their feet as the angel of the Lord Jehovah {b} descended from heaven. Lightning flashed around him and his robe was dazzling white! The guards were stunned and terrified—lying motionless like dead men. Then the angel walked up to the tomb, rolled away the stone, and sat on top of it!" | TPT reorders — stone-rolling (KJV v2) moved to the *end*, after the guards' reaction (KJV v4). User-specified: v2 = "...descended from heaven." / v3 = "Lightning flashed...dazzling white!" / v4 = "The guards were stunned...sat on top of it!" |

---

### Revelation ✅ Complete
- **Chapters:** 22
- **Verses:** 405 (KJV has 404 — see versification note below)
- **Footnotes resolved:** 433
- **Footnotes with cross_references:** 96
- **Total cross_references:** 167
- **Script:** `extract_revelation.py` (v3 parser; pages 2801–2933, END exclusive — by far the largest book extracted so far, 132 pages)
- **Output:** `TPT/TPT_Revelation.json`
- **Combined verses:** None detected.
- **Versification note (Rev 12:17–18):** KJV keeps "and stood upon the sand of the sea" as the tail of v17; TPT (like 3 John 14/15) splits it into its own v18. Confirmed via the footnote apparatus itself — footnote `l` is explicitly labeled `12:18` in the source. Not a bug.
- **Minor OCR/PDF glitch fixed:** `22:6` extracted as "swift1ly" (a stray "1" embedded mid-word, same font/size as the surrounding text — a PDF rendering artifact, not a footnote marker). The identical phrase "swiftly" elsewhere in the book (1:1) extracted cleanly, confirming this was page-specific noise. Fixed by direct text correction; scanned the whole book for other embedded-digit artifacts and found none.

**⚠ Major parser defect found and FIXED in the shared core (not just worked around) — see "Bold-quote defect" in Notes & Concerns for full detail:**
Revelation renders most of Christ's/God's direct speech in bold ~8.4pt — the same style `classify_word()` treats as a section header (the Hebrews 10:5–9 bug). Here the impact was much larger: it silently ate almost all of the seven letters to the churches (Rev 2–3), verse 16:15 entirely, and parts of 22:6–20. A chapter-verse-count check against KJV caught the *large* losses (Rev 1, 2, 3 came up 1/6/8 verses short) but **missed** the smaller mid-verse losses in chapters 16 and 22, where the verse count still matched KJV by coincidence (the verse number survived; only its bold body text was dropped). Added a supplementary check — scanning for any verse whose text is abnormally short after stripping footnote markers — to the standard checklist, since verse-count-vs-KJV alone is not sufficient.

Given the scale (multiple full chapters, ~20 pages of affected content), hand-reconstructing this the way Hebrews 10:5–9 was fixed wasn't practical. Instead, added an **opt-in** `bold_body_overrides` parameter to `extract_book()` in `tpt_extractor_core.py`: a book script can pass a page-by-page table saying which specific bold ~8.4pt lines are genuine section headers (kept) vs. quoted body text (reclassified). It defaults to `None`/off, so none of the 21 other already-completed books are affected or need re-verification. `extract_revelation.py` builds this table from a manual, line-by-line review of every bold run in the book (documented in the script's own comments) — not a geometric heuristic, because one was tried and found unreliable here: genuine headers (e.g. "Christ's Letter to Ephesus") sometimes sit on the *same page*, immediately adjacent to, the bold body paragraph they introduce, so simple signals like "single line = header" or "title case = header" both produced false positives/negatives (Revelation's prose is dense with capitalized divine titles like "the Living One," which defeats a title-case heuristic).
- **⚠ Important for future books:** the user independently spot-checked the Gospels and found the same bold-for-direct-speech convention there too, likely far more extensively (Jesus's parables and sermons are much longer than Revelation's letters). Do NOT assume the Revelation override table or approach transfers directly — budget real investigation time when starting Matthew/Mark/Luke/John, and check for this defect from the start rather than discovering it after extraction.

---

### Jude ✅ Complete
- **Chapters:** 1 (single-chapter book)
- **Verses:** 25 (matches KJV; single chapter)
- **Footnotes resolved:** 54
- **Footnotes with cross_references:** 10
- **Total cross_references:** 19
- **Script:** `extract_jude.py` (v3 parser; pages 2769–2782, END exclusive)
- **Output:** `TPT/TPT_Jude.json`
- **Combined verses:** None — no splits required.
- **Note:** Checked for the Hebrews bold-quote defect — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found. This includes the section right before the Enoch prophecy quotation (vv. 14–15), which was rendered in regular (non-bold) text, so it wasn't at risk. Verse count matched KJV on the first pass — no versification variance here (unlike 3 John).

---

### 3 John ✅ Complete
- **Chapters:** 1 (single-chapter book)
- **Verses:** 15 (TPT versification — see note below; KJV reference file has 14)
- **Footnotes resolved:** 21 (markers a–u, continuous)
- **Footnotes with cross_references:** 2
- **Total cross_references:** 4
- **Script:** `extract_3john.py` (v3 parser; pages 2756–2762, END exclusive)
- **Output:** `TPT/TPT_3_John.json`
- **Combined verses:** None — no splits required.
- **⚠ Verse-count "mismatch" investigated and confirmed NOT a bug:** KJV 3 John has 14 verses; TPT has 15. This is a genuine versification difference between translation traditions, not a parser defect — KJV (Textus Receptus) keeps "I hope to visit you and speak face-to-face. Peace to you, my friend..." as one verse 14, while TPT (like most modern translations, following UBS/NA versification) splits it into separate 14 and 15. Confirmed directly in the raw PDF: both "14" and "15" are printed as distinct superscript verse numbers before their respective sentences. No text was dropped or duplicated. **Implication for future books:** the standard "compare extracted count to KJV" check can produce false-positive mismatches when a book has different versification between translation traditions — always inspect the raw PDF before assuming a drop occurred, the same way real defects (like the Hebrews bold-quote issue) are confirmed by inspecting raw PDF words, not by the count alone.
- **Note:** Checked for the Hebrews bold-quote defect — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found.

---

### 2 John ✅ Complete
- **Chapters:** 1 (single-chapter book)
- **Verses:** 13 (matches KJV; single chapter)
- **Footnotes resolved:** 15 (markers a–o, continuous)
- **Footnotes with cross_references:** 1 (b → John 19:25–27)
- **Script:** `extract_2john.py` (v3 parser; pages 2745–2750, END exclusive)
- **Output:** `TPT/TPT_2_John.json`
- **Combined verses:** None — no splits required.
- **Note:** Single-chapter support (chapter defaults to 1, verse-only footnote refs) worked without any script changes — same core path as Philemon. Checked for the Hebrews bold-quote defect — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found. Verse count matched KJV on the first pass.

---

### 1 John ✅ Complete
- **Chapters:** 5
- **Verses:** 105 (matches KJV chapter breakdown: 10/29/24/21/21)
- **Footnotes resolved:** 110
- **Footnotes with cross_references:** 29
- **Total cross_references:** 55
- **Script:** `extract_1john.py` (v3 parser; pages 2706–2739, END exclusive)
- **Output:** `TPT/TPT_1_John.json`
- **Combined verses:** None — no splits required.
- **Note:** Checked for the Hebrews bold-quote defect — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found. Verse counts matched KJV on the first pass.

---

### 2 Peter ✅ Complete
- **Chapters:** 3
- **Verses:** 61 (matches KJV chapter breakdown: 21/22/18)
- **Footnotes resolved:** 90
- **Footnotes with cross_references:** 18
- **Total cross_references:** 25
- **Script:** `extract_2peter.py` (v3 parser; pages 2673–2698, END exclusive)
- **Output:** `TPT/TPT_2_Peter.json`
- **Combined verses:** None — no splits required.
- **Note:** Checked for the Hebrews bold-quote defect — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found. Verse counts matched KJV on the first pass.

---

### 1 Peter ✅ Complete
- **Chapters:** 5
- **Verses:** 105 (matches KJV chapter breakdown: 25/25/22/19/14)
- **Footnotes resolved:** 149
- **Footnotes with cross_references:** 30
- **Total cross_references:** 64
- **Script:** `extract_1peter.py` (v3 parser; pages 2627–2664, END exclusive)
- **Output:** `TPT/TPT_1_Peter.json`
- **Note:** Checked for the Hebrews bold-quote defect — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found. Verse counts matched KJV on the first pass.

**Combined verses — split applied:**

| Chapter | Original | Split point |
|---------|----------|-------------|
| 3 | 3–4 | V3 = "Let your true beauty come from your inner personality, not a focus on the external." / V4 = "For lasting beauty comes from a gentle and peaceful spirit, which is precious in God's sight and is much more important than the outward adornment of elaborate hair, jewelry, {b} and fine clothes." Only one sentence break existed in the combined text, so the cut point wasn't in question, though TPT restates the inner/outer contrast in both sentences rather than keeping KJV's one-idea-per-verse split. |

---

### James ✅ Complete
- **Chapters:** 5
- **Verses:** 108 (matches KJV chapter breakdown: 27/26/18/17/20)
- **Footnotes resolved:** 105
- **Footnotes with cross_references:** 11
- **Total cross_references:** 18
- **Script:** `extract_james.py` (v3 parser; pages 2591–2617, END exclusive)
- **Output:** `TPT/TPT_James.json`
- **Note:** Checked for the Hebrews bold-quote defect (see Notes & Concerns) — every bold ~8.4pt run in this book was a single-line section header, no multi-line runs found, so no content was silently dropped. Verse counts matched KJV on the first pass.

**Combined verses — split applied:**

| Chapter | Original | Split point |
|---------|----------|-------------|
| 1 | 7–8 | V7 = "When you are half-hearted and wavering it leaves you unstable. {e}" / V8 = "Can you really expect to receive anything from the Lord when you're in that condition?" TPT states the two ideas in reverse order from KJV (instability, then "expect to receive"), but the sentence break itself was unambiguous. |
| 3 | 11–12 | V11 = "Would you look for olives hanging on a fig tree or go to pick figs from a grapevine?" / V12 = "Is it possible that fresh and bitter water can flow out of the same spring? So neither can a bitter spring produce fresh water. {i}" Flagged for review — TPT's three sentences don't map cleanly onto KJV's two-verse content split (fig/olive, water Q, water A vs. KJV's water Q / fig+olive+water A) — split by TPT's own natural sentence grouping (the two water sentences paired as question+answer) per operator confirmation. |

---

### Hebrews ✅ Complete
- **Chapters:** 13
- **Verses:** 303 (matches KJV chapter breakdown: 14/18/19/16/14/20/28/13/28/39/40/29/25)
- **Footnotes resolved:** 321
- **Footnotes with cross_references:** 45
- **Total cross_references:** 93
- **Script:** `extract_hebrews.py` (v3 parser; pages 2498–2584, END exclusive)
- **Output:** `TPT/TPT_Hebrews.json`
- **⚠ New core-parser defect found and worked around (not fixed in shared code — see Notes & Concerns):** In Heb 10:5–9 (pages 2549–2550), the TPT renders a direct OT quotation (Ps. 40:6–8) in **bold** ~8.4pt font. The classifier's "section header" rule (`~8.4pt bold → SKIP`) wrongly treated this multi-line bold run as a header, silently dropping verse 10:6 entirely and gutting parts of verses 5, 7, 8, 9. Detected via a KJV verse-count mismatch (302 vs 303) during review — not caught automatically. Recovered manually by re-reading raw PDF words with font metadata and reconstructing the missing text. Verified safe by scanning every bold-8.4pt run in the book: genuine section headers are always a single line; this was the only multi-line bold run in the whole book (6 and 8 line-groups on pages 2549/2550 vs. 1 line everywhere else), so no other Hebrews content was affected.
- **Combined verses — split applied:**

| Chapter | Original | Split point |
|---------|----------|-------------|
| 7 | 1–2 | User-specified: V1 = etymology + priest identity + Abraham meeting/blessing ("...Melchizedek went out to meet him and blessed him.") / V2 = the tithe ("Then Abraham took a tenth...gave it to Melchizedek. {a}"). Flagged for review because TPT reorders content relative to KJV's own v1/v2 split (etymology, then narrative, then tithe) — no clean single cut matches KJV's boundary exactly. |
| 9 | 16–17 | V16 ends "...proven to have died;" / V17 = "otherwise the will cannot be in force while the person who made it is still alive." Clean match to KJV boundary. |
| 10 | 2–3 | V2 ends "...worshipers would have clean consciences." / V3 begins "Instead, once was not enough..." Clean match to KJV boundary. |

---

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
- [x] **Matthew** ✅
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
- [x] **Hebrews** ✅
- [x] **James** ✅
- [x] **1 Peter** ✅
- [x] **2 Peter** ✅
- [x] **1 John** ✅
- [x] **2 John** ✅
- [x] **3 John** ✅
- [x] **Jude** ✅
- [x] **Revelation** ✅

### Old Testament (selected)
- [ ] Psalms
- [ ] Proverbs
- [ ] Song of Solomon

---

## Next Steps

**⚠ BLOCKING — do this FIRST, before starting Mark or any other new book extraction:**
The user wants to revisit and address the TPT versification-difference handling itself (not just document it as "not a bug" and move past it) — all three examples found so far need to be reviewed together before extraction work continues:
- **3 John 14/15** — KJV's v14 tail ("Peace be to thee...") is split into its own v15 in TPT.
- **Revelation 12:17/18** — KJV keeps "and stood upon the sand of the sea" as v17's tail; TPT splits it into its own v18. Confirmed via footnote `l` explicitly labeled "12:18" in the source.
- **Matthew 11:4/5** — the PDF prints NO verse-5 number at all (jumps 4→6 in the body text); TPT folds KJV v5's content into v4. Confirmed via footnote `a` explicitly labeled "11:5" in the source even though no verse 5 is ever printed. See Matthew's entry above for the full JSON representation (no placeholder v5 created; footnote `a` manually attached to v4).
Requested explicitly on 2026-07-21, right after Matthew was finished: "the first thing I want to address is this TPT versification choice as well as all the examples you listed of where it has occurred. This must be addressed first before we start extracting the next book." Do not start Mark until this is resolved.

**Immediate priority — after the above is resolved:**
1. 20 of the 27 NT books are done (all epistles Galatians–Jude, Revelation, and now Matthew); Mark, Luke, John, Acts, Romans, 1–2 Corinthians (7 books) plus the 3 OT selections (Psalms, Proverbs, Song of Solomon) remain — 10 books left out of 30 total in scope.
   - Suggested next: Mark, continuing canonical order through the Gospels/Acts/Romans/Corinthians, then the 3 OT books.
   - Single-chapter support is in the core (chapter defaults to 1; verse-only footnote refs resolved) — not relevant to any of the remaining 10 books.
   - **Versification-difference note:** when a verse-count check flags a mismatch, don't assume it's a bug — inspect the raw PDF first (check the footnote apparatus for an explicit verse-number label, as with 3 John 14/15, Rev 12:17/18, and Matt 11:4/5 — the latter had no printed verse number at all, only the footnote apparatus confirmed it). It could be a genuine translation-versification difference, which is not an error.
   - **⚠ Bold-quote defect — status per book:** Found in Hebrews (10:5–9, minor), Revelation (chapters 2–3 almost entirely, plus 16:15 and 22:6–20 — major), and now Matthew (roughly two-thirds of chapters — every extended discourse). Fixed via the same opt-in, manually-verified override table mechanism each time (see each book's entry above) — it does NOT auto-generalize; each new book needs its own from-scratch page-by-page review before extraction. **Expect the same pattern in Mark, Luke, John** (all Gospels have extensive red-letter dialogue) — budget real investigation time, don't extract-then-discover.
   - **Verse-count checks are not sufficient on their own** — a chapter's count can match KJV even when a verse's bold body text was silently dropped (only the verse number survived; confirmed in Rev 16, 22, and nearly missed in Matt 4:10 — caught only by the short-verse-text scan). Always also scan for abnormally short verse texts (e.g. text that's just a footnote marker) after stripping `{marker}` tags, in addition to the per-chapter KJV count comparison. For very large books, also systematically verify every page with any bold ~8.4pt content appears in the override table at all — a manual review can still have gaps (see Matthew's page 783 near-miss).
   - **⚠ Large books (150+ pages) need the chunked tokenize/build extraction approach**, not a single `extract_book()` call — see Matthew's entry above and `tokenize_pages()`/`build_result_from_tokens()` in `tpt_extractor_core.py`. Mark/Luke/John/Acts should be checked for page count before assuming a single-call extraction will fit the sandbox's per-command time budget.
   - **Combined-verse detection gap:** the parser's `combined` flag misses verses where the PDF prints no verse-number digit at all for the chapter's opening verse(s) (see Matt 7:1–2 in the entry above, and [[feedback-combined-verse-splits]]). Always additionally scan for any group of verses with byte-identical text, not just parser-flagged ones.
   - **Standing rule: every combined verse gets split, no exceptions** — even when the split is imperfect or requires reordering judgment calls, per explicit user instruction (see [[feedback-combined-verse-splits]]). And always show full, untruncated KJV + TPT text for every split decision, applied or flagged.

**For future new books** — standard workflow:
- Copy any stub in `scripts/` (e.g. `scripts/extract_galatians.py`) — they are all 15 lines
- Update `BOOK_NAME`, `START_PAGE`, `END_PAGE` only — everything else is inherited from `scripts/tpt_extractor_core.py`
- To fix a parser bug or add a new book abbreviation: edit `scripts/tpt_extractor_core.py` once; all books benefit automatically
- Font taxonomy is consistent across NT books — no inspection step needed unless a book shows unexpected results

---

## Notes & Concerns

- **⚠ Bold-quote defect — `classify_word()`'s rule `~8.4pt bold → SKIP` is meant to catch section headers (e.g. "Jesus, Greater than Angels"), but the TPT sometimes renders direct-speech quotations in bold too, and those get silently dropped.**
  - **Hebrews (found June 2026, small-scale):** Heb 10:5–9 quotes Ps. 40:6–8 in bold; dropped all of v10:6 and gutted parts of 5/7/8/9. Fixed by hand (re-reading raw PDF words and reconstructing the text) — too small in scope to need a code change.
  - **Revelation (found July 2026, large-scale):** almost all of Christ's letters to the seven churches (ch. 2–3), all of 16:15, and parts of 22:6–20 are bold. Too much content to hand-reconstruct safely, so `tpt_extractor_core.py`'s `extract_book()` gained an **opt-in** `bold_body_overrides` parameter (default `None`, zero effect on any book that doesn't pass it). A book script passes a manually-verified, page-by-page table of which bold ~8.4pt lines are genuine headers (kept) vs. quote body text (reclassified to `VERSE_TEXT`). See `extract_revelation.py`'s `BOLD_OVERRIDES` table and its header comment for the full table and reasoning.
  - **Why not a generic geometric rule:** tried "single bold line = header, multi-line = body" (worked for Hebrews) and "title-case = header" — both failed on Revelation, because genuine headers (e.g. "Christ's Letter to Ephesus") sometimes sit on the *same page*, directly adjacent to, the bold paragraph they introduce, and Revelation's prose is dense with capitalized divine titles ("the Living One," "the Beginning and the End") that inflate a title-case signal. A manually-verified override table was safer than a heuristic that could misfire on unseen content.
  - **⚠ For the Gospels (not yet started):** the user independently confirmed this same bold-for-direct-speech pattern appears in the Gospels too, and likely far more extensively (much more of Matthew/Mark/Luke/John is Jesus speaking than in Revelation). Do not assume Revelation's specific override table transfers — re-investigate from scratch when those books are reached, and check for the defect immediately after first extraction rather than waiting to notice a count mismatch.
  - **Matthew (found/fixed July 2026, largest scale yet):** confirmed massively — roughly two-thirds of Matthew's 28 chapters contain extended bold discourse (Sermon on the Mount, Mission Discourse, Parables, Community Discourse, Woes to the Pharisees, Olivet Discourse, Last Supper/Gethsemane — essentially any extended first-person teaching by Jesus). Per explicit user instruction to prioritize accuracy over speed, handled via a full manual page-by-page review of all 249 pages (not a heuristic), built into `extract_matthew.py`'s `BOLD_OVERRIDES` table. Two new findings, both documented in Matthew's entry above: (1) a single-bold-line page (823) that is actually body text, not a header — proof even a strong single-line signal needs individual verification every time; (2) a real omission (page 783) that slipped through the manual review and was only caught by the downstream short-verse-text scan — manual review and automated verification are complementary, neither is sufficient alone. Mark/Luke/John should expect the same scale of defect and the same full-manual-review treatment.
  - **Detection is not just "compare verse count to KJV":** a chapter's total verse count can match KJV even when a verse's bold body was dropped (the verse *number* is a separate, unaffected small non-bold digit, so it survives even when the verse's text doesn't — confirmed in Rev 16:15, 22:6–20, and nearly missed in Matt 4:10). The full checklist per book should be: (1) compare verse counts to KJV per chapter, (2) scan every verse for abnormally short text after stripping `{marker}` tags, (3) for large books, additionally verify every page with any bold ~8.4pt content is accounted for in the override table (Matthew's page-783 near-miss showed manual review alone isn't guaranteed complete), (4) if any check flags something, inspect the raw PDF directly before concluding it's a bug (it could be versification variance instead, per the 3 John/Rev 12/Matt 11 notes above).
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
