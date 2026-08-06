"""
2026 Project Mill Cooperstown 12U
Opponent: Lake Washington 12U
Date:     08/06
Round:    Cooperstown
Result:   L  3-14
Field:    Cooperstown All Star Village
Note:     Project Mill were the HOME team (batted bottom). Two-run bottom of the
          first; Lake Washington answered with five in the 3rd and five in the 5th.

NOTE — DO NOT "FIX" THE ER VALUES. The per-pitcher ER below (5 + 2 + 6 + 0 = 13)
are confirmed correct against the box score, yet the GameChanger TEAM row reads
11. That is expected, not a data error: under official scoring, each pitcher's
earned runs are reconstructed for that pitcher individually, while the TEAM's
earned runs are reconstructed for the inning as a whole. When pitchers change
mid-inning and an error is involved — which is exactly this game (4 pitchers,
1 error) — the sum of individual ER can exceed the team ER. Both figures are
correct at their own level. We store per-pitcher rows, so 13 is right here.
"""
TEAM = "Project Mill"
DATE = "2026-08-06"

hitting = [
    {"name": "Dhilan G #34",   "ab": 3, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Noah C #8",      "ab": 2, "r": 2, "h": 2, "rbi": 0, "bb": 1, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 3, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Dylan C #7",     "ab": 3, "r": 0, "h": 0, "rbi": 2, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Issa R #5",      "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Andrew W #22",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zach B #27",     "ab": 2, "r": 0, "h": 2, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Nico Y #18",     "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #23",   "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah L #26",    "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Charlie V #45",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Abraham S #6",   "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Mark (Jr) G #13","ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Dhilan G #34",  "ip": "2.2", "h": 6, "r": 5, "er": 5, "bb": 2, "so": 3, "pitches": 55, "strikes": 29, "bf": 16, "hbp": 0, "hr": 0},
    {"name": "Abraham S #6",  "ip": "1.2", "h": 3, "r": 3, "er": 2, "bb": 1, "so": 2, "pitches": 34, "strikes": 20, "bf": 10, "hbp": 0, "hr": 0},
    {"name": "Dylan C #7",    "ip": "1.0", "h": 6, "r": 6, "er": 6, "bb": 2, "so": 0, "pitches": 31, "strikes": 15, "bf": 10, "hbp": 0, "hr": 0},
    {"name": "Carter F #23",  "ip": "0.2", "h": 0, "r": 0, "er": 0, "bb": 1, "so": 0, "pitches": 12, "strikes": 5,  "bf": 3,  "hbp": 0, "hr": 0},
]
