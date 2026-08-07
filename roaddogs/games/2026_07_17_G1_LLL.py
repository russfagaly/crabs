"""
2026 Road Dogs 12
Opponent: LLL 12U Tournament Team
Date:     07/17
Round:    Tournament
Result:   L  1-6
Field:    Buckeye Field, Lafayette
Note:     Road Dogs were the HOME team (batted bottom). Five-run LLL first ended
          it early. Only two hits on the day — the quietest offensive game of the
          set. All six LLL runs were unearned.

NOTE — one cell does not reconcile:
  · batting SO: rows sum to 5, TEAM row reads 6 (under-read by 1)
Everything else ties out: AB, R, H, RBI, BB, total bases (2, all singles), the
single steal, and the 2 errors match the line score. All pitching reconciles.
"""
TEAM = "Road Dogs"
DATE = "2026-07-17"

hitting = [
    {"name": "Zach C #3",    "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #5",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Lennon D #34", "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Hudson P #2",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sammy E #11",  "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles M #7",   "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Sam G #12",    "ip": "1.2", "h": 4, "r": 5, "er": 0, "bb": 1, "so": 3, "pitches": 50, "strikes": 32, "bf": 12, "hbp": 1, "hr": 0},
    {"name": "Zeke W #17",   "ip": "2.0", "h": 2, "r": 1, "er": 0, "bb": 2, "so": 3, "pitches": 35, "strikes": 22, "bf": 10, "hbp": 0, "hr": 0},
    {"name": "Julian W #22", "ip": "2.0", "h": 1, "r": 0, "er": 0, "bb": 0, "so": 2, "pitches": 29, "strikes": 20, "bf": 7,  "hbp": 0, "hr": 0},
]
