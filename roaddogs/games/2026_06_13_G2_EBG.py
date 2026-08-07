"""
2026 Road Dogs 12
Opponent: East Bay Gamers BATS
Date:     06/13 (Game 2)
Round:    Tournament
Result:   L  5-6
Field:    TBD
Note:     Road Dogs were the AWAY team (batted top). Tied 5-5 into the bottom of
          the 6th; East Bay walked it off on a Quentin T single.

NOTE — two cells do not reconcile against the GameChanger TEAM row:
  · batting R:  rows sum to 4, TEAM row AND the line score both read 5 (under-read by 1)
  · batting SO: rows sum to 5, TEAM row reads 7                        (under-read by 2)
The run total is independently confirmed by the line score (BRKR 2 0 1 0 2 0 = 5),
so a player run is definitely missing. AB/H/RBI/BB reconcile exactly, total bases
tie out at 3 (all singles), and the 2 errors match the line score. All pitching
reconciles. Rows entered as read — worth a Plays-tab check.
"""
TEAM = "Road Dogs"
DATE = "2026-06-13"

hitting = [
    {"name": "Zach C #3",    "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 2, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #5",  "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Lennon D #34", "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Hudson P #2",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 1, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 2, "r": 1, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sammy E #11",  "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Zach C #3",    "ip": "2.0", "h": 1, "r": 1, "er": 1, "bb": 0, "so": 2, "pitches": 32, "strikes": 23, "bf": 9,  "hbp": 1, "hr": 0},
    {"name": "Carter F #5",  "ip": "2.0", "h": 5, "r": 3, "er": 3, "bb": 1, "so": 2, "pitches": 38, "strikes": 22, "bf": 12, "hbp": 0, "hr": 0},
    {"name": "Julian W #22", "ip": "1.0", "h": 4, "r": 2, "er": 1, "bb": 1, "so": 1, "pitches": 32, "strikes": 19, "bf": 9,  "hbp": 0, "hr": 0},
]
