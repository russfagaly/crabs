"""
2026 Road Dogs 12
Opponent: Extreme 12U
Date:     08/09
Round:    Tournament
Result:   L  9-12
Field:    TBD
Note:     Road Dogs were the HOME team (batted bottom). Came back from 2-0 and
          led the middle innings, then Extreme scored in five of six. Kaleo P
          homered; Oliver R tripled. Extreme collected 17 hits.

GameChanger also credits a sacrifice fly (SF: Miles M). The game-file schema has
no "sf" field, so it is not recorded — a marginally overstated OBP for Miles M,
since SF belongs in the OBP denominator.

Every column reconciles against the GameChanger TEAM rows, batting and pitching.
"""
TEAM = "Road Dogs"
DATE = "2026-08-09"

hitting = [
    {"name": "Zach C #3",    "ab": 3, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 3, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 3, "r": 0, "h": 1, "rbi": 2, "bb": 0, "so": 1, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Huston G #20", "ab": 3, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Kaleo P #10",  "ab": 3, "r": 2, "h": 2, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 1, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 3, "r": 2, "h": 2, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 1, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 3, "r": 1, "h": 2, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 3, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 3, "r": 1, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles M #7",   "ab": 0, "r": 1, "h": 0, "rbi": 2, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Zeke W #17",   "ip": "2.0", "h": 6, "r": 2, "er": 2, "bb": 0, "so": 3, "pitches": 36, "strikes": 27, "bf": 12, "hbp": 0, "hr": 0},
    {"name": "Huston G #20", "ip": "2.0", "h": 8, "r": 6, "er": 4, "bb": 1, "so": 4, "pitches": 50, "strikes": 33, "bf": 15, "hbp": 0, "hr": 0},
    {"name": "Julian W #22", "ip": "1.0", "h": 2, "r": 2, "er": 1, "bb": 0, "so": 1, "pitches": 21, "strikes": 15, "bf": 7,  "hbp": 0, "hr": 0},
    {"name": "Sam G #12",    "ip": "1.0", "h": 1, "r": 2, "er": 1, "bb": 1, "so": 2, "pitches": 22, "strikes": 13, "bf": 6,  "hbp": 0, "hr": 0},
]
