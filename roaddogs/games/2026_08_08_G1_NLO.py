"""
2026 Road Dogs 12
Opponent: No Limit Ohana 12U
Date:     08/08
Round:    Tournament
Result:   W  13-2
Field:    TBD
Note:     Road Dogs were the HOME team (batted bottom). Run-ruled after four —
          six in the first, six in the second. Never batted the bottom of the 4th.
          13 hits, 13 runs, and only 2 strikeouts as a team.

First appearance of Kaleo P #10: 3-for-3 with a triple and 4 RBI.

Every column reconciles against the GameChanger TEAM rows, batting and pitching.
The recap corroborates the RBI detail (Kaleo P 4, Miles M 2 on a double, Miles D
on a bases-loaded walk, Julian W on a groundout).
"""
TEAM = "Road Dogs"
DATE = "2026-08-08"

hitting = [
    {"name": "Zach C #3",    "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 2, "r": 2, "h": 1, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Huston G #20", "ab": 2, "r": 2, "h": 2, "rbi": 2, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
    {"name": "Kaleo P #10",  "ab": 3, "r": 2, "h": 3, "rbi": 4, "bb": 0, "so": 0, "doubles": 0, "triples": 1, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 2, "r": 2, "h": 1, "rbi": 1, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 2, "r": 1, "h": 2, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 1, "r": 1, "h": 0, "rbi": 1, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 2, "r": 0, "h": 0, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles M #7",   "ab": 1, "r": 0, "h": 1, "rbi": 2, "bb": 1, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Zeke W #17",   "ip": "3.0", "h": 2, "r": 0, "er": 0, "bb": 0, "so": 5, "pitches": 37, "strikes": 29, "bf": 11, "hbp": 0, "hr": 0},
    {"name": "Julian W #22", "ip": "1.0", "h": 2, "r": 2, "er": 1, "bb": 0, "so": 1, "pitches": 18, "strikes": 12, "bf": 5,  "hbp": 0, "hr": 0},
]
