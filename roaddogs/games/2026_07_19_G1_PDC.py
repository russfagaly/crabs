"""
2026 Road Dogs 12
Opponent: Piedmont Cobras 12U
Date:     07/19
Round:    Tournament
Result:   W  6-2
Field:    Buckeye Field, Lafayette
Note:     Road Dogs were the AWAY team (batted top). Opened the scoring on a
          steal of home. Miles D homered; Huston G and Lennon D combined on a
          five-hitter. Second win of the set.

First appearance of Huston G #20, who started and threw 3.2 innings.

GameChanger also credits a sacrifice fly (SF: Sammy E). The game-file schema has
no "sf" field — as with the other teams — so it is not recorded here. Effect is
a marginally overstated OBP for Sammy E, since SF belongs in the OBP denominator.

Every column reconciles against the GameChanger TEAM rows, batting and pitching.
"""
TEAM = "Road Dogs"
DATE = "2026-07-19"

hitting = [
    {"name": "Zach C #3",    "ab": 2, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 1, "pqab_bonus": 0},
    {"name": "Huston G #20", "ab": 3, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 3, "r": 1, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 3, "r": 0, "h": 1, "rbi": 2, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 3, "r": 1, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 2, "r": 1, "h": 1, "rbi": 1, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 1, "sb": 0, "cs": 1, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Lennon D #34", "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 2, "r": 0, "h": 2, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sammy E #11",  "ab": 1, "r": 0, "h": 0, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles M #7",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Hudson P #2",  "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
]

pitching = [
    {"name": "Huston G #20", "ip": "3.2", "h": 3, "r": 2, "er": 2, "bb": 1, "so": 4, "pitches": 47, "strikes": 34, "bf": 16, "hbp": 0, "hr": 1},
    {"name": "Lennon D #34", "ip": "2.1", "h": 2, "r": 0, "er": 0, "bb": 1, "so": 2, "pitches": 42, "strikes": 25, "bf": 10, "hbp": 0, "hr": 0},
]
