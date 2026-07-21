#!/usr/bin/env python3
"""
Extract TPT Matthew. Pages 761-1010 (0-indexed, END exclusive).

Matthew is the largest book extracted so far (249 pages) and, like
Revelation, renders long stretches of direct speech (Jesus's discourses:
Sermon on the Mount ch.5-7, Mission Discourse ch.10, Parables ch.13,
Community Discourse ch.18, Woes to the Pharisees ch.23, Olivet Discourse
ch.24-25, Last Supper/Gethsemane ch.26) in bold ~8.4pt — the same style
the shared parser normally treats as a section header (see the Hebrews
10:5-9 and Revelation defects documented in tpt-progress.md). Given the
scale here (roughly two-thirds of the book's chapters contain extended
bold discourse), the entire 249-page range was scanned page-by-page and
every single bold line manually read and classified as genuine section
header vs. quoted/narrated body text — no geometric or content heuristic
was used to shortcut this (per explicit instruction to prioritize
accuracy over speed on this project).

BOLD_OVERRIDES below is that manually-verified table. See
tpt-progress.md's Matthew entry for the full methodology writeup,
including the one confirmed edge case (page 823's single-line group is
body text, not a header — proof that "1 line = header" cannot be
shortcut even when it holds everywhere else in the book).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import extract_book

_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_NAME   = "Matthew"
START_PAGE  = 761
END_PAGE    = 1010
PDF_PATH    = os.path.join(_ROOT, "..", "The Passion Translation.pdf")
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_Matthew.json")

# Pages where ALL bold ~8.4pt content is quoted/narrated body text (no
# header on the page at all — it's mid-discourse continuation).
_ALL_BODY_PAGES = [
    777, 782, 789, 790, 794, 807, 808, 813, 816,
    823,  # confirmed edge case: single line-group "go!" is body, not a header
    832, 836, 838, 839, 840, 841, 846, 847, 850, 853, 855,
    861, 864, 865, 866, 881, 885, 894, 901, 903, 907, 911, 912,
    916, 918, 919, 920, 924, 925, 927, 936, 937, 942, 950, 952, 953,
    954, 960, 961, 964, 965, 971, 972, 974, 975, 976, 980, 983, 985, 1009,
]

# Pages with a MIX of genuine header(s) and body text.
# Value = list of top-coordinates of the header line(s); every other bold
# ~8.4pt line on that page is reclassified to body text.
_MIXED_PAGES = {
    781: [116.4],
    783: [152.4],          # "Jesus Preaches in Galilee" (rest of page is the temptation-narrative rebuke quote)
    784: [184.2],
    791: [60.0, 271.9],
    792: [282.7],
    793: [250.9],
    795: [71.4],
    803: [126.0],
    804: [61.2],
    805: [269.5],
    806: [159.0],
    812: [135.6],
    814: [93.6, 183.0],
    815: [94.2],
    818: [135.6],
    819: [61.2],
    820: [147.6],
    821: [233.5],
    822: [160.2],
    826: [164.4],
    827: [201.6],
    828: [238.9],
    829: [181.8],
    830: [222.7],
    831: [156.6, 265.3],
    837: [259.9],
    845: [164.4],
    848: [104.4],
    849: [82.8],
    852: [36.6],
    856: [214.8],
    857: [204.6],
    858: [224.5],
    859: [126.0],
    863: [36.6],
    867: [81.6],
    868: [92.4, 192.6, 271.3],
    869: [121.2],
    870: [148.2, 159.0],   # "Parables of Hidden Treasure and an / Extraordinary Pearl" (2-line header)
    871: [71.4],
    872: [72.6],
    879: [81.6],
    884: [55.2],
    886: [193.2],
    887: [191.4],
    888: [90.0],
    890: [135.6],
    891: [81.6],
    892: [82.8],
    893: [126.0],
    900: [280.9],
    902: [61.2, 72.0],     # "Jesus Prophesies Again of His Death and / Resurrection" (2-line header)
    908: [171.0],
    909: [61.8],
    910: [94.8],
    915: [135.6],
    917: [72.0, 236.5],
    923: [212.4],
    926: [36.6, 170.4],
    928: [71.4],
    932: [36.6],
    933: [246.1],
    934: [232.3],
    935: [245.5],
    941: [36.6],
    943: [36.6],
    944: [91.8],
    945: [139.8],
    946: [60.0],
    949: [174.0],
    951: [60.0],
    955: [105.0, 115.8],   # "Jesus Prophesies Judgment Coming to / Jerusalem" (2-line header)
    958: [126.0],
    959: [238.3],
    962: [115.2],
    963: [282.1],
    964: [204.0],
    969: [106.8],
    970: [259.3],
    973: [247.9],
    978: [36.6, 208.2],
    979: [192.0, 281.5],
    981: [93.6, 282.1],
    982: [249.7],
    984: [191.4],
    987: [252.7],
    996: [94.2],
    1000: [157.8],
    1007: [265.9],
    1008: [156.6],
}

BOLD_OVERRIDES = {p: 'all' for p in _ALL_BODY_PAGES}
BOLD_OVERRIDES.update(_MIXED_PAGES)

if __name__ == '__main__':
    print(f"Extracting {BOOK_NAME}…")
    extract_book(BOOK_NAME, START_PAGE, END_PAGE, PDF_PATH, OUTPUT_PATH,
                 bold_body_overrides=BOLD_OVERRIDES)
