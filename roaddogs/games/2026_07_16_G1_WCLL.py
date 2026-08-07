"""
2026 Road Dogs 12
Opponent: WCLL 12u All-Stars
Date:     07/16
Round:    Tournament
Result:   L  7-8
Field:    Upper Community Field, Lafayette Community Park
Note:     Road Dogs were the AWAY team (batted top). Out-hit WCLL 10-7 and still
          lost. Down six after the third, then a five-run fourth nearly finished
          the comeback. Six errors decided it.

First appearance of Miles M #7 — not the same player as Miles D #24.

NOTE — one cell does not reconcile:
  · batting SO: rows sum to 12, TEAM row reads 13 (under-read by 1)
Everything else ties out: AB, R, H, RBI, BB, total bases (11, against the single
double), steals, and the 6 errors match the line score. All pitching reconciles.
"""
TEAM = "Road Dogs"
DATE = "2026-07-16"

hitting = [
    {"name": "Zach C #3",    "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 3, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 3, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 3, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 3, "r": 2, "h": 2, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #5",  "ab": 3, "r": 2, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Lennon D #34", "ab": 3, "r": 1, "h": 2, "rbi": 2, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 1, "r": 1, "h": 1, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 2, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 1, "r": 0, "h": 0, "rbi": 1, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 2, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Hudson P #2",  "ab": 2, "r": 0, "h": 0, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 2, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sammy E #11",  "ab": 1, "r": 0, "h": 1, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles M #7",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Zeke W #17",  "ip": "2.0", "h": 2, "r": 2, "er": 0, "bb": 0, "so": 3, "pitches": 45, "strikes": 30, "bf": 12, "hbp": 0, "hr": 0},
    {"name": "Carter F #5", "ip": "0.1", "h": 5, "r": 5, "er": 4, "bb": 2, "so": 0, "pitches": 33, "strikes": 19, "bf": 9,  "hbp": 0, "hr": 0},
    {"name": "Zach C #3",   "ip": "2.0", "h": 0, "r": 1, "er": 0, "bb": 0, "so": 3, "pitches": 34, "strikes": 22, "bf": 8,  "hbp": 1, "hr": 0},
]
