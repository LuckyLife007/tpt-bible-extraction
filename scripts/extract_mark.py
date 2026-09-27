#!/usr/bin/env python3
"""
Extract TPT Mark. Pages 1019-1178 (0-indexed, END exclusive; the book's
introduction on pages 1010-1018 is skipped, matching the convention used
for every other book).

Like Matthew and Revelation, Mark renders extended direct speech (Jesus's
teaching, parables ch.4, Olivet Discourse ch.13, Last Supper/Gethsemane
ch.14, the Great Commission ch.16) in bold ~8.4pt - the same style the
shared parser normally treats as a section header (see the Hebrews
10:5-9, Revelation, and Matthew defects documented in tpt-progress.md).
Per the standing instruction to prioritize accuracy over speed, all 159
pages were scanned and every bold ~8.4pt line manually read and
classified as genuine section header vs. quoted body text - no geometric
or content heuristic was used.

BOLD_OVERRIDES below is that manually-verified table.
Notable findings from the review (documented in tpt-progress.md):
- Page 1079: the page's ONLY bold line is "Ethpathakh," - a single-line
  group that is quoted speech, not a header (same trap as Matthew's
  page 823 "go!").
- Pages 1119-1120: the section header "Jesus Drives Merchants Out of the
  Temple / Courts" breaks ACROSS a page boundary - "Courts" is the lone
  first bold line of p1120 and is a header continuation, not body text.
  First time a cross-page two-line header has been seen.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpt_extractor_core import extract_book

_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_NAME   = "Mark"
START_PAGE  = 1019
END_PAGE    = 1178
PDF_PATH    = os.path.join(_ROOT, "..", "The Passion Translation.pdf")
OUTPUT_PATH = os.path.join(_ROOT, "TPT", "TPT_Mark.json")

# Pages where ALL bold ~8.4pt content is quoted body text (no header on
# the page at all - mid-discourse continuation).
_ALL_BODY_PAGES = [
    1025, 1035, 1041, 1046, 1050, 1054, 1055, 1057, 1058, 1067,
    1075,
    1079,  # single line "Ethpathakh," - body, not a header (see docstring)
    1084, 1089, 1095, 1097, 1100, 1101, 1108, 1111, 1113, 1122,
    1127, 1133, 1139, 1142, 1151, 1154, 1175, 1176,
]

# Pages with a MIX of genuine header(s) and body text.
# Value = list of top-coordinates of the header line(s); every other bold
# ~8.4pt line on that page is reclassified to body text.
_MIXED_PAGES = {
    1021: [175.8],
    1022: [201.0],
    1023: [212.4],
    1024: [147.0, 157.8],   # "Jesus Prays, Preaches, Heals, and Casts Out / Demons" (2-line header)
    1031: [78.0],
    1032: [224.5],
    1033: [241.3],
    1034: [213.0],
    1037: [242.5],
    1039: [129.6],
    1040: [182.4],
    1045: [237.1],
    1047: [136.2],
    1048: [82.2, 216.6],
    1049: [61.2, 149.4],
    1063: [254.5],
    1064: [180.6],
    1068: [235.9],
    1069: [245.5],
    1076: [159.6],
    1077: [171.6],
    1078: [168.6],
    1083: [202.8],
    1085: [36.6, 168.0, 178.8],  # "The Pharisees Demand a Sign" + "Jesus Warns of the Yeast of the Pharisees and of / Herod" (2-line header)
    1086: [212.4],
    1087: [157.8],
    1088: [71.4, 234.7],
    1094: [55.2],
    1096: [36.6],
    1098: [100.8, 111.6, 232.3, 243.1],  # two 2-line headers
    1099: [169.8],
    1106: [271.3],
    1107: [189.6],
    1109: [267.1, 277.9],   # "Jesus Again Prophesies His Death and / Resurrection" (2-line header)
    1110: [199.8],
    1112: [104.4],
    1118: [36.6],
    1119: [178.2, 277.9],
    1120: [36.6, 265.3],    # 36.6 = "Courts", continuation of p1119's header across the page break (see docstring)
    1121: [260.5],
    1126: [78.0],
    1128: [36.6],
    1129: [36.6],
    1130: [104.4],
    1131: [198.6],
    1132: [122.4, 268.3],
    1136: [106.8, 234.7],
    1137: [258.1],
    1138: [259.3],
    1140: [72.0, 256.3],
    1141: [148.8, 238.9],
    1146: [278.5],
    1147: [114.6],
    1148: [233.5],
    1149: [138.6],
    1150: [123.6],
    1152: [36.6],
    1155: [36.6],
    1163: [106.8],
    1167: [187.8],
}

# Pages whose bold ~8.4pt content is ONLY genuine header(s) - no override
# needed (default SKIP classification is correct). Listed for the
# completeness audit (every bold page must be accounted for somewhere):
# 1019, 1020, 1036, 1038, 1044, 1053, 1056, 1062, 1066, 1074, 1105,
# 1145, 1153, 1164, 1165, 1166, 1168, 1173, 1174

BOLD_OVERRIDES = {p: 'all' for p in _ALL_BODY_PAGES}
BOLD_OVERRIDES.update(_MIXED_PAGES)

if __name__ == '__main__':
    print(f"Extracting {BOOK_NAME}…")
    extract_book(BOOK_NAME, START_PAGE, END_PAGE, PDF_PATH, OUTPUT_PATH,
                 bold_body_overrides=BOLD_OVERRIDES)
