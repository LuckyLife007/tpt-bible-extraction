#!/usr/bin/env python3
"""Apply the 4 approved combined-verse splits to TPT_Galatians.json."""

import json, re, copy

INPUT  = "TPT/TPT_Galatians.json"
OUTPUT = "TPT/TPT_Galatians.json"

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

def get_footnotes_for_text(all_fns, text):
    """Return footnotes whose marker appears in the given text."""
    markers_in_text = set(re.findall(r'\{(\w+)\}', text))
    return [fn for fn in all_fns if fn["marker"] in markers_in_text]

def find_verse(chapters, ch_num, v_num):
    """Return (chapter_dict, verse_idx) for a given chapter+verse number."""
    for ch in chapters:
        if ch["chapter"] == ch_num:
            for i, v in enumerate(ch["verses"]):
                if v["verse"] == v_num:
                    return ch, i
    raise ValueError(f"Ch{ch_num}:V{v_num} not found")

# ── Split 1: Gal 1:3-4 ────────────────────────────────────────────────────────
# V3 ends after "from the Lord Jesus. {f}"
# V4 begins "He's the Anointed Messiah…"
# {e},{f} → V3 | {g} → V4
ch1, idx3 = find_verse(data["chapters"], 1, 3)
_, idx4   = find_verse(data["chapters"], 1, 4)
combined1 = ch1["verses"][idx3]
all_fns1  = combined1["footnotes"]
full_text1 = combined1["text"]

SPLIT1 = "from the Lord Jesus. {f}"
split_pos1 = full_text1.index(SPLIT1) + len(SPLIT1)
v3_text = full_text1[:split_pos1].strip()
v4_text = full_text1[split_pos1:].strip()

new_v3 = {
    "verse": 3,
    "text": v3_text,
    "footnotes": get_footnotes_for_text(all_fns1, v3_text),
    "combined_source": [3, 4]
}
new_v4 = {
    "verse": 4,
    "text": v4_text,
    "footnotes": get_footnotes_for_text(all_fns1, v4_text),
    "combined_source": [3, 4]
}

# Replace both duplicate entries (idx3 and idx4) with the two splits
ch1["verses"][idx3:idx4+1] = [new_v3, new_v4]
print(f"Split 1 applied: Ch1:V3-4")
print(f"  V3 ({len(new_v3['footnotes'])} fns): {v3_text[:80]!r}…")
print(f"  V4 ({len(new_v4['footnotes'])} fns): {v4_text[:80]!r}…")

# ── Split 2: Gal 3:17-18 ──────────────────────────────────────────────────────
# V17 ends after "given before the law. {o}"
# V18 begins "If that were the case…"
# {n},{o} → V17 | V18 no footnotes
ch3, idx17 = find_verse(data["chapters"], 3, 17)
_, idx18   = find_verse(data["chapters"], 3, 18)
combined2  = ch3["verses"][idx17]
all_fns2   = combined2["footnotes"]
full_text2 = combined2["text"]

SPLIT2 = "given before the law. {o}"
split_pos2 = full_text2.index(SPLIT2) + len(SPLIT2)
v17_text = full_text2[:split_pos2].strip()
v18_text = full_text2[split_pos2:].strip()

new_v17 = {
    "verse": 17,
    "text": v17_text,
    "footnotes": get_footnotes_for_text(all_fns2, v17_text),
    "combined_source": [17, 18]
}
new_v18 = {
    "verse": 18,
    "text": v18_text,
    "footnotes": get_footnotes_for_text(all_fns2, v18_text),
    "combined_source": [17, 18]
}

ch3["verses"][idx17:idx18+1] = [new_v17, new_v18]
print(f"\nSplit 2 applied: Ch3:V17-18")
print(f"  V17 ({len(new_v17['footnotes'])} fns): {v17_text[:80]!r}…")
print(f"  V18 ({len(new_v18['footnotes'])} fns): {v18_text[:80]!r}…")

# ── Split 3: Gal 4:21-22 ──────────────────────────────────────────────────────
# V21 ends after "what the law really says?"
# V22 begins "Have you forgotten…" (contains {k})
# {k} → V22
ch4, idx21 = find_verse(data["chapters"], 4, 21)
_, idx22   = find_verse(data["chapters"], 4, 22)
combined3  = ch4["verses"][idx21]
all_fns3   = combined3["footnotes"]
full_text3 = combined3["text"]

SPLIT3 = "what the law really says?"
split_pos3 = full_text3.index(SPLIT3) + len(SPLIT3)
v21_text = full_text3[:split_pos3].strip()
v22_text = full_text3[split_pos3:].strip()

new_v21 = {
    "verse": 21,
    "text": v21_text,
    "footnotes": get_footnotes_for_text(all_fns3, v21_text),
    "combined_source": [21, 22]
}
new_v22 = {
    "verse": 22,
    "text": v22_text,
    "footnotes": get_footnotes_for_text(all_fns3, v22_text),
    "combined_source": [21, 22]
}

ch4["verses"][idx21:idx22+1] = [new_v21, new_v22]
print(f"\nSplit 3 applied: Ch4:V21-22")
print(f"  V21 ({len(new_v21['footnotes'])} fns): {v21_text[:80]!r}…")
print(f"  V22 ({len(new_v22['footnotes'])} fns): {v22_text[:80]!r}…")

# ── Split 4: Gal 5:22-23 ──────────────────────────────────────────────────────
# V22 ends after "faith that prevails,"
# V23 begins "gentleness of heart, and strength of spirit. {r}…"
# {l},{m},{n},{o},{p},{q} → V22 | {r},{s} → V23
ch5, idx22b = find_verse(data["chapters"], 5, 22)
_, idx23    = find_verse(data["chapters"], 5, 23)
combined4   = ch5["verses"][idx22b]
all_fns4    = combined4["footnotes"]
full_text4  = combined4["text"]

SPLIT4 = "faith that prevails,"
split_pos4 = full_text4.index(SPLIT4) + len(SPLIT4)
v22_text_b = full_text4[:split_pos4].strip()
v23_text   = full_text4[split_pos4:].strip()

new_v22b = {
    "verse": 22,
    "text": v22_text_b,
    "footnotes": get_footnotes_for_text(all_fns4, v22_text_b),
    "combined_source": [22, 23]
}
new_v23 = {
    "verse": 23,
    "text": v23_text,
    "footnotes": get_footnotes_for_text(all_fns4, v23_text),
    "combined_source": [22, 23]
}

ch5["verses"][idx22b:idx23+1] = [new_v22b, new_v23]
print(f"\nSplit 4 applied: Ch5:V22-23")
print(f"  V22 ({len(new_v22b['footnotes'])} fns): {v22_text_b[:80]!r}…")
print(f"  V23 ({len(new_v23['footnotes'])} fns): {v23_text[:80]!r}…")

# ── Verify totals ─────────────────────────────────────────────────────────────
total_verses = sum(len(ch["verses"]) for ch in data["chapters"])
total_fns    = sum(len(v.get("footnotes",[])) for ch in data["chapters"] for v in ch["verses"])
print(f"\nFinal totals: {total_verses} verses, {total_fns} footnote entries")

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved → {OUTPUT}")
