"""
2026 Road Dogs 12
Opponent: Delta Valley Bruins 12U
Date:     06/13
Round:    Tournament
Result:   W  13-10
Field:    TBD
Note:     Road Dogs were the AWAY team (batted top). 12 hits; Delta Valley
          committed 7 errors. Julius N went 3-for-3 with two doubles.

Batting corrected 2026-08-07 from a scorebook check: added BB for Julian W and
Jonah M (BB now 5), and removed a strikeout from Carter F (SO now 7). All batting
columns reconcile against the TEAM row.

Pitching corrected the same day: removed a strikeout from Zach C (SO now 7).
Every batting and pitching column reconciles.
"""
TEAM = "Road Dogs"
DATE = "2026-06-13"

hitting = [
    {"name": "Zach C #3",    "ab": 2, "r": 3, "h": 2, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 3, "r": 2, "h": 3, "rbi": 2, "bb": 0, "so": 0, "doubles": 2, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 3, "r": 1, "h": 2, "rbi": 2, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 3, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 3, "r": 1, "h": 1, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 3, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
    {"name": "Carter F #5",  "ab": 3, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 2, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Lennon D #34",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Hudson P #2",  "ab": 3, "r": 1, "h": 1, "rbi": 2, "bb": 0, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 1, "r": 1, "h": 0, "rbi": 1, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sammy E #11",  "ab": 1, "r": 1, "h": 1, "rbi": 1, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 2, "r": 0, "h": 0, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Zeke W #17",  "ip": "3.0", "h": 2, "r": 5, "er": 5, "bb": 3, "so": 6, "pitches": 73, "strikes": 41, "bf": 14, "hbp": 0, "hr": 0},
    {"name": "Sam G #12",   "ip": "1.0", "h": 1, "r": 0, "er": 0, "bb": 2, "so": 1, "pitches": 17, "strikes": 7,  "bf": 5,  "hbp": 0, "hr": 0},
    {"name": "Carver D #6", "ip": "0.0", "h": 1, "r": 4, "er": 4, "bb": 2, "so": 0, "pitches": 20, "strikes": 7,  "bf": 4,  "hbp": 1, "hr": 0},
    {"name": "Zach C #3",   "ip": "1.0", "h": 2, "r": 1, "er": 1, "bb": 1, "so": 0, "pitches": 18, "strikes": 10, "bf": 5,  "hbp": 0, "hr": 0},
]
